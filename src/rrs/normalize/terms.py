"""Term annotation against glossary/terms.yaml (spec 01 section 3.2).

Persian variants are matched on the compact form, but aligned to token starts so that a short
variant does not fire inside an unrelated word (جست, Jest, inside جستجو). A match may end inside
a token only when the rest of the token is a common Persian suffix or enclitic (اسکیلشو).
Latin variants are matched as whole `norm` token sequences, with an optional plural "s".
"""

from __future__ import annotations

from dataclasses import dataclass

from rrs.glossary import Term
from rrs.normalize.text import arabic_share, norm

PERSIAN_SUFFIXES = frozenset(
    [
        "", "ها", "های", "هایی", "هاش", "هاشو", "هاشون", "هات", "هامون", "هاتون", "هارو",
        "ی", "یی", "ای", "و", "رو", "ش", "شو", "شون", "شونو", "ت", "تو", "تون", "م", "مو",
        "مون", "اش", "ام", "ات", "مه", "ه", "هه", "یه", "ست", "اس",
    ]
)


@dataclass(frozen=True)
class _Variant:
    canonical: str
    variant: str
    persian: bool
    key: str | tuple[str, ...]  # compact string for Persian, token tuple for Latin
    amb: tuple[str, ...]


class TermMatcher:
    def __init__(self, terms: list[Term]):
        self.variants: list[_Variant] = []
        for t in terms:
            for v in t.variants:
                n = norm(v)
                if not n:
                    continue
                persian = (arabic_share(v) or 0) > 0.5
                key = n.replace(" ", "") if persian else tuple(n.split(" "))
                self.variants.append(_Variant(t.canonical, v, persian, key, tuple(t.ambiguous_with)))

    def annotate(self, norm_text: str) -> list[dict]:
        tokens = norm_text.split(" ") if norm_text else []
        hits: list[tuple[int, int, _Variant]] = []
        for v in self.variants:
            for start in _find(tokens, v):
                hits.append((start, -len(v.variant), v))
        out: list[dict] = []
        seen: set[tuple[str, str]] = set()
        for _, _, v in sorted(hits, key=lambda h: (h[0], h[1], h[2].canonical)):
            if (v.canonical, v.variant) in seen:
                continue
            seen.add((v.canonical, v.variant))
            d = {"c": v.canonical, "v": v.variant}
            if v.amb:
                d["amb"] = list(v.amb)
            out.append(d)
        return out


def _find(tokens: list[str], v: _Variant) -> list[int]:
    if v.persian:
        return _find_persian(tokens, v.key)  # type: ignore[arg-type]
    return _find_latin(tokens, v.key)  # type: ignore[arg-type]


def _find_latin(tokens: list[str], key: tuple[str, ...]) -> list[int]:
    n = len(key)
    found = []
    for i in range(len(tokens) - n + 1):
        window = tokens[i : i + n]
        if window[:-1] != list(key[:-1]):
            continue
        last = window[-1]
        if last == key[-1] or (len(key[-1]) > 1 and last == key[-1] + "s"):
            found.append(i)
    return found


def _find_persian(tokens: list[str], key: str) -> list[int]:
    found = []
    for i in range(len(tokens)):
        if not key.startswith(tokens[i][: len(key)]):
            continue
        acc = ""
        for j in range(i, len(tokens)):
            before = len(acc)
            acc += tokens[j]
            if len(acc) >= len(key):
                if before < len(key) and acc.startswith(key) and acc[len(key) :] in PERSIAN_SUFFIXES:
                    found.append(i)
                break
            if not key.startswith(acc):
                break
    return found
