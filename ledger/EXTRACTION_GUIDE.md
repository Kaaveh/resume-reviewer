# Extraction guide

Condensed from docs/specs/02 sections 4 to 7 and ADR 0003. Sessions read this file, `rrs ledger rules
--compact` and one chunk; not the whole spec.

**Rules are statistical facts.** A rule is worth the number of distinct recruiters who state it, so
every mapping is a count. Map a claim to a rule only when the recruiter states that rule; record
numbers as values on measure rules; word new rules only from the claims in front of you.

## Steps, one chunk at a time

1. `uv run rrs chunks next [Sxxx]` names the chunk and its staging file.
2. Read this guide, `uv run rrs ledger rules --compact --proposed Sxxx` and the chunk.
3. Write draft claims (no `id`) to `ledger/staging/Sxxx.cNNN.jsonl`, one JSON object per line.
   Propose a rule in `ledger/staging/Sxxx.new-rules.yaml` only when no rule fits.
4. `uv run rrs ledger validate ledger/staging/Sxxx.cNNN.jsonl`; fix every error, read every warning.
5. `uv run rrs ledger review ledger/staging/Sxxx.cNNN.jsonl` and show the table to the owner. Apply
   the owner's edits and re-validate. When the owner accepts proposed rules (sets `decision`),
   run `uv run rrs ledger rules --accept Sxxx`, which rewrites `NEW-n` in the staging files.
6. After the owner approves the chunk: `uv run rrs ledger review <file> --approve`, then
   `uv run rrs ledger merge <file>`, then commit `ledger: Sxxx cNNN, N claims`.

## What counts as a claim

**In scope:** how CVs are screened (time, order, tools), what in a CV's content, structure or
format helps or hurts, rejection triggers, profile and link behavior (LinkedIn, GitHub), region
and personal-data norms, gaps and job history, seniority signals.

