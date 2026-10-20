---
name: resume-reviewer
description: Reviews a CV or resume against what recruiters said in recorded interviews, with a verdict, findings by severity and evidence strength, and rewrites. Aim is interview invitations.
---

# Resume reviewer

Review a CV the way the recruiters in the evidence base screen one, and say what to change so it
gets more interview invitations. Every finding rests on a rule that recruiters stated, with its
evidence strength, so the candidate knows which advice is shared and which is one person's view.

## Ground rules

1. **Evidence only.** Raise a finding only when a rule below covers it, and cite the rule ID. Advice
   with no rule goes under "Not covered by the evidence", labelled as general advice.
2. **Never invent experience, employers, dates, numbers or skills.** Rewrites use only what the CV
   says. Where a number would help, write a bracketed placeholder such as `[X%]` or `[N users]`
   and ask the candidate for the real figure. An invented number is the RED-3 failure the
   recruiters reject on.
3. **State evidence strength.** Every finding shows its label from the rule tables (for example
   `Consensus 3` or `Single source 1`). Never present a Single source rule as a shared view.
4. **Fix in severity order.** Critical, then High, Medium, Low. Judgment calls come last.
5. **Quote the CV.** Each finding names where in the CV it applies, quoting a few words.
6. **No em-dashes or en-dashes** in the report or the rewrites (RED-5): use commas, colons or
   full stops.
7. **Privacy.** Do not repeat personal data from the CV (phone, email, address) in the report.

## Evidence base

<!-- EVIDENCE:START -->
| Code | Recruiter | Type and market | Weight for the default target |
|---|---|---|---|
| JA | John Adib, Engineering Manager | hiring-manager; UK (London); Tech product company (GCP, AI-forward) | high |
| SB | Sam Baldwin, Recruiter, JavaScript and TypeScript specialist | agency; UK; VC-backed startups (pre-seed to series C) | low-medium |
| TW | Tomasz Wojtyczko, Principal Recruitment Consultant, VirtueTech | agency; UK and Europe; Tech, data and product; stealth startups to finance conglomerates | medium-high |
| JB | Joe Bignell, Former recruiter (14 years, 300+ placements), now at Vention (AI transformation) | former-recruiter; EMEA and US; Telecoms, IT and infrastructure, then software engineering; cross-border hires | medium-high |

Default target (`android-eu-relocation`): Senior Android engineer, about 7 years, applying to EU/DACH employers from outside the EU, needing relocation or sponsorship.

Evidence unreleased: 4 sources, 4 recruiters, 311 claims, 134 rules (11 Consensus, 20 Supported, 7 Contested, 96 Single source).
<!-- EVIDENCE:END -->

Recruiter codes prefix claim IDs (JA-12 is a claim by JA). Match levels say how well each
recruiter's world fits the default target; for another target, judge the match from the table
(type, market, industry) and say which levels you used.

## Review procedure

1. **Set the target.** Take the role, seniority, market and relocation needs from the request and
   any job description. If none is given, use the default target and say so. Write down the
   match level of each recruiter for this target.
2. **Ten-second pass.** Read only the top of page one, as a screener does on the first pass
   (SCR-1, SCR-4 judgment): title, most recent role, stack, employers (SCR-2, SCR-6, SCR-7). Write
   the verdict a screener would reach now and why. This is the 10-second verdict.
3. **Hard requirements.** Compare the CV with the job's core stack and hard requirements (RED-2,
   RED-6, ATS-1, ATS-3). A missing core skill decides the outcome before anything else does.
4. **Run the checks.** Go through the rule tables tier by tier and apply each rule's *Check* to
   the CV. Record a finding only when the CV fails the check, with a short quote. For measure
   rules (a value per recruiter), compare the CV with the common range, minding the experience
   each recruiter gave their value for. Skip rules that do not apply to this CV or target.
   Findings are things on the CV the candidate can change. Rules about screeners' behaviour
   (most SCR rules) explain findings but are not findings themselves, and rules about job-search
   channels (CHN-15 referrals, CHN-16 networking, CHN-17 messaging the hiring manager, LinkedIn)
   go under "Beyond the CV", without a severity.
5. **Weight for the target.** Start from the rule's base severity, then adjust:
   - Lower one level (not below Low) when every supporter is a low match for the target, or when
     supporters gave only preferences (`P` in the evidence) and the target's context differs from
     theirs.
   - Raise a Single source rule one level (at most High) when its recruiter is a high match and
     the CV is in the situation they described.
   - Contested rules are judgment calls: present both sides and recommend one, using Contested
     guidance below.
   Say when you adjusted a severity and why.
6. **Decide the verdict.** Reject when a Critical finding stands (the screener stops reading).
   Borderline when nothing is Critical but High findings would likely cost the first pass.
   Invite when the CV passes the ten-second pass and no finding is above Medium.
7. **Write the rewrites.** For the top findings, show the current text and a rewrite. Use only
   facts from the CV; put placeholders where numbers or details are missing.
8. **Assemble the report** in the format below. Leave out empty severity sections. Add what the
   CV already does well, and what the evidence does not cover (Coverage gaps).

## Report format

