import yaml

from rrs.config import ReanchorSettings
from rrs.jsonio import read_jsonl, write_jsonl
from rrs.ledger.reanchor import reanchor_claim, run_reanchor
from rrs.segment.episodes import Episode, assign, validate_episodes

from helpers import build

S = ReanchorSettings()


def claim(cid, recruiter, source, quote, sentence_id="S000.t0001.s001", t_start=None, episode=None):
    return {"id": cid, "recruiter": recruiter, "source": source, "episode": episode,
            "anchors": [{"sentence_id": sentence_id, "t_start": t_start, "quote": quote}]}


def test_exact_english_across_sentence_boundary(mini_repo):
    t = build(mini_repo, "S003")
    c = claim("TW-1", "TW", "S003", "always going to be a straight no and I know that", t_start=20.0)
    (r,) = reanchor_claim(c, t, S, {})
    assert r.status == "accepted" and r.candidates[0].exact
    a = r.candidates[0].anchor()
    assert a == {"sentence_id": "S003.t0004.s001", "t_start": 20.0,
                 "quote": "always going to be a straight no and I know that"}


def test_exact_persian_with_zwnj_and_yeh_differences(mini_repo):
    t = build(mini_repo, "S001")
    # Arabic Yeh and a ZWNJ where the transcript has neither: still an exact match.
    c = claim("JA-1", "JA", "S001", "دواب كه ايبليوس يا جی‌سی‌پی بلد نباشه")
    (r,) = reanchor_claim(c, t, S, {})
    assert r.status == "accepted" and r.candidates[0].exact
    assert r.candidates[0].quote == "دواب که ایبلیوس یا جی سی پی بلد نباشه"
    assert r.candidates[0].sentence_id == "S001.t0003.s002"


def test_perturbed_quote_maps_fuzzily(mini_repo):
    t = build(mini_repo, "S003")
    (r,) = reanchor_claim(claim("TW-2", "TW", "S003", "managers pick on it very quickly"), t, S, {})
    assert r.status in ("accepted", "review")
    assert r.candidates[0].sentence_id.startswith("S003.t0004")
    assert "pick on it" in r.candidates[0].quote


def test_only_the_claims_recruiter_is_searched(mini_repo):
    t = build(mini_repo, "S003")
    c = claim("TW-3", "TW", "S003", "what is the first thing you look at in a CV")
    (r,) = reanchor_claim(c, t, S, {})
    assert r.status != "accepted" or not r.candidates[0].exact


def test_time_window_narrows_then_falls_back(mini_repo):
    t = build(mini_repo, "S003")
    c = claim("TW-4", "TW", "S003", "two pages is the general sweet spot", t_start=1800.0)
    (r,) = reanchor_claim(c, t, S, {})
    assert r.status == "accepted" and "whole source" in r.note


def test_episode_narrowing(mini_repo):
    t = build(mini_repo, "S001")
    eps = [Episode.model_validate(e) for e in [
        {"id": "S001.e01", "type": "intro", "label": "Intro", "from": "S001.t0001.s001",
         "to": "S001.t0002.s001"},
        {"id": "S001.e02", "type": "cv-review", "label": "CV#01", "verdict": "reject",
         "from": "S001.t0003.s001", "to": "S001.t0005.s001"},
    ]]
    assign(t, validate_episodes(t, eps))
    (r,) = reanchor_claim(claim("JA-2", "JA", "S001", "این رزومه ریجکته", episode="S001.e02"), t, S, {})
    assert r.status == "accepted" and r.note == "episode S001.e02"


def test_run_reanchor_writes_anchors_report_and_applies_decisions(mini_repo):
    from rrs.ingest.parse import run_import
    from rrs.segment.build import run_segment

    for sid in ("S001", "S003"):
        run_import(mini_repo, sid)
        run_segment(mini_repo, sid)
    path = mini_repo.ledger / "claims.jsonl"
    write_jsonl(path, [
        claim("TW-1", "TW", "S003", "pictures of any kind", "S003.t0099.s001", 20.0),
        claim("JA-1", "JA", "S001", "چیزی که اصلا گفته نشده"),
    ])
    results, report = run_reanchor(mini_repo)
    assert {r.claim_id: r.status for r in results} == {"TW-1": "accepted", "JA-1": "manual"}
    rows = read_jsonl(path)
    assert rows[0]["anchors"][0]["sentence_id"] == "S003.t0004.s001"
    assert rows[1]["anchors"][0]["sentence_id"] == "S000.t0001.s001"  # unchanged until decided
    assert "## Manual (1)" in report
    (mini_repo.ledger / "migration" / "reanchor-decisions.yaml").write_text(
        yaml.safe_dump([{"claim": "JA-1", "anchor": 0, "sentence_id": "S001.t0005.s001",
                         "reason": "owner"}])
    )
    results, _ = run_reanchor(mini_repo, ["S001"])
    assert [(r.claim_id, r.status) for r in results] == [("JA-1", "decided")]
    assert read_jsonl(path)[1]["anchors"][0]["sentence_id"] == "S001.t0005.s001"
