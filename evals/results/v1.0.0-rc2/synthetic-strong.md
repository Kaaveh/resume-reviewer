# CV review: Senior Android Engineer for Germany (relocating from Serbia)

**Verdict:** Invite

**10-second verdict:** The top of page one shows the target title ("Senior Android Engineer"), the core stack in the first line of the summary ("Kotlin and Jetpack Compose"), a concrete scale ("a fitness app used by 3 million people") and a most recent role that is the same job at a Berlin company ("Senior Android Engineer, Pulsefield Health ... remote for a Berlin company"). A screener has enough relevant experience to keep reading (SCR-1, SCR-2, SCR-7) and can see the employer at once (SCR-6). On a 10-second first pass (SCR-4, JA's figure) this CV keeps the reader.

**Target and weighting:** Senior Android Engineer, about 8 to 10 years, applying to German (DACH) employers from outside the EU and relocating; from the request, and it matches the default target `android-eu-relocation`. Match: JA high, TW medium-high, JB medium-high, SB low-medium. No job description was given, so hard requirements were checked against a typical Senior Android stack (Kotlin, Jetpack Compose, coroutines, testing). DACH note: no recruiter in the evidence hires in DACH or mainland Europe, so German CV conventions may differ from the findings below.

## Findings

### Medium
- **RED-3** (Single source 1, Medium; base Low, raised one level because SB reports rejecting on it): the summary says "8 years building consumer apps", but the dates run from "Sep 2016" to "present", about 10 years. If the 8 counts from Kestrel (Jun 2018), a screener who checks the dates may still ask which number is right, and any figure the candidate cannot explain on a call is a risk. Fix: state the number the dates support, or say what it counts (for example "8 years since [Jun 2018], 10 including junior roles"). Ask the candidate which they mean; do not guess.
- **SKL-3** (Supported 2, Medium): several skills have no role or project behind them: "Hilt, Retrofit", "Coroutines, Flow", "MockK", "GitHub Actions", "Firebase Crashlytics". The Kestrel role names no language or libraries at all ("Rebuilt the driver app's location tracking with a foreground service"). Fix: name where each was used, either inside a bullet or with a one-line stack under each role (SKL-2 guidance accepts one line per role).
- **STR-17** (Single source 1, Medium; base Low, raised one level because JA is the high match and the CV is in the situation described): first person in the Pulsefield context line, "I joined the 6-person Android team to fix slow sync and crash rates." Fix: drop the pronoun (see Rewrites). DACH conventions may differ; no DACH recruiter is in the evidence.

### Low
- **REG-15** (Single source 1, Low; JB is medium-high, so not raised): the header says "relocating to Germany" but not the candidate's right-to-work status for Germany. Fix: if the candidate already holds a German or EU work permit, or has one approved, state it in plain words in the header. If not, leave the line as it is and do not write that sponsorship is needed (REG-2). DACH conventions may differ; no DACH recruiter is in the evidence.
- **STR-22** (Single source 1, Low; JA at most 1 line per bullet): several bullets are likely to wrap to two lines on a printed page, for example "Designed offline-first sync with Room and WorkManager, cutting sync failures by 72% and one-star reviews about sync by half." Not raised, because the line count depends on the final layout. Fix: check the PDF and trim any bullet that wraps.
- **ACH-3** (Single source 1, Low; SB is a low-medium match and gave a preference): bullets lead with the technology and end with the result, for example "Led the move from XML views to Jetpack Compose across 60 screens; crash-free sessions rose from 98.1% to 99.6%." A non-technical first screener (SCR-11) reads the result last. Fix: lead with the outcome on the two or three strongest bullets; the rest can stay as they are.

### Judgment calls
- **REG-17** (Contested 2-1): for: SB and TW say screeners or client ATS systems notice a foreign number (SB-39, TW-60); against: JA says screeners do not know dialling codes and location comes out on the first call (JA-104). The CV shows a "+381" number. Recommendation: keep the real number with its country code (REG-3); the header already states relocation (REG-5). Use a German number only if the candidate really has one.
- **REG-16** (Contested 1-1): for: TW says location filters screen out applicants from abroad (TW-59, TW-60); against: JA says skill gaps, not location, cause rejections (JA-40). Recommendation: the CV already does what the guidance asks: no skill gaps against the core stack, the real city stated (REG-14) and relocation in one line (REG-5). No change.
- **STR-2** (Contested range 4): the CV fits on about one page. JA (high match) prefers one page at this level; TW and JB accept two. Recommendation: keep it at one page or a light two; do not pad it.

## Rewrites

**Pulsefield context line (STR-17)**
- Before: "Pulsefield builds a subscription fitness app (3M monthly users, 40-person product team). I joined the 6-person Android team to fix slow sync and crash rates."
- After: "Pulsefield builds a subscription fitness app (3M monthly users, 40-person product team). Joined the 6-person Android team to fix slow sync and crash rates."

**Summary, years of experience (RED-3)**
- Before: "Android engineer with 8 years building consumer apps in Kotlin and Jetpack Compose"
- After: "Android engineer with [N] years building consumer apps in Kotlin and Jetpack Compose" (use the count the dates support, and the candidate's own figure)

**Kestrel role, stack line (SKL-3)**
- Before: "Kestrel runs a ride-hailing app in four Balkan countries (1.2M users)."
- After: "Kestrel runs a ride-hailing app in four Balkan countries (1.2M users). Stack: [Kotlin or Java], [libraries used, for example Coroutines, Hilt, Retrofit]."

**Pulsefield bullet, outcome first (ACH-3, STR-22)**
- Before: "Led the move from XML views to Jetpack Compose across 60 screens; crash-free sessions rose from 98.1% to 99.6%."
- After: "Raised crash-free sessions from 98.1% to 99.6% by leading the Compose migration of 60 screens."

**Pulsefield bullet (SKL-3)**
- Before: "Introduced screenshot tests (Paparazzi) and UI tests (Espresso) in CI; regressions reaching production fell from 9 to 2 per quarter."
- After: "Cut production regressions from 9 to 2 per quarter with Paparazzi screenshot tests and Espresso UI tests in [GitHub Actions] CI."

## What already works
- Every recent role says what was built, what the candidate did and what changed, with measured results (ACH-1, ACH-6): "98.1% to 99.6%", "cutting sync failures by 72%", "from 11 to 6 minutes". The percentages are not all round (ACH-8).
- The most recent role is the target role with the target stack, in reverse date order (SCR-2, SCR-7), and the strongest result opens the summary (ACH-10).
- Concrete AI tool use in daily work: "Used Claude Code and Copilot to migrate 180 legacy Java classes to Kotlin in four weeks, reviewing every change" (SKL-4, SKL-7).
- Named testing tools with what they achieved (SKL-10), and ownership plus teamwork: "Led", "Designed", "Mentored two mid-level engineers" (ACH-12, SEN-7).
- Scale and domain for each recent employer: "3M monthly users, 40-person product team", "ride-hailing app in four Balkan countries (1.2M users)" (ACH-2, ACH-7, STR-7).
- A relevant side project with visible traction: "Compose Charts (open source, 2023 to present) ... 1.4k GitHub stars" (ACH-4, STR-15).
- Plain one-column layout, grouped skills section with no proficiency labels, no photo, titles first in role headings, months on every date, education after experience (STR-3, SKL-8, SKL-17, REG-7, STR-14, STR-24, STR-26). On the photo, German CV conventions may differ; no DACH recruiter is in the evidence.
- Header gives city, relocation intent, email, phone with country code and LinkedIn, with no sponsorship request (REG-14, REG-5, REG-3, CHN-5, REG-2).
- No gaps or short stints (GAP-2, GAP-3), no em-dashes (RED-5), no typos found (RED-1).

## Beyond the CV
- **CHN-15** (Consensus 3): ask for referrals into German employers; a referral gets the CV a more careful read. Pulsefield is a Berlin company, so colleagues there are a natural starting point.
- **CHN-18** (Consensus 3) and **CHN-20** (Single source 1): keep LinkedIn complete (photo, full history, what was done at each job, bio) and make its dates and titles match the CV, including the years-of-experience figure.
- **CHN-16** (Supported 2) and **CHN-17** (Supported 2): network alongside applications, and send the hiring manager a short message on why the candidate fits.
- **CHN-6, CHN-9** (Supported 2) and **CHN-14** (Single source 1): GitHub is linked and hiring managers will open it. Make sure Compose Charts shows recent activity and a clear README; JA counts a profile as standing out from about 1000 contributions a year.

## Not covered by the evidence
- German language level: the CV has no languages section. The evidence does not say whether German employers expect one for English-speaking Android teams (general advice: if the candidate has any German, add it with an honest level; REG-10 notes a basic level shows learning but is not a working skill).
- German CV conventions (photo, personal details, Lebenslauf format): no DACH recruiter is in the evidence.
- Visa route (for example an EU Blue Card) and salary expectations for Germany: out of scope for the CV rules; general advice only.
- No job description was given, so keyword match (ATS-1, SKL-11) and hard requirements (ATS-3, RED-6) could not be checked. Rerun the review against each specific job ad.
