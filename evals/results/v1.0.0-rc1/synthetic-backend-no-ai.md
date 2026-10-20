# CV review: Senior Backend Engineer (Java) for UK product companies, relocation from India

**Verdict:** Borderline

**10-second verdict:** The top of page one shows "Senior Backend Engineer", Pune, India, 8 years of Java and Spring Boot, and a current senior role at Quillstone Software with REST APIs, PostgreSQL and microservices. The title and core stack match, so a screener keeps reading past the first glance (SCR-1, SCR-7). What they find next is a list of duties ("Responsible for developing REST APIs", "Worked on microservices") with no result, number, scale or ownership, and a location abroad with no relocation line. There is nothing a recruiter can quote to justify a shortlist (SCR-5), and an undecided screener rejects (SCR-15). Likely outcome: a no, or a maybe that becomes a no.

**Target and weighting:** From the request: Senior Backend Engineer (Java), UK product companies, candidate based in India and needing relocation. No job description was given, so hard requirements were checked against a generic Java backend role (Java, Spring Boot, SQL, messaging, cloud, testing). Match: JA high (UK hiring manager at a tech product company), TW medium-high (UK agency, tech and product), JB medium-high (cross-border hiring across EMEA), SB low (JavaScript and TypeScript startups only). Severity raises below are for Single source JA rules, because JA is the high match and the CV is in the situation he described.

## Findings

### High
- **ACH-1** (Consensus 4, High): Every bullet is a duty or a technology, not a problem, a personal contribution and a result: "Responsible for developing REST APIs in Java and Spring Boot", "Worked on microservices", "Fixed bugs and implemented new features", "Wrote SQL queries". The most recent role shows the right stack but not the kind of problem solved (SCR-2). Fix: rewrite each recent bullet as what was built, what the candidate personally did, and what changed (see Rewrites).
- **ACH-6** (Consensus 3, 1 report rejecting, High): There is not a single number on the CV. No latency, throughput, users, uptime, ticket volume or time saved. The strongest result therefore cannot sit at the top (ACH-10). Fix: add real figures to the main bullets of the last two roles; use placeholders such as `[X ms]` or `[N requests per day]` until the candidate supplies the true values. Never estimate them (RED-3), and avoid all-round percentages (ACH-8).
- **SKL-4** (Supported 2, 1 report rejecting, High): No mention of AI coding tools anywhere. JA (high match) says hiring managers now look for this, and TW adds that they do not want someone against AI (SKL-7, Single source 1, Low). Fix: if the candidate uses tools such as Copilot, Cursor or Claude in daily work, add one concrete line on how (for example generating tests or reviewing code). If not, do not invent it.
- **ACH-12** (Single source 1, 1 report rejecting, Medium raised to High: JA is the high match and the CV shows no ownership): "Participated in code reviews and sprint planning", "Handled production support tickets", "Worked with Kafka and Redis" describe taking part, not driving work to the end. Fix: name one or two pieces of work the candidate led from design to release and followed up after launch, for example a service they owned.
- **SKL-10** (Single source 1, 1 report rejecting, Medium raised to High: JA is the high match and the CV names no testing tool): No testing tools appear in roles or skills. JA rejects on this. Fix: name the testing tools actually used (for example JUnit, Mockito, Testcontainers, if true) and how, in a bullet and in the skills list.
- **ACH-4** (Consensus 3, 1 report rejecting, High): No side projects, open source or hackathons. Fix: add a short Projects section if the candidate has any relevant work outside the job, each with dates and context (STR-15). If there is none, this is a gap to accept, not to fill with invented work.
- **CHN-15** (Consensus 3, High; not a CV check): A candidate abroad applying to UK companies is likely relying on cold applications. Fix: ask former colleagues now in the UK for referrals, and pair applications with a short note to the hiring manager on why the candidate fits (CHN-17, Supported 2, Medium) and wider networking (CHN-16, Supported 2, Medium).

