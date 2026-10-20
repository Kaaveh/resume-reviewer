from rrs.config import SegmentSettings
from rrs.segment.sentences import (
    length_guard,
    merge_fragments,
    split_english,
    split_persian,
    split_turn,
    windows,
)

S = SegmentSettings()


def words(n, prefix="w"):
    return [f"{prefix}{i}" for i in range(n)]


def test_persian_punctuation_split():
    assert split_persian("سلام. خوبی؟ آره! باشه؛ تموم") == ["سلام.", "خوبی؟", "آره!", "باشه؛", "تموم"]


def test_persian_split_keeps_decimals():
    assert split_persian("نمره ۷.۵ گرفت. بعدی 7.5 هم") == ["نمره ۷.۵ گرفت.", "بعدی 7.5 هم"]


def test_english_split_handles_abbreviations():
    assert split_english("Use tools e.g. Jest. Then ship it.") == ["Use tools e.g. Jest.", "Then ship it."]


def test_length_guard_splits_at_comma_nearest_middle():
    w = words(45)
    w[19] = w[19] + ","
    w[5] = w[5] + ","
    out = length_guard(w, S)
    assert [len(p) for p in out] == [20, 25]


def test_length_guard_keeps_41_to_60_without_comma():
    assert length_guard(words(55), S) == [words(55)]


def test_length_guard_hard_split_over_60():
    out = length_guard(words(130), S)
    assert all(len(p) <= 60 for p in out)
    assert sum(out, []) == words(130)


def test_fragment_merge():
    assert merge_fragments([["a", "b", "c"], ["d"], ["e", "f", "g"]], 3) == [
        ["a", "b", "c", "d"], ["e", "f", "g"]
    ]
    assert merge_fragments([["a"], ["b", "c", "d"]], 3) == [["a", "b", "c", "d"]]
    assert merge_fragments([["a"]], 3) == [["a"]]


def test_unpunctuated_turn_uses_windows():
    text = " ".join(words(60))
    out, unpunct = split_turn(text, persian=False, s=S)
    assert unpunct
    assert [len(p) for p in out] == [25, 25, 10]


def test_window_remainder_fragment_merges():
    out, _ = split_turn(" ".join(words(52)), persian=False, s=S)
    assert [len(p) for p in out] == [25, 27]


def test_windows_never_cross_pieces():
    assert windows(words(30), 25)[1] == words(30)[25:]


def test_punctuated_turn():
    out, unpunct = split_turn("One two three. Four five six! Seven eight nine?", False, S)
    assert not unpunct
    assert [" ".join(p) for p in out] == ["One two three.", "Four five six!", "Seven eight nine?"]


def test_segmented_transcript(mini_repo):
    from helpers import build

    t = build(mini_repo, "S003")
    assert t["timing"] == "turn"
    first_guest = t["turns"][1]
    assert [s["id"] for s in first_guest["sentences"]] == ["S003.t0002.s001", "S003.t0002.s002"]
    assert all(s["start"] == turn["start"] for turn in t["turns"] for s in turn["sentences"])
    long_turn = t["turns"][3]
    assert long_turn["split"] == "window"
    assert all(len(s["text"].split()) <= 27 for s in long_turn["sentences"])
    assert {s["lang"] for turn in t["turns"] for s in turn["sentences"]} == {"en"}


def test_corrections_logged(mini_repo):
    from helpers import build

    s = build(mini_repo, "S003")["turns"][0]["sentences"][0]
    assert "Tomasz" in s["text"] and s["text_orig"].endswith("hi Tomas How are you doing")


def test_persian_transcript(mini_repo):
    from helpers import build

    t = build(mini_repo, "S001")
    s = [s for turn in t["turns"] for s in turn["sentences"]]
    assert all(x["lang"] == "fa" for x in s)
    assert all(x["start"] is None for x in s)
    third = t["turns"][2]["sentences"]
    assert third[0]["text"] == "رزومه اول مال یه دواب هست."
    assert "۷.۵" in third[2]["text"]
    assert {"c": "DevOps", "v": "دواب"} in third[1]["terms"]
