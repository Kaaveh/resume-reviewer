"""Counting, labels and severity (spec 02 section 8, ADR 0001) and change reports (section 9)."""

from __future__ import annotations

import datetime as dt

from rrs.config import Repo
from rrs.jsonio import read_json, write_json
from rrs.ledger.models import (
    CATEGORY_ORDER,
    Claim,
    Rule,
    load_claims,
    load_recruiters,
    load_rules,
    load_targets,
    rule_sort_key,
)

TALLY_SCHEMA = "rrs.tally/1"
TIERS = ["Consensus", "Supported", "Contested", "Single source", "No support"]
SEVERITIES = ["Low", "Medium", "High", "Critical"]
SEVERITY_RANK = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1, "Judgment": 0, "n/a": -1}


def counts(c: Claim, count_independent_hosts: bool) -> bool:
    return c.speaker_role == "guest" or (c.independent and count_independent_hosts)


def tally_rule(rule: Rule, claims: list[Claim], count_independent_hosts: bool) -> dict:
    C = [c for c in claims if rule.id in c.rules and counts(c, count_independent_hosts)]
    plus = {c.recruiter for c in C if c.stance == "+"}
    minus = {c.recruiter for c in C if c.stance == "-"}
    both = plus & minus
    plus -= both
    minus -= both
    plus_claims = [c for c in C if c.stance == "+" and c.recruiter in plus]
    n_f = len({c.recruiter for c in plus_claims if c.type in ("F", "F!")})
    n_p = len(plus) - n_f
    n_rej = len({c.recruiter for c in plus_claims if c.type == "F!"})

    measure = measure_summary(rule, C) if rule.measure else None
    if measure is not None and len(plus) >= 2 and measure["common"] is None:
        tier, label = "Contested", f"Contested range {len(plus)}"
    elif plus and minus:
        tier, label = "Contested", f"Contested {len(plus)}-{len(minus)}"
    elif len(plus) >= 3:
        tier, label = "Consensus", f"Consensus {len(plus)}"
    elif len(plus) == 2:
        tier, label = "Supported", "Supported 2"
    elif len(plus) == 1:
        tier, label = "Single source", "Single source 1"
    else:
        tier, label = "No support", "No support"

    if rule.category == "X":
        severity = "n/a"
    elif tier == "Contested":
        severity = "Judgment"
    elif tier == "No support":
        severity = "n/a"
    else:
        start = {"Consensus": "High", "Supported": "Medium", "Single source": "Low"}[tier]
        severity = start
        if n_rej >= 2:
            severity = "Critical"
        elif n_rej == 1:
            severity = SEVERITIES[min(SEVERITIES.index(start) + 1, SEVERITIES.index("High"))]

    evidence = f"{label} ({n_f}F/{n_p}P, {n_rej} report rejecting)"
    if measure is not None and measure["by_recruiter"]:
        evidence += f"; {measure['text']}"
    ids = sorted(c.id for c in C if c.id)
    by_stance = {s: sorted(c.id for c in claims if rule.id in c.rules and c.stance == s and c.id)
                 for s in "+-~"}
    return {
        "category": rule.category,
        "text": rule.text,
        "check": rule.check,
        "status": rule.status,
        "tier": tier,
        "label": label,
        "evidence": evidence,
        "measure": measure,
        "plus": sorted(plus),
        "minus": sorted(minus),
        "self_contradicting": sorted(both),
        "n_f": n_f,
        "n_p": n_p,
        "n_rej": n_rej,
        "severity": severity,
        "claims": {"counted": ids, "for": by_stance["+"], "against": by_stance["-"],
                   "notes": by_stance["~"]},
    }


def fmt_num(x: float | None) -> str:
    return "" if x is None else f"{x:g}"


def fmt_range(lo: float | None, hi: float | None, unit: str) -> str:
    if lo is not None and lo == hi:
        if lo == 1 and unit.endswith("s"):
            unit = unit[:-1]  # "1 page", "1 second"
        return f"{fmt_num(lo)} {unit}"
    if lo is None:
        return f"at most {fmt_num(hi)} {unit}"
    if hi is None:
        return f"at least {fmt_num(lo)} {unit}"
    return f"{fmt_num(lo)} to {fmt_num(hi)} {unit}"


def _median(xs: list[float]) -> float | None:
    xs = sorted(xs)
    if not xs:
        return None
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2


