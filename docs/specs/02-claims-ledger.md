# 02. Phase 2: claims, rules and the evidence ledger

**Goal:** extract atomic, anchored claims from the corpus inside Claude Code sessions, map them to a stable rule index, and compute per rule how many distinct recruiters support or contradict it. This phase also owns starting the ledger (section 11) and the loop for adding new transcripts.
**Runs:** anywhere.
**Sessions:** 2 (protocol, agreement study, then extraction of every source). Read `00-overview.md` first.

## 1. Inputs and outputs

| Input | Output |
|---|---|
| `corpus/*/transcript.json`, `chunks/*` | `ledger/claims.jsonl` (source of truth) |
| Owner approval of new rules | `ledger/rules.yaml`, `ledger/recruiters.yaml`, `ledger/targets.yaml` |
| | `ledger/claims-ledger.md` (generated render) |
| | `reports/tally.json` (snapshot at each release), `reports/changes/*.md` |
| | `reports/verification/*.md`, `reports/agreement-S004.md` |
| | `ledger/EXTRACTION_GUIDE.md` (section 6 condensed for sessions) |

CLI: `rrs ledger validate | review | merge | tally | render | rules`, `rrs chunks next`.

## 2. Ledger layout

```text
ledger/
  recruiters.yaml     # profiles (section 3)
  targets.yaml        # target candidate profiles and recruiter match levels
  rules.yaml          # rule index (section 4)
  claims.jsonl        # one claim per line (section 5); append-only except for edits by `merge`
  staging/            # drafts per chunk, before review and merge
  migration/          # re-anchoring reports after a transcript changes
  claims-ledger.md    # generated, never edited
  EXTRACTION_GUIDE.md
```

## 3. Recruiter profiles and targets

Every recruiter gets a profile, because advice is weighted by how well the recruiter's world matches the target candidate.

```yaml
# ledger/recruiters.yaml
JA:
  name: John Adib
  type: hiring-manager        # agency | in-house-recruiter | hiring-manager | former-recruiter
  title: Engineering Manager
  region: UK (London)
  industry: Tech product company (GCP, AI-forward)
  roles_hired: Software engineers (backend, frontend, mobile, DevOps, data); junior to senior
  year: 2026
  year_basis: inferred        # metadata | stated | inferred
  sources: [S001]
  caveats: Says his calls are personal; another reader may decide differently.
```

The four current profiles: JA in-house engineering hiring manager, London, 2026; SB agency, UK VC-backed startups, JavaScript and TypeScript, self-described non-technical; TW agency, UK and Europe, tech, data and product, 2026; JB former agency recruiter of 14 years, EMEA and US, cross-border engineering hires, now at Vention.

```yaml
# ledger/targets.yaml
default: android-eu-relocation
targets:
  android-eu-relocation:
    description: Senior Android engineer, about 7 years, applying to EU/DACH employers from outside the EU, needing relocation or sponsorship
    match: {JA: high, TW: medium-high, JB: medium-high, SB: low-medium}
```

## 4. Rule index

```yaml
# ledger/rules.yaml
- id: RED-1
  category: RED                 # SCR ATS STR ACH SKL RED REG SEN GAP CHN, or X for out of scope
  text: Missing a core requirement of the target role or the employer's stack is a rejection.
  check: Compare JD must-haves and core role skills with the CV; any missing core item is Critical.
  status: active                # active | retired
  added_in: v0.1
```

Categories follow the project brief: SCR screening time and skim behavior, ATS ATS and keywords, STR structure and length, ACH achievements and metrics, SKL skills section, RED red flags and auto-rejects, REG region norms (photo, personal data, language, location), SEN seniority signals, GAP gaps and job hopping, CHN channel and profiles around the CV, X out of scope (interviews, visas, job-search tactics, process).

