import copy

import pytest
import yaml

from rrs.chunks.build import build_chunks
from rrs.ingest.parse import run_import
from rrs.jsonio import read_json, read_jsonl, write_jsonl
from rrs.ledger.models import Claim, Rule
from rrs.ledger.render import render_ledger
from rrs.ledger.tally import change_report, compute, tally_rule
from rrs.ledger.validate import validate_file, validate_rows
from rrs.ledger.workflow import (
    WorkflowError,
    accept_rules,
    approve,
    merge,
    next_chunk,
    review_table,
)
from rrs.segment.build import run_segment

RECRUITERS = {
    "TW": {"name": "Tomasz Wojtyczko", "type": "agency", "title": "Consultant", "region": "UK",
           "industry": "Tech", "roles_hired": "Engineers", "year": 2026, "year_basis": "inferred",
           "sources": ["S003"]},
    "JA": {"name": "John Adib", "type": "hiring-manager", "title": "EM", "region": "UK",
           "industry": "Tech", "roles_hired": "Engineers", "year": 2026, "year_basis": "inferred",
           "sources": ["S001"]},
}
RULES = [
    {"id": "RED-1", "category": "RED", "text": "Photos and logos are a rejection.",
     "check": "Any photo or logo.", "added_in": "v1.0"},
    {"id": "STR-1", "category": "STR", "text": "Two pages is the norm.", "check": "Count pages.",
     "added_in": "v1.0"},
    {"id": "SKL-1", "category": "SKL", "text": "Old rule.", "check": "x", "added_in": "v1.0",
     "status": "retired", "superseded_by": "STR-1"},
    {"id": "X-INT", "category": "X", "text": "Interview tips.", "check": "n/a", "added_in": "v1.0"},
]


@pytest.fixture
def lrepo(mini_repo):
    for sid in ("S001", "S003"):
        run_import(mini_repo, sid)
        run_segment(mini_repo, sid)
        build_chunks(mini_repo, sid)
    led = mini_repo.ledger
    led.mkdir(exist_ok=True)
    (led / "recruiters.yaml").write_text(yaml.safe_dump(RECRUITERS))
    (led / "rules.yaml").write_text(yaml.safe_dump(RULES, sort_keys=False))
    (led / "targets.yaml").write_text(yaml.safe_dump(
        {"default": "t", "targets": {"t": {"description": "Android", "match": {"TW": "medium"}}}}))
    return mini_repo


TW = {
    "recruiter": "TW", "source": "S003", "speaker_role": "guest", "attribution": "speaker-label",
    "independent": False,
    "anchors": [{"sentence_id": "S003.t0004.s001", "t_start": 20.0,
                 "quote": "pictures of any kind is a is a is always going to be a straight no"}],
    "episode": None, "type": "F!", "rules": ["RED-1"], "stance": "+",
    "claim_en": "Rejects any CV with pictures or logos.", "quote_en": None, "status": "draft",
    "extracted": {"date": "2026-10-19", "chunk": "S003.c001"}, "notes": "",
}
JA = {
    **TW, "recruiter": "JA", "source": "S001", "type": "F!",
    "anchors": [{"sentence_id": "S001.t0003.s002", "t_start": None,
                 "quote": "دواب كه ايبليوس يا جی‌سی‌پی بلد نباشه"}],
    "claim_en": "Rejects a DevOps CV without AWS or GCP.", "quote_en": "A DevOps without AWS or GCP",
    "extracted": {"date": "2026-10-19", "chunk": "S001.c001"},
}


def codes(repo, row, level="error", **kw):
    return {i.code for i in validate_rows(repo, [row], staging=True, ledger=[], **kw)
            if i.level == level}


def mod(base, path, value):
    row = copy.deepcopy(base)
    target = row
    *head, last = path
    for k in head:
        target = target[k]
    target[last] = value
    return row


def test_valid_english_and_persian_drafts_pass(lrepo):
    assert codes(lrepo, TW) == set() and codes(lrepo, TW, "warning") == set()
    assert codes(lrepo, JA) == set()


