import dataclasses

from rrs.chunks.build import Packer, build_chunks
from rrs.config import ChunkSettings
from rrs.glossary import load_people
from rrs.jsonio import read_json, write_json
from rrs.segment.episodes import propose
from rrs.sources import load_source

from helpers import build


def packer(repo, sid, budget=None, with_episodes=False):
    t = build(repo, sid)
    labels = {}
    if with_episodes:
        from rrs.segment.episodes import Episode, assign, validate_episodes

        eps = [Episode.model_validate(e) for e in propose(t, load_source(repo, sid).format)]
        assign(t, validate_episodes(t, eps))
        labels = {e.id: e.label for e in eps}
    s = ChunkSettings()
    if budget:
        s = dataclasses.replace(s, budget_fa=budget, budget_en=budget)
    names = {k: v.name for k, v in load_people(repo).people.items()}
    return Packer(t, load_source(repo, sid), names, labels, s)


def check(p: Packer):
    chunks = p.pack()
    flat = [i for c in chunks for i in c]
    assert flat == list(range(len(p.lines))), "every sentence exactly once, in order"
    for k, c in enumerate(chunks, 1):
        assert len(p.render(k, c)) <= p.budget
    return chunks


def test_budget_respected_real_sources(real_repo):
    for sid in ("S001", "S003"):
        p = packer(real_repo, sid, with_episodes=True)
        assert p.budget == (12000 if sid == "S001" else 24000)
        check(p)


def test_small_budget_splits_at_turns_then_sentences(mini_repo):
    p = packer(mini_repo, "S003", budget=700)
    chunks = check(p)
    assert len(chunks) > 1


def test_context_repeats_last_host_question(mini_repo):
    p = packer(mini_repo, "S003", budget=700)
    chunks = p.pack()
    later = [p.render(k, c) for k, c in enumerate(chunks, 1)][1:]
    assert any("## Context" in r and "HOST [00:00:12] S003.t0003.s001 JA(host)" in r for r in later)


def test_line_format(mini_repo):
    p = packer(mini_repo, "S003")
    text = p.render(1, list(range(len(p.lines))))
    assert "[00:00:20] S003.t0004.s001 TW(guest): So logos" in text
    assert "HOST [00:00:00] S003.t0001.s001 JA(host): hello" in text
    fa = packer(mini_repo, "S001")
    assert "S001.t0003.s001 JA(guest): رزومه اول" in fa.render(1, list(range(len(fa.lines))))


def test_deterministic_and_progress_carried(mini_repo):
    from rrs.ingest.parse import run_import
    from rrs.segment.build import run_segment

    run_import(mini_repo, "S001")
    run_segment(mini_repo, "S001")
    m1 = build_chunks(mini_repo, "S001")
    files1 = {f.name: f.read_text() for f in (mini_repo.chunks / "S001").iterdir()}
    m1["chunks"][0]["status"] = "merged"
    write_json(mini_repo.chunks / "S001" / "manifest.json", m1)
    m2 = build_chunks(mini_repo, "S001")
    assert m2["chunks"][0]["status"] == "merged"
    m2["chunks"][0]["status"] = "pending"
    files2 = {f.name: f.read_text() for f in (mini_repo.chunks / "S001").iterdir()}
    assert {k: v for k, v in files1.items() if k != "manifest.json"} == {
        k: v for k, v in files2.items() if k != "manifest.json"
    }
    assert read_json(mini_repo.chunks / "S001" / "manifest.json")["chunks"][0]["status"] == "merged"