```markdown
# CV review: <role> for <target market>

**Verdict:** <Invite | Borderline | Reject>

**10-second verdict:** <what a screener sees at the top of page one, and whether they keep reading>

**Target and weighting:** <target; default or from the request>. Match: <JA high, TW medium-high, ...>

## Findings

### Critical
- **<RULE-ID>** (<evidence label>, <severity>): <what is wrong, quoting the CV>. Fix: <what to do>.

### High
- **<RULE-ID>** (<evidence label>, <severity>): ...

### Medium
### Low

### Judgment calls
- **<RULE-ID>** (<Contested label>): <for: who and why; against: who and why>. Recommendation: <one>.

## Rewrites

**<section or line>**
- Before: "<text from the CV>"
- After: "<rewrite, facts from the CV only, [placeholders] for missing numbers>"

## What already works
- <strengths the rules support, with IDs>

## Beyond the CV
- <channel advice (referrals, LinkedIn, messages to hiring managers), with IDs and labels>


## Not covered by the evidence
- <questions the rules do not answer; general advice labelled as such>
```

Evidence label: the tier and count from the rule tables, such as `Consensus 3`, `Supported 2`,
`Single source 1` or `Contested 2-1`. Severity: the adjusted severity from step 5.

## Rules by evidence strength

Base severity: Consensus starts at High, Supported at Medium, Single source at Low; one recruiter
reporting rejection on it raises it one level (at most High), two or more make it Critical.
Contested rules have no base severity (Judgment). Evidence reads `<label> (<n>F/<n>P, <n> report
rejecting)`: F counts recruiters stating a fact or practice, P those giving a preference.
Single source rules are grouped by the one person behind them, with their role (hiring manager,
agency recruiter, former recruiter): weight each by that person's role and match for the target.

<!-- RULES:START -->
### Consensus (11)

| ID | Rule and check | Evidence | Base severity | Sources |
|---|---|---|---|---|
| ACH-1 | Under each role, describe the problem, the candidate's personal contribution and the result, not a list of technologies or responsibilities. *Check:* Does each recent role say what was built, what the candidate personally did and what changed? Flag bullets that are only technology names or duties. | Consensus 4 (4F/0P, 0 report rejecting) | High | JA-26, JA-75, JA-77, JB-13, JB-17, SB-01, SB-19, TW-07, TW-13, TW-21; notes: TW-16 |
| RED-2 | Missing a core skill of the role's stack is a rejection. *Check:* Compare the job's core stack (language, main frameworks) with the CV; a missing core item is critical. | Consensus 3 (3F/0P, 3 report rejecting) | Critical | JA-09, JA-38, JA-55, JA-87, SB-34, TW-06; notes: JA-97 |
| SCR-2 | Screeners read the most recent role first and judge fit mainly from recent, relevant experience. *Check:* Does the most recent role, at the top of the experience section, show the target role's core stack and kind of problem? Is the experience in reverse date order? | Consensus 3 (3F/0P, 0 report rejecting) | High | JB-03, SB-06, TW-44 |
| SCR-7 | Screeners look at the candidate's tech stack on the first look. *Check:* Is the stack of each recent role easy to find, and does it match the target role's core stack? | Consensus 3 (3F/0P, 0 report rejecting) | High | JA-04, JA-11, SB-07, TW-05 |
| STR-1 | Keep the CV focused; do not document every task from every job. *Check:* Are older or less relevant roles cut down to the essentials? Does any role list routine duties at length? | Consensus 3 (2F/1P, 0 report rejecting) | High | JB-15, SB-10, SB-17, TW-48 |
| STR-3 | Use a plain layout the reader can navigate quickly; fancy graphics add nothing. *Check:* Are there graphics, icons, skill bars, heavy colors or multi-column designs that slow down skimming? | Consensus 3 (2F/1P, 0 report rejecting) | High | JA-21, JB-16, TW-02, TW-37 |
| ACH-4 | Side projects and hackathons show genuine interest in the work and help a CV. *Check:* Are relevant side projects or hackathons listed? | Consensus 3 (2F/1P, 1 report rejecting) | High | JA-125, SB-21, TW-24 |
| ACH-6 | Make achievements measurable where possible. *Check:* Do the bullet points carry numbers (percentages, counts, time, money)? | Consensus 3 (2F/1P, 1 report rejecting) | High | JA-17, JA-57, JA-63, JA-76, JA-79, SB-19, TW-07, TW-13; notes: JA-88 |
| REG-14 | State where the candidate is actually based (the city), truthfully, on the CV and LinkedIn. *Check:* Does the CV header name the current city, and does it match LinkedIn? | Consensus 3 (1F/2P, 0 report rejecting) | High | JB-24, SB-40, SB-42, TW-62 |
| CHN-15 | Ask for referrals; a referral gets the CV looked at more carefully. *Check:* Not a CV check; recommend it when the candidate relies only on cold applications. | Consensus 3 (3F/0P, 0 report rejecting) | High | JB-25, JB-27, SB-49, TW-57, TW-58 |
| CHN-18 | Keep the LinkedIn profile complete and current (photo, full job history, what was done at each job, a bio). *Check:* Does the profile have a photo, full and up-to-date job history and a bio? | Consensus 3 (2F/1P, 0 report rejecting) | High | JB-44, JB-47, SB-31, TW-31, TW-34 |

### Supported (20)

