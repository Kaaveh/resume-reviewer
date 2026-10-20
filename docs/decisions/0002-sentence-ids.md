# 0002. Sentence ID scheme and segmentation rules
Date: 2026-10-19. Status: accepted

## Context
Claims anchor to sentences (00 decision D6), so sentence IDs must be stable and reproducible.
v0.1 anchored by quote only, and most anchors could not be checked by script. Three of the four
NotebookLM transcripts are effectively unpunctuated (S001: 42 sentence marks in 25,000 words;
S003: 5; S004: 1), and S002 mostly has one period at the end of each turn.

## Options considered
1. Number sentences across the whole source (`S001.s0042`): simple, but inserting or fixing one
   turn renumbers everything after it.
2. Number per turn (`S001.t0042.s003`): a change in one turn only renumbers that turn.
3. Content hashes: stable under edits elsewhere, but unreadable and they change on any fix.

## Decision
Option 2, as in spec 01 section 7.
- Turn `S001.t0042` (4 digits, the turn's position in the transcript file, starting at 1);
  sentence `S001.t0042.s003` (3 digits, position in the turn); episode `S001.e05`; chunk
  `S001.c003`. `id_scheme: 1` in transcript.json.
- IDs are a pure function of transcript.raw.json and the `[segment]` settings in rrs.toml.
  Source `corrections` are applied after segmentation, so adding a correction never moves a
  boundary. Glossary changes only touch `norm`, `norm_compact` and `terms`.
- Segmentation per turn: split at sentence-final punctuation (pysbd for English, a rule-based
  splitter for Persian and mixed text that keeps `7.5` and `۷.۵` whole). A turn is
  **unpunctuated** when it has more than 25 words and its punctuation pieces average more than
  40 words (`unpunctuated_avg_words`); its pieces are then cut into 25-word windows. Otherwise
  the 40-word guard splits at the comma nearest the middle, and pieces over 60 words with no
  comma are split at the middle word. Fragments under 3 words merge into the previous sentence
  of the same turn (a short first sentence merges into the next).
- The density rule is our reading of 01 section 5 item 4, which does not say how to tell an
  unpunctuated turn. It treats a turn with only a final period (common in S002) as unpunctuated.

## Consequences (including what must be re-run)
- Changing any `[segment]` setting, the splitters, or the transcript file changes IDs: bump
  `transcript_version` (for a new transcript), re-run `rrs build-corpus`, then `rrs reanchor`
  so every claim's quote is mapped to the new IDs. Claims keep their quotes for this reason.
- Quotes regularly cross the 25-word windows. The validator and `rrs reanchor` accept spans of
  up to 3 consecutive sentences, and `rrs search` matches across 2 sentences of one turn.
- `tests/test_ids.py` checks that two runs give byte-identical JSON and that the committed
  corpus matches a rebuild.