### Medium
- **STR-4** (Supported 2, Medium): The summary is generic: "Hard-working team player with strong communication skills." It says nothing a UK product company can use. Fix: three or four lines (STR-21) on specialism, the kind of systems built and why the candidate fits, with the relocation line (see Rewrites).
- **SKL-3** (Supported 2, Medium): "Docker" and "MySQL" in Skills appear in no role, so the reader cannot tell where they were used. Fix: name each in the role where it was used, or drop it.
- **SEN-5** (Single source 1, Low raised to Medium: JA, high match): 8 years and a senior title lead the reader to expect design decisions, ownership and impact; the bullets read like junior duties. JA adds that a candidate hired from abroad must look stronger than the team's average, because relocation is a months-long investment (SEN-6). Fix: covered by ACH-1, ACH-6 and ACH-12; make the senior role show senior work.
- **ACH-7** (Single source 1, Low raised to Medium: JA, high match): No sense of scale: size of product, traffic, company or team. Fix: add `[team of N]`, `[N users]` or `[N services]` where true.
- **ACH-9** (Single source 1, Low raised to Medium: JA, high match): Nothing shows recent learning; the newest technologies listed are the same as in 2018 ("Worked with Kafka and Redis"). Fix: show any newer tool, framework or practice adopted at Quillstone, if real.
- **ACH-13** (Single source 1, Low raised to Medium: JA, high match): Two bullets open with "Responsible for", three with "Developed", one with "Worked". Fix: open with varied action verbs (Built, Designed, Migrated, Reduced).
- **SKL-18** (Single source 1, Low raised to Medium: JA, high match): "Git, Jira, Agile" are listed as if they were distinguishing skills. Fix: remove them.
- **SKL-8** (Single source 1, Low raised to Medium: JA, high match): Skills are one flat line. Fix: group into Languages and frameworks, Data and messaging, Infrastructure, Testing.
- **SKL-14** (Single source 1, Low raised to Medium: JA, high match): Java is named in the summary, the skills list and all three roles. Fix: keep it in the summary and skills, and in a one-line stack per recent role (SKL-2 guidance) rather than in every bullet. For a Java role the word must stay visible (ATS-1), so trim repetition only.

### Low
- **REG-5** (Single source 1, Low): The CV does not say the candidate would relocate; a UK reader sees only "Pune, India". Fix: add "Open to relocating to the UK" to the header line (see REG-16 below).
- **REG-15** (Single source 1, Low): Right-to-work status for the UK is not stated. Fix: state it plainly in one line. Per REG-2 (Single source 1, Low), do not write a request for sponsorship on the CV; "Open to relocating to the UK" plus the right-to-work fact is enough.
- **CHN-5** (Single source 1, Low): No LinkedIn URL in the header. Recruiters use LinkedIn to check experience (CHN-21, Supported 2, Medium), and the profile should be complete and current (CHN-18, Consensus 3, High: photo, full history, what was done at each job, bio) and match the CV dates (CHN-20). Fix: add the URL and bring the profile in line with the rewritten CV.
- **STR-7** (Single source 1, Low): No company context under the role titles; a UK reader will not know Quillstone Software or Mervale Systems. Fix: two to four lines (STR-8) on what each company does, its product and the team. This also covers ACH-2 (Single source 1, Low: domain and end customers not named).
- **SCR-5** (Single source 1, Low): A recruiter could not pull two or three concrete reasons to shortlist from the CV. Fix: the rewritten summary and first role should each carry one quotable result.
- **RED-4** (Single source 1, Low): "Responsible for developing ..." is the stock phrasing TW associates with AI-written CVs. Fix: removed by the ACH-1 rewrites.

### Judgment calls
- **REG-16** (Contested 1-1): For: TW says location filters and client ATS systems screen out applicants from abroad (TW-59, TW-60). Against: JA says skill gaps, not location, cause the rejections (JA-40). Recommendation: fix the content gaps first (ACH-1, ACH-6, SKL-10), then state the real city (already done, REG-14) and readiness to relocate in one line.
- **REG-17** (Contested 2-1): For: SB and TW say a foreign number gets noticed. Against: JA says screeners do not know dialling codes. Here the +91 number matches the stated city, so there is no conflict. Recommendation: keep the real number with its country code (REG-3); do not add a UK number the candidate does not have.
- **SKL-5** (Contested 1-1): For: SB treats cloud providers as interchangeable. Against: JA says they are not. This CV names no cloud provider at all, only Docker. Recommendation: if the candidate deployed to AWS, GCP or Azure, name it with what was done there; check the job ad's cloud and treat a missing one as a gap (JA), without claiming a provider not used.
- **STR-2** (Contested range 4): JA 1 page; SB 2 pages; TW 2 to 4 pages for experienced candidates; JB 2 to 5 pages. The CV is one short page for 8 years. Recommendation: one full page or two; the problem is not length but that the page is thin. Adding results and context will fill it naturally.

