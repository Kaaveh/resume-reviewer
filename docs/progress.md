# Progress

## 2026-10-21, README: NotebookLM transcript prompt

**Changed**
- README.md now records the exact NotebookLM prompt used to produce the transcripts (verbatim,
  speaker labels, [mm:ss] timestamps, [inaudible] and [crosstalk] markers), with
  `[VIDEO TITLE]` and `[YOUTUBE URL]` placeholders, so it can be reused for new sources.
- No code, corpus or ledger changes.

**Next**
- Unchanged from the previous entry.

**Open questions for the owner**
- None new.

## 2026-10-20, Session 3 (spec 03): skill built, evals on four of five cases

**Changed**
- `skill/SKILL.md` written fresh (03 section 2): ground rules, review procedure with the target
  weighting of section 5, report format, Contested guidance for all 7 contested rules, Coverage
  gaps, Updating. EVIDENCE and RULES blocks generated; all four tiers shown, Single source rules
  labelled as one recruiter's view (the default for the open question; the owner can still ask for
  a minimum). 325 lines.
- `rrs skill build [--check] | lint | install [--global]` (`src/rrs/skill.py`) and
  `rrs eval grade` (`src/rrs/evals.py`). CI also runs `ledger validate`, `skill build --check`
  and `skill lint`. Lint caught the owner's name in the repository URL: SKILL.md names the
  repository without the URL.
- Evals: four synthetic cases and expected files with the new rule IDs (03 section 7 mapping:
  v0.1 RED-1 to RED-2, RED-8 to RED-5, RED-5 to REG-7, RED-7 to REG-6, SKL-2 to SKL-4, STR-9 to
  STR-2 judgment). Round 1 (`evals/results/v1.0.0-rc1`): 11/12, the photo missed because Coverage
  gaps told the reviewer not to flag DACH conventions, and channel advice (CHN-15) reported as a
  High finding. Both fixed in SKILL.md ("Beyond the CV" section). Round 2 (`evals/results/v1.0.0`):
  skill 12/12 must_flag, 4/4 verdicts, no must_not_flag hits, no invented numbers, no dashes;
  baseline 0/12 by rule ID (it uses none) and 3/4 verdicts. Grader fix: every rule ID in a bold
  span counts (`**REG-8 / REG-9**`).
- Synthetic CVs: year counts corrected (the backend CV said 8 years over 10 years of dates);
  spec 03 case description updated to 10 years.

**Next**
1. Owner: provide the CV text for `evals/cases/owner-cv-s001.md` (CV#10 as reviewed in S001, or
   the current CV). Expectations: verdict invite, RED-5 (double dash) at least Low, no Critical or
   High; "Medium linked twice" has no rule in the new index, so it is not expected.
2. Run the owner case with and without the skill, grade, then the owner reads the rewrites.
3. Release v1.0.0 (03 section 8): `rrs ledger tally --report`, `skill/CHANGELOG.md`, rebuild
   (the EVIDENCE line then reads `Evidence v1.0.0`), snapshot, tag, install globally, claude.ai
   and project mirror.

**Open questions for the owner**
- Owner CV text (above).
- Keep Single source rules in the skill as labelled (current), or set a minimum?
- The validator warning for `quote_en` with fewer " / " segments than anchors is still not added.

## 2026-10-20, Session 2 closed: S001 done, verification, rule splits, first snapshot

**Decisions by the owner**
- Remote branches `claude/dreamy-rubin-8cyjqs`, `claude/gifted-wright-1f40dw` and
  `claude/keen-newton-nh2j2q` had no commits beyond `main`; deleted. Only `main` remains.
- Open questions from the previous entry settled as Claude recommended: split compound rules
  where a recruiter states one clause only; reword STR-4 without a number; keep single-comment
  rules (they count as Single source; any minimum for the skill is a spec 03 decision); JA on both
  sides of STR-6 and SKL-2 is the intended reading.

