"""Re-anchor claims to sentence IDs after a transcript changes (spec 01 sections 7 and 10).

A new NotebookLM export of a source changes its sentence IDs, so every claim's anchors are mapped
again from their quotes. For each anchor: search the claim's source, restricted to sentences by
the claim's recruiter, over windows of 1 to 3 consecutive sentences. Narrow by context first (the
old start time +- the window when the source has timing, otherwise the claim's episode); fall back
to the whole source when the narrowed search finds nothing. Exact matches are accepted; otherwise
rapidfuzz partial_ratio on `norm` decides accepted, review or manual. Owner decisions for review
and manual items go in ledger/migration/reanchor-decisions.yaml and are applied on the next run.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from rapidfuzz import fuzz

from rrs.config import ReanchorSettings, Repo
from rrs.jsonio import fmt_time, read_json, read_jsonl, read_yaml, write_jsonl
from rrs.normalize.text import compact_with_map, is_arabic_letter, norm_with_map


@dataclass
class Window:
    sentences: list[dict]  # sentence dicts, consecutive in the transcript, all by the recruiter
    start: float | None

    @property
    def text(self) -> str:
        return " ".join(s["text"] for s in self.sentences)


@dataclass
class Candidate:
    window: Window
    score: float
    exact: bool
    quote: str  # verbatim span of the window's text

    @property
    def sentence_id(self) -> str:
        return self.window.sentences[0]["id"]

    def anchor(self) -> dict:
        return {"sentence_id": self.sentence_id, "t_start": self.window.start, "quote": self.quote}


@dataclass
class QuoteResult:
    claim_id: str
    index: int  # position in the claim's anchors
    old_sentence_id: str | None
    quote: str
    status: str  # accepted | review | manual | decided
    candidates: list[Candidate] = field(default_factory=list)
    note: str = ""


def claim_anchors(claim: dict) -> list[dict]:
    return [a for a in claim.get("anchors") or [] if (a.get("quote") or "").strip()]


def is_persian(s: str) -> bool:
    return any(is_arabic_letter(c) for c in s)


def windows_for(transcript: dict, person: str, max_n: int) -> list[Window]:
    """All windows of 1..max_n consecutive sentences spoken by `person`."""
    flat = [(t, s) for t in transcript["turns"] for s in t["sentences"]]
    out = []
    for i in range(len(flat)):
        for n in range(1, max_n + 1):
            span = flat[i : i + n]
            if len(span) < n or any(t["person"] != person for t, _ in span):
                break
            out.append(Window([s for _, s in span], span[0][1]["start"]))
    return out


def _expand_to_words(text: str, a: int, b: int) -> tuple[int, int]:
    while a > 0 and not text[a - 1].isspace():
        a -= 1
    while b < len(text) and not text[b].isspace():
        b += 1
    return a, b


def exact_span(window: Window, quote: str) -> str | None:
    text = window.text
    if is_persian(quote):
        key, _ = compact_with_map(quote)
        hay, hmap = compact_with_map(text)
        i = hay.find(key) if key else -1
        if i < 0:
            return None
        a, b = hmap[i], hmap[i + len(key) - 1] + 1
    else:
        key, _ = norm_with_map(quote)
        hay, hmap = norm_with_map(text)
        if not key:
            return None
        i = f" {hay} ".find(f" {key} ")
        if i < 0:
            return None
        a, b = hmap[i], hmap[i + len(key) - 1] + 1
    a, b = _expand_to_words(text, a, b)
    return text[a:b]


def fuzzy_span(window: Window, quote: str) -> tuple[float, str]:
    key, _ = norm_with_map(quote)
    hay, hmap = norm_with_map(window.text)
    if not key or not hay:
        return 0.0, ""
    al = fuzz.partial_ratio_alignment(key, hay)
    if al is None or al.dest_end <= al.dest_start:
        return 0.0, ""
    a, b = hmap[al.dest_start], hmap[al.dest_end - 1] + 1
    a, b = _expand_to_words(window.text, a, b)
    return al.score, window.text[a:b]


def best_candidates(windows: list[Window], quote: str, top: int = 3) -> list[Candidate]:
    exact = []
    for w in windows:
        span = exact_span(w, quote)
        if span is not None:
            exact.append(Candidate(w, 100.0, True, span))
    if exact:
        # Shortest window first, then earliest; drop windows that only extend a shorter hit.
        exact.sort(key=lambda c: (len(c.window.sentences), c.sentence_id))
        return exact[:top]
    scored = []
    for w in windows:
        score, span = fuzzy_span(w, quote)
        if span:
            scored.append(Candidate(w, score, False, span))
    scored.sort(key=lambda c: (-c.score, len(c.window.sentences), c.sentence_id))
    out: list[Candidate] = []
    for c in scored:
        if all(c.sentence_id != o.sentence_id for o in out):
            out.append(c)
        if len(out) == top:
            break
    return out


def narrow(windows: list[Window], claim: dict, anchor: dict, transcript: dict,
           settings: ReanchorSettings) -> tuple[list[Window], str]:
    t = anchor.get("t_start")
    if t is not None and transcript["timing"] != "none":
        lo, hi = t - settings.time_window_s, t + settings.time_window_s
        return [w for w in windows if w.start is not None and lo <= w.start <= hi], (
            f"within {settings.time_window_s}s of {fmt_time(t)}"
        )
    episode = claim.get("episode")
    if episode and any(w.sentences[0].get("episode") == episode for w in windows):
        return [w for w in windows if w.sentences[0].get("episode") == episode], f"episode {episode}"
    return windows, ""


def load_decisions(repo: Repo) -> dict[tuple[str, int], dict]:
    path = repo.ledger / "migration" / "reanchor-decisions.yaml"
    if not path.exists():
        return {}
    out = {}
    for d in read_yaml(path) or []:
        out[(d["claim"], int(d.get("anchor", 0)))] = d
    return out


def _decided_anchor(d: dict, transcript: dict) -> dict:
    sentences = {s["id"]: s for t in transcript["turns"] for s in t["sentences"]}
    s = sentences.get(d["sentence_id"])
    if s is None:
        raise ValueError(f"decision for {d['claim']}: unknown sentence {d['sentence_id']}")
    return {"sentence_id": s["id"], "t_start": s["start"], "quote": d.get("quote_text") or s["text"]}


def reanchor_claim(claim: dict, transcript: dict, settings: ReanchorSettings,
                   decisions: dict) -> list[QuoteResult]:
    results = []
    all_windows = windows_for(transcript, claim["recruiter"], settings.max_window_sentences)
    for i, anchor in enumerate(claim_anchors(claim)):
        q = anchor["quote"]
        old = anchor.get("sentence_id")
        if (claim["id"], i) in decisions:
            results.append(QuoteResult(claim["id"], i, old, q, "decided"))
            continue
        windows, how = narrow(all_windows, claim, anchor, transcript, settings)
        cands = best_candidates(windows, q) if windows else []
        note = how
        if how and not (cands and (cands[0].exact or cands[0].score >= settings.accept)):
            wide = best_candidates(all_windows, q)
            if wide and (not cands or wide[0].score > cands[0].score):
                cands = wide
                note = f"not found {how}; searched the whole source"
        if not cands:
            results.append(QuoteResult(claim["id"], i, old, q, "manual", [], note or "no candidates"))
            continue
        top = cands[0]
        if top.exact or top.score >= settings.accept:
            status = "accepted"
        elif top.score >= settings.review:
            status = "review"
        else:
            status = "manual"
        results.append(QuoteResult(claim["id"], i, old, q, status, cands, note))
    return results


def run_reanchor(repo: Repo, sources: list[str] | None = None,
                 write: bool = True) -> tuple[list[QuoteResult], str]:
    """Re-anchor the claims of `sources` (default: all). A claim's anchors are replaced only
    when every one of them is accepted or decided; the rest wait for decisions."""
    path = repo.ledger / "claims.jsonl"
    if not path.exists():
        raise FileNotFoundError("ledger/claims.jsonl not found: there are no claims to re-anchor")
    claims = read_jsonl(path)
    settings = repo.settings.reanchor
    decisions = load_decisions(repo)
    transcripts: dict[str, dict] = {}
    all_results: list[QuoteResult] = []
    for claim in claims:
        sid = claim["source"]
        if (sources and sid not in sources) or not claim_anchors(claim):
            continue
        if sid not in transcripts:
            transcripts[sid] = read_json(repo.transcript_path(sid))
        results = reanchor_claim(claim, transcripts[sid], settings, decisions)
        all_results.extend(results)
        if all(r.status in ("accepted", "decided") for r in results):
            claim["anchors"] = [
                _decided_anchor(decisions[(r.claim_id, r.index)], transcripts[sid])
                if r.status == "decided"
                else r.candidates[0].anchor()
                for r in results
            ]
    report = render_report(all_results, claims)
    if write:
        write_jsonl(path, claims)
        out = repo.ledger / "migration" / "reanchor-report.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
    return all_results, report


def _cell(s: str, n: int = 120) -> str:
    s = s.replace("|", "\\|").replace("\n", " ")
    return s if len(s) <= n else s[: n - 3] + "..."


def render_report(results: list[QuoteResult], claims: list[dict]) -> str:
    source_of = {c["id"]: c["source"] for c in claims}
    statuses = ["accepted", "decided", "review", "manual"]
    by_source: dict[str, dict[str, int]] = {}
    for r in results:
        row = by_source.setdefault(source_of[r.claim_id], dict.fromkeys(statuses, 0))
        row[r.status] += 1
    lines = [
        "# Re-anchoring report",
        "",
        "Generated by `rrs reanchor`; do not edit. Record decisions in "
        "`ledger/migration/reanchor-decisions.yaml` and re-run.",
        "",
        "| Source | " + " | ".join(statuses) + " | total |",
        "|---|" + "---|" * (len(statuses) + 1),
    ]
    totals = dict.fromkeys(statuses, 0)
    for sid in sorted(by_source):
        row = by_source[sid]
        for k in statuses:
            totals[k] += row[k]
        lines.append(f"| {sid} | " + " | ".join(str(row[k]) for k in statuses)
                     + f" | {sum(row.values())} |")
    lines.append("| all | " + " | ".join(str(totals[k]) for k in statuses)
                 + f" | {sum(totals.values())} |")
    exact = sum(1 for r in results if r.status == "accepted" and r.candidates[0].exact)
    lines += ["", f"Exact matches: {exact}. Fuzzy accepted: {totals['accepted'] - exact}.", ""]
    for status in ("review", "manual"):
        items = [r for r in results if r.status == status]
        lines += [f"## {status.capitalize()} ({len(items)})", ""]
        if not items:
            lines += ["None.", ""]
            continue
        lines += ["| Claim | Old sentence | Quote | Candidates (score, sentence, text) | Note |",
                  "|---|---|---|---|---|"]
        for r in items:
            cands = "<br>".join(
                f"{c.score:.0f} `{c.sentence_id}` {_cell(c.quote, 90)}" for c in r.candidates
            ) or "none"
            claim_ref = f"{r.claim_id}" + (f" a{r.index}" if r.index else "")
            lines.append(f"| {claim_ref} | `{r.old_sentence_id}` | {_cell(r.quote)} | {cands} "
                         f"| {_cell(r.note, 60)} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
