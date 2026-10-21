# resume-reviewer

Turns hand-made NotebookLM transcripts of public recruiter and hiring-manager interviews into a corpus, a ledger of atomic claims about how CVs are screened, and the `resume-reviewer` skill built from them.

Start with [docs/specs/00-overview.md](docs/specs/00-overview.md) and [docs/progress.md](docs/progress.md).

- `docs/specs/`: overview (00) and phase specs 01 to 03; `docs/decisions/`: ADRs
- `transcripts/`: NotebookLM transcripts, one per source, read-only
- `sources/`: one YAML per source (metadata, speaker mapping, corrections)
- `glossary/`: tech terms and the people registry
- `corpus/`: canonical transcripts, renders and the sentence index (generated)
- `chunks/`: extraction inputs for Claude Code sessions (generated)
- `ledger/`: claims, rules, recruiter profiles; `ledger/claims-ledger.md` is the readable version
- `skill/SKILL.md`: the `resume-reviewer` skill (copy it to `~/.claude/skills/resume-reviewer/`)
- `evals/`: synthetic eval cases, expected results and graded runs
- `src/rrs/`: the `rrs` CLI (`uv run rrs --help`)

```sh
uv sync
uv run rrs build-corpus          # import, segment, normalize, episodes, render, index, chunks
uv run rrs search "two pages"    # English: phrase match; Persian: compact substring match
uv run pytest && uv run ruff check .
```

## Sources and attribution

The evidence comes from four public video interviews. The words are the speakers'; the
transcripts here are machine-made (NotebookLM) and kept verbatim so every claim can be traced to
a sentence. They are included for research and to make the ledger checkable, not as a
replacement for the original videos. If you are one of the speakers and want a transcript
removed or credited differently, please open an issue.

| Source | Interview | Guest | Host |
|---|---|---|---|
| S001 | "کدوم رزومه انتخاب می‌شه؟ \| بررسی واقعی رزومه‌ها با جان ادیب" (live CV reviews, Persian and English) | John Adib, Engineering Manager | Sahar |
| S002 | "How to get hired by a UK startup?" | Sam Baldwin, JavaScript and TypeScript recruiter | John Adib |
| S003 | "How Recruiters Really Screen Your Resume and How to Stand Out?" | Tomasz Wojtyczko, Principal Recruitment Consultant, VirtueTech | John Adib |
| S004 | "Can you still get hired in tech?" | Joe Bignell, former recruiter, now at Vention | John Adib |

Video links are added to `sources/*.yaml` (`url`) as they are confirmed. CV owners in the live
reviews (S001) are referred to by episode labels such as CV#05 in the ledger and the skill.

## NotebookLM transcript prompt

This is the prompt given to NotebookLM, together with the YouTube interview as a source, to
produce each file in `transcripts/`. Reuse it for new sources: replace `[VIDEO TITLE]` and
`[YOUTUBE URL]`, then save the output as a `.md` file in `transcripts/`.

```text
Produce a complete VERBATIM transcript of the entire YouTube source "[VIDEO TITLE]", from the first word to the last, and save it as a standalone Markdown (.md) file.

The file must start with:
# [VIDEO TITLE]
Source: [YOUTUBE URL]
---
After that, only the transcript. No commentary, notes, or summary.

Transcription rules:
1. Transcribe every word exactly as spoken. Do NOT summarize, paraphrase, condense, reorder, or skip anything.
2. Keep filler words, false starts, repetitions, and self-corrections as they appear.
3. Do not fix grammar or word choice. Write what was said, not what was meant.
4. Separate speakers with generic labels: **Interviewer:** and **Guest:** (use **Guest 2:** etc. if there are more). Start a new paragraph whenever the speaker changes. If unsure, use **Speaker:**.
5. Add a [mm:ss] timestamp at the start of each speaker turn when possible.
6. Mark unclear parts as [inaudible] and overlapping speech as [crosstalk].
```

## License

Code, skill, specs and synthetic evals: MIT (see `LICENSE`). Transcripts and quoted speech are
not covered; see `NOTICE`.