| ID | Rule and check | Evidence | Base severity | Sources |
|---|---|---|---|---|
| SKL-4 | Show on the CV how AI tools are used in the development workflow. *Check:* Does the CV mention concrete use of AI coding tools in daily work? | Supported 2 (2F/0P, 1 report rejecting) | High | JA-114, JA-116, JA-142, JA-28, SB-32, SB-33 |
| REG-6 | Working English good enough to follow technical requirements and product direction is expected. *Check:* If the CV has a language section, is English stated at a working level? | Supported 2 (1F/1P, 1 report rejecting) | High | JA-101, SB-51 |
| SCR-1 | The first pass only decides whether there is enough relevant experience to keep reading; it is not a read of the whole career. *Check:* Is enough relevant experience visible at a first glance, from the top of page one? | Supported 2 (2F/0P, 0 report rejecting) | Medium | JA-119, JB-02 |
| SCR-6 | Screeners look at where the candidate has worked (the employers) on the first look. *Check:* Are employer names easy to spot in each role heading? | Supported 2 (2F/0P, 0 report rejecting) | Medium | SB-04, TW-03 |
| ATS-4 | Screening decisions are made by people reading the CV; the ATS is not relied on to judge candidates. *Check:* Context for ATS advice: write for the human reader and do not trade readability for keyword density. | Supported 2 (2F/0P, 0 report rejecting) | Medium | for: JA-02, JB-08, TW-14; against: TW-15 |
| STR-4 | Open the CV with a few tailored sentences saying who you are, what you specialize in and why you fit the role. *Check:* Is there a short summary at the top? Is it specific to the target role, or generic? | Supported 2 (0F/2P, 0 report rejecting) | Medium | JA-05, JB-30; notes: JA-44 |
| STR-27 | Include education with the university's name and the degree, even when the degree is not computer science. *Check:* Is there an education section naming the university and the degree? | Supported 2 (1F/1P, 0 report rejecting) | Medium | JA-107, SB-05, SB-46 |
| SKL-3 | Show where each listed technology was used (in which role or project). *Check:* For each key technology in the skills list, can the reader tell in which role it was used? | Supported 2 (1F/1P, 0 report rejecting) | Medium | JA-72, SB-12 |
| SKL-6 | Startups look for breadth across the stack rather than a narrow focus on one layer. *Check:* For startup applications, does the CV show work across frontend, backend and data, not one layer only? | Supported 2 (0F/2P, 0 report rejecting) | Medium | SB-02, TW-20 |
| REG-3 | Give contact details in the header, including email and a phone number with the correct country code. *Check:* Are an email and a phone number with country code in the header? | Supported 2 (0F/2P, 0 report rejecting) | Medium | JA-70, SB-37, SB-38 |
| GAP-2 | Explain gaps and short stints on the CV; unexplained ones are a red flag. *Check:* Is there a gap of several months, or a role of under about a year, without a reason given? | Supported 2 (2F/0P, 0 report rejecting) | Medium | SB-11, TW-53, TW-54 |
| GAP-3 | Length of an employment gap, in months, from which the CV should explain it. *Check:* Find gaps between roles; compare their length with the recruiters' common range and check that longer ones are explained (GAP-2). | Supported 2 (0F/2P, 0 report rejecting); JA at most 36 months, TW 6 months; common 6 months | Medium | JA-34, TW-55 |
| GAP-6 | A gap is not a problem in itself. *Check:* Do not treat a gap alone as a weakness; see GAP-7 and GAP-3. | Supported 2 (2F/0P, 0 report rejecting) | Medium | JB-18, TW-56 |
| GAP-7 | Show what was done during a gap to stay current (learning, projects). *Check:* For any gap of several months, does the CV show learning, projects or other activity in it? | Supported 2 (1F/1P, 0 report rejecting) | Medium | JB-18, SB-27 |
| CHN-3 | Skip a generic cover letter unless the employer asks for one; anything written should be short and specific to the company. *Check:* Is there a generic cover letter about passion and hard work? If a letter is required, is it short and specific? | Supported 2 (1F/1P, 0 report rejecting) | Medium | JA-59, JB-29, JB-32, JB-46; notes: JB-31 |
| CHN-6 | Link GitHub only when it shows real activity; an empty GitHub can hurt. *Check:* If a GitHub link is present, does the profile show recent contributions? | Supported 2 (1F/1P, 0 report rejecting) | Medium | JA-18, JA-20, JA-92, SB-29 |
| CHN-9 | Hiring managers usually open a GitHub link on the CV and browse the projects quickly. *Check:* Context for CHN-6 and CHN-8; if GitHub is linked, what will a quick browse show? | Supported 2 (2F/0P, 0 report rejecting) | Medium | JA-19, TW-32 |
| CHN-16 | Network and build relationships alongside applications rather than relying only on applying. *Check:* Not a CV check; recommend it when the candidate relies only on cold applications. | Supported 2 (0F/2P, 0 report rejecting) | Medium | JB-25, JB-41, TW-58 |
| CHN-17 | Send the hiring manager a short message saying why the candidate fits the role. *Check:* Not a CV check; recommend it alongside an application. | Supported 2 (2F/0P, 0 report rejecting) | Medium | JB-26, TW-22, TW-23 |
| CHN-21 | Recruiters and hiring managers use LinkedIn to find candidates and check their experience. *Check:* Context for CHN rules; flag a candidate with no LinkedIn profile. | Supported 2 (2F/0P, 0 report rejecting) | Medium | SB-30, TW-33 |

### Contested (7)

