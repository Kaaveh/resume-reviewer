"""Source registry: one hand-written YAML per source in sources/ (spec 01 section 1.2)."""

from __future__ import annotations

import datetime as dt
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from rrs.config import Repo
from rrs.jsonio import read_yaml

Role = Literal["guest", "host"]


class PersonRole(BaseModel):
    model_config = ConfigDict(extra="forbid")
    person: str
    role: Role


class SpeakerOverride(BaseModel):
    model_config = ConfigDict(extra="forbid")
    turn: int
    person: str
    reason: str


class Correction(BaseModel):
    """A proper-noun fix applied to sentence `text`; the original is kept as `text_orig`."""

    model_config = ConfigDict(extra="forbid")
    find: str
    replace: str
    reason: str
    person: str | None = None  # only in sentences spoken by this person
    turns: list[int] | None = None  # only in these turns (numbers as in transcript.raw.json)
    ignore_case: bool = False


class Source(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(pattern=r"^S\d{3}$")
    slug: str
    transcript_file: str
    transcript_version: int = 1
    url: str | None = None
    title: str
    channel: str | None = None
    upload_date: dt.date | None = None
    recorded_date: dt.date | None = None
    duration_s: int | None = None
    languages: list[str]
    format: Literal["interview", "live-cv-review", "panel", "talk"]
    people: list[PersonRole]
    speakers: dict[str, str]
    speakers_confirmed: bool = False
    speaker_overrides: list[SpeakerOverride] = []
    corrections: list[Correction] = []
    notes: str = ""

    @field_validator("speakers")
    @classmethod
    def _labels_nonempty(cls, v: dict[str, str]) -> dict[str, str]:
        if not v:
            raise ValueError("speakers must map at least one transcript label")
        return v

    @property
    def roles(self) -> dict[str, str]:
        return {p.person: p.role for p in self.people}

    def check(self) -> None:
        roles = self.roles
        for label, person in self.speakers.items():
            if person not in roles:
                raise ValueError(f"{self.id}: speaker {label!r} maps to {person}, not in people")
        for o in self.speaker_overrides:
            if o.person not in roles:
                raise ValueError(f"{self.id}: override for turn {o.turn} names {o.person}")
        for c in self.corrections:
            if c.person and c.person not in roles:
                raise ValueError(f"{self.id}: correction {c.find!r} names {c.person}")


def load_source(repo: Repo, source_id: str) -> Source:
    matches = sorted(repo.sources.glob(f"{source_id}-*.yaml"))
    if len(matches) != 1:
        raise FileNotFoundError(f"expected one sources/{source_id}-*.yaml, found {len(matches)}")
    src = Source.model_validate(read_yaml(matches[0]))
    if src.id != source_id:
        raise ValueError(f"{matches[0].name} has id {src.id}")
    src.check()
    return src


def all_source_ids(repo: Repo) -> list[str]:
    return sorted({p.name.split("-", 1)[0] for p in repo.sources.glob("S[0-9][0-9][0-9]-*.yaml")})
