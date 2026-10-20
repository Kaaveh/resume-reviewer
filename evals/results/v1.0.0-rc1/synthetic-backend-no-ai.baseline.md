# CV review: Priya Vantongeren

Target: Senior Backend Engineer (Java), UK product companies, relocating from India.

## Verdict: reject (as written)

The underlying profile (10 years of Java, Spring Boot, Kafka, Redis, PostgreSQL, current Senior title) fits the target role. The CV does not show it. Every bullet lists duties rather than results, so nothing shows the seniority, scale or impact a UK product company looks for. A sponsored overseas hire also has to clear a higher bar than a local candidate, and the CV never mentions relocation or visa status. A recruiter skimming for 10 to 30 seconds has no reason to pick this over a local candidate with numbers. The profile could reach "invite" once rewritten.

## Problems by severity

### Critical

1. **Duty-only bullets, no outcomes or scale.** "Responsible for developing REST APIs", "Worked on microservices", "Fixed bugs and implemented new features". These describe a job description, not achievements. None of them has a number: no traffic (RPS, users), data volume, latency, uptime, cost, team size or delivery speed. For a Senior role this is the main reason to reject.
2. **No evidence of senior-level scope.** The current role shows no design ownership, technical decisions, mentoring, incident leadership or cross-team work. "Participated in code reviews and sprint planning" reads as a mid-level engineer. Show what you designed, led and decided.
3. **Relocation and right to work not addressed.** A UK recruiter will wonder at once whether the candidate needs sponsorship and when they could start. Leaving it out reads as a hidden problem and often leads to a silent rejection. State it in the header.

### Major

4. **Years of experience contradict the dates.** The summary says 8 years, but the roles run from Jun 2016 to the present (about 10 years). Recruiters notice this, and it looks careless. Use the correct figure (10+), or "8 years of backend work" only if you deliberately leave out the junior role, and then say so.
5. **Generic summary.** "Hard-working team player with strong communication skills" says nothing and wastes the most-read lines. Replace it with what you build, at what scale, and what you are looking for.
6. **Product-company signals missing.** UK product companies want to see what the product is, who uses it and how your work moved a metric. "Quillstone Software" and "Mervale Systems" are unknown names, so add one line on each: what the company or product does, and the domain (fintech, logistics, SaaS and so on).
7. **Skills list missing modern expectations.** There is no cloud (AWS, GCP or Azure), Kubernetes, CI/CD, testing (JUnit, Testcontainers), observability (Prometheus, Grafana, ELK) or Java version. A UK Senior Java posting will usually ask for most of these, and ATS keyword matching will penalise their absence. List only what you have actually used.

### Minor

8. **"Handled production support tickets"** sounds like L2 support. Reframe it as on-call and incident ownership, with an outcome (MTTR, number of recurring incidents removed).
9. **Older roles are too thin.** Mervale (nearly 3 years) has three vague bullets. Give it two or three concrete achievements. Ostrava can stay short.
10. **No links.** Add GitHub (if it has meaningful content) and LinkedIn. A LinkedIn profile helps overseas candidates in particular because recruiters use it to verify history.
11. **Phone and location.** Keep the +91 number but also give a time zone or availability for calls in UK hours. Drop "Pune, India" as a bare location and pair it with the relocation line.
12. **Agile and Jira in skills** add nothing at senior level. Remove them to make room for stronger keywords.

## Rewrites

Placeholders in [brackets] must be filled with real figures. Do not invent numbers. An honest estimate ("about 2k RPS") is fine.

### Header

```
Priya Vantongeren
Senior Backend Engineer (Java, Spring Boot, Kafka)
Pune, India. Relocating to the UK; requires Skilled Worker visa sponsorship. Notice period: [X weeks].
priya.v@example.com | +91 98200 55501 | linkedin.com/in/[handle] | github.com/[handle]
```

### Summary

```
Senior backend engineer with 10 years of Java, building [domain, e.g. payments / B2B SaaS]
services on Spring Boot, Kafka and PostgreSQL. Currently own [N] microservices handling
[X requests/day or X events/day] at Quillstone, where I led [one headline result, e.g. the
move from a monolith to event-driven services, cutting p99 latency from X to Y ms].
Looking for a senior backend role at a UK product company.
```

### Quillstone Software, Senior Backend Engineer (Apr 2021 to present)

Add one context line: `[What the product does, who uses it, scale.]`

Before:
- Responsible for developing REST APIs in Java and Spring Boot.
- Responsible for maintaining the PostgreSQL database.
- Worked on microservices.
- Participated in code reviews and sprint planning.
- Handled production support tickets.

After:
- Designed and built [N] Spring Boot REST services for [feature/domain], serving [X] requests/day at p99 [Y] ms.
- Cut [query / endpoint] latency by [X%] by [indexing, query rewrites, partitioning] on a [size] PostgreSQL database.
- Led the split of [module] out of the monolith into [N] Kafka-driven services, reducing deploy time from [X] to [Y].
- Set code review standards and mentored [N] engineers; [result, e.g. two promoted, review turnaround down from X to Y days].
- Own on-call for [N] services; reduced recurring incidents by [X%] through [alerting, retries, idempotency fixes].

### Mervale Systems, Backend Engineer (Jul 2018 to Mar 2021)

Before:
- Developed backend services in Java.
- Worked with Kafka and Redis.
- Fixed bugs and implemented new features.

After:
- Built [service] in Java consuming [X] Kafka events/day for [purpose], with exactly-once / idempotent processing.
- Added a Redis caching layer to [service], cutting database load by [X%] and response time from [X] to [Y] ms.
- Delivered [feature] used by [N customers / X% of users], [business result].

### Ostrava Infotech, Junior Developer (Jun 2016 to Jun 2018)

- Built [module] in Java and Hibernate for [client/domain]; optimised SQL reports, reducing run time from [X] to [Y].

### Skills (grouped, only what you have used)

```
Languages: Java [17/21], SQL
Frameworks: Spring Boot, Spring Data/JPA, Hibernate
Data and messaging: PostgreSQL, MySQL, Kafka, Redis
Cloud and delivery: [AWS/GCP services], Docker, [Kubernetes], [Jenkins/GitHub Actions]
Quality and operations: [JUnit 5, Mockito, Testcontainers], [Prometheus, Grafana, ELK]
```

## Next steps, in priority order

1. Add the relocation and sponsorship line and fix the years figure (10 minutes, removes two easy rejection triggers).
2. Rewrite the Quillstone bullets with real numbers and ownership.
3. Replace the summary.
4. Fill out the skills you actually have (cloud, testing, observability).
5. Target companies that are licensed UK visa sponsors (the gov.uk register of licensed sponsors) so the sponsorship need is not a blocker.
