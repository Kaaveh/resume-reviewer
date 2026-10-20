"""Chunk workflow: `chunks next`, `ledger review`, `ledger merge` and `ledger rules --accept`
(spec 02 section 7, statuses in spec 01 section 11)."""

from __future__ import annotations

import datetime as dt
import shutil
import subprocess
from pathlib import Path

import yaml

from rrs.config import Repo
from rrs.jsonio import fmt_time, read_json, read_jsonl, write_json, write_jsonl
from rrs.ledger.models import (
    CLAIM_ID_RE,
    NUMBERED_RULE_RE,
    Claim,
    claims_path,
    load_claims,
    load_proposals,
    load_rules,
    proposals_path,
    source_of_staging,
    staging_dir,
)
from rrs.ledger.validate import chunk_of_staging, validate_rows
from rrs.sources import all_source_ids

STATUSES = ["pending", "extracted", "reviewed", "merged"]


class WorkflowError(ValueError):
    pass


def _manifest_path(repo: Repo, sid: str) -> Path:
    return repo.chunks / sid / "manifest.json"


def set_chunk_status(repo: Repo, chunk: str, status: str, merge_commit: str | None = None) -> None:
    sid = chunk.split(".")[0]
    path = _manifest_path(repo, sid)
    m = read_json(path)
    for c in m["chunks"]:
        if c["id"] == chunk:
            c["status"] = status
            if merge_commit is not None:
                c["merge_commit"] = merge_commit
            write_json(path, m)
            return
    raise WorkflowError(f"{chunk} is not in {path.relative_to(repo.root)}")


def chunk_status(repo: Repo, chunk: str) -> str:
    sid = chunk.split(".")[0]
    for c in read_json(_manifest_path(repo, sid))["chunks"]:
        if c["id"] == chunk:
            return c["status"]
    raise WorkflowError(f"unknown chunk {chunk}")


def next_chunk(repo: Repo, sources: list[str] | None = None) -> dict | None:
    """The first chunk, in source order, that is not merged."""
    for sid in sources or all_source_ids(repo):
        path = _manifest_path(repo, sid)
        if not path.exists():
            continue
        for c in read_json(path)["chunks"]:
            if c["status"] != "merged":
                return {**c, "path": f"chunks/{sid}/{c['file']}"}
    return None


def _cell(s: str, n: int) -> str:
    s = " ".join(s.split()).replace("|", "\\|")
    return s if len(s) <= n else s[: n - 3] + "..."


def review_table(repo: Repo, path: Path, quote_chars: int = 140) -> str:
    """The compact review table of spec 02 section 7 step 5, as Markdown."""
    rows = read_jsonl(path)
    starts: dict[str, float | None] = {}
    sid = source_of_staging(path)
    t = read_json(repo.transcript_path(sid))
    for turn in t["turns"]:
        for s in turn["sentences"]:
            starts[s["id"]] = s["start"]
    timed = t["timing"] != "none"
    head = ["#", "Time" if timed else "Sentence", "Quote", "claim_en", "Type", "Stance", "Rules"]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for i, r in enumerate(rows, 1):
        a = r["anchors"][0]
        where = fmt_time(starts.get(a["sentence_id"])) if timed else a["sentence_id"]
        quote = a["quote"] + (f" (+{len(r['anchors']) - 1} more)" if len(r["anchors"]) > 1 else "")
        if r.get("quote_en"):
            quote += f" [{r['quote_en']}]"
        claim = r["claim_en"]
        if r.get("value"):
            v = r["value"]
            claim += f" [value: {v.get('min')} to {v.get('max')}" + (
                f", {v['condition']}" if v.get("condition") else "") + "]"
        rules = ", ".join(r["rules"]) + (f" (dup of {r['duplicate_of']})" if r.get("duplicate_of")
                                         else "")
        lines.append("| " + " | ".join([
            str(i), str(where), _cell(quote, quote_chars), _cell(claim, 10_000), r["type"],
            r["stance"], rules,
        ]) + " |")
    return "\n".join(lines) + "\n"


