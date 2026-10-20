from rrs.evals import findings, grade_report, verdict

REPORT = """# CV review: DevOps for Amsterdam

**Verdict:** Reject

**10-second verdict:** No AWS at the top of page one.

## Findings

### Critical
- **RED-2** (Consensus 3, Critical): no AWS.

### Low
- **REG-8 / STR-12** (Single source 1, Low): IELTS score. Also see **RED-2**.

### Judgment calls
- **STR-2** (Contested range 4): one page.

## Rewrites

- Before: "Built Jenkins pipelines for 40 services"
- After: "Built Jenkins pipelines for 40 services, cutting lead time by [X%] and 17 hours"

## What already works
- **ACH-6** numbers.
"""
EXPECTED = {"verdict": "reject", "must_flag": [{"rule": "RED-2", "min_severity": "Critical"},
                                               {"rule": "STR-12", "min_severity": "Low"}],
            "must_not_flag": ["ACH-6"], "judgment": ["STR-2"], "max_severity": "Medium"}


def test_findings_take_the_highest_heading_and_ignore_other_sections():
    assert findings(REPORT) == {"RED-2": "Critical", "REG-8": "Low", "STR-12": "Low", "STR-2": "Judgment"}
    assert verdict(REPORT) == "reject"


def test_grade_report():
    g = grade_report(REPORT, EXPECTED, cv="Built Jenkins pipelines for 40 services")
    assert g["verdict_ok"] and g["recall"] == (2, 2) and g["missed"] == []
    assert g["must_not_hits"] == []          # ACH-6 is under "What already works", not a finding
    assert g["over_cap"] == ["RED-2"]
    assert g["judgment"] == (1, 1) and g["ten_second_verdict"] and g["evidence_labels"]
    assert g["invented_numbers"] == ["17"]
