import pytest
import yaml

from rrs.segment.episodes import (
    Episode,
    EpisodeError,
    compact_turn_list,
    propose,
    validate_episodes,
)

from helpers import build


def ep(**kw):
    kw.setdefault("type", "qa")
    kw.setdefault("label", "x")
    return Episode.model_validate(kw)


def test_propose_live_review_from_cues(mini_repo):
    t = build(mini_repo, "S001")
    eps = propose(t, "live-cv-review")
    assert [e["type"] for e in eps] == ["intro", "cv-review", "cv-review"]
    assert eps[1]["from"] == "S001.t0002.s001"
    assert eps[2]["from"] == "S001.t0004.s001"
    validate_episodes(t, [Episode.model_validate(e) for e in eps])


def test_propose_interview_from_host_questions(mini_repo):
    t = build(mini_repo, "S003")
    eps = propose(t, "interview")
    assert [e["type"] for e in eps] == ["intro", "qa"]
    assert eps[1]["from"] == "S003.t0003.s001"


def test_validation_errors(mini_repo):
    t = build(mini_repo, "S002")
    ids = [s["id"] for turn in t["turns"] for s in turn["sentences"]]
    with pytest.raises(EpisodeError, match="in no episode"):
        validate_episodes(t, [ep(id="S002.e01", **{"from": ids[0], "to": ids[0]})])
    with pytest.raises(EpisodeError, match="expected id"):
        validate_episodes(t, [ep(id="S002.e02", **{"from": ids[0], "to": ids[-1]})])
    with pytest.raises(EpisodeError, match="pseudonym"):
        validate_episodes(t, [ep(id="S002.e01", type="cv-review", label="CV#01 Ali", cv_owner="Ali",
                                 verdict="reject", **{"from": ids[0], "to": ids[-1]})])
    with pytest.raises(EpisodeError, match="needs a verdict"):
        validate_episodes(t, [ep(id="S002.e01", type="cv-review", **{"from": ids[0], "to": ids[-1]})])
    a = validate_episodes(t, [ep(id="S002.e01", **{"from": ids[0], "to": ids[1]}),
                              ep(id="S002.e02", **{"from": ids[2], "to": ids[-1]})])
    assert a[ids[0]] == "S002.e01" and a[ids[-1]] == "S002.e02"


def test_apply_via_yaml(mini_repo):
    t = build(mini_repo, "S002")
    ids = [s["id"] for turn in t["turns"] for s in turn["sentences"]]
    mini_repo.episodes_path("S002").parent.mkdir(parents=True, exist_ok=True)
    mini_repo.episodes_path("S002").write_text(yaml.safe_dump(
        [{"id": "S002.e01", "type": "qa", "label": "All", "from": ids[0], "to": ids[-1]}]
    ))
    t = build(mini_repo, "S002")
    assert {s["episode"] for turn in t["turns"] for s in turn["sentences"]} == {"S002.e01"}


def test_compact_turn_list(mini_repo):
    out = compact_turn_list(build(mini_repo, "S003"), words=3).splitlines()
    assert out[0] == "S003.t0001 [00:00:00] JA(host) n=1: hello everyone and ..."
