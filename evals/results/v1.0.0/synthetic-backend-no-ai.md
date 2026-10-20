# CV review: Senior Backend Engineer (Java) for UK product companies, relocating from India

**Verdict:** Borderline

**10-second verdict:** The top of page one shows the right title ("Senior Backend Engineer"), the right core stack ("Java and Spring Boot") and a current senior role at Quillstone Software with "REST APIs in Java and Spring Boot" and "PostgreSQL". A screener hiring for Java backend sees enough relevant experience to keep reading (SCR-1, SCR-2, SCR-7). The employer names will not be known to a UK screener (SCR-6), and the summary ("Hard-working team player with strong communication skills") gives no reason to pick this candidate over others. On the full read, every bullet is a duty with no result or number, which for a candidate hired from abroad (SEN-6) and undecided screeners (SCR-15) is likely to cost the first pass.

**Target and weighting:** Senior Backend Engineer (Java), UK product companies, candidate based in Pune and willing to relocate; from the request, not the default target. Match: JA high (hiring manager at a UK tech product company), TW medium-high (UK agency, tech and product), JB medium-high (cross-border hires), SB low-medium (UK agency, but JavaScript and TypeScript startups). No job description was given, so hard requirements were checked against the generic Java backend stack only.

## Findings

### High
- **ACH-1** (Consensus 4, High): Under each role the bullets are duties and technology names, not what was built, what the candidate personally did and what changed: "Responsible for developing REST APIs in Java and Spring Boot.", "Worked on microservices.", "Worked with Kafka and Redis.", "Fixed bugs and implemented new features." Fix: rewrite each recent bullet as problem, the candidate's own contribution, result (see Rewrites).
- **ACH-6** (Consensus 3, High): No bullet anywhere carries a number (latency, throughput, users, uptime, ticket volume, time saved). Fix: add the real figures for the top two or three achievements per recent role; do not estimate figures the candidate cannot defend (RED-3).
- **ACH-12** (Single source 1, JA, hiring manager; raised from Medium to High because JA is the high match and the CV is in the situation described): The recent role reads as tasks completed, not work owned and delivered: "Participated in code reviews and sprint planning.", "Handled production support tickets." Fix: name one or two pieces of work the candidate drove from design to release and followed up on after release.
- **SKL-4** (Supported 2, High): The CV shows no use of AI coding tools in daily work. JA (high match) reports rejecting on this, and TW adds that hiring managers want some hands-on AI exposure (SKL-7, Single source 1, Low). Fix: if the candidate uses AI tools at work (for example code assistants for tests, reviews or migrations), add one concrete line saying which tool and for what. Do not add it if it is not true.
- **ACH-4** (Consensus 3, High): No side projects or hackathons. Fix: if the candidate has any relevant Java or backend side project, open-source contribution or hackathon, add a short Projects section with dates and context (STR-15). If none exist, this stays a gap rather than something to invent.
- **SKL-10** (Single source 1, JA, hiring manager; raised from Medium to High because JA is the high match and reports rejecting on it): No testing tools are named anywhere. Fix: name the testing tools actually used (for example the unit and integration test frameworks) and how, inside a bullet of the most recent role and in the skills list.

### Medium
- **STR-4** (Supported 2, Medium): The summary is generic: "Hard-working team player with strong communication skills." It does not say what the candidate specializes in or why they fit a UK product company. Fix: 3 to 4 lines (STR-21) naming the specialism, the strongest result and the relocation line (see Rewrites).
- **SKL-3** (Supported 2, Medium): Some listed skills cannot be tied to any role: "Docker" and "MySQL" appear only in the skills list. Fix: mention each in the bullet of the role where it was used, or drop it.
- **SEN-5** (Single source 1, JA, hiring manager; raised from Low to Medium because JA is the high match): "10 years of experience" leads the reader to expect design decisions, scale and leadership, but the bullets show maintenance and tickets. Fix: show senior-level work in the current role (design of services, mentoring, decisions with trade-offs), only where true.
- **ACH-7** (Single source 1, JA, hiring manager; raised from Low to Medium): No scale is given for the product, company or team at any employer. Fix: add team size, number of services and traffic or users, as `[N]` placeholders until the candidate supplies real figures.
- **ACH-13** (Single source 1, JA, hiring manager; raised from Low to Medium): Bullets do not start with action verbs: "Responsible for developing", "Responsible for maintaining". Fix: start with varied verbs (Built, Designed, Cut, Migrated).
- **ACH-9** (Single source 1, JA, hiring manager; raised from Low to Medium): Nothing shows recent learning; the stack has not visibly changed since 2018. Fix: show any newer tool or practice adopted at work in the last two years, if there is one.
- **SKL-18** (Single source 1, JA, hiring manager; raised from Low to Medium): The skills list ends with "Git, Jira, Agile", which every engineer uses. Fix: remove them and use the space for testing and cloud tools.
- **SKL-8** (Single source 1, JA, hiring manager; raised from Low to Medium): The skills section is one flat list. Fix: group into languages and frameworks, data and messaging, infrastructure, testing.

### Low
- **RED-4** (Single source 1, TW, agency recruiter, Low): "Responsible for developing ..." is the phrasing TW names as reading like generic or AI-written text. Fix: covered by the ACH-1 rewrites.
- **STR-7** (Single source 1, TW, agency recruiter, Low): No company context under any role. Quillstone Software, Mervale Systems and Ostrava Infotech will be unknown to a UK screener (SCR-6). Fix: under each recent role, 2 to 4 lines (STR-8) on what the company does, its product and the team.
- **ACH-2** (Single source 1, JB, former recruiter, Low): No business domain or end customers are named for any role. Fix: say which domain (for example payments, logistics) and who used the product.
- **REG-5** (Single source 1, SB, agency recruiter, Low): The header says "Pune, India" but nothing says the candidate would relocate to the UK. Fix: add "Open to relocating to the UK" to the header or summary. See REG-16 below.
- **REG-15** (Single source 1, JB, former recruiter, Low): Right-to-work status for the UK is not stated. Fix: state the status plainly in the header line only if it helps; per REG-2 (Single source 1, JB, Low), do not write that sponsorship is needed.
- **CHN-5** (Single source 1, SB, agency recruiter, Low): No LinkedIn URL in the header. Fix: add it, and make sure it matches the CV (CHN-20).

