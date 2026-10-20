import pytest

from rrs.normalize.text import (
    clean_text,
    compact_with_map,
    lang_tag,
    norm,
    norm_compact,
    norm_with_map,
)


def test_zwnj_variants_share_compact_form():
    forms = ["می‌خوام", "میخوام", "می خوام"]
    assert len({norm_compact(f) for f in forms}) == 1


def test_zwnj_becomes_space_in_norm_but_stays_in_text():
    assert norm("می‌خوام") == "می خوام"
    assert clean_text("می‌خوام") == "می‌خوام"


@pytest.mark.parametrize(
    ("src", "want"),
    [
        ("ي", "ی"),  # Arabic Yeh
        ("ى", "ی"),  # Alef Maksura
        ("ك", "ک"),  # Arabic Kaf
        ("ة", "ه"),  # Teh Marbuta
        ("ۀ", "ه"),  # Heh with Yeh above
        ("آ", "ا"),
        ("أ", "ا"),
        ("إ", "ا"),
        ("ؤ", "و"),
        ("ئ", "ی"),
    ],
)
def test_letter_unification(src, want):
    assert norm(src) == want


def test_text_keeps_letters():
    assert clean_text("كتاب يك") == "كتاب يك"


def test_digits():
    assert norm("۱۰") == "10"
    assert norm("١٠") == "10"
    assert clean_text("۱۰") == "۱۰"


def test_diacritics_and_tatweel_removed():
    assert norm("كـتـاب") == "کتاب"
    assert norm("مُحَمَّد") == "محمد"
    assert norm("ٰ") == ""


def test_bidi_marks_removed_from_both():
    s = "‏سلام‎ ‫دنیا‬﻿ ⁧x⁩"
    assert clean_text(s) == "سلام دنیا x"
    assert norm(s) == "سلام دنیا x"


def test_punctuation_removed_including_dashes():
    assert norm("سلام، دنیا؛ خوبی؟ «آره» - well\u2014done!") == "سلام دنیا خوبی اره well done"


def test_latin_lowercased_and_nfkc():
    assert norm("AWS ＡＷＳ") == "aws aws"


def test_whitespace():
    assert clean_text("  a \n\t b  ") == "a b"
    assert norm("  a \n\t b  ") == "a b"


def test_hash_kept_for_tech_terms():
    assert norm("C# and F#") == "c# and f#"


def test_map_points_back_into_text():
    text = "Hello, \u200cWorld \u2013 ok"
    n, m = norm_with_map(text)
    assert n == "hello world ok"
    assert len(m) == len(n)
    assert text[m[n.index("world")]] == "W"
    c, cm = compact_with_map(text)
    assert c == "helloworldok" and text[cm[-1]] == "k"


def test_lang_tag():
    assert lang_tag("سلام دنیا") == "fa"
    assert lang_tag("hello world") == "en"
    assert lang_tag("سلام hello world from here") == "mixed"
    assert lang_tag("۱۰", default="fa") == "fa"