@pytest.mark.parametrize("path,value,code", [
    (("type",), "X", "schema"),
    (("stance",), "!", "schema"),
    (("anchors",), [], "schema"),
    (("rules",), ["RED-99"], "rule"),
    (("rules",), ["SKL-1"], "rule"),
    (("rules",), ["RED-1", "RED-1"], "rule"),
    (("recruiter",), "SB", "recruiter"),
    (("speaker_role",), "host", "role"),
    (("independent",), True, "role"),
    (("anchors", 0, "sentence_id"), "S003.t0009.s001", "sentence"),
    (("anchors", 0, "sentence_id"), "S003.t0003.s001", "speaker"),
    (("anchors", 0, "quote"), "pictures are fine", "quote"),
    (("anchors", 0, "quote"), "pictures of any ki", "quote"),
    (("anchors", 0, "t_start"), 21.0, "t_start"),
    (("anchors", 0, "t_start"), None, "t_start"),
    (("claim_en",), "عکس نذارید", "claim-en"),
    (("claim_en",), "Rejects photos — always.", "dash"),
    (("quote_en",), "No photos – ever", "dash"),
    (("episode",), "S003.e09", "episode"),
    (("extracted", "chunk"), "S003.c009", "chunk"),
    (("id",), "TW-01", "draft"),
    (("attribution",), "content-override", "attribution"),
])
def test_each_check_fails_on_a_bad_draft(lrepo, path, value, code):
    assert code in codes(lrepo, mod(TW, path, value))


def test_quote_may_span_up_to_three_sentences_of_the_recruiter(lrepo):
    three = mod(TW, ("anchors", 0, "quote"), "and I know that that sounds harsh but it is what it is "
                "and managers do pick on it very very quickly so keep it plain and simple and make it "
                "easy to read")
    assert codes(lrepo, three) == set()
    across_speakers = mod(TW, ("anchors", 0), {"sentence_id": "S003.t0004.s003", "t_start": 20.0,
                                               "quote": "who opens it thanks"})
    assert "quote" in codes(lrepo, across_speakers)


def test_content_override_with_reason_may_anchor_another_speaker(lrepo):
    row = mod(TW, ("anchors", 0), {"sentence_id": "S003.t0003.s001", "t_start": 12.0,
                                   "quote": "the first thing you look at"})
    row.update(attribution="content-override", notes="label wrong; video shows TW", type="F",
               claim_en="Looks at a CV first for the basics.")
    assert codes(lrepo, row) == set()


def test_independent_host_claim_is_valid(lrepo):
    row = mod(TW, ("anchors", 0), {"sentence_id": "S003.t0003.s001", "t_start": 12.0,
                                   "quote": "the first thing you look at"})
    row.update(recruiter="JA", speaker_role="host", independent=True, type="F",
               claim_en="Asks what recruiters look at first.")
    assert codes(lrepo, row) == set()


def test_persian_quote_needs_quote_en(lrepo):
    assert "quote-en" in codes(lrepo, mod(JA, ("quote_en",), None))


def test_proposed_rule_is_a_warning_and_rejected_one_an_error(lrepo):
    path = lrepo.ledger / "staging" / "S003.new-rules.yaml"
    path.parent.mkdir(parents=True)
    path.write_text(yaml.safe_dump([
        {"id": "NEW-1", "category": "STR", "text": "t", "check": "c", "rationale": "r"},
        {"id": "NEW-2", "category": "STR", "text": "t", "check": "c", "rationale": "r",
         "decision": "rejected"},
    ]))
    assert codes(lrepo, mod(TW, ("rules",), ["NEW-1"]), "warning") == {"proposed-rule"}
    assert "rule" in codes(lrepo, mod(TW, ("rules",), ["NEW-2"]))


def test_warnings_for_duplicates_and_f_bang_without_rejection(lrepo):
    assert codes(lrepo, mod(TW, ("claim_en",), "Dislikes pictures."), "warning") == {"f-bang"}
    issues = validate_rows(lrepo, [TW, TW], staging=True, ledger=[])
    assert [(i.line, i.code) for i in issues if i.level == "warning"] == [(2, "duplicate")]
    merged = Claim.model_validate({**TW, "id": "TW-01", "status": "merged"})
    issues = validate_rows(lrepo, [TW], staging=True, ledger=[merged])
    assert "TW-01" in next(i.message for i in issues if i.code == "duplicate")
    folded = {**TW, "duplicate_of": "TW-01"}
    assert not validate_rows(lrepo, [folded], staging=True, ledger=[merged])
    assert "duplicate-of" in {i.code for i in validate_rows(
        lrepo, [{**TW, "duplicate_of": "TW-07"}], staging=True, ledger=[merged])}


