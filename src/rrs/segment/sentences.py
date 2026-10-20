"""Split one turn's cleaned text into sentences (spec 01 section 5).

The result is a list of word lists. Words are whitespace tokens of `text`, so joining a
sentence's words with single spaces gives its verbatim (whitespace-tidied) `text`.
"""

from __future__ import annotations

import functools
import re

from rrs.config import SegmentSettings

FINAL = ".?!؟…"
PERSIAN_FINAL = ".?!؟؛…"
CLOSERS = "\"'»)]”’"
COMMAS = ",،"
FINAL_RE = re.compile(r"[.?!؟…]")


@functools.cache
def _pysbd():
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        import pysbd

    return pysbd.Segmenter(language="en", clean=False)


def split_persian(text: str) -> list[str]:
    """Rule-based split on . ؟ ! ؛ (and ? …), never inside numbers such as 7.5 or ۷.۵."""
    out: list[str] = []
    start = 0
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch in PERSIAN_FINAL:
            if ch == "." and 0 < i < n - 1 and text[i - 1].isdigit() and text[i + 1].isdigit():
                i += 1
                continue
            j = i + 1
            while j < n and (text[j] in PERSIAN_FINAL or text[j] in CLOSERS):
                j += 1
            if j == n or text[j].isspace():
                out.append(text[start:j])
                start = j
            i = j
            continue
        i += 1
    out.append(text[start:])
    return [s.strip() for s in out if s.strip()]


def split_english(text: str) -> list[str]:
    return [s.strip() for s in _pysbd().segment(text) if s.strip()]


def punctuation_split(text: str, persian: bool) -> list[list[str]]:
    words = [p.split() for p in (split_persian(text) if persian else split_english(text))]
    # A splitter may only cut the text, never change it; fall back to the rule-based one.
    if [w for p in words for w in p] != text.split():
        words = [p.split() for p in split_persian(text)]
    return words


def _comma_cut(words: list[str]) -> int | None:
    """Index after which to cut: the comma nearest the middle, never at either end."""
    candidates = [i + 1 for i, w in enumerate(words[:-1]) if w and w[-1] in COMMAS]
    if not candidates:
        return None
    mid = len(words) / 2
    return min(candidates, key=lambda k: (abs(k - mid), k))


def length_guard(words: list[str], s: SegmentSettings) -> list[list[str]]:
    if len(words) <= s.max_words:
        return [words]
    cut = _comma_cut(words)
    if cut is None:
        if len(words) <= s.hard_max_words:
            return [words]
        cut = len(words) // 2
    return length_guard(words[:cut], s) + length_guard(words[cut:], s)


def windows(words: list[str], size: int) -> list[list[str]]:
    return [words[i : i + size] for i in range(0, len(words), size)]


def merge_fragments(sentences: list[list[str]], min_words: int) -> list[list[str]]:
    out: list[list[str]] = []
    for s in sentences:
        if out and len(s) < min_words:
            out[-1] = out[-1] + s
        else:
            out.append(s)
    # A short first sentence has no previous sentence: merge it into the next one.
    if len(out) > 1 and len(out[0]) < min_words:
        out[1] = out[0] + out[1]
        out.pop(0)
    return out


def is_unpunctuated(pieces: list[list[str]], s: SegmentSettings) -> bool:
    n_words = sum(len(p) for p in pieces)
    return n_words > s.window_words and n_words / len(pieces) > s.unpunctuated_avg_words


def split_turn(text: str, persian: bool, s: SegmentSettings) -> tuple[list[list[str]], bool]:
    """Sentences of one turn as word lists, and whether the turn was treated as unpunctuated."""
    if not text.strip():
        return [], False
    pieces = punctuation_split(text, persian)
    unpunct = is_unpunctuated(pieces, s)
    out: list[list[str]] = []
    for p in pieces:
        out.extend(windows(p, s.window_words) if unpunct else length_guard(p, s))
    return merge_fragments(out, s.min_fragment_words), unpunct
