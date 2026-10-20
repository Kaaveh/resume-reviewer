"""Build corpus/Sxxx/transcript.json from transcript.raw.json (spec 01 sections 2, 5, 7, 8)."""

from __future__ import annotations

import re

from rrs.config import Repo, Settings
from rrs.glossary import load_terms
from rrs.jsonio import read_json, write_json
from rrs.normalize.terms import TermMatcher
from rrs.normalize.text import clean_text, lang_tag, norm_with_map
from rrs.schemas import validate
from rrs.segment.sentences import split_turn
from rrs.sources import Correction, Source, load_source

SCHEMA = "rrs.transcript/1"
ID_SCHEME = 1


def turn_id(source_id: str, n: int) -> str:
    return f"{source_id}.t{n:04d}"


def sentence_id(tid: str, k: int) -> str:
    if k > 999:
        raise ValueError(f"{tid}: more than 999 sentences")
    return f"{tid}.s{k:03d}"


def segment(raw: dict, source: Source, settings: Settings) -> dict:
    """Turns and sentences with IDs, text, lang and start. A pure function of its inputs."""
    roles = source.roles
    default_lang = source.languages[0] if source.languages else "en"
    turns = []
    for t in raw["turns"]:
        text = clean_text(t["text"])
        turn_lang = lang_tag(text, settings.lang.fa_min, settings.lang.en_max, default_lang)
        sents, unpunct = split_turn(text, turn_lang != "en", settings.segment)
        tid = turn_id(raw["source_id"], t["n"])
        sentences = []
        for k, words in enumerate(sents, 1):
            stext = " ".join(words)
            sentences.append(
                {
                    "id": sentence_id(tid, k),
                    "episode": None,
                    "lang": lang_tag(stext, settings.lang.fa_min, settings.lang.en_max, turn_lang),
                    "start": t["start"],
                    "text": stext,
                }
            )
        turn = {
            "id": tid,
            "n": t["n"],
            "person": t["person"],
            "role": roles[t["person"]],
            "start": t["start"],
            "split": "window" if unpunct else "punctuation",
            "sentences": sentences,
        }
        turns.append(turn)
    return {
        "schema": SCHEMA,
        "source_id": raw["source_id"],
        "transcript_version": source.transcript_version,
        "id_scheme": ID_SCHEME,
        "transcript_sha256": raw["transcript_sha256"],
        "timing": raw["timing"],
        "roles": dict(roles),
        "turns": turns,
    }


def _correction_re(c: Correction) -> re.Pattern:
    flags = re.IGNORECASE if c.ignore_case else 0
    return re.compile(rf"(?<!\w){re.escape(c.find)}(?!\w)", flags)


def apply_corrections(transcript: dict, corrections: list[Correction]) -> dict[str, int]:
    """Apply proper-noun corrections to sentence `text`, keeping `text_orig`. Idempotent."""
    counts: dict[str, int] = {}
    patterns = [(c, _correction_re(c)) for c in corrections]
    for turn in transcript["turns"]:
        for s in turn["sentences"]:
            original = s.pop("text_orig", s["text"])
            text = original
            for c, pat in patterns:
                if c.person and c.person != turn["person"]:
                    continue
                if c.turns is not None and turn["n"] not in c.turns:
                    continue
                text, n = pat.subn(c.replace, text)
                if n:
                    counts[c.find] = counts.get(c.find, 0) + n
            s["text"] = text
            if text != original:
                s["text_orig"] = original
    return counts


def normalize(transcript: dict, matcher: TermMatcher) -> None:
    """Fill `norm`, `norm_compact` and `terms` of every sentence from its `text`."""
    for turn in transcript["turns"]:
        for s in turn["sentences"]:
            n, _ = norm_with_map(s["text"])
            s["norm"] = n
            s["norm_compact"] = n.replace(" ", "")
            s["terms"] = matcher.annotate(n)


SENTENCE_KEYS = ["id", "episode", "lang", "start", "text", "text_orig", "norm", "norm_compact", "terms"]


def order_keys(transcript: dict) -> dict:
    for turn in transcript["turns"]:
        turn["sentences"] = [
            {k: s[k] for k in SENTENCE_KEYS if k in s} for s in turn["sentences"]
        ]
    return transcript


def transcript_from_raw(
    raw: dict, source: Source, settings: Settings, matcher: TermMatcher
) -> tuple[dict, dict[str, int]]:
    t = segment(raw, source, settings)
    counts = apply_corrections(t, source.corrections)
    normalize(t, matcher)
    return order_keys(t), counts


def build_transcript(repo: Repo, source_id: str) -> tuple[dict, dict[str, int]]:
    raw = read_json(repo.raw_path(source_id))
    matcher = TermMatcher(load_terms(repo))
    return transcript_from_raw(raw, load_source(repo, source_id), repo.settings, matcher)


def run_segment(repo: Repo, source_id: str) -> tuple[dict, dict[str, int]]:
    """Segment and normalize; episodes are re-applied by `rrs episodes --apply`."""
    from rrs.segment.episodes import apply_episodes_if_present

    t, counts = build_transcript(repo, source_id)
    apply_episodes_if_present(repo, t)
    validate(t, "transcript")
    write_json(repo.transcript_path(source_id), t)
    return t, counts


def run_normalize(repo: Repo, source_id: str) -> tuple[dict, dict[str, int]]:
    """Re-run corrections, normalization and terms on an existing transcript.json."""
    source = load_source(repo, source_id)
    path = repo.transcript_path(source_id)
    t = read_json(path)
    counts = apply_corrections(t, source.corrections)
    normalize(t, TermMatcher(load_terms(repo)))
    validate(order_keys(t), "transcript")
    write_json(path, t)
    return t, counts


def iter_sentences(transcript: dict):
    """(turn, sentence) pairs in transcript order."""
    for turn in transcript["turns"]:
        for s in turn["sentences"]:
            yield turn, s
