# 0003. Rules are statistical facts; quantities are measured
Date: 2026-10-19. Status: accepted (owner decision in Session 2)

## Context
The project's foundation is statistics collected from several recruiters: a rule is worth what
the number of distinct recruiters who state it says it is worth (00 section 1). Two things in the
S004 drafts broke that:
- A rule was worded from what earlier, not yet extracted sources were remembered to say (NEW-8
  "about two pages", worded for SB and TW while only JB's claims existed, and JB contradicting it).
- Claims were mapped to rules they only supported indirectly ("the ATS was never relied on"
  counted as support for "write for a human"), which inflates a rule's count with recruiters who
  never stated it.
Quantities make it worse: "two pages", "two to five pages" and "one page" turned into yes/no
rules with arbitrary thresholds hide the distribution that the recruiters actually gave.

## Options considered
1. Keep binary rules for quantities and let disagreement show as Contested. Rejected: the
   threshold in the rule text is itself an unmeasured choice, and a recruiter giving "two to five"
   is neither for nor against "about two".
2. Measure rules: the rule names the quantity, each claim states a value, the tally reports the
   distribution. Chosen.

## Decision
- **Rules are statistical facts.** A rule is worded only from claims in hand, never from
  sources not yet extracted. A claim maps to a rule only when the recruiter states that rule; a
  claim that only supports a rule's premise gets a rule of its own (or no claim). Later sources
  that disagree map with stance `-`, as before.
- **Measure rules** (`measure: {unit, question}` in `rules.yaml`) record quantities: CV length in
  pages, first-pass time in seconds. A claim on a measure maps to that rule only, has stance `+`
  and a `value: {min, max, condition}` (a point is `min == max`; a missing bound is open).
- **Counting** (extends ADR 0001; binary rules are unchanged):
  - Each recruiter's range is the intersection of their unconditional values on the rule (all
    their values when every one has a `condition`), or the hull of them when they conflict.
    Conditional values ("junior: 1 page") are listed beside the range, not intersected with it.
  - Supporters are the recruiters with a counted value, so the label is `Consensus n`,
    `Supported 2` or `Single source 1`, and severity follows ADR 0001.
  - When two or more recruiters' ranges have no common overlap, the label is
    `Contested range n` and the severity `Judgment`.
  - The evidence cell appends the distribution:
    `Supported 2 (0F/2P, 0 report rejecting); JB 2 to 5 pages, SB 2 pages; common 2 pages`.
  - The tally also reports medians of the lower and upper bounds.

## Consequences (including what must be re-run)
- Spec 02 sections 4 to 8 and the extraction guide describe measures; spec 03 shows the
  distribution in the RULES block.
- S004 drafts: NEW-8 becomes the length measure, NEW-9 folds into it, the first-pass time
  becomes a measure, and the two indirect mappings get rules of their own.
- Changing how ranges combine changes labels: it needs a new ADR, `rrs ledger tally --report`,
  `rrs ledger render` and `rrs skill build`.