## Rewrites

**Header line**
- Before: "Senior Backend Engineer | Pune, India | [email] | [phone]"
- After: "Senior Backend Engineer (Java) | Pune, India, open to relocating to the UK | [email] | [phone] | [LinkedIn URL]"

**Summary**
- Before: "Backend engineer with 8 years of experience in Java and Spring Boot. Hard-working team player with strong communication skills."
- After: "Senior backend engineer with 8 years building Java and Spring Boot services, REST APIs and event-driven systems on PostgreSQL, Kafka and Redis. At Quillstone Software, [one-line strongest result, e.g. built X that cut Y by [X%]]. Open to relocating to the UK."

**Quillstone Software, first bullets**
- Before: "Responsible for developing REST APIs in Java and Spring Boot."
- After: "Built [N] REST APIs in Java and Spring Boot for [product or feature], serving [N requests per day] for [type of customer]."
- Before: "Responsible for maintaining the PostgreSQL database."
- After: "Improved [query or schema] in PostgreSQL, reducing [response time or load] by [X%]."
- Before: "Worked on microservices."
- After: "Designed and owned the [name] microservice from design to release, [what it enabled]."
- Before: "Handled production support tickets."
- After: "Resolved [N] production incidents per [month], and [fix that prevented repeats, e.g. added monitoring or tests with [testing tool]]."

**Mervale Systems**
- Before: "Worked with Kafka and Redis."
- After: "Introduced Kafka [for which flow] and Redis caching [for which data], cutting [latency or load] by [X%]."

**Skills**
- Before: "Java, Spring Boot, Hibernate, PostgreSQL, MySQL, Kafka, Redis, Docker, REST, Microservices, Git, Jira, Agile"
- After: "Languages and frameworks: Java, Spring Boot, Hibernate, REST | Data and messaging: PostgreSQL, MySQL, Kafka, Redis | Infrastructure: Docker, [cloud provider if used] | Testing: [tools actually used]"

## What already works
- Title and core stack (Java, Spring Boot) are visible at the very top, and the most recent role matches the target (SCR-7, SCR-1, SCR-3).
- Experience is in reverse date order with clear headings that lead with the job title (SCR-2, STR-14, SCR-9), employer names are easy to spot (SCR-6), each has a location (STR-19) and month dates (STR-24).
- No gaps or short stints (GAP-2), and a visible progression from Junior Developer to Senior Backend Engineer.
- Plain single-column layout with no photo, graphics or skill bars (STR-3, REG-7), no first-person pronouns (STR-17), no proficiency labels (SKL-17), no references section (STR-12).
- Current city stated truthfully (REG-14); email and phone with country code in the header (REG-3).
- Education names the university and the degree, placed after experience (STR-27, STR-26).
- Focused and short, with no long lists of routine duties in old roles (STR-1).

## Not covered by the evidence
- **Java and backend specialism.** No recruiter in the evidence specializes in Java or backend hiring; JA hires across disciplines and SB covers JavaScript startups only. Java-specific expectations (for example Spring version, reactive stacks, JVM tuning) are general advice, not evidence.
- **Hard requirements and keyword match.** Without a job description, RED-6, SKL-11 (JA: about 80 percent of listed skills) and ATS-1 could not be checked. Run this check against each ad before applying.
- **Visa routes.** UK Skilled Worker sponsorship rules and which employers sponsor are outside the CV rules; general advice: target companies on the UK register of licensed sponsors.
- **Salary and notice period.** Not covered; general advice: be ready to state notice period and relocation timing on the first call.