**Out of scope**, mapped to `X-` rules only so the ledger stays complete: interview-stage tips
(`X-INT`), visa routes and sponsorship processes (`X-VISA`), job boards and channels (`X-JOB`),
application volume and targeting (`X-VOL`), how hiring processes run (`X-PROC`), fake job ads
(`X-FAKE`). An `X-` rule is created like any other (proposed, then accepted), under its name.
Extract out-of-scope assertions only when they are concrete advice or practice; skip chat
about the industry (AI and the future of engineering, the recruiter's career).

**Who counts:** the guest only. Host paraphrases ("so you mean...") are never claims, and a guest
merely agreeing with a host paraphrase ("yeah exactly") is not a claim either. Viewer questions
read aloud are context. A registered recruiter acting as host (John Adib in S002 to S004) may
yield a claim only with `speaker_role: host` and `independent: true`, and only when the host
states their own practice rather than restating the guest; the tally ignores it by default.

**Atomicity:** one assertion per claim; split compound statements ("length, presentation and
bare tech lists are the top three mistakes" is three claims). Repeats of the same assertion by the
same recruiter become extra anchors on one claim, not new claims. A later repeat of a merged claim
is a draft with `duplicate_of: <claim id>`; merge folds its anchors into that claim.

**Type:**
- `F!` a fact that reports rejecting on it: "A DevOps CV without AWS or GCP is a reject";
  "pictures of any kind are a straight no"; "that'll probably make me reject them instantly".
  The `claim_en` must say so (rejects, screens out, does not progress).
- `F` a fact or practice: "on the first pass probably about 30 seconds"; "managers do pick on it
  very very quickly". A hiring manager or recruiter describing their own decisions is `F` (or
  `F!`), scoped to them in `claim_en`.
- `P` a preference or advice: "two pages is the general sweet spot"; "I recommend you drop the
  language section". Advice phrased as "you should" is `P` even when it sounds certain.
- Hedged practice ("it's difficult to keep going when...") is `F` when it describes what the
  recruiter does, `F!` only when it plainly reports rejecting or stopping.
- Added after the S004 agreement study, where the two extractions split on these:
  - The recruiter's account of what they see, do or react to when screening is `F`: naming the
    mistakes or red flags they see most ("the first mistake I see is length"), their reading
    behavior ("a cover letter that probably wouldn't get read"), their reactions ("there's
    nothing worse than coming across a profile with no picture").
  - What the candidate should do, and the recruiter's wishes ("I would rather see", "I want to
    see", "you don't need to"), is `P`. A reason attached to advice stays part of the `P` claim
    unless it is reported as something screeners actually do; "it gives people a reason to
    click past" is a hedged reason, so `P`.
  - `F!` needs a reported or flat-out rejection, including automatic filtering out in the
    recruiter's own process ("you'd need the ATS to filter anybody that wasn't SC eligible").
    A risk or an incentive ("can count against", "gives a reason to pass") is not `F!`.
  - Split a sentence that mixes types: advice plus the recruiter's reaction is two claims.

**Stance:** `+` supports the rule; `-` contradicts it ("GPA, nobody cares" against "include grades
only if notable"; "make it one page" at 6 to 10 years against "two pages"); `~` qualifies it
without taking a side ("honestly, just delete the summary"; "using AI is fine if you rework it").
Never create the opposite of an existing rule: map the claim to that rule with `-`.

**Mapping:** prefer an existing rule if a reviewer applying that rule would catch the same CV
problem, but only when the recruiter states that rule. Test: would a skeptical reader count this
recruiter as saying the rule's text? A claim that only supports a rule's premise ("the ATS was
never relied on" for "write for a human") gets a rule of its own. One assertion may map to
several rules with the same stance; split the claim if the stances differ.

**Quantities:** a stated number is a claim on the measure rule for that quantity (`rrs ledger rules`
marks them `[measure: unit]`), mapped to that rule only, stance `+`, with
`"value": {"min": 2, "max": 5, "condition": ""}`. A point is `min == max`; an open side is
`null` ("one page is too short" is `min: 2, max: null`); `condition` keeps the scope ("with 10 to
15 years of experience"). The tally reports the distribution across recruiters. Never turn a
number into a threshold rule; if no measure exists for the quantity, propose one.

**Context:** set `episode` to the episode of the first anchor. For CV reviews, `claim_en` may say
"for the DevOps CV" but never the CV owner's name.

**Language:** `claim_en` is always English and keeps the speaker's scope ("In their own
screening, ...", "For their startup clients, ..."). Refer to the recruiter as "the recruiter",
"the hiring manager" or by role, never with gendered pronouns. Quotes stay in the original
language; add `quote_en` for every non-English quote. No em-dashes or en-dashes anywhere.

**Self-check before validating:** would a skeptical reader who opens the quote in that sentence
agree with the paraphrase, the type and the stance? Is this the guest speaking? Is the scope
(their company, their clients, the market) preserved? Read the window before the anchor too:
scope words ("in my own experience", "on that first phone screening") often sit there and must
reach `claim_en`. Keep hedges ("can look a bit more carefully" is not "looks more carefully").
Added after the S002 and S003 verifications:
- Everything in `claim_en` must be inside an anchor quote. Phrases from the sentence just before
  or after the quote (a scope, a reason, "it happens quite a lot") need the quote extended.
- Hedges carry into new rules too: a rule worded from a hedged claim keeps the hedge ("usually").
- An `F!` claim names who rejects: the recruiter, managers, or a filter.
- A claim on a measure carries only the quantity; other assertions in the same breath are claims
  of their own.
- Start the quote at the guest's answer words, in the sentence the anchor names (the validator
  warns `anchor-start` when the quote begins in a later sentence).
Added after the S001 verification:
- Unreliable speaker labels: host questions and "so you mean" turns can sit inside guest-labelled
  turns. Read each anchored sentence for one; when the guest's answer is in the next turn, anchor
  there.
- Gloss every anchor: `quote_en` has one " / " segment per anchor, in anchor order.
- English terms come through Persian ASR as sound-alikes ("کور استرنج" core strengths, "ایبلیوس"
  AWS, "نوید" novice). Read the next sentences before glossing, and write "uncertain reading" in
  `notes` when a rule depends on the gloss.
- When repeats from other CVs are folded into a claim, generalize `claim_en` ("backend CVs without
  infrastructure, such as CV#03") instead of naming only the first CV.
- An `F!` names every reason the recruiter gives for the rejection, and sits on the rule naming the
  trait rejected, not only on a premise rule.

## Anchors

- `sentence_id` is where the quote starts; the quote may run into the next two sentences of the
  same speaker (unpunctuated sources are cut into 25-word windows, so this is common).
- `quote` is verbatim from the transcript `text`: whole words, at least about 6 words, enough to
  carry the assertion. The validator matches English on `norm` (case and punctuation ignored,
  whole words) and Persian on `norm_compact` (spaces, ZWNJ, Yeh and Kaf forms, digits ignored).
- `t_start` is the anchored sentence's `start` from the chunk line; `null` when the source has no
  timing.
- `attribution: content-override` only when the speaker label is wrong, with the reason in
  `notes`.

## Draft line

```json
{"recruiter": "JB", "source": "S004", "speaker_role": "guest", "attribution": "speaker-label",
 "independent": false,
 "anchors": [{"sentence_id": "S004.t0004.s001", "t_start": null,
              "quote": "on the first pass probably about 30 seconds"}],
 "episode": "S004.e02", "type": "F", "rules": ["SCR-1"], "stance": "+",
 "claim_en": "On the first pass the recruiter spends about 30 seconds on a CV.",
 "quote_en": null, "status": "draft",
 "extracted": {"date": "2026-10-19", "chunk": "S004.c001"}, "notes": ""}
```

(One object per line in the file; wrapped here for reading.)

## Proposed rules

```yaml
# ledger/staging/S004.new-rules.yaml
- id: NEW-1                  # temporary, unique within the file; X- rules use their name
  category: SCR              # SCR ATS STR ACH SKL RED REG SEN GAP CHN, or X
  text: One generalizable, checkable assertion, worded for the "for" side.
  check: How a reviewer spots a violation in a CV.
  rationale: Why no existing rule fits, and which claims use it.
  decision: proposed         # the owner sets accepted or rejected; rejected may add `use: <rule>`
```

Categories: SCR screening time and skim behavior, ATS ATS and keywords, STR structure and length,
ACH achievements and metrics, SKL skills section, RED red flags and auto-rejects, REG region norms
(photo, personal data, language, location, right to work), SEN seniority signals, GAP gaps and
job hopping, CHN channel and profiles around the CV (LinkedIn, GitHub, referrals, cover letters),
X out of scope.

Rule wording: one assertion a reviewer can check against a CV, general enough that another
recruiter could support or contradict it, and worded from the claims in hand. Every part of the
text must be something a recruiter said: do not join a stated fact to a CV conclusion nobody drew
(put how a reviewer uses the fact in `check`). Rules are worded from the claims in hand (never from what
a source not yet extracted is expected to say). Facts about screening practice that are not CV
checks ("the ATS rarely decides") are rules too, with a `check` saying how the reviewer uses them.
Numbers go in measure rules:

```yaml
- id: NEW-7
  category: STR
  text: CV length in pages.
  check: Count pages; compare with the recruiters' common range for the candidate's experience.
  measure: {unit: pages, question: How long should the CV be?}
  rationale: ...
```
