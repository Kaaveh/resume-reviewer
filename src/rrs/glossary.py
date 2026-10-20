"""Term glossary and people registry (spec 01 sections 3.2 and 4)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from rrs.config import Repo
from rrs.jsonio import read_yaml


class Term(BaseModel):
    model_config = ConfigDict(extra="forbid")
    canonical: str
    kind: str
    variants: list[str] = Field(min_length=1)
    ambiguous_with: list[str] = []
    notes: str = ""


class Person(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    kind: Literal["recruiter", "host"]
    aliases: list[str] = []


class People(BaseModel):
    model_config = ConfigDict(extra="forbid")
    people: dict[str, Person]
    orgs: dict[str, list[str]] = {}
    places: dict[str, list[str]] = {}


def load_terms(repo: Repo) -> list[Term]:
    path = repo.glossary / "terms.yaml"
    if not path.exists():
        return []
    return [Term.model_validate(t) for t in read_yaml(path) or []]


def load_people(repo: Repo) -> People:
    return People.model_validate(read_yaml(repo.glossary / "people.yaml"))