| ID | Rule and check | Evidence | Base severity | Sources |
|---|---|---|---|---|
| STR-2 | CV length in pages. *Check:* Count pages; compare with the recruiters' common range, minding the experience each range was given for. | Contested range 4 (0F/4P, 0 report rejecting); JA 1 page (6 years of DevOps experience (CV#01): 1 page; 8 years of mobile experience (CV#02): 1 page; 10 years as a data analyst (CV#04): 1 page), JB 2 to 5 pages, SB 2 pages (junior with little experience: 1 page; very experienced engineer, CTO or VP: at least 2 pages), TW 2 to 4 pages (junior or mid-level, one to two years of experience: 1 page; more than 10 years of experience: 3 to 4 pages); common none | Judgment | for: JA-15, JA-32, JA-58, JB-19, JB-20, SB-14, SB-15, SB-16, TW-49, TW-50, TW-51; against: none |
| SCR-4 | Time a screener spends on the first pass of a CV, in seconds. *Check:* Context for the first-pass rules: what must be visible within that time (SCR-1, SCR-3). | Contested range 2 (2F/0P, 0 report rejecting); JA 10 seconds (checking a CV for the required tech stack: 5 to 10 seconds), JB 30 seconds (first pass: 30 seconds); common none | Judgment | for: JA-10, JA-50, JA-81, JB-01; against: none |
| REG-17 | Screeners notice a phone number from another country. *Check:* Does the phone number's country code conflict with the stated location? | Contested 2-1 (2F/0P, 0 report rejecting) | Judgment | for: SB-39, TW-60; against: JA-104 |
| STR-28 | Give a notable grade (such as merit or distinction) in the education section. *Check:* Does the education entry show a notable grade where the candidate has one? | Contested 1-1 (0F/1P, 0 report rejecting) | Judgment | for: SB-46; against: JA-13 |
| SKL-2 | Do not repeat a full technology list under every role; name technologies in the context of the work. *Check:* Do role entries end with long tech lists that repeat the skills section? | Contested 1-1 (0F/1P, 0 report rejecting) | Judgment | for: JB-22; against: JA-73 |
| SKL-5 | Screeners weigh the core stack (language, frontend and backend frameworks) most; cloud providers such as AWS and GCP are treated as interchangeable. *Check:* Context for SKL and RED rules; do not treat a different cloud provider as a missing core skill. | Contested 1-1 (1F/0P, 0 report rejecting) | Judgment | for: SB-36; against: JA-56 |
| REG-16 | Screeners compare the candidate's location with the job's location. *Check:* Does the stated location fit the job's location? If not, expect location to weigh in screening. | Contested 1-1 (1F/0P, 1 report rejecting) | Judgment | for: TW-59, TW-60; against: JA-40 |

### Single source (96)

#### JA, John Adib: hiring manager (Engineering Manager), 57 rules

