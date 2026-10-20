# 0001. Counting rules, labels and base severity
Date: 2026-10-19. Status: accepted

## Context
The skill ranks rules by how many distinct recruiters agree with them. The v0.1 session used a
counting algorithm that every label depends on; changing it silently would make labels
incomparable across versions (00 section 3, D7). Spec 02 section 8 states the algorithm; this
ADR records it as the normative version, implemented in `src/rrs/ledger/tally.py`.

## Options considered
1. Count claims per rule. Rejected: a talkative recruiter would outweigh three quiet ones.
2. Count distinct recruiters per rule and stance (v0.1). Chosen.
3. Weight recruiters by match with the target. Deferred: applied at review time instead
   (spec 03 section 5), so the tally stays target-independent.

## Decision
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

Qualifying claims (`~`) are listed with the rule but never counted. `count_independent_hosts`
in `rrs.toml` defaults to false. Evidence cells read `Consensus 4 (4F/0P, 4 report rejecting)`.

## Consequences (including what must be re-run)
- Any change to this algorithm needs a new ADR that supersedes this one, then
  `rrs ledger tally --report`, `rrs ledger render` and `rrs skill build`, and a change report
  in the PR.
- Flipping `count_independent_hosts` changes labels in the same way and needs the same re-runs.
