# CV review: Elena Vasquez-Moroz, Senior Android Engineer, Germany (relocating)

## Verdict: INVITE

This is a strong CV. It shows 8 years of steady progress from junior to senior. Almost every bullet has a measured result: crash-free sessions rose from 98.1% to 99.6%, sync failures fell 72%, production regressions dropped from 9 to 2 per quarter, and clean builds went from 11 to 6 minutes. The scope is clear (3M monthly users, a 6-person team), the stack is current (Compose, Coroutines/Flow, Room, WorkManager, Hilt), it covers testing, and there is an open-source project with real adoption. She has also worked remotely for a Berlin company since 2021, which is the best signal a German employer could ask for. The gaps are mostly about relocation logistics, plus a few places where she could say more about senior-level scope. None of them would stop a recruiter from calling her.

## Problems by severity

### High (fix before sending to German employers)
1. **Work authorisation is not stated.** She is a Serbian resident relocating, so the recruiter's first question is whether she needs a visa. Say it up front, for example: "Eligible for EU Blue Card; no relocation sponsorship beyond visa needed", or "Blue Card application in progress". Otherwise many recruiters will set the CV aside.
2. **No languages section.** German employers expect to see English and German levels (CEFR). Leaving them out makes readers assume no German and leaves English unclear. Add for example "English: C1 (daily working language since 2021); German: A2, learning".
3. **Relocation timeline and location are vague.** "Relocating to Germany" gives no date and no city. Add a target city or "open to Berlin, Munich, Hamburg, remote", plus an availability date or notice period.

### Medium
4. **The Berlin connection is undersold.** "Remote for a Berlin company" sits in parentheses. Two to three years working with a German team, across time zones and German business culture, belongs in the summary.
5. **Senior-level scope is underplayed.** The bullets show strong delivery, but there is little about architecture decisions, technical direction, or working with product, design and backend. Say who decided the sync architecture, whether she wrote RFCs, and whether she ran the Android hiring loop. German senior roles often probe for ownership and influence.
6. **Architecture and modularisation are missing from Skills.** There is nothing on MVVM/MVI, Clean Architecture, multi-module or convention plugins, even though the Kestrel bullet proves modular Gradle experience. KMP is missing too: it is common in 2026 job ads, so list it if she has used it.
7. **Degree recognition.** For a Blue Card, the Serbian BSc usually needs to be recognised (anabin "H+" or a ZAB statement). If she has the statement, say so, for example "recognised in Germany (anabin H+)".

### Low
8. **The Compose Charts project has no link** and doesn't say what's notable about it (downloads, Maven Central, contributors). Add the repo URL.
9. **Kestrel has only two bullets** for almost 3 years. Add one about the passenger app or a release/process improvement if she has one.
10. **The Tisa Digital bullet is generic.** That's fine for a junior role, but one concrete result would help. She could also shorten it.
11. **"Using AI tools to move faster" in the summary is vague.** The Claude Code migration bullet is the proof. Either drop the summary phrase or make it specific ("AI-assisted migrations with full code review").
12. **German CV conventions.** She has rightly left out the photo, date of birth and marital status, and none are needed. Add "Kotlin" and "Android" keywords near the title for ATS. Keep it to 1 to 2 pages, which it already is.

## Rewrites

**Header**
> Senior Android Engineer | Belgrade, Serbia; relocating to Berlin or Munich from [Month 2027] | EU Blue Card eligible | elena.vm@example.com | +381 64 555 0199 | linkedin.com/in/example-evm | github.com/example-evm

**Summary**
> Senior Android engineer with 8 years in Kotlin, the last 5 working remotely for a Berlin health-tech company. Led the Jetpack Compose migration and offline-first sync rewrite of a fitness app with 3M monthly users, raising crash-free sessions to 99.6% and cutting sync failures by 72%. Owns features from architecture to release, builds testing into CI, and mentors mid-level engineers. Relocating to Germany; English C1, German A2.

**Pulsefield, added bullet on scope (only if true)**
> - Defined the Android architecture (MVVM, multi-module, Hilt) for the rewrite, wrote the sync design doc, and agreed API contracts with the backend team.

**Pulsefield AI bullet (tighter)**
> - Migrated 180 legacy Java classes to Kotlin in four weeks using Claude Code and Copilot, with every change reviewed and covered by tests.

**Kestrel bullet**
> - Split the monolith into 14 Gradle modules with convention plugins, cutting clean build time from 11 to 6 minutes.

**Skills, added rows**
> **Architecture:** MVVM/MVI, Clean Architecture, multi-module Gradle, offline-first
> **Languages:** English C1, German A2 (in progress), Serbian native

**Education**
> BSc Software Engineering, University of Novi Sad, 2016 (recognised in Germany, anabin H+)

**Projects**
> **Compose Charts** (open source, 2023 to present): chart library for Jetpack Compose on Maven Central; 1.4k GitHub stars, 20+ contributors. github.com/example-evm/compose-charts

Placeholders in brackets, and numbers such as module or contributor counts, must be replaced with her real figures. Do not invent them.