| ID | Rule and check | Evidence | Base severity | Sources |
|---|---|---|---|---|
| SCR-15 | A screener who is undecided about a CV rejects it, because an interview costs half an hour. *Check:* Context; a borderline CV is a rejected CV, so remove every doubt. | Single source 1 (1F/0P, 1 report rejecting) | Medium | JA-51 |
| STR-16 | Present the candidate as a software engineer rather than as a developer of one language or framework (such as a .NET developer). *Check:* Does the title or summary tie the candidate to one language? | Single source 1 (1F/0P, 1 report rejecting) | Medium | JA-118, JA-41 |
| ACH-12 | Show ownership on the CV; the candidate took responsibility for work and delivered it to the end, not just completed tasks. *Check:* Do the bullets show work the candidate drove and finished, and followed up after release? | Single source 1 (1F/0P, 1 report rejecting) | Medium | JA-79, JA-82, JA-83 |
| SKL-10 | Show hands-on experience with testing tools (at least one or two) on the CV. *Check:* Does the CV name the testing tools used and how? | Single source 1 (1F/0P, 1 report rejecting) | Medium | JA-144, JA-30, JA-39 |
| RED-6 | A CV missing most of the skills the job lists is not moved to the next stage. *Check:* Count the job ad's listed skills the CV shows; compare with SKL-11's common range. | Single source 1 (1F/0P, 1 report rejecting) | Medium | JA-54 |
| SCR-11 | At larger companies the first screener is often an HR recruiter who knows the names of technologies but cannot judge the technical detail of a CV. *Check:* Context for ACH-3 and SCR-7; would a non-technical reader see the match from titles and named technologies alone? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-03 |
| SCR-12 | Screeners give the summary only a quick look. *Check:* Context for STR-4; can the summary be read in a glance? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-42 |
| SCR-13 | Screeners do not read a CV in full, even for candidates they invite to interview. *Check:* Context; what matters must be visible without a full read. | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-45 |
| SCR-14 | Screeners judge the CV against the salary the candidate asked for; a higher salary raises the bar. *Check:* If the application states a salary, does the CV justify it? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-49 |
| SCR-16 | Screening outcomes depend on who reads the CV; different screeners can judge the same CV differently. *Check:* Present a verdict as one screener's likely view, not a certainty; do not over-fit the CV to a single reader's preference. | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-133 |
| STR-12 | Leave references off the CV; they add nothing. *Check:* Is there a references section? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-14 |
| STR-13 | Left-align the text of an English CV; justified text is not needed. *Check:* Is the body text justified? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-22 |
| STR-14 | In each role heading, put the job title first and more prominent than the company name. *Check:* Does each role heading lead with the job title? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-24 |
| STR-15 | Give each listed project its dates and context (in a job, freelance or personal). *Check:* Does every project say when and in what context it was done? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-31 |
| STR-17 | Do not use first-person pronouns (I, my) in the CV. *Check:* Do the summary or bullets use I, me or my? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-43 |
| STR-18 | Put certificates at the end of the CV. *Check:* Does a certificates section come before the work history? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-65 |
| STR-19 | Give each employer's location in the work history. *Check:* Does each role say where the employer is? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-68 |
| STR-20 | Head the CV with the name and the job title; leave out invented taglines. *Check:* Is there a slogan or tagline in the header besides the name and title? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-69 |
| STR-21 | Length of the summary at the top of the CV, in lines. *Check:* Count the summary's lines; compare with the recruiters' common range. | Single source 1 (1F/0P, 0 report rejecting); JA 3 to 4 lines | Low | JA-115, JA-71 |
| STR-22 | Length of a bullet point, in lines. *Check:* Count the lines of each bullet; compare with the recruiters' common range. | Single source 1 (0F/1P, 0 report rejecting); JA at most 1 lines | Low | JA-74 |
| STR-23 | Bold only what should catch the reader's eye, such as a strong result, not routine items like the university name. *Check:* What is in bold, and is it what the reader should notice? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-105, JA-89 |
| STR-24 | Give the start and end month of each role, not just the year. *Check:* Do role dates include months? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-106 |
| STR-25 | Under the name, write the title of the job being applied for, matching it. *Check:* Does the title under the name match the target job's title? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-110 |
| STR-26 | Education usually goes at the top of the CV only for fresh graduates without work experience. *Check:* Is education above experience on a CV with work experience? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-123 |
| STR-29 | Do not add a separate core strengths section; put those points in the summary or the bullet points. *Check:* Is there a core strengths (or key strengths) section that repeats what the summary and bullets should say? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-12 |
| ACH-7 | Give the scale of the work in the bullet points (how big the product, the company and the team were). *Check:* Can a reader tell from the bullets how large the product, company and team were? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-25, JA-64 |
| ACH-8 | Metrics that are all round numbers (25, 30, 40, 50 percent) look rounded, and screeners notice it. *Check:* Are all the percentages round numbers? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-27 |
| ACH-9 | Show that the candidate keeps learning new skills and technologies. *Check:* Does the CV show recent learning (new tools, courses applied in work, side projects)? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-103, JA-29 |
| ACH-10 | Put the biggest achievement at the top, where the reader sees it first. *Check:* Does the strongest result come first in the summary or the first role? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-62 |
| ACH-11 | In a large company, claim only the candidate's own part of an impact that a whole team or organization produced. *Check:* Do bullets claim sole credit for company-wide results? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-78 |
| ACH-13 | Start bullet points with action verbs, and vary the first word. *Check:* Do the bullets start with action verbs, and not all with the same one? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-94 |
| SKL-8 | Group the skills list into categories. *Check:* Is the skills section grouped (languages, cloud, tools), not one flat list? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-08, JA-124 |
| SKL-9 | Do not list soft skills in a section of their own; show them in the summary and the bullet points. *Check:* Is there a soft skills list (teamwork, leadership)? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-16 |
| SKL-11 | Share of the skills listed in a job ad that the CV must show, in percent. *Check:* Count the job ad's listed skills the CV shows; compare with the recruiters' common range. | Single source 1 (0F/1P, 0 report rejecting); JA 80 percent | Low | JA-53 |
| SKL-12 | Listing a required technology in the skills section can be enough for a screener to invite the candidate. *Check:* Context for SKL-11; is every required technology the candidate has used named in the skills section? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-66 |
| SKL-13 | A CV that lists JavaScript should also show TypeScript. *Check:* Does a JavaScript CV name TypeScript? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-102, JA-86 |
| SKL-14 | Do not repeat the same technology many times across the CV; naming it once is enough. *Check:* Is one technology named in the summary, the skills list and every role? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-99 |
| SKL-15 | Do not list skills labelled as basic. *Check:* Does the skills list mark any item as basic or beginner? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-100 |
| SKL-16 | Include a skills section. *Check:* Is there a skills section? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-108; notes: JA-109 |
| SKL-17 | Do not label skill proficiency levels (expert, advanced, intermediate, novice). *Check:* Does the skills section rate the candidate's level per skill? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-112, JA-113 |
| SKL-18 | Leave out practices every engineer uses, such as Agile; they add nothing. *Check:* Does the CV list generic practices (Agile, Scrum, Git) as if they were distinguishing? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-122 |
| SKL-19 | List technologies outside the target role when they relate to the job (such as frontend frameworks on a backend CV); they count as a plus even when the job does not ask for them. *Check:* Does the CV leave out related technologies the candidate knows because the target role does not name them, or list technologies with no link to the job? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-130, JA-131 |
| RED-5 | Em-dashes read as a sign that AI wrote the CV. *Check:* Are there em-dashes or double dashes in the CV? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-93 |
| REG-8 | Do not list English test scores such as IELTS or TOEFL on the CV; many recruiters do not know what they mean. *Check:* Is there an IELTS or TOEFL score on the CV? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-06, JA-07 |
| REG-9 | On an English CV, listing English as a language adds nothing; leave it out. *Check:* Does an English CV list English in a languages section? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-23 |
| REG-10 | A basic level of the local language (such as German A1) on the CV shows learning but is not a working skill. *Check:* Context only; do not present a basic level as a usable language skill. | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-33 |
| REG-11 | The CV can use the name the candidate goes by (a nickname); the legal name is needed only where an application form asks for it. *Check:* Context only; a nickname on the CV and LinkedIn is fine if used consistently. | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-37 |
| REG-12 | A candidate's name can affect how many interviews they get. *Check:* Context for REG-11. | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-36 |
| REG-13 | Write the whole CV in English; leave no text in another language. *Check:* Is any part of an English CV in another language? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-98 |
| SEN-5 | The more years of experience a CV claims, the more the screener expects it to show. *Check:* Do the achievements match what the stated years of experience lead a reader to expect? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-61 |
| SEN-6 | A candidate hired from abroad must be stronger than the hiring team's average, because relocation takes months and is an investment. *Check:* Context for the target profile; does the CV show the candidate would raise the team's level? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-80 |
| SEN-7 | Show teamwork; presenting work as done alone is not an advantage, because hiring managers want someone who will adapt to the team. *Check:* Do the bullets show work with a team, or only solo work? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-111, JA-95, JA-96 |
| GAP-4 | Do not show a full-time job overlapping other work (another full-time job or freelance work). *Check:* Do the dates of a full-time role overlap other roles? | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-90, JA-91 |
| GAP-5 | Experience at a startup that failed is not a problem; list it like any other job. *Check:* Does the candidate hide or apologize for work at a startup that no longer exists? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-143 |
| CHN-12 | Screeners do not read the cover letter in full; they may look at it when undecided about the CV. *Check:* Context for CHN-3; the CV must carry the decision on its own. | Single source 1 (1F/0P, 0 report rejecting) | Low | JA-48 |
| CHN-13 | Link only profiles that add value; a Stack Overflow profile is rarely opened any more, and an inactive one adds nothing. *Check:* Are there profile links (Stack Overflow, others) that are inactive or unlikely to be opened? | Single source 1 (0F/1P, 0 report rejecting) | Low | JA-84 |
| CHN-14 | Number of GitHub contributions in a year from which a profile stands out. *Check:* Count last year's contributions; compare with the recruiters' common range before calling GitHub a strength. | Single source 1 (1F/0P, 0 report rejecting); JA at least 1000 contributions | Low | JA-121 |

