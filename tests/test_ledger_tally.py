

def test_fmt_range_singular_unit():
    from rrs.ledger.tally import fmt_range

    assert fmt_range(1, 1, "pages") == "1 page"
    assert fmt_range(2, 2, "pages") == "2 pages"
    assert fmt_range(1, 2, "pages") == "1 to 2 pages"