def test_ledger_mode_requires_unique_ids_matching_the_recruiter(lrepo):
    ok = {**TW, "id": "TW-01", "status": "merged"}
    assert not validate_rows(lrepo, [ok], staging=False)
    issues = validate_rows(lrepo, [ok, ok, {**ok, "id": "JA-02"}, {**ok, "id": None}], staging=False)
    assert [(i.line, i.code) for i in issues] == [(2, "id"), (3, "id"), (4, "id")]


def write_staging(repo, name, rows):
    path = repo.ledger / "staging" / name
    write_jsonl(path, rows)
    return path


def test_review_approve_merge_and_fold(lrepo):
    second = {**TW, "type": "P", "rules": ["STR-1"], "claim_en": "Two pages is the sweet spot.",
              "anchors": [{"sentence_id": "S003.t0006.s001", "t_start": 70.0,
                           "quote": "two pages is the general sweet spot"}]}
    path = write_staging(lrepo, "S003.c001.jsonl", [TW, second])
    table = review_table(lrepo, path)
    assert "| 1 | 00:00:20 |" in table and "RED-1" in table and "| P | + | STR-1 |" in table
    with pytest.raises(WorkflowError, match="approve"):
        merge(lrepo, path)
    assert approve(lrepo, path) == "S003.c001"
    r = merge(lrepo, path)
    assert r["new"] == ["TW-01", "TW-02"] and not path.exists()
    assert (lrepo.ledger / "staging" / "archive" / "S003.c001.jsonl").exists()
    ledger = read_jsonl(lrepo.ledger / "claims.jsonl")
    assert [c["id"] for c in ledger] == ["TW-01", "TW-02"]
    assert all(c["status"] == "merged" and "duplicate_of" not in c for c in ledger)
    assert read_json(lrepo.chunks / "S003" / "manifest.json")["chunks"][0]["status"] == "merged"
    assert next_chunk(lrepo, ["S003"]) is None and next_chunk(lrepo)["id"] == "S001.c001"
    assert not [i for i in validate_file(lrepo, lrepo.ledger / "claims.jsonl") if i.level == "error"]

    # A later repeat folds into TW-01 as an extra anchor (chunk files only merge once, so a
    # non-chunk staging file stands in for a re-extraction).
    repeat = {**TW, "duplicate_of": "TW-01", "anchors": [
        {"sentence_id": "S003.t0004.s002", "t_start": 20.0, "quote": "managers do pick on it"}]}
    r = merge(lrepo, write_staging(lrepo, "S003.extra.jsonl", [repeat]))
    assert r == {"chunk": None, "new": [], "folded": ["TW-01"]}
    assert len(read_jsonl(lrepo.ledger / "claims.jsonl")[0]["anchors"]) == 2


def test_merge_refuses_invalid_or_proposed(lrepo):
    path = write_staging(lrepo, "S003.c001.jsonl", [mod(TW, ("anchors", 0, "quote"), "nope")])
    with pytest.raises(WorkflowError, match="quote"):
        approve(lrepo, path)


def test_accept_rules_assigns_ids_and_rewrites_staging(lrepo):
    staging = lrepo.ledger / "staging"
    staging.mkdir(parents=True)
    (staging / "S003.new-rules.yaml").write_text(yaml.safe_dump([
        {"id": "NEW-1", "category": "RED", "text": "Pictures.", "check": "c", "rationale": "r",
         "decision": "accepted"},
        {"id": "NEW-2", "category": "STR", "text": "Pages.", "check": "c", "rationale": "r",
         "decision": "rejected", "use": "STR-1"},
        {"id": "X-VOL", "category": "X", "text": "Volume.", "check": "n/a", "rationale": "r",
         "decision": "accepted"},
        {"id": "NEW-3", "category": "SCR", "text": "Later.", "check": "c", "rationale": "r"},
    ]))
    path = write_staging(lrepo, "S003.c001.jsonl", [mod(TW, ("rules",), ["NEW-1", "NEW-2"])])
    pairs = accept_rules(lrepo, "S003", "v1.0")
    assert pairs == [("NEW-1", "RED-2"), ("NEW-2", "STR-1"), ("X-VOL", "X-VOL")]
    assert read_jsonl(path)[0]["rules"] == ["RED-2", "STR-1"]
    rules = yaml.safe_load((lrepo.ledger / "rules.yaml").read_text())
    assert [r["id"] for r in rules][-2:] == ["RED-2", "X-VOL"]
    left = yaml.safe_load((staging / "S003.new-rules.yaml").read_text())
    assert [p.get("assigned") for p in left] == ["RED-2", "STR-1", "X-VOL", None]
    assert accept_rules(lrepo, "S003", "v1.0") == []  # idempotent


