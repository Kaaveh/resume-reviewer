"""`rrs eval grade`: score review reports against evals/expected (spec 03 section 7)."""

from __future__ import annotations

import re
from pathlib import Path

from rrs.config import Repo
from rrs.jsonio import read_yaml
from rrs.skill import RULE_REF_RE

LEVELS = ["Judgment", "Low", "Medium", "High", "Critical"]
RANK = {s: i for i, s in enumerate(LEVELS)}
HEADING_RE = re.compile(r"^#+\s.*?\b(Critical|High|Medium|Low|Judgment)\b", re.I)
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
VERDICT_RE = re.compile(r"\*\*Verdict:?\*\*:?\s*\**\s*(invite|borderline|reject)", re.I)
LOOSE_VERDICT_RE = re.compile(r"verdict\W{0,8}(?:\w+\W+){0,3}?(invite|borderline|reject)", re.I)
TEN_SECOND_RE = re.compile(r"\b(10|ten)[- ]second", re.I)
LABEL_RE = re.compile(r"\b(Consensus|Supported|Single source|Contested(?: range)?) \d")
NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)*")


def findings(report: str) -> dict[str, str]:
    """Rule ID -> highest severity it is listed under (bold IDs under severity headings)."""
    out: dict[str, str] = {}
    level = None
    for line in report.splitlines():
        m = HEADING_RE.match(line)
        if m:
            level = m.group(1).capitalize()
            continue
        if line.startswith("#"):
            level = None
            continue
        if level:
            for rid in (r for b in BOLD_RE.findall(line) for r in RULE_REF_RE.findall(b)):
                if rid not in out or RANK[level] > RANK[out[rid]]:
                    out[rid] = level
    return out


def verdict(report: str) -> str | None:
    m = VERDICT_RE.search(report) or LOOSE_VERDICT_RE.search(report)
    return m.group(1).lower() if m else None


def invented_numbers(report: str, cv: str) -> list[str]:
    """Numbers in the rewrites' "After" lines that are neither in the CV nor in [placeholders]."""
    m = re.search(r"^#+\s*Rewrites?\b(.*?)(?=^#{1,2}\s|\Z)", report, re.M | re.S | re.I)
    if not m:
        return []
    cv_numbers = set(NUMBER_RE.findall(cv))
    out = []
    for line in m.group(1).splitlines():
        if re.match(r"\s*[-*]?\s*\**After", line, re.I):
            out += [n for n in NUMBER_RE.findall(re.sub(r"\[[^\]]*\]", "", line)) if n not in cv_numbers]
    return out


def grade_report(report: str, expected: dict, cv: str) -> dict:
    found = findings(report)
    must = expected.get("must_flag") or []
    hits = [m["rule"] for m in must if m["rule"] in found]
    at_level = [m["rule"] for m in must
                if m["rule"] in found and RANK[found[m["rule"]]] >= RANK[m["min_severity"]]]
    cap = expected.get("max_severity")
    over = sorted(r for r, s in found.items() if cap and RANK[s] > RANK[cap])
    judgment = expected.get("judgment") or []
    return {
        "verdict": verdict(report),
        "verdict_ok": verdict(report) == expected["verdict"],
        "recall": (len(hits), len(must)),
        "severity_ok": (len(at_level), len(must)),
        "missed": [m["rule"] for m in must if m["rule"] not in at_level],
        "must_not_hits": sorted(r for r in expected.get("must_not_flag") or [] if r in found),
        "over_cap": over,
        "judgment": (sum(1 for r in judgment if r in report), len(judgment)),
        "ten_second_verdict": bool(TEN_SECOND_RE.search(report)),
        "evidence_labels": bool(LABEL_RE.search(report)),
        "invented_numbers": invented_numbers(report, cv),
        "dashes": report.count("—") + report.count("–"),
    }


def passes(g: dict) -> bool:
    return (g["severity_ok"][0] == g["severity_ok"][1] and not g["must_not_hits"] and not g["over_cap"]
            and not g["invented_numbers"])


def _row(case: str, kind: str, g: dict) -> str:
    def frac(t):
        return f"{t[0]}/{t[1]}"
    fmt = "yes" if g["ten_second_verdict"] and g["evidence_labels"] else (
        "10s only" if g["ten_second_verdict"] else "labels only" if g["evidence_labels"] else "no")
    return (f"| {case} | {kind} | {g['verdict'] or '?'} {'ok' if g['verdict_ok'] else 'WRONG'} | "
            f"{frac(g['recall'])} | {frac(g['severity_ok'])} | {', '.join(g['missed']) or '-'} | "
            f"{', '.join(g['must_not_hits'] + g['over_cap']) or '-'} | {frac(g['judgment'])} | {fmt} | "
            f"{', '.join(g['invented_numbers']) or '-'} | {g['dashes']} |")


def grade_dir(repo: Repo, results: Path) -> str:
    cases_dir, expected_dir = repo.root / "evals" / "cases", repo.root / "evals" / "expected"
    lines = [f"# Eval grades: {results.name}", "",
             "| Case | Run | Verdict | Recall | At severity | Missed | Should not flag | Judgment | "
             "Format | Invented numbers | Dashes |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    skill_pass = verdict_ok = n = 0
    totals = {"skill": [0, 0], "baseline": [0, 0]}
    for exp_path in sorted(expected_dir.glob("*.yaml")):
        case = exp_path.stem
        expected = read_yaml(exp_path)
        cv = "\n".join(p.read_text(encoding="utf-8") for p in sorted(cases_dir.glob(f"{case}*.md")))
        for kind, name in (("skill", f"{case}.md"), ("baseline", f"{case}.baseline.md")):
            path = results / name
            if not path.exists():
                lines.append(f"| {case} | {kind} | missing | | | | | | | | |")
                continue
            g = grade_report(path.read_text(encoding="utf-8"), expected, cv)
            totals[kind][0] += g["recall"][0]
            totals[kind][1] += g["recall"][1]
            lines.append(_row(case, kind, g))
            if kind == "skill":
                n += 1
                skill_pass += passes(g)
                verdict_ok += g["verdict_ok"]
    gate = skill_pass == n and n >= 5 and verdict_ok >= 4
    lines += ["", f"Recall of must_flag: skill {totals['skill'][0]}/{totals['skill'][1]}, "
              f"baseline {totals['baseline'][0]}/{totals['baseline'][1]}.",
              f"Skill cases passing must_flag, must_not_flag and numbers: {skill_pass}/{n}; "
              f"verdicts right: {verdict_ok}/{n}.",
              f"Gate (spec 03 section 7): {'met' if gate else 'NOT met'}. The owner still reads the "
              "rewrites for quality.", ""]
    return "\n".join(lines)