def _intersect(ranges):
    los = [lo for lo, _ in ranges if lo is not None]
    his = [hi for _, hi in ranges if hi is not None]
    return (max(los) if los else None), (min(his) if his else None)


def own_range(ranges: list[tuple[float | None, float | None]]) -> tuple[float | None, float | None]:
    """One recruiter's range: their statements read as constraints ("2 to 5 pages" and "more
    than one page" give 2 to 5); when they conflict, the hull of everything they said."""
    lo, hi = _intersect(ranges)
    if lo is None or hi is None or lo <= hi:
        return lo, hi
    los = [x for x, _ in ranges]
    his = [y for _, y in ranges]
    return (None if None in los else min(los)), (None if None in his else max(his))


def measure_summary(rule: Rule, counted_claims: list[Claim]) -> dict:
    """Distribution of the stated values on a measure rule (ADR 0003). Each recruiter's range is
    the union of their values; `common` is the range every recruiter's range contains, or None
    when two of them do not overlap."""
    unit = rule.measure.unit
    values: dict[str, list[tuple[float | None, float | None]]] = {}
    conditional: dict[str, list[tuple[float | None, float | None, str]]] = {}
    for c in counted_claims:
        if c.value is None or c.stance != "+":
            continue
        values.setdefault(c.recruiter, [])
        if c.value.condition:
            conditional.setdefault(c.recruiter, []).append(
                (c.value.min, c.value.max, c.value.condition))
        else:
            values[c.recruiter].append((c.value.min, c.value.max))
    # A recruiter's range comes from their unconditional values; one who only gave conditional
    # values is represented by all of them.
    by = {r: list(own_range(v or [(lo, hi) for lo, hi, _ in conditional[r]]))
          for r, v in values.items()}
    los = [lo for lo, _ in by.values() if lo is not None]
    his = [hi for _, hi in by.values() if hi is not None]
    c_lo = max(los) if los else None
    c_hi = min(his) if his else None
    common = None if c_lo is not None and c_hi is not None and c_lo > c_hi else [c_lo, c_hi]
    parts = []
    for r, (lo, hi) in sorted(by.items()):
        cond = "; ".join(f"{c}: {fmt_range(a, b, unit)}" for a, b, c in conditional.get(r, []))
        parts.append(f"{r} {fmt_range(lo, hi, unit)}" + (f" ({cond})" if cond else ""))
    text = ", ".join(parts)
    if len(by) > 1:
        text += "; common " + (fmt_range(*common, unit) if common else "none")
    return {"unit": unit, "question": rule.measure.question,
            "by_recruiter": {r: v for r, v in sorted(by.items())}, "common": common,
            "conditional": {r: [list(x) for x in v] for r, v in sorted(conditional.items())},
            "median_min": _median(los), "median_max": _median(his), "text": text}


def order_key(rule_id: str, r: dict) -> tuple:
    tier = {"Consensus": 0, "Supported": 1, "Contested": 2, "Single source": 3}.get(r["tier"], 4)
    return (tier, -len(r["plus"]), -SEVERITY_RANK[r["severity"]], CATEGORY_ORDER[r["category"]],
            rule_sort_key(rule_id))


def compute(repo: Repo, claims: list[Claim] | None = None, rules: list[Rule] | None = None) -> dict:
    claims = load_claims(repo) if claims is None else claims
    rules = load_rules(repo) if rules is None else rules
    flag = repo.settings.ledger.count_independent_hosts
    out = {rule.id: tally_rule(rule, claims, flag) for rule in rules}
    order = sorted(out, key=lambda rid: order_key(rid, out[rid]))
    active = [rid for rid in order if out[rid]["status"] == "active"]
    labels = {t: sum(1 for rid in active if out[rid]["tier"] == t and out[rid]["category"] != "X")
              for t in TIERS}
    return {
        "schema": TALLY_SCHEMA,
        "count_independent_hosts": flag,
        "totals": {
            "sources": len({c.source for c in claims}),
            "recruiters": len({c.recruiter for c in claims}),
            "claims": len(claims),
            "rules": sum(1 for rid in active if out[rid]["category"] != "X"),
            "out_of_scope_rules": sum(1 for rid in active if out[rid]["category"] == "X"),
            "labels": labels,
        },
        "recruiters": sorted({c.recruiter for c in claims}),
        "order": order,
        "rules": out,
    }


