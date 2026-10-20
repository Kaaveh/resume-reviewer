from pathlib import Path

import yaml

from rrs.glossary import load_people
from rrs.render.markdown import render
from rrs.segment.episodes import Episode
from rrs.sources import load_source

from helpers import build

SNAPSHOTS = Path(__file__).parent / "fixtures" / "snapshots"


def _render(repo, sid, episodes):
    t = build(repo, sid)
    names = {k: v.name for k, v in load_people(repo).people.items()}
    return render(t, load_source(repo, sid), names, episodes)


def test_render_snapshot(mini_repo):
    eps = [
        {"id": "S001.e01", "type": "intro", "label": "Intro", "from": "S001.t0001.s001",
         "to": "S001.t0001.s002"},
        {"id": "S001.e02", "type": "cv-review", "label": "CV#01 DevOps", "cv_owner": "Private",
         "verdict": "reject", "from": "S001.t0002.s001", "to": "S001.t0005.s001"},
    ]
    mini_repo.episodes_path("S001").parent.mkdir(parents=True, exist_ok=True)
    mini_repo.episodes_path("S001").write_text(yaml.safe_dump(eps, allow_unicode=True))
    episodes = {e["id"]: Episode.model_validate(e) for e in eps}
    out = _render(mini_repo, "S001", episodes) + "\n---\n\n" + _render(mini_repo, "S003", {})
    snap = SNAPSHOTS / "render.md"
    if not snap.exists():  # first run writes the snapshot; review it before committing
        snap.parent.mkdir(parents=True, exist_ok=True)
        snap.write_text(out, encoding="utf-8")
    assert out == snap.read_text(encoding="utf-8")


def test_render_rules(mini_repo):
    out = _render(mini_repo, "S003", {})
    assert "**TW** [00:00:20] `S003.t0004.s001`" in out
    assert "*hello everyone and hi Tomasz How are you doing*" in out
    fa = _render(mini_repo, "S001", {})
    assert '<div dir="rtl"><em>خب بریم سراغ رزومه اول؟</em></div>' in fa
    assert "Private" not in fa