**Changed**
- S001 c014 to c016 merged: JA-123 to JA-143; new rules STR-26, SKL-19, SCR-16, GAP-5.
  `scripts/merge_chunk.sh` uses `perl -pi` (BSD `sed -i` failed on macOS).
- S001 verification (`reports/verification/S001.md`, fresh subagent): 45 of 47 agree. JA-12 was
  built on a mistranslation ("کور استرنج" is core strengths, not courses): STR-11 retired for
  STR-29. JA-54 moved from RED-2 to the new RED-6 (missing most listed skills). CHN-12 and SCR-15
  reworded to JA's words. JA-30 split; its observation is JA-144. Nits, missing glosses, the JA-129
  quote and the ACH-6 cross-mapping (TW-07, TW-13, SB-19) applied in
  `ledger/amendments/S001-verification.yaml`. Guide updated with the verification's patterns.
- Compound rules split (`ledger/amendments/rule-splits.yaml`, 36 claims remapped): STR-5 to STR-27
  and STR-28; REG-1 to REG-14 and REG-15; REG-4 to REG-16, REG-17 and REG-18; CHN-1 to CHN-15 to
  CHN-17; CHN-2 to CHN-18 to CHN-20; CHN-7 to CHN-21 and CHN-22; GAP-1 to GAP-6 and GAP-7. ACH-2
  kept (only JB, who states both parts). STR-4 reworded.
- Change report `reports/changes/2026-10-20-S001.md`; first snapshot `reports/tally.json`
  (session-2): 4 sources, 4 recruiters, 311 claims, 134 active rules (11 Consensus, 20 Supported,
  7 Contested, 96 Single source). Spec 02 section 14 complete. 143 tests, ruff clean.

**Next**
- Session 3 (spec 03): `rrs skill build | lint`, SKILL.md written fresh, eval expectations with the
  new rule IDs.

**Open questions for the owner**
- 96 of 134 rules are Single source. Should the skill show them (labelled), or only rules with two
  or more recruiters? Spec 03 decides; a default is needed before the build.
- Suggested by the verification, not done: a validator warning when `quote_en` has fewer " / "
  segments than anchors. Add it?

## 2026-10-19, Session 2 (continued): S004 follow-ups, S002 and S003 done, S001 paused at c013

Paused by the owner mid-source to resume in a fresh session. Work is on `main` (fast-forwarded
from the session branch, which mirrors it).

**Changed**
- S004 follow-ups: NEW-24 and NEW-25 accepted as ACH-2 and CHN-4 (the CHN-4 measure needed
  block-style YAML); JB-13 lost the domain anchor, JB-28 moved to CHN-4 with value 70 (early
  career), JB-49 added on ACH-2 (`ledger/amendments/S004-followup.yaml`).
- S002 merged: SB-01 to SB-52 (one repeat folded into SB-28). Verification
  (`reports/verification/S002.md`): 11 of 12 agree; SB-47 split by type (SB-52 is the advice),
  7 notes applied (`ledger/amendments/S002-verification.yaml`). Change report
  `reports/changes/2026-10-19-S002.md`.
- S003 merged: TW-01 to TW-66, 18 new rules (SCR-8 to SCR-10, RED-4, STR-7 to STR-10, CHN-8 to
  CHN-11, ACH-5, SKL-7, REG-7, GAP-3, ATS-5, X-FAKE; measures STR-8 lines, STR-10 years, GAP-3
  months). TW is on both sides of ATS-4 (own agency manual, client ATS AI rejects), so neutral.
  Verification (`reports/verification/S003.md`): 18 of 18 agree, 14 notes applied
  (`ledger/amendments/S003-verification.yaml`); ATS-5 keeps TW's "usually". Change report
  `reports/changes/2026-10-19-S003.md`.
- Validator: new warning `anchor-start` (a quote that begins after the anchored sentence); it
  found and fixed four older anchors (JB-30, SB-23, TW-42, TW-52). Tally prints "1 page", not
  "1 pages". 143 tests, ruff clean.
- Extraction guide: lessons from the S002 and S003 verifications (everything in `claim_en` inside
  a quote, hedges carry into rules, `F!` names who rejects, measure claims carry only the quantity,
  start the quote where the anchor says).