def test_accept_into_the_empty_rules_file_keeps_its_header(lrepo):
    from rrs.ledger.models import load_rules

    (lrepo.ledger / "rules.yaml").write_text("# Rule index.\n[]\n")
    staging = lrepo.ledger / "staging"
    staging.mkdir(parents=True)
    (staging / "S003.new-rules.yaml").write_text(yaml.safe_dump([
        {"id": "NEW-1", "category": "STR", "text": "Length.", "check": "c", "rationale": "r",
         "decision": "accepted", "measure": {"unit": "pages", "question": "How long?"}},
        {"id": "NEW-2", "category": "STR", "text": "x", "check": "c", "rationale": "r",
         "decision": "rejected", "use": "NEW-1"}]))
    assert accept_rules(lrepo, "S003", "v1.0") == [("NEW-1", "STR-1"), ("NEW-2", "STR-1")]
    text = (lrepo.ledger / "rules.yaml").read_text()
    assert text.startswith("# Rule index.\n- id: STR-1") and "[]" not in text
    (rule,) = load_rules(lrepo)
    assert rule.measure.unit == "pages"


def C(cid, rec, rule, stance="+", typ="F", role="guest", independent=False):
    return Claim.model_validate({
        **TW, "id": cid, "recruiter": rec, "rules": [rule], "stance": stance, "type": typ,
        "speaker_role": role, "independent": independent, "status": "merged"})


R = Rule(id="RED-1", category="RED", text="t", check="c", added_in="v1.0")


@pytest.mark.parametrize("claims,label,severity,evidence", [
    ([C("A-1", "AA", "RED-1", typ="F!"), C("B-1", "BB", "RED-1", typ="F!"),
      C("D-1", "DD", "RED-1", typ="P")], "Consensus 3", "Critical",
     "Consensus 3 (2F/1P, 2 report rejecting)"),
    ([C("A-1", "AA", "RED-1"), C("B-1", "BB", "RED-1", typ="F!")], "Supported 2", "High", None),
    ([C("A-1", "AA", "RED-1", typ="F!")], "Single source 1", "Medium", None),
    ([C("A-1", "AA", "RED-1", typ="P")], "Single source 1", "Low", None),
    ([C("A-1", "AA", "RED-1"), C("B-1", "BB", "RED-1", stance="-")], "Contested 1-1", "Judgment",
     None),
    # Self-contradiction is neutral: AA drops out of both sides.
    ([C("A-1", "AA", "RED-1"), C("A-2", "AA", "RED-1", stance="-"), C("B-1", "BB", "RED-1")],
     "Single source 1", "Low", None),
    ([C("A-1", "AA", "RED-1", stance="~")], "No support", "n/a", None),
    ([C("A-1", "AA", "RED-1", role="host", independent=True)], "No support", "n/a", None),
])
def test_tally_labels_and_severity(claims, label, severity, evidence):
    r = tally_rule(R, claims, False)
    assert (r["label"], r["severity"]) == (label, severity)
    if evidence:
        assert r["evidence"] == evidence


def test_tally_independent_host_switch_and_x_rules():
    host = [C("A-1", "AA", "RED-1", role="host", independent=True)]
    assert tally_rule(R, host, True)["label"] == "Single source 1"
    x = Rule(id="X-INT", category="X", text="t", check="c", added_in="v1.0")
    assert tally_rule(x, [C("A-1", "AA", "X-INT", typ="F!")], False)["severity"] == "n/a"


def test_tally_order_and_change_report(lrepo):
    rules = [Rule.model_validate(r) for r in RULES]
    claims = [C("TW-01", "TW", "STR-1"), C("JA-01", "JA", "STR-1"), C("TW-02", "TW", "RED-1", typ="F!")]
    t = compute(lrepo, claims, rules)
    assert t["order"][:2] == ["STR-1", "RED-1"]
    assert t["totals"]["labels"]["Supported"] == 1 and t["totals"]["rules"] == 2
    old = compute(lrepo, claims[:1] + claims[2:], rules)
    report = change_report(lrepo, t, old, "test")
    assert "STR-1: Single source 1 -> Supported 2" in report
    assert "JA John Adib" in report and "—" not in report


