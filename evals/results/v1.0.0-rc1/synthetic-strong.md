# CV review: Senior Android Engineer for Germany (relocating from Serbia)

**Verdict:** Invite

**10-second verdict:** The top of page one shows "Senior Android Engineer", the current city with "relocating to Germany", a summary naming 8 years of Kotlin and Jetpack Compose, and a most recent role as "Senior Android Engineer, Pulsefield Health" (remote for a Berlin company) on a 3M-user app. Title, core stack, employer and recent relevant experience are all visible at a glance (SCR-1, SCR-2, SCR-6, SCR-7). A screener keeps reading.

**Target and weighting:** Senior Android Engineer, Germany, candidate relocating from outside the EU; from the request, and it matches the default target (`android-eu-relocation`), so the default match levels apply. Match: JA high, TW medium-high, JB medium-high, SB low-medium. No job description was given, so hard requirements were checked against a typical senior Android core stack (Kotlin, Jetpack Compose, Android Jetpack libraries, testing): all present, no RED-2 or RED-6 issue.

## Findings

### Medium
- **SKL-3** (Supported 2, Medium): several key technologies in the skills list are not tied to any role. "Hilt, Retrofit", "Coroutines, Flow", "MockK", "JUnit", "GitHub Actions" and "Firebase Crashlytics" appear only under Skills, so the reader cannot tell where they were used. Fix: name them inside the bullets where they mattered, or add a one-line stack under each recent role (accepted under SKL-2, see Judgment calls).
- **STR-17** (Single source 1, Medium; raised from Low because JA is the high match and the CV is in the situation described): the Pulsefield context paragraph uses the first person: "I joined the 6-person Android team". Fix: drop the pronoun, as in the rewrite below.

### Low
- **STR-22** (Single source 1, Low): JA wants bullets of at most one line. Some bullets are long enough to wrap, for example "Designed offline-first sync with Room and WorkManager, cutting sync failures by 72% and one-star reviews about sync by half." Fix: tighten to one line each. If they wrap to two lines in the rendered CV, treat this as Medium (JA is the high match).
- **RED-4** (Single source 1, Low): the summary's second sentence reads as generic: "Comfortable owning features from design to release, testing them well and using AI tools to move faster." Fix: replace the general claims with the concrete facts the CV already has (rewrite below).
- **REG-15** (Single source 1, Low): the CV does not state the right-to-work status for Germany. JB also advises against stating a need for sponsorship on the CV (REG-2, which the CV already follows). Fix: if the candidate already holds a German or EU work permit, say so in the header; if not, keep the current "relocating to Germany" line and do not add a sponsorship request.
- **CHN-15, CHN-17** (Consensus 3 and Supported 2; not CV checks, no severity): for a candidate abroad, referrals get the CV read more carefully, and a short note to the hiring manager saying why she fits helps. Recommend both alongside applications, especially to Berlin companies given the remote Berlin employer.

### Judgment calls
- **REG-17** (Contested 2-1): the phone number has a Serbian country code while the header says "relocating to Germany". For: SB and TW say screeners or client ATS systems notice a foreign number. Against: JA says screeners do not know dialling codes and location comes out on the first call. Recommendation: keep the real number with its country code (REG-3); use a German number only if the candidate actually has one. Never add a number she does not have (RED-3).
- **REG-16** (Contested 1-1): location may weigh in screening. For: TW says location filters screen out applicants from abroad. Against: JA says skill gaps, not location, cause rejections. Recommendation: the CV already does what the guidance asks: real city stated (REG-14) and relocation in one line (REG-5). No change.
- **STR-2** (Contested range 4): the CV runs to about one page for 8 years. JA (high match) prefers one page; TW and JB accept two. Recommendation: keep it at one page; it is not too dense to scan.
- **SKL-2** (Contested 1-1): roles have no stack line today. JB says name technologies within the work; JA says a one-line stack per role is good when there is space. Recommendation: a one-line stack per recent role is acceptable and also fixes SKL-3.