- S001 c001 to c013 merged: JA-01 to JA-122, 53 S001 rules accepted under the standing approval
  (`ledger/staging/S001.new-rules.yaml`, NEW-1 to NEW-53, all `accepted`). Every Persian quote has
  `quote_en`; no CV owner name is in any quote, `claim_en` or `quote_en` (CVs named by episode
  label, e.g. CV#05). No host-labelled S001 turn was used as an anchor.
- Helpers committed: `scripts/draft_claims.py`, `scripts/merge_chunk.sh`,
  `scripts/fill_amend_tstart.py` (spec 02 section 7, CLAUDE.md). Ledger now 289 claims (JB 49,
  SB 52, TW 66, JA 122) and 125 rules.

**Next (resume here)**
1. S001 c014 to c016: `uv run rrs chunks next S001`. Notes already made for c014 (not written):
   CV#24 ML (education at the top is what fresh graduates do; recommend grouping skills, SKL-8 P;
   no projects for an ML career start, not invited, ACH-4 F!), e43 recruiters and agencies
   (X-PROC F, connect with agency recruiters on LinkedIn X-JOB P). Fold repeats with `dup`; the
   validator lists probable duplicates by ID.
2. S001 verification subagent (fresh, not seeing staging or progress): every F! and "-" claim plus
   a random 20% of S001 claims, extra attention to Persian glosses and the speaker check.
   Resolve with `ledger/amendments/S001-verification.yaml`, then
   `uv run rrs ledger tally --report --label S001`, `uv run rrs ledger render`, show the owner
   the review tables (`ledger/staging/archive/S001.*.jsonl`) and the verification.
3. Pending cross-mapping (ADR 0003, stated, so they count): ACH-6 "make achievements measurable"
   was created in S001; TW-07, TW-13 (statistics) and SB-19 (40% load time) state it too. Add
   ACH-6 to their `rules` in an amendment after the S001 verification.
4. Close Session 2: `rrs ledger tally --snapshot session-2`, `rrs ledger render`, last box in
   02 section 14, tests and ruff, progress entry with Session 3 (spec 03) next steps.

**Open questions for the owner**
- Compound rules split recruiters: a recruiter who states one clause supports the whole rule, and
  JA is now on both sides of STR-5 (names the university, rejects GPAs), so neutral there.
  Candidates to split (retire and replace): STR-5 (education / notable grade), REG-1 (location /
  right to work), REG-4 (location / phone country), CHN-1, CHN-2, CHN-7, GAP-1, ACH-2 (domain /
  end customers). Split now, before the snapshot?
- STR-4 still carries "three or four sentences" in its text; summary length is now the measure
  STR-21 (JA: at most 5, and 3 to 4 lines). Reword STR-4 without the number?
- JA contradicts STR-6 (tailor every CV; "keep it general, apply 50 a day", stance "-") and
  SKL-2 (a stack line under each job is good). Both labels become Contested once others are
  counted; is that the intended reading?
- Several S001 rules rest on one CV comment (bold, alignment, certificates at the end). They are
  facts about JA and count as Single source; keep, or set a minimum before a rule enters the skill?

## 2026-10-19, Session 2 (continued): owner decisions for the next session

**Decisions by the owner**
- NEW-24 and NEW-25 (S004, found by the independent extraction) accepted.
- All 26 S002 proposals accepted; startup-specific rules stay ordinary rules and target matching
  weighs them at review time (spec 03 section 5). Decisions are recorded in the two
  `ledger/staging/*.new-rules.yaml` files; nothing has been accepted into `rules.yaml` yet.
- Standing approval for the rest of Session 2: Claude may accept proposals, approve and merge
  chunks as recommended without stopping per chunk, but shows the owner each source's review
  table and verification result before starting the next source. Rules stay statistical facts
  (ADR 0003).
- Work is committed directly on `main`.

## 2026-10-19, Session 2 (continued): rules as statistical facts, S004 done, S002 drafted

