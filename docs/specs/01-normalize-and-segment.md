# 01. Phase 1: import, normalize, segment and build the corpus

**Goal:** turn each hand-made NotebookLM transcript into the canonical corpus: verbatim text plus normalized matching fields, term annotations, sentences with stable IDs (and timestamps when the transcript has them), topic episodes, a human-readable render, a search index, and chunks sized for claim extraction in Claude Code. Then re-anchor the 194 v0.1 claims to sentence IDs.
**Runs:** anywhere.
**Session:** 1. Read `00-overview.md` first.

## 1. Inputs, import and outputs

The pipeline starts from transcripts the owner makes by hand in NotebookLM. Nothing in this repo downloads media, transcribes or diarizes.

### 1.1 Transcripts

One Markdown file per source in `transcripts/`, exported from NotebookLM and committed as is. The parser accepts the shapes of the four v0.1 files:

```markdown
# <video title>
Source: <YouTube URL>        (optional)
---                          (optional)

[mm:ss] **Interviewer:** text on the same line or on the next lines
**Guest:** text
```

- A turn starts with `**<Label>:**`. The label is whatever NotebookLM wrote (`Guest`, `Interviewer`, or a name) and is mapped to a person in the source YAML.
- An optional `[mm:ss]` or `[hh:mm:ss]` prefix is the turn's start time. S003 has them; S001, S002 and S004 do not. When making a new transcript, ask NotebookLM to prefix every turn with its start time so claims get timestamps.
- A committed transcript is never edited. A better transcript replaces the file and bumps `transcript_version` (section 7).

### 1.2 Source registry

One YAML per source, written by hand at intake. The metadata fixes two v0.1 problems: lost URLs and guessed interview years.

```yaml
id: S001
slug: john-adib-live-cv-review
transcript_file: "John Adib, engineering Manager.md"   # in transcripts/
url: https://www.youtube.com/watch?v=...
title: "..."
channel: "..."
upload_date: 2026-08-..   # for livestreams this is the stream date
recorded_date: null       # only if the video states it
duration_s: 7421
languages: [fa, en]       # spoken languages
format: live-cv-review    # interview | live-cv-review | panel | talk
people:
  - {person: JA, role: guest}     # codes from glossary/people.yaml
  - {person: H01, role: host}
speakers: {Guest: JA, Interviewer: H01}   # transcript labels to people
speaker_overrides: []
corrections: []           # proper-noun fixes, logged (section 2)
notes: "Viewer questions are read aloud by the host; they are not claims."
```

