"""Repository paths and settings from rrs.toml."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class SegmentSettings:
    max_words: int = 40
    hard_max_words: int = 60
    min_fragment_words: int = 3
    window_words: int = 25
    unpunctuated_avg_words: int = 40


@dataclass(frozen=True)
class LangSettings:
    fa_min: float = 0.5
    en_max: float = 0.1


@dataclass(frozen=True)
class ChunkSettings:
    budget_fa: int = 12000
    budget_en: int = 24000
    context_host_sentences: int = 2


@dataclass(frozen=True)
class ReanchorSettings:
    accept: int = 90
    review: int = 75
    time_window_s: int = 120
    max_window_sentences: int = 3


@dataclass(frozen=True)
class LedgerSettings:
    count_independent_hosts: bool = False


@dataclass(frozen=True)
class Settings:
    segment: SegmentSettings = field(default_factory=SegmentSettings)
    lang: LangSettings = field(default_factory=LangSettings)
    chunks: ChunkSettings = field(default_factory=ChunkSettings)
    reanchor: ReanchorSettings = field(default_factory=ReanchorSettings)
    ledger: LedgerSettings = field(default_factory=LedgerSettings)

    @classmethod
    def from_toml(cls, path: Path) -> Settings:
        data = tomllib.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        return cls(
            segment=SegmentSettings(**data.get("segment", {})),
            lang=LangSettings(**data.get("lang", {})),
            chunks=ChunkSettings(**data.get("chunks", {})),
            reanchor=ReanchorSettings(**data.get("reanchor", {})),
            ledger=LedgerSettings(**data.get("ledger", {})),
        )


@dataclass(frozen=True)
class Repo:
    """Paths inside a repository checkout (or a test fixture laid out the same way)."""

    root: Path

    @classmethod
    def find(cls, start: Path | None = None) -> Repo:
        env = os.environ.get("RRS_ROOT")
        if env:
            return cls(Path(env).resolve())
        here = (start or Path.cwd()).resolve()
        for d in (here, *here.parents):
            if (d / "rrs.toml").exists():
                return cls(d)
        raise FileNotFoundError("no rrs.toml found in this directory or its parents")

    @property
    def settings(self) -> Settings:
        return Settings.from_toml(self.root / "rrs.toml")

    @property
    def transcripts(self) -> Path:
        return self.root / "transcripts"

    @property
    def sources(self) -> Path:
        return self.root / "sources"

    @property
    def glossary(self) -> Path:
        return self.root / "glossary"

    @property
    def corpus(self) -> Path:
        return self.root / "corpus"

    @property
    def chunks(self) -> Path:
        return self.root / "chunks"

    @property
    def ledger(self) -> Path:
        return self.root / "ledger"

    def corpus_dir(self, source_id: str) -> Path:
        return self.corpus / source_id

    def raw_path(self, source_id: str) -> Path:
        return self.corpus_dir(source_id) / "transcript.raw.json"

    def transcript_path(self, source_id: str) -> Path:
        return self.corpus_dir(source_id) / "transcript.json"

    def episodes_path(self, source_id: str) -> Path:
        return self.corpus_dir(source_id) / "episodes.yaml"

    def render_path(self, source_id: str) -> Path:
        return self.corpus_dir(source_id) / "transcript.md"

    @property
    def index_path(self) -> Path:
        return self.corpus / "index.jsonl"
