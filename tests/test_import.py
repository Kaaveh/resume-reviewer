import pytest

from rrs.ingest.parse import TranscriptImportError, import_source, parse_transcript, run_import
from rrs.sources import Source, SpeakerOverride, all_source_ids, load_source


def test_real_transcripts_parse(real_repo):
    expected = {"S001": "none", "S002": "none", "S003": "turn", "S004": "none"}
    for sid in all_source_ids(real_repo):
        raw = import_source(real_repo, load_source(real_repo, sid))
        assert raw["timing"] == expected[sid]
        assert {t["label"] for t in raw["turns"]} == {"Guest", "Interviewer"}
        assert all(t["text"] for t in raw["turns"])


def test_s001_labels_on_their_own_line(real_repo):
    raw = import_source(real_repo, load_source(real_repo, "S001"))
    assert raw["turns"][0]["text"].startswith("سلام به همه")
    assert raw["title"].startswith("کدوم رزومه")


def test_s002_without_source_line(real_repo):
    raw = import_source(real_repo, load_source(real_repo, "S002"))
    assert raw["turns"][0]["text"].startswith("...but yeah")


def test_s003_timestamps(real_repo):
    raw = import_source(real_repo, load_source(real_repo, "S003"))
    assert raw["turns"][0]["start"] == 0.0
    assert raw["turns"][-1]["start"] == 55 * 60 + 14


def test_header_shapes():
    md = "# Title\nSource: [YOUTUBE URL]\n---\n\n[01:02:03] **Guest:** hi\nmore\n\n**Host:**\n\nyo\n"
    p = parse_transcript(md)
    assert p.title == "Title" and p.url is None
    assert [t.label for t in p.turns] == ["Guest", "Host"]
    assert p.turns[0].start == 3723.0
    assert p.turns[0].text == "hi\nmore"
    assert p.turns[1].text == "yo"


def test_text_before_first_turn_fails():
    with pytest.raises(TranscriptImportError):
        parse_transcript("# T\nsome stray line\n**Guest:** hi\n")


def test_mapping_and_overrides(mini_repo):
    src = load_source(mini_repo, "S001")
    src.speaker_overrides = [SpeakerOverride(turn=2, person="JA", reason="test")]
    raw = import_source(mini_repo, src)
    assert [t["person"] for t in raw["turns"]] == ["JA", "JA", "JA", "H01", "JA"]
    assert raw["overrides_applied"] == [{"turn": 2, "from": "H01", "to": "JA", "reason": "test"}]


def test_unmapped_label_fails(mini_repo):
    src = load_source(mini_repo, "S001")
    data = src.model_dump(by_alias=True)
    data["speakers"] = {"Guest": "JA"}
    with pytest.raises(TranscriptImportError, match="unmapped"):
        import_source(mini_repo, Source.model_validate(data))


def test_override_for_missing_turn_fails(mini_repo):
    src = load_source(mini_repo, "S001")
    src.speaker_overrides = [SpeakerOverride(turn=99, person="JA", reason="test")]
    with pytest.raises(TranscriptImportError, match="missing turns"):
        import_source(mini_repo, src)


def test_mixed_timing_fails(mini_repo):
    path = mini_repo.transcripts / "English plain.md"
    path.write_text(path.read_text() + "\n[00:10] **Guest:** timed\n")
    with pytest.raises(TranscriptImportError, match="no start time"):
        import_source(mini_repo, load_source(mini_repo, "S002"))


def test_run_import_writes_valid_raw(mini_repo):
    raw = run_import(mini_repo, "S003")
    assert mini_repo.raw_path("S003").exists()
    assert raw["schema"] == "rrs.transcript.raw/1"
    assert len(raw["transcript_sha256"]) == 64
