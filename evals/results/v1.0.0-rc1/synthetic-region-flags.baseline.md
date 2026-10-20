# CV review: Mateus Ferreira-Lindqvist (synthetic-region-flags)

Target: Senior Java Engineer, employers in Germany and Austria, visa sponsorship needed.

## Verdict: borderline

The core is strong. He has 10 years of Java, a relevant domain (banking payments) and two quantified wins (2M transactions a day, 38% latency cut). A DACH recruiter will still hesitate for three reasons: the CV calls his English "Intermediate", he is offshore and needs a visa with no relocation signal, and the most recent role, which carries the senior claim, has only two bullets. Each of these can be fixed on paper. If the English line stays as it is, many recruiters will reject the CV at the screen.

## Problems by severity

### Critical

1. **"English: Intermediate" next to "German: A1".** For a non-German speaker applying in DACH, English is the working language. "Intermediate" tells the recruiter he cannot work in English, and a senior role needs design discussions and stakeholder communication. If his real level is B2/C1, write that. If it really is intermediate, that is a gap he has to close before applying, not a wording problem.
2. **Sponsorship flag with nothing to reduce the risk.** The bold "Requires visa sponsorship" line, placed on its own under the header, raises the cost question before anyone has read the experience. It is right to be open about it, but frame it as eligibility: Blue Card eligible, recognised degree, willing to relocate, available within a stated notice period. Germany's Blue Card is quick for IT roles above the salary threshold, and employers react better to "eligible" than to "requires".

### Major

3. **The current senior role is thin.** Banco Arvoredo, 2020 to present, has two bullets. Nothing shows senior scope: team size, mentoring, design ownership, on-call/reliability, PCI-DSS or regulatory work, code review standards. Banking compliance experience matters to German and Austrian banks and fintechs.
4. **Skill star ratings.** Star ratings carry no information and invite the reader to count down: "Kubernetes 2/5, AWS 2/5" reads as a weakness list. German ATS parsers also handle the symbols badly. Use a plain grouped list instead.
5. **Earlier roles have one bullet each, with no outcome.** "Built checkout and inventory APIs" and "Maintained Java EE applications" give no scale, impact or technology version.
6. **No location or relocation signal.** The header gives only Recife, Brazil. Add "Relocating to Germany/Austria" and the notice period.

### Minor

7. **Dates are years only.** DACH recruiters expect MM/YYYY.
8. **No phone, LinkedIn or GitHub.** For an international candidate, LinkedIn is the first thing they check.
9. **The profile is one generic line.** Use it to state the target and the visa/relocation position in one place.
10. **The photo is fine for DACH.** A professional headshot is common and accepted in Germany and Austria, so keep it. Remove it for other markets (UK, US, Ireland).
11. **Education does not say whether the degree is recognised.** Add a note that the degree is recognised (anabin H+), if it is, because it speeds up the Blue Card.

## Rewrites

**Header**
```
Mateus Ferreira-Lindqvist
Senior Java Engineer | Recife, Brazil, relocating to Germany or Austria
+55 ... | mateus.fl@example.com | linkedin.com/in/... | github.com/...
EU Blue Card eligible (recognised CS degree) | Available on 2 months' notice
```

**Profile**
```
Senior Java engineer with 10 years building payment and e-commerce backends in
Java 17, Spring Boot and Kafka. Currently runs card payment services at 2M
transactions a day for a Brazilian bank. Looking for a senior backend role in
Germany or Austria; EU Blue Card eligible and ready to relocate. Works in English
(C1); learning German (A1, course in progress).
```
(Write C1 only if it is true; if not, say B2 and get a certificate.)

**Banco Arvoredo, Senior Software Engineer, 03/2020 to present**
```
- Built and own payment microservices (Java 17, Spring Boot) processing 2M
  transactions a day at [X]% availability.
- Led migration of the card authorisation service to Kafka, cutting p99
  latency by 38%.
- [Mentored N engineers / led a team of N; ran design reviews for X.]
- [Delivered PCI-DSS / central bank compliance work: ...]
```

**Lojamar Commerce, Software Engineer, MM/2017 to MM/2020**
```
- Built checkout and inventory APIs in Java and Spring serving [N orders/day];
  [result, e.g. cut checkout errors by X%].
```

**Tecnorte Sistemas, Software Engineer, MM/2014 to MM/2017**
```
- Maintained and extended Java EE policy systems for [N] insurance clients;
  [one concrete improvement].
```

**Skills**
```
Languages and frameworks: Java (8 to 17), Spring Boot, Spring, Java EE
Messaging and data: Kafka, PostgreSQL
Infrastructure: Docker, Kubernetes, AWS
```

**Languages**
```
Portuguese (native), English (C1, or the true CEFR level with a certificate), German (A1, learning)
```

**Education**
```
BSc Computer Science, Universidade Federal de Pernambuco, 2014 (recognised in Germany, anabin H+)
```