**Decisions by the owner**
- S004 proposals accepted as recommended.
- Rules are statistical facts: a rule is worth the number of distinct recruiters who state it, and
  the specs may be rewritten to serve that. Recorded as ADR 0003 and principle D10 (00 sections 1
  and 3); spec 02 sections 4 to 8, spec 03 section 3 and the guide updated.
- Skipping CV-review process advice and the AI-and-the-future section was right.

**Changed**
- Measure rules (ADR 0003): quantities are rules with `measure: {unit, question}`; claims carry
  `value: {min, max, condition}`; the tally reports each recruiter's range (from unconditional
  values, conditional ones listed beside it), the common range and medians, and labels
  non-overlapping ranges `Contested range n`.
- `rrs ledger amend` edits merged claims from a reviewed YAML, validated and logged in
  `ledger/amendments.jsonl`. `rrs ledger validate --isolated` for independent extractions.
  Fixes: appending to the empty `rules.yaml`; `use:` naming a proposal accepted in the same pass.
  141 tests, ruff clean.
- S004 rules: 27 accepted (23 numbered, X-INT, X-VISA, X-VOL, X-PROC). Length (STR-2) and
  first-pass time (SCR-4) are measures; NEW-9 folded into STR-2; ATS-4 and SCR-5 split out of
  indirect mappings.
- S004 merged: 48 claims (JB-01 to JB-48). Verification by a fresh subagent
  (`reports/verification/S004.md`): 8 of 11 agree; the 3 disagreements and 3 notes applied with
  `ledger/amendments/S004-verification.yaml`, SCR-5 narrowed to what JB stated.
- Agreement study (`reports/agreement-S004.md`): A found by B 1.00, B found by A 0.90 (target 0.8
  met), stance 1.00, type 0.73. All type differences traced to three gaps in the guide's typing
  section, now written; the ledger amended to match (`ledger/amendments/S004-agreement.yaml`).
- `reports/changes/2026-10-19-S004.md` (no snapshot yet, so every rule is new).
- S002 drafted: c001 31 drafts, c002 21 (one repeat of c001 to fold), 26 proposed rules
  (`ledger/staging/S002.new-rules.yaml`). Both validate with no errors.

**Next**
1. Owner: decide NEW-24 and NEW-25 in `ledger/staging/S004.new-rules.yaml` (found only by the
   independent extraction) and the 26 S002 proposals; review the S002 chunks.
2. Claude: accept, then for S004 move the S004.t0022.s004 anchor off JB-13 and JB-28 onto the new
   rules; merge S002 c001 and c002, verification subagent for S002.
3. S003 (timed, English), then S001 (Persian, 16 chunks); first `reports/tally.json` snapshot.

**Open questions for the owner**
- NEW-24 (domain and end customers under each role) and NEW-25 (share of placements from
  referrals, a measure): accept?
- The S002 proposals include several startup-specific rules (stage and funding, zero to one,
  big-company context, breadth across the stack). They are facts about one recruiter's startup
  market; the target is EU employers. Keep them as rules (counted like any other) and let target
  matching weigh them at review time?

## 2026-10-19, Session 2: ledger tooling and the S004 drafts (spec 02)

**Changed**
- `rrs ledger validate | review | merge | rules | tally | render | agree` and `rrs chunks next`
  (`src/rrs/ledger/`): every check in 02 section 7 step 4 with one passing and one failing
  fixture each; counting as in 02 section 8; change reports (section 9); the markdown ledger
  (section 10); rule-level comparison for the agreement study (section 12). 135 tests, ruff clean.
