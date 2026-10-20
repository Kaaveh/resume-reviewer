from rrs.glossary import Term
from rrs.normalize.terms import TermMatcher
from rrs.normalize.text import norm


def annotate(real_repo, text):
    from rrs.glossary import load_terms

    return TermMatcher(load_terms(real_repo)).annotate(norm(text))


def test_persian_variant(real_repo):
    assert {"c": "AWS", "v": "ایبلیوس"} in annotate(real_repo, "دواب که ایبلیوس بلد نباشه")


def test_multiword_persian_variant_with_any_spacing(real_repo):
    for text in ["جی سی پی", "جی‌سی‌پی", "جیسی پی"]:
        assert {"c": "GCP", "v": "جی سی پی"} in annotate(real_repo, text)


def test_ambiguous_flagged(real_repo):
    hits = annotate(real_repo, "اسکیلشو بنویسید")
    assert {"c": "skill", "v": "اسکیل", "amb": ["scale"]} in hits


def test_latin_token_not_inside_word(real_repo):
    assert annotate(real_repo, "these laws are strict") == []
    assert {"c": "AWS", "v": "AWS"} in annotate(real_repo, "I know AWS well")


def test_short_persian_variant_not_inside_word(real_repo):
    assert not any(t["c"] == "Jest" for t in annotate(real_repo, "جستجو کردم"))


def test_latin_plural_and_phrase():
    m = TermMatcher([Term(canonical="CV", kind="cv", variants=["CV"]),
                     Term(canonical="Node.js", kind="tech", variants=["Node.js"])])
    assert m.annotate(norm("their CVs use Node.js")) == [
        {"c": "CV", "v": "CV"}, {"c": "Node.js", "v": "Node.js"}
    ]


def test_dedupe_and_order():
    m = TermMatcher([Term(canonical="AWS", kind="tech", variants=["AWS", "ایبلیوس"])])
    assert m.annotate(norm("ایبلیوس و AWS و ایبلیوس")) == [
        {"c": "AWS", "v": "ایبلیوس"}, {"c": "AWS", "v": "AWS"}
    ]