Rule policy (rules are statistical facts, ADR 0003):
- One generalizable, checkable assertion per rule. `check` tells a reviewer how to spot a violation.
- Word a rule only from claims already extracted; never from what a source not yet extracted is expected to say.
- A quantity (CV length in pages, first-pass time in seconds) is a **measure rule**: `measure: {unit, question}`, text naming the quantity, no threshold. Recruiters' values are its evidence (section 8).
- Create a rule only when no existing rule fits. A claim that disagrees with an existing rule maps to it with stance `-`; never create the opposite rule.
- IDs are permanent. Retire with `status: retired` and `superseded_by: <id>`; never renumber or delete.
- Contested rules keep the wording of the "for" side.
- New rules proposed during extraction go to `ledger/staging/<source>.new-rules.yaml` with a rationale and are accepted by the owner.

## 5. Claim schema

```json
{"id": "JA-16", "recruiter": "JA", "source": "S001",
 "speaker_role": "guest", "attribution": "speaker-label", "independent": false,
 "anchors": [{"sentence_id": "S001.t0003.s041", "t_start": null,
              "quote": "دواب که ایبلیوس یا جی سی پی بلد نباشه"}],
 "episode": "S001.e03",
 "type": "F!", "rules": ["RED-1"], "stance": "+",
 "claim_en": "Rejects when a core skill of the role is missing: DevOps without AWS, GCP or Azure.",
 "quote_en": "A DevOps engineer who doesn't know AWS or GCP: this CV is a reject.",
 "status": "merged",
 "extracted": {"date": "2026-10-25", "chunk": "S001.c002"},
 "notes": ""}
```

| Field | Rule |
|---|---|
| `id` | Recruiter code + running number, assigned at merge; permanent |
| `speaker_role` | `guest` counts; `host` counts only with `independent: true` and the config switch on (default off) |
| `attribution` | `speaker-label`, or `content-override` when the speaker label was wrong (explain in `notes`, as for v0.1 claim JA-43) |
| `anchors` | One or more; each quote must be found by the validator; `t_start` is the sentence start, null when the source has no timing |
| `type` | `F` fact or practice, `F!` fact that reports rejecting on it, `P` preference or advice |
| `rules` | One or more rule IDs, all with the same stance; split the claim if stances differ |
| `stance` | `+` supports, `-` contradicts, `~` qualifies (listed, not counted) |
| `claim_en` | English paraphrase that keeps the speaker's scope ("In his own hiring, ...") |
| `quote_en` | Recommended gloss when the quote is not English |
| `value` | Only on claims about a measure rule: `{min, max, condition}`, a point when `min == max`, open when a bound is null; `condition` keeps the scope ("with 10 to 15 years"). Such a claim maps to that one rule with stance `+` |
| `duplicate_of` | Staging only: the merged claim this draft repeats; merge folds its anchors there |

## 6. Extraction guide (what counts as a claim)

Condense this section into `ledger/EXTRACTION_GUIDE.md`; sessions read that file, not the whole spec.

**In scope:** how CVs are screened (time, order, tools), what in a CV's content, structure or format helps or hurts, rejection triggers, profile and link behavior (LinkedIn, GitHub), region and personal-data norms, gaps and job history, seniority signals.
**Out of scope** (map to `X-` rules only so the ledger stays complete): interview-stage tips (`X-INT`), visa routes (`X-VISA`), job boards and channels (`X-JOB`), application volume (`X-VOL`), how processes run (`X-PROC`), fake job ads (`X-FAKE`).

**Who counts:** guests only. Host paraphrases ("so you mean...") are never claims. Viewer questions read aloud are context. A registered recruiter acting as host (John Adib in S002, S003 and S004) may yield a claim only with `independent: true`, and the tally ignores it unless the config says otherwise.

**Atomicity:** one assertion per claim. Split compound statements. Repeats of the same assertion by the same recruiter become extra anchors on one claim, not new claims; they would not change the counts anyway.

