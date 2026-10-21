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

## License

Code, skill, specs and synthetic evals: MIT (see `LICENSE`). Transcripts and quoted speech are
not covered; see `NOTICE`.