def approve(repo: Repo, path: Path) -> str:
    chunk = chunk_of_staging(path)
    if chunk is None:
        raise WorkflowError(f"{path.name} is not a chunk staging file")
    _require_valid(repo, path)
    set_chunk_status(repo, chunk, "reviewed")
    return chunk


def _require_valid(repo: Repo, path: Path) -> list[dict]:
    rows = read_jsonl(path)
    issues = validate_rows(repo, rows, staging=True, chunk=chunk_of_staging(path))
    errors = [i for i in issues if i.level == "error"]
    proposed = [i for i in issues if i.code == "proposed-rule"]
    if errors or proposed:
        detail = "\n".join(str(i) for i in errors + proposed)
        raise WorkflowError(f"{path.name} does not validate:\n{detail}")
    return rows


def _git_commit_for(repo: Repo, chunk: str) -> str | None:
    """The commit that merged a chunk, found by its message `ledger: S004 c001, ...`."""
    sid, c = chunk.split(".")
    try:
        out = subprocess.run(
            ["git", "log", "-n1", "--format=%h", "--fixed-strings", f"--grep=ledger: {sid} {c},"],
            cwd=repo.root, capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return out or None


def backfill_merge_commits(repo: Repo, sid: str) -> None:
    path = _manifest_path(repo, sid)
    m = read_json(path)
    changed = False
    for c in m["chunks"]:
        if c["status"] == "merged" and not c["merge_commit"]:
            commit = _git_commit_for(repo, c["id"])
            if commit:
                c["merge_commit"] = commit
                changed = True
    if changed:
        write_json(path, m)


def dump_claim(c: Claim) -> dict:
    d = c.model_dump(exclude={"duplicate_of"})
    if d["value"] is None:
        del d["value"]
    return d


def merge(repo: Repo, path: Path, today: dt.date | None = None) -> dict:
    """Assign IDs, fold duplicates, append to claims.jsonl, mark the chunk merged and archive
    the staging file. Returns counts and the new IDs."""
    chunk = chunk_of_staging(path)
    if chunk is not None and chunk_status(repo, chunk) != "reviewed":
        raise WorkflowError(f"{chunk} is {chunk_status(repo, chunk)}; approve it with "
                            f"`rrs ledger review {path.name} --approve` first")
    rows = _require_valid(repo, path)
    ledger = load_claims(repo)
    by_id = {c.id: c for c in ledger}
    numbers: dict[str, int] = {}
    for c in ledger:
        m = CLAIM_ID_RE.match(c.id or "")
        if m:
            numbers[m.group(1)] = max(numbers.get(m.group(1), 0), int(m.group(2)))
    new_ids, folded = [], []
    for row in rows:
        draft = Claim.model_validate(row)
        if draft.duplicate_of:
            target = by_id[draft.duplicate_of]
            have = {(a.sentence_id, a.quote) for a in target.anchors}
            target.anchors += [a for a in draft.anchors if (a.sentence_id, a.quote) not in have]
            folded.append(draft.duplicate_of)
            continue
        n = numbers.get(draft.recruiter, 0) + 1
        numbers[draft.recruiter] = n
        draft.id = f"{draft.recruiter}-{n:02d}"
        draft.status = "merged"
        ledger.append(draft)
        by_id[draft.id] = draft
        new_ids.append(draft.id)
    write_jsonl(claims_path(repo), [dump_claim(c) for c in ledger])
    if chunk is not None:
        set_chunk_status(repo, chunk, "merged")
        backfill_merge_commits(repo, chunk.split(".")[0])
    archive = staging_dir(repo) / "archive"
    archive.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), archive / path.name)
    return {"chunk": chunk, "new": new_ids, "folded": folded}