**Typing, with v0.1 examples:**
- `F!`: "A DevOps CV without AWS or GCP is a reject" (JA-16); "pictures of any kind are a straight no" (TW-28); "that'll probably make me reject them instantly" (SB-26).
- `F`: "on the first pass probably about 30 seconds" (JB-01); "managers do pick on it very very quickly" (TW-08).
- `P`: "two pages is the general sweet spot" (SB-11); "I recommend you drop the language section" (JA-28).
A hiring manager describing his own decisions is `F` (or `F!`), scoped to him in `claim_en`.

**Stance, with v0.1 examples:**
- `-`: "GPA, nobody cares" (JA-14) contradicts STR-10 "include grades only if notable"; "make it one page" at 6 to 10 years (JA-15) contradicts STR-1.
- `~`: "honestly, just delete the summary" (JA-10) qualifies STR-7 without taking a side; "using AI is fine if you rework it" (TW-13) qualifies RED-4.

**Mapping:** prefer an existing rule if a reviewer applying that rule would catch the same CV problem, but only when the recruiter states that rule: a claim that merely supports a rule's premise ("the ATS was never relied on" for "write for a human") gets its own rule, because every mapping is a count. One assertion may map to several rules with the same stance (v0.1 SB-22 maps to CHN-3 and RED-3).

**Quantities:** a stated number (pages, seconds, years) is a claim on the measure rule for that quantity, with a `value`; a recruiter who says "one page is too short" states `min: 2`. Never turn a number into a threshold rule.

**Context:** set `episode`; for CV reviews, the claim's paraphrase may say "for the DevOps CV" but never the owner's name.

**Translation:** `claim_en` is always English; quotes stay in the original language; add `quote_en` for Persian.

**Self-check before validating each draft:** Would a skeptical reader who opens the quote in that sentence agree with the paraphrase, the type and the stance? Is this the guest speaking? Is the scope (his company, his clients, the market) preserved?

## 7. Extraction protocol inside Claude Code

One chunk per step, so every output stays small and the work can resume from the manifest at any point.

1. `rrs chunks next` prints the next pending chunk.
2. Read `ledger/EXTRACTION_GUIDE.md`, `rrs ledger rules --compact` (ID, category, text) and the chunk.
3. Append draft claims (no IDs) to `ledger/staging/S005.c003.jsonl`; propose new rules in `ledger/staging/S005.new-rules.yaml` only when nothing fits. `scripts/draft_claims.py` writes the file from a compact spec and copies `t_start` and `episode` from the corpus; `scripts/merge_chunk.sh` runs steps 4 to 7 under a standing approval.
4. `rrs ledger validate ledger/staging/S005.c003.jsonl` and fix every error:
   - schema valid; types, stances and rule IDs valid; rules active
   - recruiter registered, and a guest in that source (or `independent` host)
   - each anchor's sentence exists and belongs to the claim's recruiter (unless `content-override` with a reason)
   - each quote is found in that sentence or in up to 3 consecutive sentences starting there: `norm_compact` substring for Persian or mixed text, `norm` substring for English
   - `t_start` equals the anchored sentence's start (both null when the source has no timing)
   - `claim_en` is English and contains no em-dashes or en-dashes; `quote_en` present for non-English quotes
   - warnings: probable duplicate (same recruiter, rule and stance), `F!` whose paraphrase never mentions rejecting, a quote that starts after the anchored sentence (`anchor-start`)
5. `rrs ledger review ledger/staging/S005.c003.jsonl` prints a compact table (time, original quote, `claim_en`, type, stance, rules). The owner approves or edits; Claude applies edits and re-validates.
6. `rrs ledger merge ledger/staging/S005.c003.jsonl` assigns IDs, folds approved duplicates into existing claims as extra anchors, appends the rest to `claims.jsonl`, marks the chunk `merged` in the manifest, and archives the staging file.
7. Commit: `ledger: S005 c003, N claims`.
8. After the last chunk of a source, run an **independent verification** with a fresh subagent that has not seen the drafting: it checks a random 20% of the source's claims plus every `F!` and every `-` claim (quote supports paraphrase, type, stance, rule), and writes `reports/verification/S005.md`. The owner resolves disagreements.
9. `rrs ledger tally --report` writes the change report (section 9); then `rrs skill build` (spec 03).

