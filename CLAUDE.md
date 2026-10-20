# resume-reviewer

Turns hand-made NotebookLM transcripts of recruiter interviews into a corpus, an evidence ledger
of atomic claims, and the `resume-reviewer` skill. Specs: docs/specs/ (start with 00).

## Rules for every session
- Read docs/progress.md and the spec for the phase you are working on before changing code.
- Never hand-edit generated files: corpus/*/transcript*.json, corpus/*/transcript.md,
  corpus/index.jsonl, chunks/*, ledger/claims-ledger.md, ledger/migration/reanchor-report.md,
  reports/*, and the blocks between markers in skill/SKILL.md. Change the inputs and rerun the
  generator.
- Transcripts are verbatim. Never edit files in transcripts/ or a sentence's `text`; corrections
  go through glossary/terms.yaml or a source's `corrections` list and are logged.
- Every claim needs an anchor that passes `rrs ledger validate`.
- Counting rules (docs/specs/02 section 8) change only through an ADR in docs/decisions/.
- Segmentation settings in rrs.toml change sentence IDs (ADR 0002): changing them needs an ADR
  and a re-anchoring run.
- Keep outputs small: process one chunk at a time, append to JSONL, commit often.
- No em-dashes or en-dashes in generated prose, templates or the skill.
- CV owners from live reviews are private people: pseudonyms only outside the repo.

## Commands
- `uv run pytest` and `uv run ruff check .` before every commit
- `uv run rrs <import|segment|normalize|episodes|render|index|search|chunks|reanchor|build-corpus> ...`
- `uv run rrs chunks next [Sxxx]`, `uv run rrs ledger validate|review|merge|rules|tally|render|agree`;
  extraction follows ledger/EXTRACTION_GUIDE.md (chunk statuses change only through these commands)
- `uv run rrs skill build|lint` (Phase 3)
- Helpers: `scripts/draft_claims.py` (drafts from a compact spec), `scripts/merge_chunk.sh Sxxx cNNN`
  (accept, validate, approve, merge, commit), `scripts/fill_amend_tstart.py` (amendment anchors)

## End of session
Tests green, commit, and add a dated entry to docs/progress.md: what changed, what is next,
open questions for the owner.