def problems(tally: dict) -> list[str]:
    """Active in-scope rules with no support are errors (spec 02 section 8)."""
    return [f"{rid}: No support" for rid in tally["order"]
            if tally["rules"][rid]["tier"] == "No support" and tally["rules"][rid]["category"] != "X"
            and tally["rules"][rid]["status"] == "active"]


def snapshot_path(repo: Repo):
    return repo.root / "reports" / "tally.json"


def write_snapshot(repo: Repo, tally: dict, version: str | None = None) -> None:
    data = {**tally, "version": version, "date": dt.date.today().isoformat()}
    write_json(snapshot_path(repo), data)


def change_report(repo: Repo, new: dict, old: dict | None, title: str) -> str:
    """Markdown report of what changed between the last snapshot and now (spec 02 section 9)."""
    old_rules = (old or {}).get("rules", {})
    new_rules = new["rules"]
    lines = [f"# Change report: {title}", "",
             "Generated by `rrs ledger tally --report`; compared with "
             + (f"`reports/tally.json` ({old.get('version') or 'unversioned'}, {old.get('date')})."
                if old else "nothing (no `reports/tally.json` yet), so every rule is new."), ""]

    def section(name: str, items: list[str]) -> None:
        lines.extend([f"## {name} ({len(items)})", ""])
        lines.extend(f"- {i}" for i in items) if items else lines.append("None.")
        lines.append("")

    def sev(r: dict) -> str:
        return f"{r['label']} [{r['severity']}]"

    label_changes, sev_changes, supporters, contested, lost, added, retired = ([] for _ in range(7))
    for rid in new["order"]:
        r = new_rules[rid]
        o = old_rules.get(rid)
        if o is None:
            added.append(f"{rid} ({r['category']}): {r['text']} {sev(r)}")
            continue
        if r["status"] == "retired" and o["status"] != "retired":
            retired.append(rid)
            continue
        if r["label"] != o["label"]:
            label_changes.append(f"{rid}: {o['label']} -> {r['label']}")
        elif r["plus"] != o["plus"] or r["minus"] != o["minus"]:
            supporters.append(f"{rid}: {r['label']}, for {', '.join(o['plus']) or 'none'} -> "
                              f"{', '.join(r['plus']) or 'none'}; against "
                              f"{', '.join(o['minus']) or 'none'} -> {', '.join(r['minus']) or 'none'}")
        if r["severity"] != o["severity"]:
            sev_changes.append(f"{rid}: {o['severity']} -> {r['severity']}")
        if r["tier"] == "Contested" and o["tier"] != "Contested":
            contested.append(f"{rid}: {r['label']} (for {', '.join(r['plus'])}; against "
                             f"{', '.join(r['minus'])})")
        if r["tier"] == "No support" and o["tier"] != "No support":
            lost.append(f"{rid}: was {o['label']}")
    section("Label changes", label_changes)
    section("Severity changes", sev_changes)
    section("Supporter set changed, same label", supporters)
    section("Newly contested", contested)
    section("Lost all support", lost)
    section("New rules", added)
    section("Retired rules", retired)

    recruiters = load_recruiters(repo)
    targets = load_targets(repo)
    match = targets.default_target.match if targets else {}
    new_people = [r for r in new["recruiters"] if r not in (old or {}).get("recruiters", [])]
    section("New recruiters", [
        f"{code} {recruiters[code].name if code in recruiters else '?'}: "
        f"{recruiters[code].type if code in recruiters else '?'}, match for "
        f"{targets.default if targets else 'the default target'}: {match.get(code, 'not set')}"
        for code in new_people
    ])
    t = new["totals"]
    lines.append(f"Totals: {t['sources']} sources, {t['recruiters']} recruiters, {t['claims']} claims, "
                 f"{t['rules']} rules (" + ", ".join(f"{t['labels'][k]} {k}" for k in TIERS[:4])
                 + f"), {t['out_of_scope_rules']} out of scope.")
    return "\n".join(lines) + "\n"


def write_report(repo: Repo, label: str, today: dt.date | None = None) -> tuple[str, str]:
    """Write reports/changes/<date>-<label>.md. Returns (path relative to the repo, text)."""
    new = compute(repo)
    path = snapshot_path(repo)
    old = read_json(path) if path.exists() else None
    date = (today or dt.date.today()).isoformat()
    text = change_report(repo, new, old, f"{date} {label}")
    out = repo.root / "reports" / "changes" / f"{date}-{label}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    return str(out.relative_to(repo.root)), text
