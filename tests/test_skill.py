import pytest

from rrs.skill import build, lint, replace_block, strip_blocks


def test_committed_skill_is_built_and_clean(real_repo):
    old, new, _ = build(real_repo)
    assert old == new, "run `rrs skill build`"
    assert lint(real_repo, new) == []


def test_replace_and_strip_blocks():
    text = "a\n<!-- RULES:START -->\nold\n<!-- RULES:END -->\nb\n"
    new = replace_block(text, "RULES", "new")
    assert new == "a\n<!-- RULES:START -->\nnew\n<!-- RULES:END -->\nb\n"
    assert strip_blocks(new) == "a\n\nb\n"
    with pytest.raises(ValueError):
        replace_block("no markers", "EVIDENCE", "x")


def test_lint_finds_each_problem(real_repo):
    _, text, _ = build(real_repo)
    bad = (text.replace("name: resume-reviewer", "name: other")
           .replace("| SKL-5 |", "| ACH-1 |")       # SKL-5 loses its row, ACH-1 is not contested
           .replace("## Updating", "## Updating\n\nSee SKL-1 and ZZ-99 — and Kaaveh.\n\n| a | b |\n|---|\n"))
    msgs = " ".join(m for _, m in lint(real_repo, bad))
    for expected in ["name is 'other'", "em-dash", "SKL-5 is contested", "ACH-1 has a Contested",
                     "ZZ-99 is not a claim", "CV owner's name", "1 columns, header has 2"]:
        assert expected in msgs, expected


def test_single_source_rules_are_grouped_by_person(real_repo):
    from rrs.ledger.models import load_recruiters
    from rrs.ledger.tally import compute
    from rrs.skill import rules_block

    tally = compute(real_repo)
    block = rules_block(tally, load_recruiters(real_repo))
    single = block.split("### Single source")[1]
    assert "#### JA, John Adib: hiring manager" in single
    assert "#### SB, Sam Baldwin: agency recruiter" in single
    for rid in [r for r in tally["order"] if tally["rules"][r]["tier"] == "Single source"
                and tally["rules"][r]["category"] != "X" and tally["rules"][r]["status"] == "active"]:
        head = single.split(f"| {rid} |")[0].rsplit("#### ", 1)[1]
        assert head.startswith(tally["rules"][rid]["plus"][0])
