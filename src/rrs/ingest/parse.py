"""Parse a NotebookLM transcript and map its speaker labels to people."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

from rrs.config import Repo
from rrs.jsonio import write_json
from rrs.schemas import validate
from rrs.sources import Source, load_source

TURN_RE = re.compile(
    r"^(?:\[(?P<ts>\d{1,2}:\d{2}(?::\d{2})?)\]\s*)?\*\*(?P<label>[^*]+?):\*\*\s*(?P<rest>.*)$"
)
SOURCE_RE = re.compile(r"^Source:\s*(?P<url>.*)$")
RAW_SCHEMA = "rrs.transcript.raw/1"


class TranscriptImportError(ValueError):
    """The transcript cannot be imported as it stands (for example, an unmapped label)."""


@dataclass
class ParsedTurn:
    label: str
    start: float | None
    lines: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return "\n".join(line for line in self.lines if line)


@dataclass
class ParsedTranscript:
    title: str | None
    url: str | None
    turns: list[ParsedTurn]


def parse_timestamp(ts: str) -> float:
    parts = [int(p) for p in ts.split(":")]
    seconds = 0
    for p in parts:
        seconds = seconds * 60 + p
    return float(seconds)


def parse_transcript(md: str) -> ParsedTranscript:
    title = url = None
    turns: list[ParsedTurn] = []
    for lineno, raw in enumerate(md.splitlines(), 1):
        line = raw.strip()
        m = TURN_RE.match(line)
        if m:
            ts = m.group("ts")
            turn = ParsedTurn(m.group("label").strip(), parse_timestamp(ts) if ts else None)
            if m.group("rest").strip():
                turn.lines.append(m.group("rest").strip())
            turns.append(turn)
            continue
        if turns:
            turn = turns[-1]
            if line or turn.lines:
                turn.lines.append(line)
            continue
        # Header, before the first turn.
        if not line or line == "---":
            continue
        if line.startswith("# ") and title is None:
            title = line[2:].strip()
        elif (sm := SOURCE_RE.match(line)) and url is None:
            u = sm.group("url").strip()
            url = u if u and not u.startswith("[") else None
        else:
            raise TranscriptImportError(
                f"line {lineno}: unexpected text before the first turn: {line[:60]!r}"
            )
    for t in turns:
        while t.lines and not t.lines[-1]:
            t.lines.pop()
    return ParsedTranscript(title, url, turns)


def import_source(repo: Repo, source: Source) -> dict:
    path = repo.transcripts / source.transcript_file
    data = path.read_bytes()
    parsed = parse_transcript(data.decode("utf-8"))
    if not parsed.turns:
        raise TranscriptImportError(f"{source.id}: no turns found in {source.transcript_file}")

    labels = sorted({t.label for t in parsed.turns})
    unmapped = [lab for lab in labels if lab not in source.speakers]
    if unmapped:
        raise TranscriptImportError(f"{source.id}: unmapped speaker labels {unmapped}; add them to speakers:")

    timed = [t.start is not None for t in parsed.turns]
    if all(timed):
        timing = "turn"
    elif not any(timed):
        timing = "none"
    else:
        missing = [i for i, ok in enumerate(timed, 1) if not ok]
        raise TranscriptImportError(f"{source.id}: turns {missing[:10]} have no start time but others do")

    overrides = {o.turn: o for o in source.speaker_overrides}
    bad = [n for n in overrides if not 1 <= n <= len(parsed.turns)]
    if bad:
        raise TranscriptImportError(f"{source.id}: speaker_overrides name missing turns {bad}")

    turns = []
    applied = []
    for n, t in enumerate(parsed.turns, 1):
        person = source.speakers[t.label]
        if n in overrides:
            o = overrides[n]
            applied.append({"turn": n, "from": person, "to": o.person, "reason": o.reason})
            person = o.person
        turns.append({"n": n, "label": t.label, "person": person, "start": t.start, "text": t.text})

    return {
        "schema": RAW_SCHEMA,
        "source_id": source.id,
        "transcript_file": source.transcript_file,
        "transcript_sha256": hashlib.sha256(data).hexdigest(),
        "title": parsed.title,
        "timing": timing,
        "speakers": dict(source.speakers),
        "overrides_applied": applied,
        "turns": turns,
    }


def run_import(repo: Repo, source_id: str) -> dict:
    raw = import_source(repo, load_source(repo, source_id))
    validate(raw, "transcript_raw")
    write_json(repo.raw_path(source_id), raw)
    return raw