## Rewrites

**Pulsefield Health, company context**
- Before: "Pulsefield builds a subscription fitness app (3M monthly users, 40-person product team). I joined the 6-person Android team to fix slow sync and crash rates."
- After: "Pulsefield builds a subscription fitness app (3M monthly users, 40-person product team). Joined the 6-person Android team to fix slow sync and crash rates."

**Summary, second sentence**
- Before: "Comfortable owning features from design to release, testing them well and using AI tools to move faster."
- After: "Owns features from design to release, with screenshot and UI tests in CI (Paparazzi, Espresso) and AI-assisted migrations with Claude Code and Copilot."

**Pulsefield Health, sync bullet**
- Before: "Designed offline-first sync with Room and WorkManager, cutting sync failures by 72% and one-star reviews about sync by half."
- After: "Designed offline-first sync (Room, WorkManager): sync failures down 72%, sync-related one-star reviews halved."

**Stack line under each recent role (SKL-3)**
- Before: (none; "Hilt, Retrofit", "Coroutines, Flow", "MockK" appear only in Skills)
- After, Pulsefield: "Stack: Kotlin, Jetpack Compose, Room, WorkManager, Paparazzi, Espresso, [Hilt, Retrofit, Coroutines, Flow, MockK, GitHub Actions: keep only those used in this role]"
- After, Kestrel: "Stack: Kotlin, Gradle, [technologies used in this role]"

## What already works
- Each recent role states the problem, her contribution and the result (ACH-1), with concrete numbers that are not all round: "98.1% to 99.6%", "72%", "9 to 2 per quarter", "11 to 6 minutes" (ACH-6, ACH-8).
- The most recent role leads the experience in reverse date order and shows the target stack (SCR-2, SCR-7); the target fit is obvious on page one (SCR-3).
- Concrete, hands-on AI tool use in daily work: "Used Claude Code and Copilot to migrate 180 legacy Java classes to Kotlin in four weeks, reviewing every change" (SKL-4, SKL-7).
- Named testing tools and how they were used: "screenshot tests (Paparazzi) and UI tests (Espresso) in CI" (SKL-10).
- A relevant open source side project with dates, context and traction: "Compose Charts ... 1.4k GitHub stars" (ACH-4, STR-15).
- Real city stated with relocation intent, without a sponsorship request (REG-14, REG-5, REG-2); contact details with country code and a LinkedIn URL in the header (REG-3, CHN-5).
- Company context with domain, users and team size under recent roles (STR-7, ACH-2, ACH-7); ownership and teamwork shown ("Led", "Designed", "Mentored two mid-level engineers") (ACH-12, SEN-7).
- Clean structure: title first in role headings, months in dates, employer locations, grouped skills without proficiency labels, education after experience with university and degree, no photo, no references, no gaps (STR-14, STR-24, STR-19, SKL-8, SKL-17, STR-26, STR-27, REG-7, STR-12, GAP-2).

## Not covered by the evidence
- **German market conventions.** No recruiter in the evidence hires in Germany or DACH, so local conventions (photo, German CV format, expected German language level) are not covered. General advice: many German employers in tech accept English CVs without a photo, but check each employer's ad; if the candidate has any German, stating the real level is worth considering, presented as learning rather than a working skill (REG-10 context).
- **No job description.** ATS-1, SKL-11 and STR-6 (keyword match and tailoring) could not be checked. Tailor the title, summary and skill order to each ad's wording.
- **GitHub activity.** The CV links GitHub; whether the profile shows recent activity (CHN-6, CHN-9, CHN-14) cannot be judged from the CV. Check it before applying.
- **Visa route.** Visa options for Germany (for example an EU Blue Card) are out of scope for these rules; general advice only, and confirm with official sources.
- **Android specialism.** No recruiter in the evidence specializes in mobile; JA hires mobile engineers among others, so Android-specific expectations rest mainly on one hiring manager's view.