## 8. Counting, labels and severity (normative)

This is the v0.1 algorithm (ADR 0001), extended for measure rules by ADR 0003 (below the block). Changing it needs an ADR, because it changes every label.

```text
counts(c) = c.speaker_role == "guest" or (c.independent and config.count_independent_hosts)

for each rule R:
  C      = [c for c in claims if R in c.rules and counts(c)]
  plus   = {c.recruiter for c in C if c.stance == "+"}
  minus  = {c.recruiter for c in C if c.stance == "-"}
  both   = plus & minus;  plus -= both;  minus -= both      # self-contradiction is neutral
  n_f    = |{r in plus: some "+" claim of r on R has type F or F!}|
  n_p    = |plus| - n_f
  n_rej  = |{r in plus: some "+" claim of r on R has type F!}|

  label  = "Contested |plus|-|minus|"  if plus and minus
           "Consensus |plus|"          if |plus| >= 3
           "Supported 2"               if |plus| == 2
           "Single source 1"           if |plus| == 1
           "No support"                otherwise (an error unless R is X- or retired)

  base severity:
    X- rules  -> n/a
    Contested -> Judgment
    otherwise start at Consensus: High, Supported: Medium, Single: Low, then
      n_rej >= 2 -> Critical;  n_rej == 1 -> raise one level, at most High

  order: tier (Consensus, Supported, Contested, Single), then more supporters first,
         then higher severity, then category order SCR ATS STR ACH SKL RED REG SEN GAP CHN,
         then rule number
```

Measure rules (ADR 0003): each recruiter's range is the intersection of their unconditional values (all values when every one is conditional; the hull when they conflict), with conditional values listed beside it; supporters are the recruiters with a counted value, labels and severity as above, except that two or more ranges without a common overlap give `Contested range n` with severity Judgment. The tally reports per-recruiter ranges, the common range and the medians of the bounds.

Evidence cell format in renders: `Consensus 4 (4F/0P, 4 report rejecting)`; measure rules append the distribution: `Supported 2 (0F/2P, 0 report rejecting); JB 2 to 5 pages, SB 2 pages; common 2 pages`.

## 9. Change reports

`rrs ledger tally --report` compares the current tally with `reports/tally.json` (the last release) and writes `reports/changes/<date>-<source>.md`:

- label changes (for example `SKL-6: Single source 1 -> Supported 2`) and severity changes
- rules whose supporter set changed with the same label (`Consensus 3 -> Consensus 4`)
- newly contested rules, rules that lost all support, new and retired rules
- new recruiters and their profile match for the default target

The report goes into the commit or PR description. `reports/tally.json` is rewritten only at release (spec 03 section 8).

## 10. Generated markdown ledger

`rrs ledger render` writes `ledger/claims-ledger.md` in the v0.1 layout: conventions, recruiter profiles, rule index, then one table per recruiter. The locator column becomes `S001.t0003.s041 q:"..."`, with `[HH:MM:SS]` after the ID when the source has timing. It exists for reading and for the claude.ai project mirror; nothing parses it.

## 11. Starting the ledger (no v0.1 migration)

The v0.1 ledger is not migrated (owner decision, 2026-10-19; 00 section 2). The ledger starts empty:
1. Write `ledger/recruiters.yaml` (the four profiles in section 3) and `ledger/targets.yaml` by hand.
2. `ledger/rules.yaml` starts empty. Rules are proposed during extraction in `ledger/staging/<source>.new-rules.yaml` and accepted by the owner (section 4); IDs follow the category prefixes in section 4, numbered in order of acceptance.
3. Extract every source with the section 7 protocol, starting with S004 (section 12).
4. Write ADR 0001 recording section 8 as the counting rules.