def test_render_ledger(lrepo):
    write_jsonl(lrepo.ledger / "claims.jsonl", [{**TW, "id": "TW-01", "status": "merged"}])
    text = render_ledger(lrepo)
    assert 'S003.t0004.s001 [00:00:20] q:"pictures of any kind' in text
    assert "## TW Tomasz Wojtyczko (1 claims)" in text
    assert "Single source 1 (1F/0P, 1 report rejecting)" in text


def test_cli_validate_marks_extracted_and_chunks_next(lrepo, monkeypatch):
    from typer.testing import CliRunner

    from rrs.cli import app

    monkeypatch.setenv("RRS_ROOT", str(lrepo.root))
    run = CliRunner().invoke
    out = run(app, ["chunks", "next", "S003"])
    assert out.exit_code == 0 and "S003.c001 (pending)" in out.output
    bad = write_staging(lrepo, "S003.c001.jsonl", [mod(TW, ("rules",), ["RED-9"])])
    out = run(app, ["ledger", "validate", str(bad)])
    assert out.exit_code == 1 and "unknown rule RED-9" in out.output
    write_staging(lrepo, "S003.c001.jsonl", [TW])
    assert run(app, ["ledger", "validate", str(bad)]).exit_code == 0
    assert "S003.c001 (extracted)" in run(app, ["chunks", "next", "S003"]).output
    assert run(app, ["ledger", "review", str(bad), "--approve"]).exit_code == 0
    out = run(app, ["ledger", "merge", str(bad)])
    assert out.exit_code == 0 and "1 claims merged (TW-01 to TW-01)" in out.output
    out = run(app, ["ledger", "tally", "--report", "--label", "S003"])
    assert "RED-1: Single source 1" in out.output
    assert list((lrepo.root / "reports" / "changes").glob("*-S003.md"))


def test_agreement_compares_rule_sets_stances_and_types():
    from rrs.ledger.agreement import compare, render

    def row(rules, stance="+", typ="F"):
        return {"recruiter": "JB", "rules": rules, "stance": stance, "type": typ}

    a = [row(["SCR-1"]), row(["STR-1"], "-"), row(["ACH-1"], typ="F!"), row(["CHN-1"]),
         row(["CHN-2"], "~")]
    b = [row(["SCR-1"], typ="P"), row(["STR-1"], "+"), row(["ACH-1"], typ="F!"), row(["GAP-1"])]
    r = compare(a, b)
    assert r["only_a"] == ["CHN-1"] and r["only_b"] == ["GAP-1"]
    assert r["a_found_by_b"] == 0.75 and r["b_found_by_a"] == 0.75
    assert r["stance_differs"] == ["STR-1"] and r["type_differs"] == ["SCR-1"]
    text = render(r, "S004", "A", "B", {"CHN-1": "B skipped the anecdote."})
    assert "| CHN-1 | only in A | + F (1 claims) | not used | B skipped the anecdote. |" in text
    assert "not met." in text and "*not explained yet*" in text


PAGES = Rule(id="STR-9", category="STR", text="CV length.", check="Count pages.", added_in="v1.0",
             measure={"unit": "pages", "question": "How long should the CV be?"})


def V(cid, rec, lo, hi, typ="P", condition=""):
    return Claim.model_validate({**TW, "id": cid, "recruiter": rec, "rules": ["STR-9"], "type": typ,
                                 "status": "merged",
                                 "value": {"min": lo, "max": hi, "condition": condition}})


def test_measure_rule_reports_the_distribution_of_values():
    r = tally_rule(PAGES, [V("JB-1", "JB", 2, 5), V("JB-2", "JB", 2, None), V("SB-1", "SB", 2, 2)],
                   False)
    assert r["measure"]["by_recruiter"] == {"JB": [2, 5], "SB": [2, 2]}
    assert r["measure"]["common"] == [2, 2] and r["label"] == "Supported 2"
    assert r["evidence"].endswith("JB 2 to 5 pages, SB 2 pages; common 2 pages")
    # Ranges that do not overlap are a contest, decided at review time.
    r = tally_rule(PAGES, [V("JB-1", "JB", 2, 5), V("JA-1", "JA", 1, 1)], False)
    assert (r["label"], r["severity"]) == ("Contested range 2", "Judgment")
    # Conflicting statements by one recruiter fall back to the hull of what they said.
    r = tally_rule(PAGES, [V("JB-1", "JB", 1, 1), V("JB-2", "JB", 3, 4)], False)
    assert r["measure"]["by_recruiter"] == {"JB": [1, 4]} and r["label"] == "Single source 1"


