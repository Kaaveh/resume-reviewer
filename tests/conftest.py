"""Shared fixtures: a tiny repository laid out like the real one."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from rrs.config import Repo

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def mini_repo(tmp_path: Path) -> Repo:
    """A copy of tests/fixtures/repo plus the real rrs.toml and glossary."""
    dst = tmp_path / "repo"
    shutil.copytree(FIXTURES / "repo", dst)
    shutil.copy(ROOT / "rrs.toml", dst / "rrs.toml")
    shutil.copytree(ROOT / "glossary", dst / "glossary")
    return Repo(dst)


@pytest.fixture
def real_repo() -> Repo:
    return Repo(ROOT)
