"""Build corpus objects in memory, without touching the committed files."""

from __future__ import annotations

from rrs.config import Repo
from rrs.glossary import load_terms
from rrs.ingest.parse import import_source
from rrs.normalize.terms import TermMatcher
from rrs.segment.build import transcript_from_raw
from rrs.segment.episodes import assign, load_episodes, validate_episodes
from rrs.sources import load_source


def build(repo: Repo, sid: str, episodes: bool = True) -> dict:
    source = load_source(repo, sid)
    raw = import_source(repo, source)
    t, _ = transcript_from_raw(raw, source, repo.settings, TermMatcher(load_terms(repo)))
    if episodes and repo.episodes_path(sid).exists():
        assign(t, validate_episodes(t, load_episodes(repo, sid)))
    return t