## 12. Agreement study (Session 2)

Measure how repeatable extraction is before trusting it on new sources.

1. Extract S004 (Joe Bignell, English, the smallest source) twice with the section 7 protocol: once in the main session (the ledger of record) and once in a fresh subagent that sees only the guide, the accepted rules and the chunks, not the first extraction.
2. Compare at the rule level: the set of rules JB supports (`+`) and opposes (`-`) in each extraction. Report agreement in both directions (rules found by one and missed by the other), stance agreement, and type agreement (`F`, `F!`, `P`) on matched rules.
3. Write `reports/agreement-S004.md` with every difference explained, and update the extraction guide where the differences came from vague guidance. Target: at least 0.8 of each extraction's rules found by the other.

## 13. Sourcing plan for new transcripts

Fill the coverage gaps found in v0.1, in this order:
1. DACH-based recruiters or hiring managers (German or English): photo norms, length, German-language expectations.
2. Android or mobile engineering hiring managers and specialist recruiters.
3. In-house talent acquisition at EU scale-ups (Netherlands, Germany).
4. More hiring managers in general (three of four v0.1 sources are agency or ex-agency).

Selection criteria: the speaker's role is verifiable; recorded in 2025 or later; concrete talk about CV screening; at least 15 minutes of relevant content; usable audio. Intake checklist: a NotebookLM transcript in `transcripts/` (with turn timestamps), URL, metadata, people codes and roles, languages, speaker mapping. The first German source must add German rules to the normalizer (case folding, `ß` to `ss`, umlaut matching) and a German term list.

## 14. Acceptance criteria

Session 2:
- [x] Ledger started as in section 11; ADR 0001 written.
- [x] `validate`, `review`, `merge`, `tally --report`, `render` and `chunks next` work as specified, with tests (validator: one passing and one failing fixture per check).
- [x] `ledger/EXTRACTION_GUIDE.md` written.
- [x] Agreement study report for S004, guide updated.
- [x] Verification report produced by a fresh subagent for S004.
- [x] S001 to S003 extracted, verified and merged; first `reports/tally.json` snapshot written.

## 15. Kickoff prompts

Session 2:

```text
Read CLAUDE.md, docs/progress.md, docs/specs/00-overview.md and docs/specs/02-claims-ledger.md.
Implement the ledger commands in section 7 test-first, write ledger/EXTRACTION_GUIDE.md from
section 6, start the ledger as in section 11, then run the agreement study in section 12 on S004.
Show me each staging chunk with `rrs ledger review` before merging it. Finish with the agreement report and a verification subagent pass.
Small commits; progress entry at the end.
```

Resuming Session 2 (S001 from `rrs chunks next S001`):

```text
Read CLAUDE.md, the top entry of docs/progress.md, ledger/EXTRACTION_GUIDE.md and
docs/decisions/0003-rules-as-statistical-facts.md. Work on main. Continue S001 from
`uv run rrs chunks next S001` with the standing approval in docs/progress.md: draft each chunk
with scripts/draft_claims.py, validate, merge with scripts/merge_chunk.sh. Then the S001
verification subagent, amendments, `rrs ledger tally --report --label S001`, show me; then
close Session 2 (progress.md "Next").
```

Adding a new source (any later session):

```text
Read CLAUDE.md, docs/progress.md and ledger/EXTRACTION_GUIDE.md. Source S00N has a canonical
transcript and chunks. Run the extraction protocol in docs/specs/02 section 7 chunk by chunk: validate,
show me the review table, merge after my approval, commit per chunk. Then run the verification
subagent, `rrs ledger tally --report` and `rrs skill build`, and summarize which rules changed.
```