def test_measure_claims_need_one_rule_a_value_and_stance_plus(lrepo):
    rules = yaml.safe_load((lrepo.ledger / "rules.yaml").read_text())
    rules.append({**PAGES.model_dump(exclude_none=True), "id": "STR-9"})
    (lrepo.ledger / "rules.yaml").write_text(yaml.safe_dump(rules, sort_keys=False))
    ok = {**TW, "type": "P", "rules": ["STR-9"], "claim_en": "Two pages is the sweet spot.",
          "value": {"min": 2, "max": 2}}
    assert codes(lrepo, ok) == set()
    assert "measure" in codes(lrepo, {**ok, "value": None})
    assert "measure" in codes(lrepo, {**ok, "rules": ["STR-9", "RED-1"]})
    assert "measure" in codes(lrepo, {**ok, "stance": "-"})
    assert "measure" in codes(lrepo, {**TW, "value": {"min": 2, "max": 2}})
    assert "schema" in codes(lrepo, {**ok, "value": {"min": 3, "max": 2}})
    assert "schema" in codes(lrepo, {**ok, "value": {"condition": "x"}})


def test_decided_proposal_ids_are_errors(lrepo):
    staging = lrepo.ledger / "staging"
    staging.mkdir(parents=True)
    (staging / "S003.new-rules.yaml").write_text(yaml.safe_dump([
        {"id": "NEW-1", "category": "RED", "text": "t", "check": "c", "rationale": "r",
         "decision": "accepted", "assigned": "RED-2"}]))
    assert "RED-2" in next(i.message for i in validate_rows(
        lrepo, [mod(TW, ("rules",), ["NEW-1"])], staging=True, ledger=[]) if i.code == "rule")


def test_measure_range_uses_unconditional_values_and_lists_conditional_ones():
    r = tally_rule(PAGES, [V("SB-1", "SB", 1, 1, condition="junior"), V("SB-2", "SB", 2, 2),
                           V("SB-3", "SB", 2, None, condition="CTO or VP")], False)
    m = r["measure"]
    assert m["by_recruiter"] == {"SB": [2, 2]}
    assert m["text"] == "SB 2 pages (junior: 1 page; CTO or VP: at least 2 pages)"
    only_conditional = tally_rule(PAGES, [V("TW-1", "TW", 1, 2, condition="junior")], False)
    assert only_conditional["measure"]["by_recruiter"] == {"TW": [1, 2]}


def test_amend_edits_merged_claims_with_a_log_and_refuses_invalid_edits(lrepo):
    from rrs.ledger.workflow import amend

    write_jsonl(lrepo.ledger / "claims.jsonl", [{**TW, "id": "TW-01", "status": "merged"}])
    edits = lrepo.root / "edits.yaml"
    edits.write_text(yaml.safe_dump([{"claim": "TW-01", "set": {"type": "F"},
                                      "reason": "verification: no rejection reported"}]))
    assert amend(lrepo, edits) == ["TW-01"]
    assert read_jsonl(lrepo.ledger / "claims.jsonl")[0]["type"] == "F"
    (entry,) = read_jsonl(lrepo.ledger / "amendments.jsonl")
    assert (entry["old"], entry["new"], entry["field"]) == ("F!", "F", "type")
    edits.write_text(yaml.safe_dump([{"claim": "TW-01", "set": {"rules": ["RED-99"]}, "reason": "x"}]))
    with pytest.raises(WorkflowError, match="unknown rule"):
        amend(lrepo, edits)
    assert read_jsonl(lrepo.ledger / "claims.jsonl")[0]["rules"] == ["RED-1"]
    edits.write_text(yaml.safe_dump([{"claim": "TW-01", "set": {"id": "TW-02"}, "reason": "x"}]))
    with pytest.raises(WorkflowError, match="cannot change"):
        amend(lrepo, edits)


def test_quote_that_starts_after_the_anchored_sentence_warns(lrepo):
    late = mod(TW, ("anchors", 0, "quote"), "managers do pick on it very very quickly")
    assert "anchor-start" in codes(lrepo, late, level="warning")
    assert "anchor-start" not in codes(lrepo, TW, level="warning")