#### SB, Sam Baldwin: agency recruiter (Recruiter, JavaScript and TypeScript specialist), 12 rules

| ID | Rule and check | Evidence | Base severity | Sources |
|---|---|---|---|---|
| RED-3 | Everything on the CV must be accurate and defensible; a line the candidate cannot back up is an instant rejection. *Check:* Is any claim on the CV unsupported or likely to fall apart under a question (watch AI-written lines)? | Single source 1 (1F/0P, 1 report rejecting) | Medium | SB-47, SB-52 |
| STR-6 | Tailor the CV to each job, so the skills and experience the job asks for are apparent. *Check:* Does the CV emphasize what this job's description asks for? | Single source 1 (0F/1P, 0 report rejecting) | Low | for: JA-141, SB-35; against: JA-46; notes: JA-117 |
| ACH-3 | Lead each achievement with the outcome in plain English, then the technical detail, so a non-technical screener can follow it. *Check:* Does each bullet state the problem or result in plain words before the technology names? | Single source 1 (0F/1P, 0 report rejecting) | Low | SB-18 |
| RED-1 | Typos are a red flag. *Check:* Spell-check the whole CV. | Single source 1 (1F/0P, 0 report rejecting) | Low | SB-13 |
| REG-5 | If the candidate would relocate, say so on the CV (for example "happy to relocate"). *Check:* For a candidate abroad, does the CV state willingness to relocate? | Single source 1 (0F/1P, 0 report rejecting) | Low | SB-43 |
| REG-18 | Screeners look at how far the candidate lives from the office. *Check:* For on-site or hybrid roles, how far is the stated location from the office? | Single source 1 (1F/0P, 0 report rejecting) | Low | SB-41 |
| SEN-1 | For startup roles, give each employer's stage and funding (seed, series A, VC backing, amount raised) and the tenure through it. *Check:* For startup applications, does each startup employer show its stage or funding? | Single source 1 (1F/0P, 0 report rejecting) | Low | SB-08 |
| SEN-2 | Visible progression within a company, such as a promotion to senior, is a positive signal. *Check:* Are promotions shown as separate titles with dates under the same employer? | Single source 1 (1F/0P, 0 report rejecting) | Low | SB-09 |
| SEN-3 | For startup roles, state zero-to-one product building experience explicitly. *Check:* For startup applications, if the candidate built a product from scratch, does the CV say so in those words? | Single source 1 (0F/1P, 0 report rejecting) | Low | SB-20 |
| SEN-4 | For startup roles, a big-company background can count against the candidate unless the CV shows startup-like work (greenfield projects, shipping fast). *Check:* For a startup application from a large company, does the CV describe the team's pace and greenfield work? | Single source 1 (1F/0P, 0 report rejecting) | Low | SB-45 |
| CHN-5 | Include a LinkedIn URL on the CV. *Check:* Is there a LinkedIn URL in the header? | Single source 1 (0F/1P, 0 report rejecting) | Low | SB-28 |
| CHN-22 | Without a LinkedIn profile, screening the candidate is harder. *Check:* Flag a candidate with no LinkedIn profile. | Single source 1 (1F/0P, 0 report rejecting) | Low | SB-30 |

#### TW, Tomasz Wojtyczko: agency recruiter (Principal Recruitment Consultant, VirtueTech), 16 rules

