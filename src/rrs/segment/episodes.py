"""Topic episodes: proposal, validation and application (spec 01 section 6)."""

from __future__ import annotations

import re
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

from rrs.config import Repo
from rrs.jsonio import fmt_time, read_json, read_yaml, write_json
from rrs.normalize.text import norm_compact

EpisodeType = Literal["intro", "outro", "promo", "qa", "cv-review", "audience-q", "other"]
Verdict = Literal["invite", "borderline", "reject", "none"]

CUE_GAP = 3
LIVE_REVIEW_CUES = ["رزومه بعدی", "بریم سراغ", "بریم بعدی", "رزومه اول"]
QUESTION_RE = re.compile(
    r"\b(what|whats|how|why|when|where|which|who|do you|did you|does|can you|could you|"
    r"would you|should|is it|is there|are there|are you|have you|tell us|tell me|any advice|"
    r"any tips|talk about|let s talk|thoughts|opinion|introduce)\b"
)


class Episode(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(pattern=r"^S\d{3}\.e\d{2,3}$")
    type: EpisodeType
    label: str
    cv_owner: str | None = None
    from_: str = Field(alias="from")
    to: str
    verdict: Verdict | None = None
    verdict_reasons: list[str] = []
    notes: str = ""


class EpisodeError(ValueError):
    pass


def load_episodes(repo: Repo, source_id: str) -> list[Episode]:
    data = read_yaml(repo.episodes_path(source_id)) or []
    return [Episode.model_validate(e) for e in data]


def sentence_ids(transcript: dict) -> list[str]:
    return [s["id"] for t in transcript["turns"] for s in t["sentences"]]


def validate_episodes(transcript: dict, episodes: list[Episode]) -> dict[str, str]:
    """Check that episodes tile the transcript in order; return sentence ID -> episode ID."""
    sid = transcript["source_id"]
    ids = sentence_ids(transcript)
    pos = {s: i for i, s in enumerate(ids)}
    errors = []
    if not episodes:
        raise EpisodeError(f"{sid}: no episodes")
    expected_next = 0
    assignment: dict[str, str] = {}
    for k, e in enumerate(episodes, 1):
        want = f"{sid}.e{k:02d}"
        if e.id != want:
            errors.append(f"{e.id}: expected id {want}")
        if e.from_ not in pos or e.to not in pos:
            errors.append(f"{e.id}: unknown sentence {e.from_ if e.from_ not in pos else e.to}")
            continue
        a, b = pos[e.from_], pos[e.to]
        if a != expected_next:
            want_from = ids[expected_next] if expected_next < len(ids) else "the end"
            errors.append(f"{e.id}: starts at {e.from_}, expected {want_from}")
        if b < a:
            errors.append(f"{e.id}: ends before it starts")
        if e.cv_owner and e.cv_owner.casefold() in e.label.casefold():
            errors.append(f"{e.id}: label contains the CV owner's name; use a pseudonym")
        if e.type == "cv-review" and e.verdict is None:
            errors.append(f"{e.id}: cv-review needs a verdict (use none if the reviewer gave none)")
        for i in range(a, b + 1):
            assignment[ids[i]] = e.id
        expected_next = b + 1
    if expected_next != len(ids):
        errors.append(f"{sid}: sentences from {ids[expected_next]} on are in no episode")
    if errors:
        raise EpisodeError("\n".join(errors))
    return assignment


def assign(transcript: dict, assignment: dict[str, str] | None) -> None:
    for t in transcript["turns"]:
        for s in t["sentences"]:
            s["episode"] = assignment.get(s["id"]) if assignment else None


def apply_episodes_if_present(repo: Repo, transcript: dict) -> bool:
    path = repo.episodes_path(transcript["source_id"])
    if not path.exists():
        assign(transcript, None)
        return False
    assign(transcript, validate_episodes(transcript, load_episodes(repo, transcript["source_id"])))
    return True


def run_apply(repo: Repo, source_id: str) -> int:
    path = repo.transcript_path(source_id)
    t = read_json(path)
    episodes = load_episodes(repo, source_id)
    assign(t, validate_episodes(t, episodes))
    write_json(path, t)
    return len(episodes)


def _first_words(text: str, n: int = 15) -> str:
    words = text.split()
    return " ".join(words[:n]) + (" ..." if len(words) > n else "")


def compact_turn_list(transcript: dict, words: int = 15) -> str:
    """One line per turn: ID, time if any, person and role, sentence count, first words."""
    lines = []
    for t in transcript["turns"]:
        if not t["sentences"]:
            continue
        ts = fmt_time(t["start"])
        text = " ".join(s["text"] for s in t["sentences"])
        lines.append(
            f"{t['id']}{' [' + ts + ']' if ts else ''} {t['person']}({t['role']}) "
            f"n={len(t['sentences'])}: {_first_words(text, words)}"
        )
    return "\n".join(lines)


def _is_question(norm_text: str) -> bool:
    return "?" in norm_text or bool(QUESTION_RE.search(norm_text))


def propose(transcript: dict, fmt: str) -> list[dict]:
    """Mechanical first proposal; Claude reviews it and the owner confirms before --apply."""
    sid = transcript["source_id"]
    flat = [(t, s) for t in transcript["turns"] for s in t["sentences"]]
    starts: list[tuple[int, str, str]] = []  # (index into flat, type, label)
    cues = [norm_compact(c) for c in LIVE_REVIEW_CUES]
    i = 0
    for t in transcript["turns"]:
        if not t["sentences"]:
            continue
        if fmt == "live-cv-review":
            for k, s in enumerate(t["sentences"]):
                if any(c in s["norm_compact"] for c in cues):
                    at = i if k < 2 else i + k
                    # One CV is often announced twice in a row ("بریم سراغ رزومه اول", then
                    # "رزومه اول ..."): ignore cues within a few sentences of the last start.
                    if not starts or at - starts[-1][0] > CUE_GAP:
                        starts.append((at, "cv-review", "CV#?? " + _first_words(s["text"], 8)))
        elif t["role"] == "host":
            question = " ".join(s["text"] for s in t["sentences"])
            if _is_question(" ".join(s["norm"] for s in t["sentences"])):
                starts.append((i, "qa", _first_words(question, 10)))
        i += len(t["sentences"])
    if starts and starts[0][0] == 0:
        starts[0] = (0, "intro", "Intro")
    else:
        starts.insert(0, (0, "intro", "Intro"))
    episodes = []
    for k, (a, typ, label) in enumerate(starts, 1):
        b = starts[k][0] - 1 if k < len(starts) else len(flat) - 1
        e = {"id": f"{sid}.e{k:02d}", "type": typ, "label": label,
             "from": flat[a][1]["id"], "to": flat[b][1]["id"]}
        if typ == "cv-review":
            e.update({"cv_owner": None, "verdict": "none", "verdict_reasons": []})
        episodes.append(e)
    return episodes


def dump_episodes(episodes: list[dict]) -> str:
    return yaml.safe_dump(episodes, allow_unicode=True, sort_keys=False, width=100)
