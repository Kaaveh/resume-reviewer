"""Search the index: Persian queries as norm_compact substrings, English as norm phrases."""

from __future__ import annotations

from rrs.jsonio import fmt_time
from rrs.normalize.text import arabic_share, norm


def is_persian_query(q: str) -> bool:
    return (arabic_share(q) or 0) > 0


def matcher(query: str):
    n = norm(query)
    if is_persian_query(query):
        key = n.replace(" ", "")
        return lambda row: bool(key) and key in row["norm_compact"]
    padded = f" {n} "
    return lambda row: bool(n) and padded in f" {row['norm']} "


def search(
    rows: list[dict],
    query: str,
    source: str | None = None,
    person: str | None = None,
    role: str | None = None,
    term: str | None = None,
    lang: str | None = None,
    span: int = 2,
) -> list[dict]:
    """Rows whose sentence matches, or whose sentence and the next ones (up to `span` sentences
    of the same turn) match together; quotes often cross the 25-word windows of unpunctuated
    turns. Such hits carry `span` > 1 and are reported at their first sentence."""
    match = matcher(query) if query else (lambda row: True)
    out = []
    for i, r in enumerate(rows):
        if source and r["source"] != source:
            continue
        if person and r["person"] != person:
            continue
        if role and r["role"] != role:
            continue
        if lang and r["lang"] != lang:
            continue
        if term and not any(t["c"].casefold() == term.casefold() for t in r["terms"]):
            continue
        if match(r):
            out.append(r)
            continue
        if not query:
            continue
        turn = r["id"].rsplit(".", 1)[0]
        for n in range(2, span + 1):
            group = rows[i : i + n]
            if len(group) < n or group[-1]["id"].rsplit(".", 1)[0] != turn:
                break
            if match(group[-1]):
                break  # the later sentence matches on its own and is reported there
            joined = {"norm": " ".join(g["norm"] for g in group),
                      "norm_compact": "".join(g["norm_compact"] for g in group)}
            if match(joined):
                out.append({**r, "span": n})
                break
    return out


def format_hit(row: dict, width: int = 160) -> str:
    ts = fmt_time(row["start"])
    more = f" (+{row['span'] - 1} sentence)" if row.get("span", 1) > 1 else ""
    text = row["text"] if len(row["text"]) <= width else row["text"][: width - 3] + "..."
    return f"{row['id']}{' [' + ts + ']' if ts else ''} {row['person']}{more}: {text}"