def accept_rules(repo: Repo, sid: str, added_in: str) -> list[tuple[str, str]]:
    """Give accepted proposals of `sid` permanent IDs, append them to rules.yaml, and rewrite the
    source's staging claims. Rejected proposals with `use` are rewritten to that rule. Returns
    (temporary ID, permanent ID) pairs."""
    proposals = load_proposals(repo, sid)
    rules = load_rules(repo)
    existing = {r.id for r in rules}
    numbers: dict[str, int] = {}
    for r in rules:
        m = NUMBERED_RULE_RE.match(r.id)
        if m:
            numbers[m.group(1)] = max(numbers.get(m.group(1), 0), int(m.group(2)))
    mapping: dict[str, str] = {}
    added: list[dict] = []
    for p in proposals:
        if p.assigned:
            continue
        if p.decision == "accepted":
            if p.category == "X":
                if not p.id.startswith("X-"):
                    raise WorkflowError(f"{p.id}: X proposals carry their final name, like X-INT")
                new = p.id
                if new in existing:
                    raise WorkflowError(f"{new} already exists")
            else:
                numbers[p.category] = numbers.get(p.category, 0) + 1
                new = f"{p.category}-{numbers[p.category]}"
            rule = {"id": new, "category": p.category, "text": p.text, "check": p.check,
                    "status": "active", "added_in": added_in}
            if p.measure:
                rule["measure"] = p.measure.model_dump()
            if p.notes:
                rule["notes"] = p.notes
            added.append(rule)
            existing.add(new)
            mapping[p.id] = new
            p.assigned = new
        elif p.decision == "rejected" and p.use:
            target = mapping.get(p.use, p.use)  # `use` may name a proposal accepted above
            if target not in existing:
                raise WorkflowError(f"{p.id}: use {p.use} is not an existing or accepted rule")
            mapping[p.id] = target
            p.assigned = target
    if added:
        rules_path = repo.ledger / "rules.yaml"
        text = rules_path.read_text(encoding="utf-8") if rules_path.exists() else ""
        if text and not text.endswith("\n"):
            text += "\n"
        if not yaml.safe_load(text):  # only comments, or the empty list `[]`
            text = "".join(line + "\n" for line in text.splitlines() if line.startswith("#"))
        text += yaml.safe_dump(added, sort_keys=False, allow_unicode=True, width=100)
        rules_path.write_text(text, encoding="utf-8")
    if mapping:
        for f in sorted(staging_dir(repo).glob(f"{sid}.c[0-9][0-9][0-9].jsonl")):
            rows = read_jsonl(f)
            for r in rows:
                r["rules"] = list(dict.fromkeys(mapping.get(x, x) for x in r["rules"]))
            write_jsonl(f, rows)
        data = [{k: v for k, v in p.model_dump(exclude_none=True).items() if v != ""}
                for p in proposals]
        proposals_path(repo, sid).write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")
    return list(mapping.items())


def amend(repo: Repo, path: Path, today: dt.date | None = None) -> list[str]:
    """Apply reviewed edits to merged claims (for example from a verification report).

    `path` is a YAML list of `{claim: JB-07, set: {field: value, ...}, reason: ...}`. The whole
    ledger must validate afterwards or nothing is written. Every change is logged with its old
    value in `ledger/amendments.jsonl`. IDs, recruiter and source cannot change."""
    from rrs.jsonio import read_yaml

    edits = read_yaml(path) or []
    rows = read_jsonl(claims_path(repo))
    by_id = {r["id"]: r for r in rows}
    log = []
    date = (today or dt.date.today()).isoformat()
    for e in edits:
        cid, changes, reason = e.get("claim"), e.get("set") or {}, (e.get("reason") or "").strip()
        if cid not in by_id:
            raise WorkflowError(f"amend: unknown claim {cid}")
        if not reason or not changes:
            raise WorkflowError(f"amend {cid}: needs `set` and a `reason`")
        frozen = {"id", "recruiter", "source", "status"} & set(changes)
        if frozen:
            raise WorkflowError(f"amend {cid}: {', '.join(sorted(frozen))} cannot change")
        row = by_id[cid]
        for field, value in changes.items():
            log.append({"date": date, "claim": cid, "field": field, "old": row.get(field),
                        "new": value, "reason": reason, "source_file": path.name})
            row[field] = value
    issues = validate_rows(repo, rows, staging=False)
    errors = [i for i in issues if i.level == "error"]
    if errors:
        raise WorkflowError("amendments do not validate:\n" + "\n".join(str(i) for i in errors))
    write_jsonl(claims_path(repo), rows)
    log_path = repo.ledger / "amendments.jsonl"
    old = read_jsonl(log_path) if log_path.exists() else []
    write_jsonl(log_path, old + log)
    return sorted({e["claim"] for e in edits})
