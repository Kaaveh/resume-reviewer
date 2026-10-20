"""`rrs ledger validate`: every check in spec 02 section 7 step 4.

Runs on a staging file (drafts without IDs) or on `ledger/claims.jsonl` (merged claims). Errors
block a merge; warnings are for the reviewer.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from pydantic import ValidationError

from rrs.config import Repo
from rrs.jsonio import read_json, read_jsonl
from rrs.ledger.models import (
    CLAIM_ID_RE,
    Claim,
    load_claims,
    load_proposals,
    load_recruiters,
    load_rules,
    source_of_staging,
)
from rrs.normalize.text import is_arabic_letter, lang_tag, norm, norm_compact
from rrs.sources import load_source

DASHES = ("—", "–")
REJECT_RE = re.compile(
    r"\b(reject\w*|screen(s|ed|ing)? (it |them |him |her )?out|bin(s|ned)?|discard\w*|"
    r"turn(s|ed)? (it |them )?down|declin\w+|straight no|rule(s|d)? (it |them )?out|"
    r"pass(es|ed)? on|no-go|dealbreaker|deal breaker|out of the process|not progress\w*)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Issue:
    level: str  # error | warning
    line: int  # 1-based line in the file; 0 for the file as a whole
    code: str
    message: str

    def __str__(self) -> str:
        where = f"line {self.line}" if self.line else "file"
        return f"{self.level.upper()} {where} [{self.code}] {self.message}"


class Corpus:
    """Lazily loaded transcripts, with sentences in order and their turns."""

    def __init__(self, repo: Repo):
        self.repo = repo
        self._t: dict[str, dict | None] = {}

    def transcript(self, sid: str) -> dict | None:
        if sid not in self._t:
            path = self.repo.transcript_path(sid)
            if not path.exists():
                self._t[sid] = None
            else:
                t = read_json(path)
                flat = [(turn, s) for turn in t["turns"] for s in turn["sentences"]]
                t["_flat"] = flat
                t["_pos"] = {s["id"]: i for i, (_, s) in enumerate(flat)}
                t["_episodes"] = {s["episode"] for _, s in flat if s["episode"]}
                self._t[sid] = t
        return self._t[sid]

    def window(self, sid: str, sentence_id: str, n: int) -> list[tuple[dict, dict]]:
        t = self.transcript(sid)
        i = t["_pos"][sentence_id]
        return t["_flat"][i : i + n]


def is_persian(s: str) -> bool:
    return any(is_arabic_letter(c) for c in s)


def quote_in(quote: str, text: str) -> bool:
    """`norm_compact` substring for Persian or mixed quotes; `norm` whole-word match for English."""
    if is_persian(quote):
        key = norm_compact(quote)
        return bool(key) and key in norm_compact(text)
    key = norm(quote)
    return bool(key) and f" {key} " in f" {norm(text)} "


def find_quote(corpus: Corpus, claim: Claim, sentence_id: str, quote: str, max_n: int,
               any_speaker: bool) -> int | None:
    """Number of sentences (1..max_n) from `sentence_id` needed to contain the quote, or None."""
    span = corpus.window(claim.source, sentence_id, max_n)
    for n in range(1, len(span) + 1):
        part = span[:n]
        if not any_speaker and any(turn["person"] != claim.recruiter for turn, _ in part):
            return None
        if quote_in(quote, " ".join(s["text"] for _, s in part)):
            return n
    return None


def manifest_chunks(repo: Repo, sid: str) -> dict[str, dict]:
    path = repo.chunks / sid / "manifest.json"
    if not path.exists():
        return {}
    return {c["id"]: c for c in read_json(path)["chunks"]}


def validate_rows(repo: Repo, rows: list[dict], *, staging: bool, chunk: str | None = None,
                  ledger: list[Claim] | None = None) -> list[Issue]:
    """Validate claim dicts. `staging` selects draft rules (no IDs) or ledger rules (IDs).
    `chunk` is the chunk a staging file is named after; `ledger` the merged claims used for the
    duplicate warning (default: `ledger/claims.jsonl` when validating staging)."""
    issues: list[Issue] = []
    corpus = Corpus(repo)
    settings = repo.settings
    recruiters = load_recruiters(repo)
    rules = {r.id: r for r in load_rules(repo)}
    proposals: dict[str, dict] = {}
    roles: dict[str, dict[str, str] | None] = {}
    manifests: dict[str, dict[str, dict]] = {}
    if ledger is None:
        ledger = load_claims(repo) if staging else []
    by_id = {c.id: c for c in ledger}
    seen_ids: set[str] = set()
    parsed: list[tuple[int, Claim]] = []

    def err(line: int, code: str, msg: str) -> None:
        issues.append(Issue("error", line, code, msg))

    def warn(line: int, code: str, msg: str) -> None:
        issues.append(Issue("warning", line, code, msg))

    for line, row in enumerate(rows, 1):
        try:
            c = Claim.model_validate(row)
        except ValidationError as e:
            for d in e.errors():
                loc = ".".join(str(x) for x in d["loc"])
                err(line, "schema", f"{loc}: {d['msg']}")
            continue
        parsed.append((line, c))
        sid = c.source

        # Status and IDs.
        if staging:
            if c.id is not None or c.status != "draft":
                err(line, "draft", "staging claims have no id and status draft")
            if c.duplicate_of is not None:
                target = by_id.get(c.duplicate_of)
                if target is None:
                    err(line, "duplicate-of", f"duplicate_of {c.duplicate_of} is not in the ledger")
                elif target.recruiter != c.recruiter:
                    err(line, "duplicate-of", f"duplicate_of {c.duplicate_of} is another recruiter's")
            if chunk and c.extracted.chunk != chunk:
                err(line, "chunk", f"extracted.chunk {c.extracted.chunk} but the file is {chunk}")
        else:
            m = CLAIM_ID_RE.match(c.id or "")
            if c.status != "merged" or not m:
                err(line, "id", "ledger claims need an id like JB-01 and status merged")
            elif m.group(1) != c.recruiter:
                err(line, "id", f"{c.id} does not start with the recruiter code {c.recruiter}")
            if c.id in seen_ids:
                err(line, "id", f"duplicate id {c.id}")
            seen_ids.add(c.id or "")
            if c.duplicate_of is not None:
                err(line, "duplicate-of", "duplicate_of belongs in staging only")

        # Rules.
        measured = []
        for rid in c.rules:
            rule = rules.get(rid)
            if rule is not None:
                if rule.status != "active":
                    err(line, "rule", f"{rid} is retired (superseded by {rule.superseded_by})")
                if rule.measure:
                    measured.append(rid)
                continue
            if staging:
                if sid not in proposals:
                    proposals[sid] = {p.id: p for p in load_proposals(repo, sid)}
                p = proposals[sid].get(rid)
                if p is not None and p.assigned:
                    err(line, "rule", f"{rid} was decided; use {p.assigned}")
                    continue
                if p is not None and p.decision != "rejected":
                    warn(line, "proposed-rule", f"{rid} is a proposed rule; the owner must accept it")
                    if p.measure:
                        measured.append(rid)
                    continue
            err(line, "rule", f"unknown rule {rid}")
        if len(set(c.rules)) != len(c.rules):
            err(line, "rule", "a rule is listed twice")
        if measured:
            if len(c.rules) > 1:
                err(line, "measure", f"{measured[0]} is a measure; a claim on it maps to no other rule")
            if c.value is None:
                err(line, "measure", f"{measured[0]} is a measure; the claim needs a value")
            if c.stance != "+":
                err(line, "measure", "claims on a measure state a value with stance +; disagreement "
                    "shows in the spread of values")
        elif c.value is not None:
            err(line, "measure", "value is only for claims on a measure rule")

        # Recruiter and role.
        if c.recruiter not in recruiters:
            err(line, "recruiter", f"{c.recruiter} is not in ledger/recruiters.yaml")
        if sid not in roles:
            try:
                roles[sid] = load_source(repo, sid).roles
            except (FileNotFoundError, ValueError):
                roles[sid] = None
        source_roles = roles[sid]
        if source_roles is None:
            err(line, "source", f"unknown source {sid}")
            continue
        role = source_roles.get(c.recruiter)
        if role is None:
            err(line, "recruiter", f"{c.recruiter} does not speak in {sid}")
        elif role != c.speaker_role:
            err(line, "role", f"{c.recruiter} is the {role} in {sid}, not the {c.speaker_role}")
        if c.speaker_role == "host" and not c.independent:
            err(line, "role", "a host claim needs independent: true (host remarks are not claims)")
        if c.speaker_role == "guest" and c.independent:
            err(line, "role", "independent is for host claims only")
        if c.attribution == "content-override" and not c.notes.strip():
            err(line, "attribution", "content-override needs the reason in notes")

        # Anchors.
        t = corpus.transcript(sid)
        if t is None:
            err(line, "source", f"corpus/{sid}/transcript.json not found")
            continue
        anchor_episodes = []
        for k, a in enumerate(c.anchors):
            at = f"anchor {k}: " if len(c.anchors) > 1 else ""
            if a.sentence_id not in t["_pos"]:
                err(line, "sentence", f"{at}sentence {a.sentence_id} does not exist")
                continue
            turn, s = t["_flat"][t["_pos"][a.sentence_id]]
            anchor_episodes.append(s["episode"])
            override = c.attribution == "content-override"
            if turn["person"] != c.recruiter and not override:
                err(line, "speaker", f"{at}{a.sentence_id} is spoken by {turn['person']}, "
                    f"not {c.recruiter}")
                continue
            n = find_quote(corpus, c, a.sentence_id, a.quote,
                           settings.reanchor.max_window_sentences, override)
            if n is None:
                err(line, "quote", f"{at}quote not found in {a.sentence_id} or the "
                    f"{settings.reanchor.max_window_sentences - 1} sentences after it: {a.quote!r}")
            elif n > 1 and quote_in(a.quote, " ".join(
                    x["text"] for _, x in corpus.window(c.source, a.sentence_id, n)[1:])):
                warn(line, "anchor-start", f"{at}quote does not start in {a.sentence_id}; "
                     "anchor it at the sentence where it starts")
            if a.t_start != s["start"]:
                err(line, "t_start", f"{at}t_start {a.t_start} but {a.sentence_id} starts at "
                    f"{s['start']}")

        # Episode and chunk.
        if c.episode is None:
            if any(anchor_episodes):
                err(line, "episode", f"episode missing; the anchor is in {anchor_episodes[0]}")
        elif c.episode not in t["_episodes"]:
            err(line, "episode", f"unknown episode {c.episode}")
        elif anchor_episodes and c.episode not in anchor_episodes:
            err(line, "episode", f"episode {c.episode} but the anchors are in "
                f"{', '.join(sorted({e for e in anchor_episodes if e}))}")
        if sid not in manifests:
            manifests[sid] = manifest_chunks(repo, sid)
        ch = manifests[sid].get(c.extracted.chunk)
        if ch is None:
            err(line, "chunk", f"unknown chunk {c.extracted.chunk}")
        elif staging and c.duplicate_of is None and c.anchors[0].sentence_id in t["_pos"]:
            p = t["_pos"][c.anchors[0].sentence_id]
            if not t["_pos"][ch["first"]] <= p <= t["_pos"][ch["last"]]:
                warn(line, "chunk", f"first anchor {c.anchors[0].sentence_id} is outside "
                     f"{c.extracted.chunk}")

        # Prose.
        if c.value is not None and any(d in c.value.condition for d in DASHES):
            err(line, "dash", "value.condition contains an em-dash or en-dash")
        if lang_tag(c.claim_en) != "en":
            err(line, "claim-en", "claim_en must be English")
        for name, value in (("claim_en", c.claim_en), ("quote_en", c.quote_en or ""),
                            ("notes", c.notes)):
            if any(d in value for d in DASHES):
                err(line, "dash", f"{name} contains an em-dash or en-dash")
        if any(lang_tag(a.quote) != "en" for a in c.anchors) and not (c.quote_en or "").strip():
            err(line, "quote-en", "quote_en is required when a quote is not English")
        if c.type == "F!" and not REJECT_RE.search(c.claim_en):
            warn(line, "f-bang", "type F! but claim_en never mentions rejecting")

    # Probable duplicates: same recruiter, rule and stance.
    if staging:
        for i, (line, c) in enumerate(parsed):
            if c.duplicate_of is not None:
                continue
            key = {(c.recruiter, r, c.stance) for r in c.rules}
            others = [o for o in ledger if {(o.recruiter, r, o.stance) for r in o.rules} & key]
            others += [o for _, o in parsed[:i] if o.duplicate_of is None
                       and {(o.recruiter, r, o.stance) for r in o.rules} & key]
            if others:
                names = [o.id or f"line {next(ln for ln, x in parsed if x is o)}" for o in others]
                warn(line, "duplicate", "probable duplicate of " + ", ".join(names)
                     + " (same recruiter, rule and stance); fold it with duplicate_of if it is "
                     "the same assertion")
    return sorted(issues, key=lambda x: (x.line, x.level != "error"))


def chunk_of_staging(path: Path) -> str | None:
    """`S004.c001.jsonl` -> `S004.c001`; None for other names."""
    m = re.match(r"^(S\d{3})\.(c\d{3})\.jsonl$", path.name)
    return f"{m.group(1)}.{m.group(2)}" if m else None


def validate_file(repo: Repo, path: Path, isolated: bool = False) -> list[Issue]:
    """`isolated` skips the duplicate check against the ledger, for an independent extraction
    that must not see the ledger's claims (spec 02 section 12)."""
    rows = read_jsonl(path)
    if path.resolve() == (repo.ledger / "claims.jsonl").resolve():
        return validate_rows(repo, rows, staging=False)
    source_of_staging(path)
    issues = validate_rows(repo, rows, staging=True, chunk=chunk_of_staging(path),
                           ledger=[] if isolated else None)
    if not rows:
        issues.insert(0, Issue("warning", 0, "empty", "no claims in this file"))
    return issues
