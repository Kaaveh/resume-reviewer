"""Ledger files and their schemas (spec 02 sections 2 to 5)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from rrs.config import Repo
from rrs.jsonio import read_jsonl, read_yaml

CATEGORIES = ["SCR", "ATS", "STR", "ACH", "SKL", "RED", "REG", "SEN", "GAP", "CHN"]
CATEGORY_ORDER = {c: i for i, c in enumerate([*CATEGORIES, "X"])}
NUMBERED_RULE_RE = re.compile(r"^(SCR|ATS|STR|ACH|SKL|RED|REG|SEN|GAP|CHN)-(\d+)$")
X_RULE_RE = re.compile(r"^X-[A-Z]+$")
PROPOSED_RULE_RE = re.compile(r"^NEW-\d+$")
CLAIM_ID_RE = re.compile(r"^([A-Z]{2})-(\d+)$")

ClaimType = Literal["F", "F!", "P"]
Stance = Literal["+", "-", "~"]
MatchLevel = Literal["high", "medium-high", "medium", "low-medium", "low"]


def rule_sort_key(rule_id: str) -> tuple[int, int, str]:
    m = NUMBERED_RULE_RE.match(rule_id)
    if m:
        return CATEGORY_ORDER[m.group(1)], int(m.group(2)), ""
    return CATEGORY_ORDER["X"], 0, rule_id


class Anchor(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sentence_id: str = Field(pattern=r"^S\d{3}\.t\d{4}\.s\d{3}$")
    t_start: float | None
    quote: str = Field(min_length=1)


class Extracted(BaseModel):
    model_config = ConfigDict(extra="forbid")
    date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    chunk: str = Field(pattern=r"^S\d{3}\.c\d{3}$")


class Measure(BaseModel):
    """Marks a rule whose evidence is a quantity (ADR 0003): each recruiter's stated value is a
    data point and the tally reports their distribution."""

    model_config = ConfigDict(extra="forbid")
    unit: str = Field(min_length=1)  # pages, seconds
    question: str = Field(min_length=1)  # "How long should the CV be?"


class Value(BaseModel):
    """A stated quantity: a point (min == max) or a range, open on one side when one bound is
    null. `condition` keeps the speaker's scope ("with 10 to 15 years of experience")."""

    model_config = ConfigDict(extra="forbid")
    min: float | None = None
    max: float | None = None
    condition: str = ""

    @model_validator(mode="after")
    def _bounds(self) -> Value:
        if self.min is None and self.max is None:
            raise ValueError("a value needs min, max or both")
        if self.min is not None and self.max is not None and self.min > self.max:
            raise ValueError("min is larger than max")
        return self


class Claim(BaseModel):
    """A claim in `claims.jsonl` (status `merged`, with an ID) or a staging draft (no ID).

    `duplicate_of` is set on a draft, after review, to fold it into an existing claim as extra
    anchors at merge time.
    """

    model_config = ConfigDict(extra="forbid")
    id: str | None = None
    recruiter: str
    source: str = Field(pattern=r"^S\d{3}$")
    speaker_role: Literal["guest", "host"]
    attribution: Literal["speaker-label", "content-override"] = "speaker-label"
    independent: bool = False
    anchors: list[Anchor] = Field(min_length=1)
    episode: str | None = None
    type: ClaimType
    rules: list[str] = Field(min_length=1)
    stance: Stance
    claim_en: str = Field(min_length=1)
    quote_en: str | None = None
    status: Literal["draft", "merged"] = "draft"
    extracted: Extracted
    notes: str = ""
    value: Value | None = None
    duplicate_of: str | None = None


class Rule(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    category: Literal["SCR", "ATS", "STR", "ACH", "SKL", "RED", "REG", "SEN", "GAP", "CHN", "X"]
    text: str
    check: str
    status: Literal["active", "retired"] = "active"
    added_in: str
    superseded_by: str | None = None
    measure: Measure | None = None
    notes: str = ""


class ProposedRule(BaseModel):
    """An entry in `ledger/staging/<source>.new-rules.yaml`.

    Claims in staging refer to it by its temporary `id` (`NEW-3`; X- rules use their final name,
    `X-INT`). The owner sets `decision`; `rrs ledger rules --accept` assigns the permanent ID
    (`assigned`) and rewrites the staging claims. A rejected proposal may name `use`: an existing
    rule its claims map to instead.
    """

    model_config = ConfigDict(extra="forbid")
    id: str
    category: Literal["SCR", "ATS", "STR", "ACH", "SKL", "RED", "REG", "SEN", "GAP", "CHN", "X"]
    text: str
    check: str
    rationale: str
    decision: Literal["proposed", "accepted", "rejected"] = "proposed"
    use: str | None = None
    assigned: str | None = None
    measure: Measure | None = None
    notes: str = ""


class Recruiter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    type: Literal["agency", "in-house-recruiter", "hiring-manager", "former-recruiter"]
    title: str
    region: str
    industry: str
    roles_hired: str
    year: int | None = None
    year_basis: Literal["metadata", "stated", "inferred"]
    sources: list[str]
    caveats: str = ""


class Target(BaseModel):
    model_config = ConfigDict(extra="forbid")
    description: str
    match: dict[str, MatchLevel]


class Targets(BaseModel):
    model_config = ConfigDict(extra="forbid")
    default: str
    targets: dict[str, Target]

    @property
    def default_target(self) -> Target:
        return self.targets[self.default]


def claims_path(repo: Repo) -> Path:
    return repo.ledger / "claims.jsonl"


def staging_dir(repo: Repo) -> Path:
    return repo.ledger / "staging"


def proposals_path(repo: Repo, source_id: str) -> Path:
    return staging_dir(repo) / f"{source_id}.new-rules.yaml"


def load_claims(repo: Repo) -> list[Claim]:
    path = claims_path(repo)
    return [Claim.model_validate(c) for c in read_jsonl(path)] if path.exists() else []


def load_rules(repo: Repo) -> list[Rule]:
    path = repo.ledger / "rules.yaml"
    if not path.exists():
        return []
    return [Rule.model_validate(r) for r in read_yaml(path) or []]


def load_proposals(repo: Repo, source_id: str) -> list[ProposedRule]:
    path = proposals_path(repo, source_id)
    if not path.exists():
        return []
    return [ProposedRule.model_validate(r) for r in read_yaml(path) or []]


def load_recruiters(repo: Repo) -> dict[str, Recruiter]:
    path = repo.ledger / "recruiters.yaml"
    if not path.exists():
        return {}
    return {k: Recruiter.model_validate(v) for k, v in (read_yaml(path) or {}).items()}


def load_targets(repo: Repo) -> Targets | None:
    path = repo.ledger / "targets.yaml"
    return Targets.model_validate(read_yaml(path)) if path.exists() else None


def source_of_staging(path: Path) -> str:
    """`ledger/staging/S004.c001.jsonl` -> `S004`."""
    m = re.match(r"^(S\d{3})\.", path.name)
    if not m:
        raise ValueError(f"{path.name}: staging files are named Sxxx.cNNN.jsonl")
    return m.group(1)
