from rrs.jsonio import dump_json
from rrs.schemas import validate

from helpers import build


def test_two_runs_identical(real_repo):
    for sid in ("S001", "S003"):
        a = dump_json(build(real_repo, sid))
        b = dump_json(build(real_repo, sid))
        assert a == b


def test_ids_unique_and_well_formed(real_repo):
    for sid in ("S001", "S002", "S003", "S004"):
        t = build(real_repo, sid)
        validate(t, "transcript")
        ids = [s["id"] for turn in t["turns"] for s in turn["sentences"]]
        assert len(ids) == len(set(ids))
        assert all(i.startswith(f"{sid}.t") for i in ids)


def test_committed_corpus_is_current(real_repo):
    """Generated files are never hand-edited: the committed transcript.json must match a rebuild."""
    from rrs.jsonio import read_json

    for sid in ("S001", "S002", "S003", "S004"):
        path = real_repo.transcript_path(sid)
        if path.exists():
            assert read_json(path) == build(real_repo, sid), f"{sid}: run rrs build-corpus {sid}"
