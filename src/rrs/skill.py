"""`rrs skill build | lint | install`: skill/SKILL.md from the ledger (spec 03 sections 2 to 4)."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

import yaml

from rrs.config import Repo
from rrs.jsonio import read_yaml
from rrs.ledger.models import (
    CLAIM_ID_RE,
    X_RULE_RE,
    load_claims,
    load_recruiters,
    load_rules,
    load_targets,
)
from rrs.ledger.render import _cell
from rrs.ledger.tally import TIERS, compute

NAME = "resume-reviewer"
MAX_LINES = 500
BLOCKS = ("EVIDENCE", "RULES")
RULE_REF_RE = re.compile(r"\b(?:(?:SCR|ATS|STR|ACH|SKL|RED|REG|SEN|GAP|CHN)-\d+|X-[A-Z]+)\b")
CLAIM_REF_RE = re.compile(r"\b[A-Z]{2}-\d+\b")
ROLE = {"agency": "agency recruiter", "in-house-recruiter": "in-house recruiter",
        "hiring-manager": "hiring manager", "former-recruiter": "former recruiter"}
VERSION_RE = re.compile(r"^## (v\d+\.\d+\.\d+)", re.M)


def skill_path(repo: Repo) -> Path:
    return repo.root / "skill" / "SKILL.md"


def evidence_version(repo: Repo) -> str:
    """The newest release heading in skill/CHANGELOG.md (`## v1.0.0 ...`), or `unreleased`."""
    path = repo.root / "skill" / "CHANGELOG.md"
    m = VERSION_RE.search(path.read_text(encoding="utf-8")) if path.exists() else None
    return m.group(1) if m else "unreleased"


def evidence_block(repo: Repo, tally: dict) -> str:
    recruiters = load_recruiters(repo)
    targets = load_targets(repo)
    match = targets.default_target.match if targets else {}
    lines = ["| Code | Recruiter | Type and market | Weight for the default target |", "|---|---|---|---|"]
    for code, r in recruiters.items():
        lines.append(f"| {code} | {_cell(r.name)}, {_cell(r.title)} | {r.type}; {_cell(r.region)}; "
                     f"{_cell(r.industry)} | {match.get(code, 'not set')} |")
    lines.append("")
    if targets:
        lines += [f"Default target (`{targets.default}`): {_cell(targets.default_target.description)}.", ""]
    t = tally["totals"]
    lines.append(f"Evidence {evidence_version(repo)}: {t['sources']} sources, {t['recruiters']} recruiters, "
                 f"{t['claims']} claims, {t['rules']} rules ("
                 + ", ".join(f"{t['labels'][k]} {k}" for k in TIERS[:4]) + ").")
    return "\n".join(lines)


def _sources(r: dict) -> str:
    c = r["claims"]
    if r["tier"] == "Contested" or c["against"]:
        parts = [f"for: {', '.join(c['for']) or 'none'}", f"against: {', '.join(c['against']) or 'none'}"]
    else:
        parts = [", ".join(c["for"])]
    if c["notes"]:
        parts.append(f"notes: {', '.join(c['notes'])}")
    return "; ".join(parts)


def skill_rules(tally: dict) -> list[str]:
    """Rule IDs that go in the RULES block: active, in scope, with support."""
    return [rid for rid in tally["order"]
            if tally["rules"][rid]["status"] == "active" and tally["rules"][rid]["category"] != "X"
            and tally["rules"][rid]["tier"] != "No support"]


def _table(tally: dict, rows: list[str]) -> list[str]:
    lines = ["| ID | Rule and check | Evidence | Base severity | Sources |", "|---|---|---|---|---|"]
    for rid in rows:
        r = tally["rules"][rid]
        lines.append(f"| {rid} | {_cell(r['text'])} *Check:* {_cell(r['check'])} | "
                     f"{_cell(r['evidence'])} | {r['severity']} | {_sources(r)} |")
    return lines + [""]


def rules_block(tally: dict, recruiters: dict | None = None) -> str:
    """One table per tier; Single source is split by the one person behind each rule, with their
    role, so the reviewer can weight a rule by who said it."""
    recruiters = recruiters or {}
    ids = skill_rules(tally)
    lines: list[str] = []
    for tier in TIERS[:4]:
        rows = [rid for rid in ids if tally["rules"][rid]["tier"] == tier]
        lines += [f"### {tier} ({len(rows)})", ""]
        if not rows:
            lines += ["None.", ""]
        elif tier != "Single source":
            lines += _table(tally, rows)
        else:
            by: dict[str, list[str]] = {}
            for rid in rows:
                by.setdefault(tally["rules"][rid]["plus"][0], []).append(rid)
            order = list(recruiters)
            for code in sorted(by, key=lambda c: (order.index(c) if c in order else len(order), c)):
                r = recruiters.get(code)
                who = (f"{code}, {r.name}: {ROLE.get(r.type, r.type)} ({_cell(r.title)})" if r else code)
                lines += [f"#### {who}, {len(by[code])} rules", ""] + _table(tally, by[code])
    return "\n".join(lines).rstrip()


def _markers(name: str) -> tuple[str, str]:
    return f"<!-- {name}:START -->", f"<!-- {name}:END -->"


def replace_block(text: str, name: str, body: str) -> str:
    start, end = _markers(name)
    i, j = text.find(start), text.find(end)
    if i < 0 or j < i:
        raise ValueError(f"SKILL.md has no {start} ... {end} block")
    return text[: i + len(start)] + "\n" + body + "\n" + text[j:]


def strip_blocks(text: str) -> str:
    """The hand-written parts: SKILL.md without the generated blocks."""
    for name in BLOCKS:
        start, end = _markers(name)
        i, j = text.find(start), text.find(end)
        if i >= 0 and j > i:
            text = text[:i] + text[j + len(end):]
    return text


def _old_rows(text: str) -> dict[str, tuple[str, str]]:
    """Rule ID -> (label, severity) from the RULES block as it stands."""
    start, end = _markers("RULES")
    i, j = text.find(start), text.find(end)
    out = {}
    for line in text[i:j].splitlines() if i >= 0 else []:
        cells = [c.strip() for c in line.strip("|").split(" | ")]
        if len(cells) == 5 and RULE_REF_RE.fullmatch(cells[0]):
            out[cells[0]] = (cells[2].split(" (")[0].split(";")[0], cells[3])
    return out


def build(repo: Repo) -> tuple[str, str, list[str]]:
    """Returns (old text, new text, change lines such as `CHANGED SKL-6: ... -> ...`)."""
    path = skill_path(repo)
    old = path.read_text(encoding="utf-8")
    tally = compute(repo)
    new = replace_block(old, "EVIDENCE", evidence_block(repo, tally))
    new = replace_block(new, "RULES", rules_block(tally, load_recruiters(repo)))
    before = _old_rows(old)
    changes = []
    for rid in skill_rules(tally):
        r = tally["rules"][rid]
        now = f"{r['label']} [{r['severity']}]"
        if rid not in before:
            changes.append(f"ADDED {rid}: {now}")
        elif before[rid] != (r["label"], r["severity"]):
            changes.append(f"CHANGED {rid}: {before[rid][0]} [{before[rid][1]}] -> {now}")
    changes += [f"REMOVED {rid}" for rid in before if rid not in set(skill_rules(tally))]
    return old, new, changes


def _frontmatter(text: str) -> dict | None:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def _section(text: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def _split_row(line: str) -> list[str]:
    return re.split(r"(?<!\\)\|", line.strip().strip("|"))


def cv_owners(repo: Repo) -> set[str]:
    names = set()
    for path in sorted(repo.corpus.glob("S*/episodes.yaml")):
        names |= {e["cv_owner"] for e in read_yaml(path) or [] if e.get("cv_owner")}
    return names


def lint(repo: Repo, text: str) -> list[tuple[str, str]]:
    """(level, message) pairs; level is `error` or `warning` (spec 03 section 4)."""
    out: list[tuple[str, str]] = []
    lines = text.splitlines()
    for n, line in enumerate(lines, 1):
        if "—" in line or "–" in line:
            out.append(("error", f"line {n}: em-dash or en-dash"))

    fm = _frontmatter(text)
    if fm is None:
        out.append(("error", "frontmatter missing or not valid YAML"))
    else:
        if fm.get("name") != NAME:
            out.append(("error", f"frontmatter name is {fm.get('name')!r}, not {NAME!r}"))
        desc = fm.get("description")
        if not isinstance(desc, str) or not desc.strip():
            out.append(("error", "frontmatter description missing"))
        elif len(desc) > 1024:
            out.append(("error", f"description is {len(desc)} characters (limit 1024)"))
        elif len(desc) > 200:
            out.append(("warning", f"description is {len(desc)} characters (aim for under 200)"))

    rules = {r.id: r for r in load_rules(repo)}
    claims = {c.id for c in load_claims(repo)}
    hand = strip_blocks(text)
    for rid in sorted(set(RULE_REF_RE.findall(hand))):
        if rid not in rules:
            out.append(("error", f"{rid} is not in the rule index"))
        elif rules[rid].status != "active":
            out.append(("error", f"{rid} is retired"))
    for cid in sorted(set(CLAIM_REF_RE.findall(hand))):
        if CLAIM_ID_RE.match(cid) and not X_RULE_RE.match(cid) and cid not in claims:
            out.append(("error", f"{cid} is not a claim in the ledger"))

    tally = compute(repo)
    contested = {rid for rid in skill_rules(tally) if tally["rules"][rid]["tier"] == "Contested"}
    guided = set()
    for line in _section(text, "Contested guidance").splitlines():
        cells = _split_row(line) if line.startswith("|") else []
        if cells and RULE_REF_RE.fullmatch(cells[0].strip()):
            guided.add(cells[0].strip())
    out += [("error", f"{rid} is contested but has no row in Contested guidance")
            for rid in sorted(contested - guided)]
    out += [("error", f"{rid} has a Contested guidance row but is no longer contested")
            for rid in sorted(guided - contested)]

    for name in sorted(cv_owners(repo)):
        if re.search(rf"\b{re.escape(name)}\b", text):
            out.append(("error", f"a CV owner's name appears in SKILL.md: {name}"))

    header = None
    for n, line in enumerate(lines, 1):
        if not line.startswith("|"):
            header = None
            continue
        cols = len(_split_row(line))
        if header is None:
            header = cols
        elif cols != header:
            out.append(("error", f"line {n}: {cols} columns, header has {header}"))

    if len(lines) > MAX_LINES:
        out.append(("warning", f"{len(lines)} lines (aim for at most {MAX_LINES})"))
    return out


def install(repo: Repo, global_: bool = False) -> Path:
    base = Path.home() if global_ else repo.root
    dst = base / ".claude" / "skills" / NAME / "SKILL.md"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(skill_path(repo), dst)
    return dst
