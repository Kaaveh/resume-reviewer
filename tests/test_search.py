import pytest

from rrs.corpus.index import index_rows
from rrs.corpus.search import search

from helpers import build

# Quotes cited for v0.1 claims in the specs, as they appear in the transcripts.
KNOWN = [
    ("S001", "دواب که ایبلیوس یا جی سی پی بلد نباشه"),
    ("S001", "اسکیلشو بنویسید"),
    ("S001", "دواب که ایبلیوس"),
    ("S004", "on the first pass probably about 30 seconds"),
    ("S003", "pictures of any kind"),
    ("S003", "managers do pick on it very very quickly"),
    ("S002", "two pages is the general sweet spot"),
    ("S002", "that'll probably make me reject them instantly"),
    ("S003", "always going to be a straight no"),
    ("S002", "ownership is um a very very important part"),
]


@pytest.fixture(scope="module")
def rows(real_repo_module):
    out = []
    for sid in ("S001", "S002", "S003", "S004"):
        out.extend(index_rows(build(real_repo_module, sid)))
    return out


@pytest.fixture(scope="module")
def real_repo_module():
    from rrs.config import Repo

    from conftest import ROOT

    return Repo(ROOT)


@pytest.mark.parametrize(("sid", "quote"), KNOWN)
def test_known_quotes_found(rows, sid, quote):
    hits = search(rows, quote)
    assert hits, quote
    assert hits[0]["source"] == sid


def test_persian_search_ignores_zwnj_and_spacing(rows):
    a = search(rows, "رزومه‌ها", source="S001")
    b = search(rows, "رزومهها", source="S001")
    assert a and [r["id"] for r in a] == [r["id"] for r in b]


def test_filters(rows):
    assert all(r["person"] == "TW" for r in search(rows, "linkedin", person="TW"))
    assert all(r["role"] == "host" for r in search(rows, "cv", role="host"))
    assert all(any(t["c"] == "AWS" for t in r["terms"]) for r in search(rows, "", term="AWS"))
    assert search(rows, "", term="AWS", source="S001")


def test_english_matches_whole_tokens(rows):
    assert not any("laws" in r["norm"].split() for r in search(rows, "aws"))
