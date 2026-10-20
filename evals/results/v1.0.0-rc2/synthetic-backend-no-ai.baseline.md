# CV review: Priya Vantongeren, Senior Backend Engineer (Java), UK product companies, relocating from India

## Verdict: reject (as written)

The underlying profile fits: 10 years of Java, Spring Boot, PostgreSQL, Kafka and Redis, three jobs that move steadily up in seniority, no gaps. But the CV gives a UK recruiter nothing to tell this person apart from hundreds of other Java applicants. Every bullet describes a duty, none shows an outcome, and nothing proves senior scope (design ownership, mentoring, scale, incidents). The candidate also needs visa sponsorship, which raises the bar, and the CV doesn't address relocation at all. A UK product company sponsoring a hire wants clear evidence that this person beats local candidates, and the CV doesn't give it. If the content were rewritten with real impact, this would likely be at least borderline and possibly an invite.

## Problems by severity

### Critical

1. **Every bullet is a duty, with no impact or outcomes.** "Responsible for developing REST APIs", "Worked on microservices", "Fixed bugs and implemented new features" and "Wrote SQL queries" would fit any backend engineer at any level. There are no numbers at all: no traffic, latency, data volume, uptime, cost, team size or release frequency. UK product companies screen for ownership and impact, so this is the main reason for rejection.
2. **Senior-level work isn't shown.** The title says Senior, but the Quillstone bullets ("Participated in code reviews and sprint planning", "Handled production support tickets") read as mid-level. Nothing mentions system design decisions, technical leadership, mentoring, cross-team work, incident ownership, or improving architecture or reliability.
3. **Relocation and right to work aren't addressed.** The header says only "Pune, India". UK recruiters will assume sponsorship is needed and will often filter out the CV before reading further. State the situation plainly, for example: "Relocating to London (or UK-wide). Requires Skilled Worker visa sponsorship. Available within 60 days." If any part doesn't apply (for example, a spouse visa or a Global Talent route), say that, because it changes the outcome.

### Major

4. **Employers aren't described.** Quillstone, Mervale and Ostrava are unknown names in the UK. The reader can't tell whether these are product companies or IT services and outsourcing firms. That matters a lot for "UK product companies": services experience gets discounted unless the CV shows product ownership. Add a one-line description under each employer (what it builds, for whom, and at what scale).
5. **The summary is generic.** "Hard-working team player with strong communication skills" is unprovable filler. Replace it with specifics: domain, scale, what the candidate is best at, and the relocation line.
6. **Gaps in the modern stack expected in UK job ads.** There's no Java version (8 versus 17/21 matters), no cloud provider (AWS, GCP or Azure), no Kubernetes, no CI/CD, no testing (JUnit, Testcontainers), and no observability tools (Prometheus, Grafana, Datadog, ELK). If the candidate has used these, they're missing from the CV. If not, the CV will lose to ones that list them, because UK job descriptions almost always ask for cloud and testing practice.
7. **Kafka and Redis appear without context.** "Worked with Kafka and Redis" is the most valuable line in the CV, but it doesn't say what was built (event-driven pipelines, caching layer, throughput).

### Minor

8. **No LinkedIn or GitHub link.** UK recruiters routinely check LinkedIn, especially for international candidates.
9. **Older roles take too much space relative to their value.** The 2016 to 2018 junior role can be cut to one line. Spend that space on the Quillstone role.
10. **Skills list is unprioritised and padded.** "Git, Jira, Agile" add nothing at senior level. Group skills (Languages, Frameworks, Data, Messaging, Cloud/DevOps, Testing) and put the strongest first.
11. **Dates.** "Apr 2021 to present" is fine; use the same month-year format everywhere (it already does). Check UK spelling throughout, for example "optimised".
12. **Education** is fine as is. Optional: add "(equivalent to a UK Bachelor's degree)" if the candidate wants to remove doubt.

## Rewrites

Placeholders in [brackets] must be replaced with real numbers. Don't invent figures: if a number isn't known, estimate it honestly ("~", "over") or describe scope in words.

### Header

> **Priya Vantongeren**
> Senior Backend Engineer (Java, Spring Boot, Kafka)
> Pune, India. Relocating to London / UK. Requires Skilled Worker visa sponsorship. Notice period: [60] days.
> priya.v@example.com | +91 98200 55501 | linkedin.com/in/[handle] | github.com/[handle]

### Summary

> Senior backend engineer with 10 years building Java and Spring Boot services, most recently [payments / logistics / SaaS domain] microservices handling [X requests per day / X events per second]. Strongest in event-driven design with Kafka, PostgreSQL performance and production reliability. Led [N] engineers on [system]. Looking for a senior backend role at a UK product company.

### Quillstone Software, Senior Backend Engineer (Apr 2021 to present)

*[One line: what Quillstone builds, for whom, and at what scale, for example "B2B SaaS platform for [industry], [N] customers".]*

- Designed and built [N] Spring Boot microservices for [capability], serving [X] requests/day at p99 latency under [Y] ms.
- Cut [query / endpoint] latency by [X]% by redesigning PostgreSQL indexes and queries on tables with [N] million rows.
- Led the move from [monolith / synchronous calls] to [event-driven Kafka flows], reducing [failed orders / coupling / deploy time] by [X].
- Owned on-call for [N] services; brought monthly P1 incidents down from [X] to [Y] by adding [alerting / retries / idempotency].
- Mentored [N] engineers and set code review standards adopted by [team / org].

### Mervale Systems, Backend Engineer (Jul 2018 to Mar 2021)

*[One line describing the company.]*

- Built a Kafka-based [pipeline / notification system] processing [X] events/day.
- Added a Redis caching layer for [service], cutting database load by [X]% and response time from [A] to [B] ms.
- Shipped [feature] used by [N] customers / contributing [business outcome].

### Ostrava Infotech, Junior Developer (Jun 2016 to Jun 2018)

- Built Java and Hibernate modules for [product / client domain].

### Skills

> **Languages:** Java [17/21], SQL
> **Frameworks:** Spring Boot, Spring Data, Hibernate
> **Data and messaging:** PostgreSQL, MySQL, Kafka, Redis
> **Cloud and DevOps:** Docker, [Kubernetes, AWS services, CI/CD tool] *(only if actually used)*
> **Testing and observability:** [JUnit, Testcontainers, Prometheus/Grafana] *(only if actually used)*

## Priority order for the candidate

1. Add the relocation, sponsorship and notice line to the header.
2. Rewrite the Quillstone bullets with outcomes and numbers, including at least one bullet that shows senior ownership.
3. Add one-line company descriptions, emphasising any product ownership.
4. Fill in the cloud, testing and Java version gaps if they're true.
5. Replace the summary and tidy up the skills.