### Judgment calls
- **REG-16** (Contested 1-1): For: TW says location filters and client ATS systems screen out applicants from abroad (TW-59, TW-60). Against: JA, the high match, says skill gaps reject candidates, not location (JA-40). Recommendation: fix the High findings first, then add one line with the real city and readiness to relocate (REG-14, REG-5), so location is a known fact rather than a surprise.
- **SKL-5** (Contested 1-1): For: SB says cloud providers are interchangeable and the core stack counts most (SB-36). Against: JA says they are not interchangeable (JA-56). The CV names no cloud provider at all, only "Docker". Recommendation: follow JA; if the candidate has deployed on AWS, GCP or Azure, name it in the role where it was used, and match the provider in each job ad where true.
- **STR-2** (Contested range 4): The CV is about one page for 10 years. JA (high match) prefers one page; TW and JB accept two or more. Recommendation: one page is fine; adding results and company context may push it to two, which is acceptable. Do not go to three.

## Rewrites

**Summary**
- Before: "Backend engineer with 10 years of experience in Java and Spring Boot. Hard-working team player with strong communication skills."
- After: "Senior backend engineer with 10 years building Java and Spring Boot services, most recently REST APIs and microservices on PostgreSQL at Quillstone Software. [Strongest result, for example: cut API latency by [X%] for [N users]]. Experienced with Kafka and Redis in production. Based in Pune, open to relocating to the UK."

**Quillstone Software, first bullet**
- Before: "Responsible for developing REST APIs in Java and Spring Boot."
- After: "Built [N] REST APIs in Java and Spring Boot for [product or feature], serving [N requests per day or N users]."

**Quillstone Software, database bullet**
- Before: "Responsible for maintaining the PostgreSQL database."
- After: "Improved the PostgreSQL database behind [service] by [what was done, for example query tuning or schema changes], reducing [query time or incidents] by [X%]."

**Quillstone Software, microservices bullet**
- Before: "Worked on microservices."
- After: "Designed and delivered [service name or purpose] as one of [N] Spring Boot microservices, owning it from design to release and [what changed after release]."

**Quillstone Software, production support bullet**
- Before: "Handled production support tickets."
- After: "Resolved [N] production incidents per [month or quarter] and fixed the root cause of [recurring issue], cutting related tickets by [X%]."

**Mervale Systems, Kafka bullet**
- Before: "Worked with Kafka and Redis."
- After: "Built [event flow or feature] on Kafka and added Redis caching to [service], [result, for example reducing response time by [X%]]."

**Skills**
- Before: "Java, Spring Boot, Hibernate, PostgreSQL, MySQL, Kafka, Redis, Docker, REST, Microservices, Git, Jira, Agile"
- After: "Languages and frameworks: Java, Spring Boot, Hibernate, REST. Data and messaging: PostgreSQL, MySQL, Kafka, Redis. Infrastructure: Docker, [cloud provider if used]. Testing: [testing tools actually used]."

## What already works
- Title under the name matches the target role, "Senior Backend Engineer" (STR-25, STR-20), and is not tied to one language (STR-16).
- The most recent role is first and shows the core stack, Java, Spring Boot, PostgreSQL; roles are in reverse date order (SCR-2, SCR-7).
- Java and Spring Boot are present, so no core skill of a Java backend role is missing (RED-2).
- Plain, single-column layout with no graphics or photo (STR-3, REG-7).
- Current city stated in the header (REG-14), and contact details include an email and a phone number with the country code (REG-3); the country code matches the stated location (REG-17).
- Each role heading leads with the job title, gives the employer's location and start and end months (STR-14, STR-19, STR-24).
- Kept to about a page with older roles short (STR-1); no gaps between roles (GAP-2, GAP-3).
- Education names the university and the degree (STR-27).
- A grouped-ready skills section on page one (SKL-16, SKL-1), with no proficiency labels (SKL-17).

## Beyond the CV
- **CHN-15** (Consensus 3): ask for referrals into UK product companies; a referral gets the CV read more carefully, which matters for an applicant from abroad.
- **CHN-18** (Consensus 3): keep the LinkedIn profile complete (photo, full job history with what was done, a bio) and consistent with the CV (CHN-20, Single source 1, TW).
- **CHN-16** (Supported 2): network with UK engineers and recruiters alongside applications.
- **CHN-17** (Supported 2): send the hiring manager a short message saying why the candidate fits the role.
- **CHN-10** (Single source 1, TW): use a standard title such as "Senior Backend Engineer" on LinkedIn so recruiters searching UK roles find the profile.

## Not covered by the evidence
- No job description was given. Check each ad's must-have terms against the CV (ATS-1, RED-6, SKL-11 at JA's 80 percent) before applying; this review only covers a generic Java backend stack.
- UK visa routes and sponsorship are out of scope for the evidence; general advice: research which UK employers hold sponsor licences before applying.
- Whether specific Indian employers are recognized by UK screeners is not covered beyond STR-7 and ACH-2; general advice: one line of company context per role helps.
- No recruiter in the evidence specializes in Java backend hiring; JA hires across engineering roles at a UK product company and is the closest match.