**Speaker mapping:** Claude proposes `speakers:` from content (who asks the questions, who says the guest's name or role) and shows three sample turns per label; the owner confirms. NotebookLM labels are unreliable (one known mislabeled block in S001, v0.1 claim JA-43), so fixes go into `speaker_overrides` by turn number:

```yaml
speaker_overrides:
  - {turn: 57, person: JA, reason: "guest answering; transcript labels it Interviewer"}
```

### 1.3 Import

`rrs import S001` parses the transcript, applies the mapping and overrides, and writes `corpus/S001/transcript.raw.json`. Unmapped labels block the import.

```json
{
  "schema": "rrs.transcript.raw/1",
  "source_id": "S001",
  "transcript_file": "John Adib, engineering Manager.md",
  "transcript_sha256": "...",
  "timing": "none",
  "speakers": {"Guest": "JA", "Interviewer": "H01"},
  "overrides_applied": [],
  "turns": [
    {"n": 1, "label": "Guest", "person": "JA", "start": null, "text": "سلام به همه ..."}
  ]
}
```

`timing` is `turn` when the turns carry start times (as in S003), otherwise `none`. Turn IDs (`S001.t0001`) are assigned during segmentation, not here.

### 1.4 Inputs and outputs

| Input | Output |
|---|---|
| `transcripts/*.md`, `sources/*.yaml` | `corpus/Sxxx/transcript.raw.json` |
| `glossary/terms.yaml`, `glossary/people.yaml` | `corpus/Sxxx/transcript.json` |
| `ledger/claims.jsonl` (only when re-anchoring, section 10) | `corpus/Sxxx/episodes.yaml` (confirmed by the owner) |
| | `corpus/Sxxx/transcript.md` and `corpus/index.jsonl` |
| | `chunks/Sxxx/cNNN.md` and `manifest.json` |
| | `ledger/migration/reanchor-report.md`, updated anchors in `ledger/claims.jsonl` |
| | `docs/decisions/0002-sentence-ids.md` |

CLI: `rrs import`, `rrs normalize`, `rrs segment`, `rrs episodes --propose | --apply`, `rrs render`, `rrs index`, `rrs search`, `rrs chunks`, `rrs reanchor`. One umbrella command `rrs build-corpus Sxxx` runs them in order.

## 2. Verbatim policy and corrections

A sentence carries three text fields. Only `text` is shown and quoted.

| Field | Content | Allowed changes |
|---|---|---|
| `text` | What was said, as transcribed | Whitespace tidy, removal of invisible bidi marks, and listed `corrections` |
| `norm` | Matching and search form, single spaces | Every rule in section 3 |
| `norm_compact` | `norm` with all spaces removed | Used for Persian substring matching |

`corrections` in a source YAML fix proper nouns only, never content, and are logged in the sentence as `text_orig` (the original):

```yaml
corrections:
  - {find: "too much", replace: "Tomasz", person: JA, reason: "host saying the guest's name"}
```

## 3. Normalization and term annotation

### 3.1 Rules

Implement these in `src/rrs/normalize/` as small, individually tested functions. `hazm` may be used as a reference, but do not make the pipeline depend on it: it has historically pinned heavy dependencies.

| Step | `text` | `norm` |
|---|---|---|
| Unicode form | NFC | NFKC |
| Whitespace | collapse runs, trim | same |
| Invisible marks (U+200E, U+200F, U+202A to U+202E, U+2066 to U+2069, U+FEFF) | remove | remove |
| Arabic Yeh U+064A and Alef Maksura U+0649 | keep | Persian Yeh U+06CC |
| Arabic Kaf U+0643 | keep | Keheh U+06A9 |
| Teh Marbuta U+0629, Heh with Yeh above U+06C0 | keep | Heh U+0647 |
| Alef with hamza or madda (U+0622, U+0623, U+0625) | keep | Alef U+0627 |
| Waw with hamza U+0624, Yeh with hamza U+0626 | keep | Waw U+0648, Yeh U+06CC |
| Tatweel U+0640, diacritics U+064B to U+065F and U+0670 | keep | remove |
| ZWNJ U+200C | keep as transcribed | replace with a space |
| Persian digits U+06F0 to U+06F9 and Arabic-Indic digits U+0660 to U+0669 | keep | ASCII 0 to 9 |
| Persian punctuation (، ؛ ؟ « ») and all other punctuation, including dashes | keep | remove (replace with a space) |
| Latin letters | keep | lowercase |

Why `norm_compact`: v0.1 anchors failed to match because the same word appeared as `می‌خوام`, `میخوام` and `می خوام`. With spaces and ZWNJ removed on both sides, all three match. Use `norm_compact` only for Persian or mixed text; English matching uses `norm` tokens.

### 3.2 Term glossary

English tech terms spoken in Persian are transcribed in Persian script, often mangled, and some are ambiguous. Do not rewrite `text`; annotate sentences instead, so search and extraction can query canonical terms.

```yaml
# glossary/terms.yaml
- canonical: AWS
  kind: tech
  variants: [AWS, ایبلیوس, ایبلی اس, ایبلیس, ایبلیو, ادبلی اس, ادبلیو اس]
- canonical: skill
  kind: cv
  variants: [اسکیل]
  ambiguous_with: [scale]   # v0.1: "اسکیلشو بنویسید" meant the company's scale
```

Matching: Persian variants against `norm_compact`, Latin variants as whole tokens against `norm`. Output per sentence: `terms: [{"c": "AWS", "v": "ایبلیوس"}, {"c": "skill", "v": "اسکیل", "amb": ["scale"]}]`. Ambiguous hits are resolved by the extractor from context, never automatically.

Seed list from v0.1 (extend as new sources arrive; each variant was seen in S001):

| Canonical | Variants seen |
|---|---|
| AWS | ایبلیوس, ایبلی اس, ایبلیس, ایبلیو, ادبلی اس |
| GCP | جی سی پی |
| Azure | آژور, آژر, آجر |
| DevOps | دواپس, دوابس, دواب, دبابس, دواس |
| Terraform | ترافرم, ترافورم |
| Kubernetes | کوبرنتیس, کوبرنتز |
| Docker | داکر |
| TypeScript | تایپ اسکریپت |
| JavaScript | جاوا اسکریپت |
| React / React Native | ریاکت / ریاکت نیتیو |
| Node.js | ناد جی اس, نا جی اس, ناجی اس |
| PHP / Laravel | پی اچ پی / لاراول, لارول |
| Flutter / Kotlin / Swift | فلاتر / کاتلین / سوئیفت |
| GraphQL | گراف کیول, گرافیکل |
| CI/CD | سیآی سی دی |
| testing | تستینگ |
| Playwright / Cypress / Jest / Vitest | پلی رایت / سایپرس / جست / وی تست |
| AI | ایآی |
| Claude / Cursor / ChatGPT | کلود, کلو / کرسر / چت جیپیتی, چت چیپیتی |
| GitHub / LinkedIn | گیتهاب, گیتاب / لینکدین |
| Stack Overflow / Medium / YouTube | استکور فلو, استکلو / میدیوم, میلیوم / یوتیوب |
| IELTS / TOEFL | آیلس / تافل |
| ATS | ایتی اس |
| CV | رزومه, سی وی |
| cover letter | کاور لتر, کابلت, کاولت |
| summary / bullet point | سامری / بلت پوینت, بولت پوینت |
| tech stack | تکستک, تک استک |
| reject | ریجکت |
| hiring manager / recruiter | هایرینگ منیجر / ریکروتر |
| ownership | اونرشیپ |
| infrastructure / deploy | اینفراستراکچر, اینفرا / دیپلوی |
| senior | سینیر, سنیور |
| software engineer / product engineer | سافتور انجینر, سافر انجینر / پروداکت انجینر |
| skill (ambiguous with scale) | اسکیل |

## 4. People registry and roles

Identity lives in `glossary/people.yaml`; recruiter profiles live in `ledger/recruiters.yaml` (spec 02). A person keeps one code across all sources; the role is per source (in the source YAML). John Adib is `JA` everywhere: guest in S001, host in S002, S003 and S004.

```yaml
people:
  JA:  {name: John Adib, kind: recruiter, aliases: [جان ادیب, جان]}
  SB:  {name: Sam Baldwin, kind: recruiter, aliases: []}
  TW:  {name: Tomasz Wojtyczko, kind: recruiter, aliases: ["too much", Tomas]}
  JB:  {name: Joe Bignell, kind: recruiter, aliases: []}
  H01: {name: Sahar, kind: host, aliases: [سحر]}
orgs:   {Vention: [Venshin], VirtueTech: []}
places: {Uzbekistan: [Isbekistan], Kyrgyzstan: [Kyrgystan]}
```

Aliases feed the `corrections` list.

## 5. Sentence segmentation

1. **Boundaries from punctuation.** Split each turn at sentence-final punctuation in the transcript (`.`, `?`, `!`, `؟`, `…`). English: `pysbd` (handles abbreviations such as "e.g."). Persian: a rule-based splitter on `.`, `؟`, `!`, `؛` that does not split inside numbers like `7.5` or `۷.۵`; use `pysbd`'s Persian mode only if it passes the same tests.
2. **Length guard.** If a sentence has more than 40 words, split at the comma nearest the middle, recursively; hard split at 60 words. Live monologues produce run-on sentences, and long sentences make anchors vague.
3. **Fragment merge.** Merge fragments under 3 words into the previous sentence of the same turn.
4. **Unpunctuated turns** (one v0.1 transcript has no punctuation at all): fixed windows of 25 words that never cross a turn.
5. **Timing.** A sentence's `start` is its turn's start time; null when the source has `timing: none`.
6. **Language tag** per sentence from the share of Arabic-script letters among all letters: at least 0.5 is `fa`, at most 0.1 is `en`, otherwise `mixed`.

## 6. Episodes (topic segments)

Episodes give claims their context (v0.1 used labels like "Review: Alireza, DevOps"), and they are the preferred chunk boundaries.

| Type | Meaning |
|---|---|
| `intro`, `outro`, `promo` | Framing, announcements, workshop ads |
| `qa` | A host question and the guest's answer |
| `cv-review` | One CV reviewed on air |
| `audience-q` | A viewer question read aloud and its answer |
| `other` | Anything else |

**Proposal.** Interviews: every host turn containing a question opens a `qa` episode. Live reviews: cue phrases (`رزومه بعدی`, `بریم سراغ`, `بریم بعدی`, `رزومه اول`) plus Claude reading a compact turn list (turn ID, timestamp if any, and first 15 words of each turn) to propose boundaries and labels. The owner confirms before `--apply`.

```yaml
# corpus/S001/episodes.yaml
- id: S001.e03
  type: cv-review
  label: "CV#01 DevOps, 6 yrs"      # pseudonymized; safe to use outside the repo
  cv_owner: Alireza                  # private; never leaves the repo
  from: S001.t0003.s001
  to: S001.t0007.s019
  verdict: reject                    # invite | borderline | reject | none, as the reviewer said
  verdict_reasons: [RED-1, SKL-6]    # optional; filled during extraction
```

`verdict` and `verdict_reasons` turn S001 into labeled data: which rule violations actually led to a reject or an invite on air. S001 includes the owner's own CV (`CV#10 Android, 8 yrs (owner)`, the tenth CV on air); spec 03 uses it as an eval case.

## 7. IDs and stability (ADR 0002)

- Turn: `S001.t0042` (4 digits). Sentence: `S001.t0042.s003` (3 digits; a 10-minute monologue turn can exceed 99 sentences). Episode: `S001.e05`. Chunk: `S001.c003`.
- IDs are a pure function of `transcript.raw.json` and the segmentation settings. Re-running Phase 1 on the same input must give identical IDs (tested).
- Replacing a source's transcript file (a new NotebookLM export) bumps `transcript_version`. Claims are then re-anchored with the section 10 tool, which is why every claim stores its quote as well as the sentence ID.

## 8. `transcript.json` schema

```json
{
  "schema": "rrs.transcript/1",
  "source_id": "S001",
  "transcript_version": 1,
  "id_scheme": 1,
  "timing": "none",
  "roles": {"JA": "guest", "H01": "host"},
  "turns": [
    {"id": "S001.t0003", "person": "JA", "role": "guest", "start": null,
     "sentences": [
       {"id": "S001.t0003.s041", "episode": "S001.e03", "lang": "fa",
        "start": null,
        "text": "...", "norm": "...", "norm_compact": "...",
        "terms": [{"c": "DevOps", "v": "دواب"}, {"c": "AWS", "v": "ایبلیوس"}, {"c": "GCP", "v": "جی سی پی"}]}
     ]}
  ]
}
```

Start times are float seconds, null when the source has `timing: none`. Validate with a JSON Schema in `src/rrs/schemas/`. Episodes stay in `episodes.yaml` (hand-confirmed) and are referenced by ID.

## 9. Render, index and search

**Render** `corpus/S001/transcript.md`: a metadata header (title, URL, upload date, duration, people and roles, transcript file, transcript version), one heading per episode, then one block per sentence. `[HH:MM:SS]` appears only when the source has timing (the S003 example):

```markdown
## S001.e03 · CV#01 DevOps, 6 yrs
**JA** `S001.t0003.s041`
<div dir="rtl">دواب که ایبلیوس یا جی سی پی بلد نباشه این رزومه ریجکته به نظر من</div>

## S003.e12 · Photos and personal data [00:24:50]
**TW** [00:24:50] `S003.t0061.s004`
So logos of anything pictures of any kind is a is a is always going to be a straight no
```

Persian and mixed sentences are wrapped with `dir="rtl"` so GitHub renders them right to left. Host sentences are rendered in italics.

**Index** `corpus/index.jsonl`: one line per sentence across all sources with `id, source, person, role, episode, start, lang, norm, norm_compact, terms`.

**Search** `rrs search "<query>" [--source S001] [--person JA] [--role guest] [--term AWS] [--lang fa]`: Persian queries are normalized to `norm_compact` and matched as substrings; English queries match `norm` tokens. Output: sentence ID, `HH:MM:SS` when known, person, and the `text` snippet. Extraction and validation both use it.

## 10. Re-anchoring claims after a transcript changes

A new NotebookLM export of a source (section 7) changes its sentence IDs. `rrs reanchor [Sxxx]` maps every claim of that source to the new IDs from the quotes the claims store:

1. For each anchor's quote, compute `norm_compact` (or `norm` for English) and search the source's new transcript, restricted to sentences spoken by that claim's recruiter, over windows of 1 to 3 consecutive sentences (quotes can cross a sentence boundary).
2. Narrow the search with context: within 120 s of the anchor's old `t_start` when the source has timing, otherwise the claim's episode; fall back to the whole source when the narrowed search finds nothing.
3. Exact match: accept. Otherwise fuzzy match with `rapidfuzz.fuzz.partial_ratio` on `norm`: 90 or above is accepted, 75 to 89 goes to review with the top three candidates, below 75 is manual.
4. Accepted anchors become `{sentence_id, quote, t_start}` where `quote` is the verbatim `text` of the shortest matching span and `t_start` the sentence start (null without timing). A claim's anchors are replaced only when all of them are accepted or decided.
5. Write `ledger/migration/reanchor-report.md` with counts per status and per source, and tables for the review and manual items. The owner's decisions go in `ledger/migration/reanchor-decisions.yaml` (`claim`, `anchor`, `sentence_id`, optional `quote_text`) and are applied on the next run.

The v0.1 claims are not migrated (00 section 2), so this tool first runs when a transcript is replaced.

## 11. Chunks for extraction sessions

Chunks are what Claude reads during extraction (spec 02 section 7). They keep each step inside the session's context and output limits; v0.1 hit the output limit when it wrote large files in one go.

- **Format** `chunks/S001/c003.md`: a header (source, title, people with roles and codes, sentence range, episodes covered with labels), then one line per sentence: `S001.t0003.s041 JA(guest): <text>`, prefixed with `[00:12:31]` when the source has timing. Host lines are kept for context with the prefix `HOST`.
- **Budget:** at most 12,000 characters when Persian dominates and 24,000 when English dominates (Persian script costs more tokens per character). Both are settings in `rrs.toml`.
- **Boundaries:** end at an episode boundary when possible; otherwise at a turn boundary; never inside a sentence. Repeat the last host question (up to 2 sentences) at the top of the next chunk as context.
- **Manifest** `chunks/S001/manifest.json`: per chunk the ID, first and last sentence, characters, sentences, episodes, and status (`pending`, `extracted`, `reviewed`, `merged`), plus the staging file and the merge commit.
- Chunks regenerate identically from the same transcript. If the transcript version changes, rebuild the manifest and carry progress over by sentence IDs.

## 12. Tests

- Import: the four v0.1 transcripts parse (S001 with labels on their own line, S002 without a `Source:` line, S003 with `[mm:ss]` prefixes); mapping and overrides applied; an unmapped label fails.
- Normalizer: each rule in 3.1; `می‌خوام`, `میخوام` and `می خوام` give the same `norm_compact`; Yeh and Kaf unification; `۱۰` becomes `10`; bidi marks removed.
- Terms: `ایبلیوس` annotated as AWS; `اسکیل` annotated as ambiguous; Latin `AWS` matched as a token, not inside `laws`.
- Segmentation: punctuation split, 40-word guard, fragment merge, unpunctuated windows, turn start inherited, language tags.
- IDs: two runs give identical output (byte-for-byte JSON).
- Render: snapshot test on a small fixture with Persian and English turns.
- Search: ten known quotes are found.
- Re-anchoring: a synthetic quote with perturbed wording maps correctly.
- Chunks: budget respected, no split sentences, deterministic output.

## 13. Acceptance criteria

- [x] S001 to S004 each have a source YAML (people and roles, confirmed speaker mapping; URL and metadata when known) and an imported `transcript.raw.json`.
- [x] `transcript.json` for S001 to S004: every sentence has an ID, `norm`, `norm_compact`, terms and an episode, and a start time when the source has timing.
- [x] `episodes.yaml` confirmed by the owner for S001 (CV reviews with pseudonymized labels and verdicts) and reviewed for S002 to S004.
- [x] Renders, index and chunks generated; `rrs search` finds Persian and English quotes.
- [x] `rrs reanchor` implemented and tested (no claims to re-anchor yet).
- [x] ADR 0002 written; tests and lint pass.

## 14. Kickoff prompt (Session 1)

```text
Read CLAUDE.md, docs/progress.md, docs/specs/00-overview.md and docs/specs/01-normalize-and-segment.md.
Implement Phase 1 for S001 to S004. Start with section 1: write the source YAMLs, propose speaker mappings with sample turns and wait for my confirmation.
Then build the normalizer and term annotation test-first from section 12.
Propose the S001 episode boundaries, labels and verdicts from a compact turn list and wait for my
confirmation before applying them. Implement the re-anchoring tool in section 10. Write ADR 0002. Small commits; progress entry at the end.
```