| ID | Rule and check | Evidence | Base severity | Sources |
|---|---|---|---|---|
| REG-7 | Do not put a photo or pictures of any kind on the CV. *Check:* Is there a photo, logo or other picture on the CV? | Single source 1 (1F/0P, 1 report rejecting) | Medium | TW-38 |
| CHN-20 | Keep LinkedIn consistent with the CV (dates, roles). *Check:* Do the dates and roles on LinkedIn match the CV? | Single source 1 (1F/0P, 1 report rejecting) | Medium | TW-30 |
| SCR-8 | Screeners notice the CV's formatting first, before reading its content. *Check:* Context for STR-3; at a glance, does the CV look clean and easy to read? | Single source 1 (1F/0P, 0 report rejecting) | Low | TW-01 |
| SCR-9 | Screeners look at the candidate's job titles early in the first pass; a title may differ from the target role's wording. *Check:* Do the job titles make the kind of role obvious? | Single source 1 (1F/0P, 0 report rejecting) | Low | TW-04 |
| SCR-10 | Screeners look for experience in the employer's industry (such as finance for a financial firm) when the hiring manager asks for it. *Check:* If the job ad or manager asks for industry experience, is it visible in the role headings or company context? | Single source 1 (1F/0P, 0 report rejecting) | Low | TW-09 |
| ATS-5 | Employer ATS systems usually give each application an automatic AI score based on the keywords in the job description. *Check:* Context for ATS-1; does the CV use the job description's keywords? | Single source 1 (1F/0P, 0 report rejecting) | Low | TW-61 |
| STR-7 | Between each job title and its bullet points, add a short paragraph on the company and the work (what the company does, its sector, the team, the main problems and how they were solved). *Check:* Does each recent role open with a few lines of company context before the bullets? | Single source 1 (1F/0P, 0 report rejecting) | Low | TW-17, TW-18; notes: JA-67 |
| STR-8 | Length of the company context paragraph under each role, in lines. *Check:* Count the lines of each company paragraph (STR-7); compare with the recruiters' common range. | Single source 1 (0F/1P, 0 report rejecting); TW 2 to 4 lines | Low | TW-19 |
| STR-9 | Keep every past employer and its dates on the CV; do not remove older jobs to look less experienced. *Check:* Are any employers or dates missing from the work history? | Single source 1 (0F/1P, 0 report rejecting) | Low | TW-43 |
| STR-10 | Years of work history to describe in detail on the CV. *Check:* How far back do detailed role descriptions go? Compare with the recruiters' common range; older roles can be listed without detail (STR-1). | Single source 1 (1F/0P, 0 report rejecting); TW 10 years (contractor with many short jobs: 6 years) | Low | TW-45, TW-46, TW-47 |
| ACH-5 | List coding contest ratings or algorithm practice (such as LeetCode or HackerRank) when the candidate has them, briefly and highlighted, for example in a side column. *Check:* If the candidate has such a rating, is it on the CV without taking much space? | Single source 1 (0F/1P, 0 report rejecting) | Low | TW-27 |
| SKL-7 | Hiring managers want candidates with some exposure to agentic development or AI tools, and do not want to hire anyone who is against AI. *Check:* Does the CV show any hands-on use of AI tools or agentic development? | Single source 1 (1F/0P, 0 report rejecting) | Low | TW-28, TW-29 |
| RED-4 | Hiring managers spot AI-written CVs quickly and do not want to see too much AI in a CV. *Check:* Does the text read as generic AI output (standard phrasing, "responsible for building ...")? | Single source 1 (1F/0P, 0 report rejecting) | Low | TW-10; notes: JA-60, TW-11 |
| CHN-8 | Keep GitHub up to date, because hiring managers sometimes look it up even when the CV does not link it. *Check:* If the candidate has a public GitHub, is it current? | Single source 1 (1F/0P, 0 report rejecting) | Low | TW-25, TW-26 |
| CHN-10 | Use a standard job title (such as software engineer or senior data engineer) on LinkedIn and keep it consistent, because recruiters search by standard titles. *Check:* Is the LinkedIn headline title a standard one, with any creative title only after it? | Single source 1 (1F/0P, 0 report rejecting) | Low | TW-35, TW-36 |
| CHN-11 | An open-to-work banner on LinkedIn does not count against the candidate with hiring managers. *Check:* Context only; do not advise removing the banner on this account. | Single source 1 (1F/0P, 0 report rejecting) | Low | TW-52 |

#### JB, Joe Bignell: former recruiter (Former recruiter (14 years, 300+ placements), now at Vention (AI transformation)), 11 rules