- Workflow details the spec left open:
  - Proposed rules carry temporary IDs (`NEW-n`; X- rules their name) in
    `ledger/staging/<source>.new-rules.yaml`. The owner sets `decision`; `rrs ledger rules
    --accept <source>` assigns permanent IDs in acceptance order and rewrites the staging claims.
    Validation treats a proposed rule as a warning; approve and merge refuse it.
  - Chunk statuses: a clean `validate` sets `extracted`, `review --approve` sets `reviewed`,
    `merge` (which requires `reviewed`) sets `merged` and archives the staging file to
    `ledger/staging/archive/`. `merge_commit` is backfilled from the `ledger: Sxxx cNNN,` commit
    message on the next merge of that source.
  - A repeat of a merged claim is a draft with `duplicate_of: <id>`; merge folds its anchors.
  - English quotes must match whole words after `norm` (stricter than a bare substring, so a
    quote cannot start or end mid-word); a quote may span 3 sentences of the same speaker.
  - Claim IDs are zero-padded to two digits (`JB-01`), as in the v0.1 examples.
  - The agreement report takes its explanations from `ledger/agreement/<source>.yaml` because
    `reports/*` is generated.
- Ledger started (02 section 11): `recruiters.yaml` (four profiles, pronoun-neutral),
  `targets.yaml`, an empty `rules.yaml`, ADR 0001 (counting rules), `ledger/EXTRACTION_GUIDE.md`.
- S004 extracted into staging: c001 31 drafts, c002 17 drafts (4 of them repeats of c001 claims,
  to be folded with `duplicate_of` once c001 is merged), 24 proposed rules (20 in scope, X-INT,
  X-VISA, X-VOL, X-PROC). Both files validate with no errors.

**Not done, and why**
- Review, merge, the agreement study and the verification pass wait on the owner: the rule
  index is empty, so every S004 claim uses a proposed rule, and 02 section 12 runs the second
  extraction against the accepted rules.

**Next**
1. Owner: decide the 24 proposals in `ledger/staging/S004.new-rules.yaml` and review the two
   chunks (`uv run rrs ledger review ledger/staging/S004.c001.jsonl`).
2. Claude: `rrs ledger rules --accept S004`, apply edits, approve and merge c001, set
   `duplicate_of` on the c002 repeats, merge c002, render, commit per chunk.
3. Agreement study: a fresh subagent extracts S004 from the guide, the accepted rules and the
   chunks; `rrs ledger agree S004 --a <ledger S004 claims> --b <subagent files>`; explain the
   differences in `ledger/agreement/S004.yaml`; update the guide.
4. Verification subagent for S004 (`reports/verification/S004.md`), then S001 to S003 and the
   first `reports/tally.json` snapshot.

**Open questions for the owner**
- NEW-8 "Keep the CV to about two pages": JB contradicts it (two to five pages), so it has no
  support until SB or TW is extracted. Keep it worded for the two-page side, or word the length
  rule another way?
- Two mappings are judgment calls: S004 c001 line 7 (the ATS was never relied on for decisions)
  as `F` support for NEW-5 "write for a human", and line 6 (the recruiter must justify a candidate
  internally) as support for NEW-12 "problem, contribution, result".
- Skipped as out of scope with no X- rule: "ask someone in the industry to review your CV"
  (S004.t0026.s006) and the AI-and-the-future-of-engineering section (e19, e20). Add an X- rule
  for CV review process advice?

## 2026-10-19, Session 1 (continued): owner decisions

**Decisions by the owner**
- The v0.1 baseline (ledger, `build.py`, SKILL.md) is dropped. Specs 00 to 03 updated: no
  Session 0 migration or golden test; the ledger starts empty and every source is extracted
  with the 02 section 7 protocol (02 section 11); the agreement study compares two independent
  extractions of S004 (02 section 12); SKILL.md is written fresh (03 section 2); eval
  expectations must be restated with the new rule IDs (03 section 7).
- YouTube URLs are not in the NotebookLM exports; `url` stays null until known.
- Speaker mappings, the three S001 overrides and all episodes accepted as proposed
  (`speakers_confirmed: true`).
- The owner's CV is CV#10 (where the reviewer reads out the name); specs updated from CV#13.
- Claude decided the open verdicts: CV#11 `invite` (read t0091.s014 as "no infrastructure, but
  I invite"); CV#06 stays `none` because the reviewer gives no verdict for it.
- S003 turn 41: "Too much" is the guest's name; the correction now covers turns 41, 43, 57, 59,
  61, case-insensitively.

