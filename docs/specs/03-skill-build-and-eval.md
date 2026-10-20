# 03. Phase 3: build, evaluate and release the skill

**Goal:** generate `skill/SKILL.md` from the ledger, prove with evals that it finds what the evidence says it should (and nothing it shouldn't), and release it to Claude Code and claude.ai.
**Runs:** anywhere.
**Sessions:** 0 sets up CI (section 9); 3 does the rest. Read `00-overview.md` first.

## 1. Inputs and outputs

| Input | Output |
|---|---|
| `ledger/claims.jsonl`, `rules.yaml`, `recruiters.yaml`, `targets.yaml` | `skill/SKILL.md` (hand-written parts plus two generated blocks) |
| | `skill/CHANGELOG.md` |
| Owner's CV as reviewed in S001 | `evals/cases/*`, `evals/expected/*.yaml`, `evals/results/<version>/*` |
| | `.claude/skills/resume-reviewer/SKILL.md` (installed copy for evals) |
| | `reports/tally.json` (rewritten at release), git tag |

CLI: `rrs skill build [--check]`, `rrs skill lint`, `rrs skill install [--global]`, `rrs eval grade <results-dir>`.

## 2. SKILL.md structure (normative)

The claude.ai skill card saves only SKILL.md and replaces the whole file, so SKILL.md must be self-contained: no instruction may depend on a file that won't be there. Keep it under about 500 lines.

| # | Part | Source |
|---|---|---|
| 1 | Frontmatter: `name: resume-reviewer`, one-sentence `description` (under 200 characters; 1024 is the hard limit) | hand-written |
| 2 | Title and purpose (goal: interview invitations) | hand-written |
| 3 | Ground rules: evidence only, never invent experience or numbers, state evidence strength, fix in severity order, no em-dashes | hand-written |
| 4 | Evidence base: recruiter table, default target, totals and evidence version | generated, `<!-- EVIDENCE:START -->` to `<!-- EVIDENCE:END -->` |
| 5 | Review procedure (8 steps, as in v0.1) | hand-written |
| 6 | Report format (fenced template) | hand-written |
| 7 | Rules by evidence strength: one table per tier | generated, `<!-- RULES:START -->` to `<!-- RULES:END -->` |
| 8 | Contested guidance: one row per contested rule | hand-written, checked by lint |
| 9 | Coverage gaps | hand-written |
| 10 | Updating: how maintainers add a transcript (points to the repo) | hand-written |

The v0.1 SKILL.md is not carried over (00 section 2): write parts 1 to 3 and 5 to 10 fresh, following this table, with the review procedure, report format and weighting in section 5.

## 3. Generated blocks

**EVIDENCE** (from `recruiters.yaml` and `targets.yaml`): a table `Code | Recruiter | Type and market | Weight for the default target`, then the default target sentence, then one line of totals, for example `Evidence v1.0: 4 sources, 4 recruiters, 194 claims, 84 rules (28 Consensus, 26 Supported, 6 Contested, 24 Single source).`

**RULES** (from the tally, spec 02 section 8): sections Consensus, Supported, Contested, Single source; columns `ID | Rule and check | Evidence | Base severity | Sources`, where the rule cell is `<text> *Check:* <check>`, evidence reads `Consensus 4 (4F/0P, 4 report rejecting)` (measure rules add the distribution of recruiters' values, ADR 0003, and the reviewer compares the CV with the common range), and sources list claim IDs (`for: ...; against: ...; notes: ...` for contested rules and qualifiers). The Single source section has one table per recruiter, headed with their name and role (owner decision, 2026-10-20). X- rules and retired rules are excluded. This is the v0.1 `build.py` output format.

## 4. Build and lint

`rrs skill build` regenerates both blocks in place and prints every rule whose label or severity changed, as v0.1 did:
`CHANGED SKL-6: Single source 1 [Medium] -> Supported 2 [High]`. With `--check` it changes nothing and exits non-zero if the file would change (used in CI).

`rrs skill lint` fails on:
- any em-dash (U+2014) or en-dash (U+2013) in SKILL.md
- invalid frontmatter, a wrong `name`, or a description over 1024 characters (warn over 200)
- a rule ID or claim ID in the hand-written parts that does not exist or is retired
- a contested rule without a row in Contested guidance, or a row for a rule that is no longer contested
- any `cv_owner` name from an `episodes.yaml` appearing anywhere in SKILL.md
- table rows whose column count differs from their header
- more than 500 lines (warning)

## 5. Weighting at review time (normative; keep in the procedure)

Base severity comes from the tally. The reviewer then adjusts for the target:
- Lower one level (not below Low) when every supporter is a low match for the target, or when supporters gave only preferences (P) and the target's context differs from theirs.
- Raise a Single source rule one level (at most High) when its recruiter is a high match and the situation is the one they described.
- Contested rules are judgment calls: present both sides and recommend one using Contested guidance.

Match levels come from `targets.yaml` and appear in the EVIDENCE table. Optional later: a weighted support score per rule (high 1.0, medium-high 0.75, medium 0.5, low-medium 0.35, low 0.25), shown next to the label.

## 6. Maintaining contested guidance and coverage gaps

- When a change report shows a rule becoming contested, add a row: who is for (and their positions), who is against, and a recommendation for the default target. When it stops being contested, delete the row. Lint enforces both.
- When a new source fills a gap (the first DACH recruiter, the first mobile specialist), rewrite that bullet in Coverage gaps and say how many recruiters now cover it.
- Never resolve a contest by deleting claims. Disagreement is data.

## 7. Evaluation

Claude Code loads project skills from `.claude/skills/`, so `rrs skill install` (without `--global`) copies the built SKILL.md there for evals.

### Cases

Rule IDs in the expectations below come from the v0.1 index. The new index (02 section 11) is built from scratch, so restate each expectation with the matching new rule ID when the case files are written.

| Case file | What it is | Expected |
|---|---|---|
| `owner-cv-s001.md` | The owner's CV in the version reviewed live in S001 (`CV#10 Android, 8 yrs (owner)`); the reviewer invited it in about 90 seconds. If that version is gone, use the current CV and keep only the expectations that still apply | Verdict Invite; Low findings RED-8 (a double dash read as AI) and STR-8 (Medium linked twice); CHN-2 for the YouTube link is optional, since an active Android channel can count as relevant; no Critical or High |
| `synthetic-devops-no-cloud.md` + `.jd.md` | 6-year DevOps CV without AWS, GCP or Azure, with an IELTS score, references section and one page | RED-1 Critical, REG-8 Low, STR-12 Low, STR-1 as a judgment call |
| `synthetic-backend-no-ai.md` | 10-year backend CV with duty bullets, no numbers, no AI and no testing tools | SKL-2 Critical; ACH-1, ACH-2, ACH-5 High; SKL-6 Medium or higher |
| `synthetic-region-flags.md` | Photo, "English: Intermediate", skill ratings, 10 years on one page, no phone, a "requires visa sponsorship" line | RED-5 High, RED-7 Medium with the DACH caveat mentioned, SKL-7 Low, STR-9 High, REG-6 Low, STR-1 judgment |
| `synthetic-strong.md` | Two-page senior Android CV with context lines, real metrics, an AI-assisted outcome and testing tools | No Critical or High findings (false-positive check) |

Write synthetic CVs with invented people and companies only.

### Expected results

```yaml
# evals/expected/synthetic-backend-no-ai.yaml
verdict: borderline            # invite | borderline | reject
must_flag:
  - {rule: SKL-2, min_severity: Critical}
  - {rule: ACH-2, min_severity: High}
must_not_flag: [RED-7]
must_include: [ten_second_verdict, evidence_labels]
```

### Running

For each case, start a subagent with the skill installed and the prompt "Review this CV for <target>" plus the case files; save the report to `evals/results/<version>/<case>.md`. Run a baseline subagent with the skill disabled and save `<case>.baseline.md`. Subagents must not see the expected files.

### Grading

`rrs eval grade evals/results/<version>` parses the report: rule IDs in bold under severity headings, the verdict line, the presence of the 10-second verdict and evidence labels. It also checks that every number in the Rewrites section either appears in the CV or is a bracketed placeholder, since inventing numbers is a RED-2 violation. Output: `grades.md` with recall of `must_flag`, hits on `must_not_flag`, severity accuracy, verdict match, format checks, and the same metrics for the baseline. The owner then reads the rewrites for quality.

**Gate for release:** every `must_flag` found at or above its minimum severity, zero `must_not_flag` hits, verdict right in at least 4 of 5 cases, and the skill clearly ahead of the baseline on recall and format.

## 8. Release

- **Version** (evidence and skill together): MAJOR when counting rules or schemas change, MINOR for new sources, claims or rules, PATCH for wording fixes that change no label. The v0.1 work becomes `v1.0.0` once Sessions 0 to 3 pass.
- **Steps:** tests, lints and evals green, then `rrs ledger tally --report`, then a `skill/CHANGELOG.md` entry (the change report plus a two-line summary), then rewrite `reports/tally.json`, then commit and `git tag vX.Y.Z`.
- **Install in Claude Code:** `rrs skill install --global` copies SKILL.md to `~/.claude/skills/resume-reviewer/SKILL.md`.
- **Install on claude.ai:** in a chat, ask Claude to propose the skill as an update to `resume-reviewer`, giving it the full SKILL.md; the card replaces the whole file.
- **Project mirror:** replace `claude/claims-ledger.md` and `claude/SKILL.md` in the "Resume Review Skills" project with the new `ledger/claims-ledger.md` and `skill/SKILL.md`.

## 9. CI (set up in Session 1)

GitHub Actions on push and pull request, `ubuntu-latest`:
1. `astral-sh/setup-uv`, then `uv sync`
2. `uv run ruff check .` and `uv run pytest`
3. `uv run rrs ledger validate`
4. `uv run rrs skill build --check` and `uv run rrs skill lint`

Optional pre-commit hook: ruff, the em-dash check and `rrs skill build --check`.

## 10. Acceptance criteria

- [ ] SKILL.md contains both generated blocks; `rrs skill build --check` and `rrs skill lint` pass.
- [ ] Five eval cases with expected files; results, baseline and grades saved for the release; gate met.
- [ ] CHANGELOG entry, `reports/tally.json` snapshot and tag `v1.0.0`.
- [ ] Installed in Claude Code, proposed on claude.ai, project mirror updated.

## 11. Kickoff prompt (Session 3)

```text
Read CLAUDE.md, docs/progress.md, docs/specs/00-overview.md and docs/specs/03-skill-build-and-eval.md.
Write skill/SKILL.md (section 2) with EVIDENCE and RULES markers, implement `rrs skill build`,
`lint` and `install`, and get both checks green. Then create the eval cases in section 7 (ask me for my
CV text for owner-cv-s001), run one subagent per case with the skill and one baseline without it,
grade them, and show me the grades and the rewrites before we decide to release v1.0.0.
Small commits; progress entry at the end.
```