| ID | Rule and check | Evidence | Base severity | Sources |
|---|---|---|---|---|
| ATS-3 | Screeners use the ATS to screen out applicants who fail a hard requirement of the role, such as security clearance eligibility. *Check:* If the job has a hard requirement (clearance, eligibility, mandatory certification), does the CV state the candidate's status for it in plain words? | Single source 1 (1F/0P, 1 report rejecting) | Medium | JB-09 |
| SCR-3 | The technical fit for the target role must be obvious on page one, without the reader searching for it. *Check:* Are the target role's must-have skills visible on page one? Would a recruiter hiring for that stack have to search through pages to find it? | Single source 1 (1F/0P, 0 report rejecting) | Low | JB-04, JB-12, JB-14 |
| SCR-5 | A recruiter has to justify internally why each candidate introduced to the hiring manager is worth meeting. *Check:* Could a recruiter take two or three concrete reasons to shortlist from the CV? | Single source 1 (1F/0P, 0 report rejecting) | Low | JB-07 |
| ATS-1 | Include the target role's keywords so recruiter searches and ATS filters find the CV. *Check:* Does the CV contain the job description's must-have terms in the same wording? | Single source 1 (0F/1P, 0 report rejecting) | Low | JB-10 |
| ATS-2 | Write the CV for a human reader, not for the ATS; keyword lists without context make it unreadable. *Check:* Are keywords embedded in statements about the work, or are there buzzword strings and stuffed keyword blocks? | Single source 1 (0F/1P, 0 report rejecting) | Low | JB-11 |
| ACH-2 | Under each role, name the business domain (such as fintech or healthcare) and the end customers the work served. *Check:* Does each recent role say which domain the work was in and who the end customers were? | Single source 1 (0F/1P, 0 report rejecting) | Low | JB-49 |
| SKL-1 | A technology list on page one shows the required skill set at a glance. *Check:* Is there a skills or technologies section on page one? | Single source 1 (0F/1P, 0 report rejecting) | Low | JB-21 |
| REG-2 | Do not state a need for visa sponsorship on the CV. *Check:* Does the CV say the candidate needs sponsorship? | Single source 1 (0F/1P, 0 report rejecting) | Low | JB-35, JB-38 |
| REG-15 | Make the candidate's right-to-work status obvious. *Check:* Does the CV state the right to work for the target country (or the visa held)? | Single source 1 (0F/1P, 0 report rejecting) | Low | JB-24 |
| CHN-4 | Share of a recruiter's placements that came from referrals, in percent. *Check:* Context for CHN-1, how much hiring runs through referrals rather than applications. | Single source 1 (1F/0P, 0 report rejecting); JB 70 percent (early career: 70 percent) | Low | JB-28 |
| CHN-19 | Be active and visible on LinkedIn rather than invisible. *Check:* Does the profile show some activity (posts, comments)? | Single source 1 (1F/0P, 0 report rejecting) | Low | JB-44, JB-47, JB-48; notes: JB-45 |
<!-- RULES:END -->

## Contested guidance

| Rule | For | Against | Recommendation for the default target |
|---|---|---|---|
| STR-2 | All four give page counts that do not overlap: JA 1 page for the 6 to 10 year CVs reviewed live (JA-15, JA-32, JA-58); TW 2 to 4 (1 for juniors); SB 2 (1 for juniors, at least 2 for very senior); JB 2 to 5 | none | 1 or 2 pages for about 7 years. JA is the high match and cuts to one page; TW and JB accept two. Flag 3 or more pages (Medium), and a one-page CV only when it is too dense to scan. |
| SCR-4 | JA about 10 seconds (5 to 30, JA-10, JA-50, JA-81); JB about 30 seconds (JB-01) | none | Plan for 10 seconds: the top third of page one has to show the title, the core stack and the most recent role. |
| REG-17 | SB checks the phone country when hiring in the UK only (SB-39); TW says client ATS systems flag a foreign number (TW-60) | JA: screeners do not know dialling codes, and location comes out on the first call (JA-104) | Low. Use a local number if the candidate really has one; otherwise keep the real number with the right country code (REG-3) and state relocation plans (REG-5). Never suggest a number the candidate does not have (RED-3). |
| STR-28 | SB: include the grade, especially a merit or distinction (SB-46) | JA: nobody cares about the GPA (JA-13) | Leave grades out for experienced candidates (JA is the high match). A named distinction may stay on the degree line. |
| SKL-2 | JB: do not repeat the stack under each role; mention tech within the work (JB-22) | JA: a stack line under each job is good when there is space (JA-73) | Accept a one-line stack per role (JA); flag only a full technology list repeated under every role. |
| SKL-5 | SB: leaders see AWS and GCP as interchangeable and weigh the core stack (SB-36) | JA: cloud providers are not interchangeable; Azure does not fit a company without Azure (JA-56) | Treat a different cloud as a gap (JA). Name the job's cloud if the candidate used it; otherwise present the cloud work as transferable without claiming the other provider. |
| REG-16 | TW: location filters and client ATS systems screen out applicants from abroad (TW-59, TW-60) | JA: candidates think location rejects them, but skill gaps do (JA-40) | Fix skill gaps first (JA). Then state the real city (REG-14) and readiness to relocate (REG-5) in one line, so location is a known fact rather than a surprise. |

## Coverage gaps

- **Markets.** All four recruiters work from the UK; JB also hired across EMEA and the US. No one
  hires in DACH or mainland Europe, so local conventions there (photos, German CV format, German
  language level) are not covered. When the target is DACH, still apply the rules (a photo is
  still REG-7) at their weighted severity, and add to each such finding that DACH conventions
  may differ and no DACH recruiter is in the evidence.
- **Recruiter types.** One hiring manager (JA), two agency recruiters (SB, TW) and one former
  recruiter (JB). No in-house recruiter at a large company; ATS practice comes from agencies.
- **Specialisms.** No recruiter specializes in mobile or Android; JA hires mobile engineers among
  others. SB covers JavaScript and TypeScript startups only.
- **Seniority.** Little on staff, principal or management CVs, and juniors appear only in passing.
- **One-person rules.** Most rules are Single source: one recruiter's practice. Present them as
  such and weight them by that recruiter's match.
- **Out of scope.** Interviews, visa routes, job boards and application volume are recorded in the
  ledger but are not CV rules; answer them as general advice if asked.

## Updating

Maintainers update the evidence in the `resume-reviewer` repository (claims ledger and `rrs` tool), not in this
file. To add a transcript: import and segment it, extract claims chunk by chunk, run
`rrs ledger tally --report`, then `rrs skill build` regenerates the Evidence base and the rule
tables. Update Contested guidance and Coverage gaps by hand when the change report shows a
contest or a new market, run `rrs skill lint` and the evals, and release a new version.