**Changed**
- `rrs reanchor [Sxxx]` is now the general tool for a replaced transcript (01 sections 7 and
  10): it re-maps each claim's existing anchors from their quotes, narrowing by old `t_start` or
  the claim's episode. The v0.1 legacy locator parsing is gone. Decisions file keys are
  `claim` and `anchor`.
- Corpus rebuilt (S003 turn 41, S001 CV#11 verdict). 89 tests, ruff clean.

**Next**
- Session 2 (spec 02): ledger commands, `ledger/EXTRACTION_GUIDE.md`, `recruiters.yaml` and
  `targets.yaml`, ADR 0001, then the S004 agreement study and extraction of S001 to S003.

**Open questions for the owner**
- None for Phase 1.

## 2026-10-19, Session 1: Phase 1 (spec 01)

**Changed**
- Bootstrapped the parts of the repo Phase 1 needs (00 section 5): `pyproject.toml` and `uv.lock`
  (Python 3.12, uv, Typer, Pydantic, pysbd, rapidfuzz, jsonschema), `rrs.toml`, `CLAUDE.md`
  (00 section 10), CI (`ruff` and `pytest` on every push), README.
- `src/rrs/`: `rrs import | segment | normalize | episodes | render | index | search | chunks |
  reanchor | build-corpus`. JSON Schemas for `transcript.raw.json` and `transcript.json`.
- Source YAMLs for S001 to S004 with proposed speaker mappings, three S001 speaker overrides and
  proper-noun corrections for S003 and S004. `glossary/terms.yaml` (seed list from 01 section
  3.2 plus Latin forms) and `glossary/people.yaml`.
- Generated corpus: 2,024 sentences (S001 1,067; S002 274; S003 433; S004 250), renders, the
  index, and 24 chunks (S001 16 at the 12,000-character budget; S002 2, S003 4, S004 2 at 24,000).
- Episodes: S001 53 (24 CV reviews with pseudonymized labels and verdicts), S002 29, S003 27,
  S004 22. Every sentence has an episode.
- ADR 0002 (sentence IDs and segmentation, including how unpunctuated turns are detected).
- 90 tests covering every item in 01 section 12; `ruff` clean.

**Not done, and why**
- Re-anchoring the 194 v0.1 claims (01 section 10) has not run: `baseline/` is not in the
  repo, so Session 0 (migration to `ledger/claims.jsonl`, spec 02 section 11) has not happened.
  `rrs reanchor` is implemented and tested on synthetic claims; it reads `legacy.locator` and
  `legacy.quotes` as spec 02 section 11 defines them and writes
  `ledger/migration/reanchor-report.md`. Owner decisions go in
  `ledger/migration/reanchor-decisions.yaml`.
- Owner confirmations were pending (resolved in the next entry).

**Notes for later sessions**
- Quotes often cross the 25-word windows of unpunctuated turns: anchors must allow spans of up
  to 3 sentences (02 section 7 already does).
- The S001 NotebookLM labels are unreliable (three overrides, three mixed turns). Claims from
  S001 host turns need a check against the video.
- `rrs search` takes `--source --person --role --term --lang`; Persian queries ignore ZWNJ,
  spacing, Yeh/Kaf forms and digits.

**Next**
1. Owner: provide `baseline/` (v0.1 `claims-ledger.md`, `build.py`, `SKILL.md`), then run
   Session 0, then `uv run rrs reanchor` and resolve review and manual items in batches of 15.
2. Owner: confirm the review document (URLs and metadata, speakers, S001 episodes and verdicts).
3. Session 2 (spec 02) can start on the S004 chunks once the corpus is confirmed.

**Open questions for the owner**
- YouTube URLs, channels, upload dates and durations for S001 to S004.
- Speaker mappings and the three S001 overrides (turns 2, 42, 142).
- S001 verdicts for CV#06 and CV#11; numbering of the owner's CV (CV#10 in order on air, CV#13
  in spec 01).
- S003 turn 41: is "Too much new" the guest's name?
