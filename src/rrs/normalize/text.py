"""Text cleanup for `text` and the `norm` / `norm_compact` matching forms.

Every `norm` rule is local to one character, so `norm_with_map` can report, for each
character of the normalized string, the index of the character of the input it came from.
Re-anchoring uses that map to cut verbatim quotes out of `text`.
"""

from __future__ import annotations

import unicodedata

ZWNJ = "‌"

# Invisible marks removed from both `text` and `norm` (section 3.1).
INVISIBLE = frozenset(
    [0x200E, 0x200F, 0xFEFF, *range(0x202A, 0x202F), *range(0x2066, 0x206A)]
)

# Character unifications applied in `norm` only.
NORM_MAP = {
    "ي": "ی",  # Arabic Yeh -> Persian Yeh
    "ى": "ی",  # Alef Maksura -> Persian Yeh
    "ك": "ک",  # Arabic Kaf -> Keheh
    "ة": "ه",  # Teh Marbuta -> Heh
    "ۀ": "ه",  # Heh with Yeh above -> Heh
    "آ": "ا",  # Alef with madda -> Alef
    "أ": "ا",  # Alef with hamza above -> Alef
    "إ": "ا",  # Alef with hamza below -> Alef
    "ؤ": "و",  # Waw with hamza -> Waw
    "ئ": "ی",  # Yeh with hamza -> Persian Yeh
}
for _i in range(10):
    NORM_MAP[chr(0x06F0 + _i)] = str(_i)  # Persian digits
    NORM_MAP[chr(0x0660 + _i)] = str(_i)  # Arabic-Indic digits

# Removed in `norm`: tatweel, harakat and related marks, superscript alef.
NORM_DROP = frozenset([0x0640, *range(0x064B, 0x0660), 0x0670])

# Punctuation kept in `norm` because it is part of tech terms (C#).
KEEP_PUNCT = frozenset("#")


def clean_text(s: str) -> str:
    """The tidy applied to `text`: NFC, invisible marks removed, whitespace collapsed."""
    s = unicodedata.normalize("NFC", s)
    s = "".join(ch for ch in s if ord(ch) not in INVISIBLE)
    return " ".join(s.split())


def _norm_char(ch: str) -> str:
    out = []
    for c in unicodedata.normalize("NFKC", ch):
        o = ord(c)
        if o in INVISIBLE or o in NORM_DROP:
            continue
        if c in NORM_MAP:
            out.append(NORM_MAP[c])
        elif c == ZWNJ or c.isspace():
            out.append(" ")
        elif unicodedata.category(c).startswith("P") and c not in KEEP_PUNCT:
            out.append(" ")
        else:
            out.append(c.lower())
    return "".join(out)


def norm_with_map(s: str) -> tuple[str, list[int]]:
    """`norm` of s, plus for each output character the index in s it came from."""
    chars: list[str] = []
    src: list[int] = []
    for i, ch in enumerate(s):
        for c in _norm_char(ch):
            if c == " " and (not chars or chars[-1] == " "):
                continue
            chars.append(c)
            src.append(i)
    if chars and chars[-1] == " ":
        chars.pop()
        src.pop()
    return "".join(chars), src


def norm(s: str) -> str:
    return norm_with_map(s)[0]


def norm_compact(s: str) -> str:
    """`norm` with every space removed: used for Persian substring matching."""
    return norm(s).replace(" ", "")


def compact_with_map(s: str) -> tuple[str, list[int]]:
    n, m = norm_with_map(s)
    keep = [i for i, c in enumerate(n) if c != " "]
    return "".join(n[i] for i in keep), [m[i] for i in keep]


def is_arabic_letter(c: str) -> bool:
    o = ord(c)
    return c.isalpha() and (
        0x0600 <= o <= 0x06FF or 0x0750 <= o <= 0x077F or 0xFB50 <= o <= 0xFDFF
        or 0xFE70 <= o <= 0xFEFF
    )


def arabic_share(s: str) -> float | None:
    letters = [c for c in s if c.isalpha()]
    if not letters:
        return None
    return sum(1 for c in letters if is_arabic_letter(c)) / len(letters)


def lang_tag(s: str, fa_min: float = 0.5, en_max: float = 0.1, default: str = "en") -> str:
    """`fa`, `en` or `mixed` from the share of Arabic-script letters among all letters."""
    share = arabic_share(s)
    if share is None:
        return default
    if share >= fa_min:
        return "fa"
    if share <= en_max:
        return "en"
    return "mixed"
