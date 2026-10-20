# CV review: Senior DevOps Engineer for Halvard Logistics, Amsterdam (relocation offered)

**Verdict:** Reject

**10-second verdict:** At the top of page one a screener sees "DevOps Engineer | Lagos, Nigeria", a one-line summary that ends "for on-premise data centres", and a most recent role (Senior DevOps Engineer, Tarnwick Payments) built on Jenkins, bare-metal Kubernetes with Rancher and Terraform with the vSphere provider. The job's first technical must-have is production AWS (EKS, IAM, VPC, RDS), and AWS appears nowhere on the CV. A screener checking for the required stack (SCR-1, SCR-7, SCR-4: about 10 seconds for JA) stops here. The rest of the CV is solid DevOps work, but it does not get read. Since the candidate would be hired from abroad, the bar is higher, not lower (SEN-6, JA context).

**Target and weighting:** From the request and job description: Senior DevOps Engineer, 5+ years, AWS platform team, Amsterdam (mainland EU), candidate based in Lagos needing relocation, which the employer offers. Match: JA high (hiring manager at a cloud-based tech product company, reviewed a 6-year DevOps CV live), JB medium-high (infrastructure and IT hiring, cross-border EMEA), TW medium-high (UK and Europe, tech and platform roles), SB low (JavaScript and TypeScript startups only). No recruiter in the evidence hires in the Netherlands (see Not covered by the evidence).

## Findings

### Critical
- **RED-2** (Consensus 3, Critical): The job's core stack is AWS ("Production experience with AWS (EKS, IAM, VPC, RDS)" and "Terraform for AWS"). The CV shows no cloud provider at all: the summary says "on-premise data centres", Kubernetes runs "on bare metal with Rancher", and Terraform uses the "vSphere provider". Against the job's seven listed skills the CV shows about five (5+ years, Kubernetes and Helm, CI/CD, Prometheus and Grafana, Python), below JA's 80 percent bar (SKL-11, Single source 1) once AWS and Terraform for AWS are counted as missing. SCR-2 and SCR-7 (both Consensus 3) explain why this decides the outcome: the most recent role is read first and its stack does not match. Fix: if the candidate has used AWS anywhere (at work, in a side project, in a migration), name the services used and where, in the most recent role and the summary. If the candidate has not, do not add AWS to the CV (RED-3): build real AWS experience first (for example a project running EKS with Terraform's AWS provider, listed under ACH-4) and, until then, put this CV toward on-premise and hybrid platform roles where it is a strong match.

### High
- **ACH-1** (Consensus 4, High): The Tarnwick role passes, but the Brightmere Telecom bullets are duties without a result: "Maintained GitLab CI runners and a private Docker registry" and "Wrote Bash and Python scripts for backups and log rotation". Fix: say what changed because of the work (see Rewrites).
- **ACH-6** (Consensus 3, High): Tarnwick bullets carry strong numbers ("two days to three hours", "90 to 25 minutes"), but "Automated server provisioning with Ansible and Terraform (vSphere provider)" and every Brightmere bullet except the count in "Moved 25 applications" have no measured result. Fix: add the real figures through placeholders such as `[X hours to Y minutes]`; do not estimate.
- **ACH-4** (Consensus 3, High): No side projects or hackathons are listed. For this candidate a side project is also the honest route to the missing AWS evidence. Fix: list relevant projects only if they exist, with dates and context (STR-15); if the candidate builds an AWS project, it goes here.
- **SKL-4** (Supported 2, High): The CV says nothing about using AI tools in daily work. Fix: if the candidate uses AI coding or ops tools (for example to write Terraform, Helm charts or scripts), add one concrete bullet saying how. TW (SKL-7, Single source 1) adds that hiring managers want some exposure to AI tools. Do not add it if it is not true.

### Medium
- **STR-4** (Supported 2, Medium), with **STR-21** (Single source 1, JA, raised from Low to Medium because JA is the high match and the CV is in the situation he described) and **STR-6** (Single source 1, SB, Low): The summary is one generic line, "DevOps engineer with 6 years of experience building CI/CD pipelines, container platforms and monitoring for on-premise data centres". It is short of JA's 3 to 4 lines, names no tools, gives none of the CV's strong results, and leads with the one word ("on-premise") that signals the gap. Fix: 3 to 4 lines naming Kubernetes, Helm, Terraform, CI/CD and monitoring and the two best results (see Rewrites).
- **STR-25** (Single source 1, JA, raised from Low to Medium): The title under the name is "DevOps Engineer" while the job, and the candidate's own current title, is "Senior DevOps Engineer". Fix: write "Senior DevOps Engineer".
- **REG-8** and **REG-9** (each Single source 1, JA, raised from Low to Medium): The languages section lists only "English: IELTS 7.5 (Academic, 2023)". JA says many screeners do not know what an IELTS score means, and that listing English on an English CV adds nothing. Fix: remove the languages section, or if kept, write "English: fluent" without the test score (REG-6, Supported 2, is met either way).
- **STR-12** (Single source 1, JA, raised from Low to Medium): There is a References section with a named referee and that person's email. It adds nothing and puts a third party's contact details on every copy of the CV. Fix: delete the section; give references when asked.
- **SKL-8** (Single source 1, JA, raised from Low to Medium): The skills list is one flat line of 16 items. Fix: group it (see Rewrites).
- **SKL-3** (Supported 2, Medium): "ELK" is in the skills list but no role says where it was used. Fix: mention it in the role where it was used, or drop it.
- **SEN-7** (Single source 1, JA, raised from Low to Medium): Every bullet reads as solo work ("Built", "Ran", "Set up"); no team is mentioned. Fix: add team size and who the work served, for example "for [N] developers across [N] teams".
- **SKL-10** (Single source 1, JA, Medium, 1 report rejecting): No testing tools are named. Not raised to High: JA's evidence is about engineers writing application code, and for a DevOps role the closer fit is pipeline testing. Fix: if pipelines ran tests or infrastructure checks (for example Terraform validation, Helm chart linting, smoke tests), name the tools in the Jenkins or GitLab CI bullet.

### Low
- **REG-5** (Single source 1, SB, Low) and **REG-15** (Single source 1, JB, Low): The header says "Lagos, Nigeria" but nothing says the candidate will relocate to Amsterdam or what their right-to-work status is. Fix: add one line such as "Open to relocating to Amsterdam" (only if true). Do not write that sponsorship is needed (REG-2, Single source 1, JB); the job offers relocation.
- **ATS-1** (Single source 1, JB, Low): The job's terms "AWS", "EKS", "IAM", "VPC", "RDS", "GitHub Actions" and "platform engineering" are missing. Fix: use the job's wording only for experience the candidate really has; "CI/CD" can sit next to "Jenkins, GitLab CI" so the similarity is plain.
- **STR-7** (Single source 1, TW, Low) and **ACH-2** (Single source 1, JB, Low): No role says what the company does, its scale or who the end customers were (Tarnwick Payments is presumably payments, but the reader has to guess). Fix: one or two lines under each recent role heading, for example "[Payments processor serving N merchants]; platform team of [N]".

### Judgment calls
- **SKL-5** (Contested 1-1): For: SB says leaders treat AWS and GCP as interchangeable and weigh the core stack (SB-36). Against: JA says cloud providers are not interchangeable (JA-56). Recommendation: this CV does not have a different cloud, it has none, so even SB's view does not help. Treat the missing AWS as the Critical gap above (JA, high match).
- **REG-16** (Contested 1-1): For: TW says location filters screen out applicants from abroad (TW-59, TW-60). Against: JA says candidates blame location when skill gaps are the real reason (JA-40). Recommendation: the employer offers relocation, so fix the AWS gap first (JA), then add the relocation line under REG-5 so Lagos is a known fact rather than a surprise.

## Rewrites

**Header title**
- Before: "DevOps Engineer | Lagos, Nigeria"
- After: "Senior DevOps Engineer | Lagos, Nigeria | Open to relocating to Amsterdam" (relocation line only if true)

**Summary**
- Before: "DevOps engineer with 6 years of experience building CI/CD pipelines, container platforms and monitoring for on-premise data centres."
- After: "Senior DevOps engineer with 6 years of experience running Kubernetes with Helm, infrastructure as code with Terraform and Ansible, CI/CD with Jenkins and GitLab CI, and Prometheus and Grafana monitoring for a payments platform. Cut release time across 40 services from two days to three hours and mean time to recovery from 90 to 25 minutes. [Add AWS experience here only if real, for example: built [project] on EKS with Terraform's AWS provider.]"

**Tarnwick Payments, provisioning bullet**
- Before: "Automated server provisioning with Ansible and Terraform (vSphere provider)."
- After: "Automated server provisioning with Terraform (vSphere provider) and Ansible, cutting new server setup from [X days] to [Y minutes]."

**Brightmere Telecom bullets**
- Before: "Moved 25 applications from VMs to Docker containers."
- After: "Moved 25 applications from VMs to Docker containers, [result, for example deployment time from X to Y or Z fewer VMs]."
- Before: "Maintained GitLab CI runners and a private Docker registry."
- After: "Ran GitLab CI runners and a private Docker registry for [N] developers and [N] pipelines, [result, for example build queue time from X to Y]."
- Before: "Wrote Bash and Python scripts for backups and log rotation."
- After: "Automated backups and log rotation across [N] servers with Bash and Python, replacing [X hours] of manual work per week."

**Skills**
- Before: "Kubernetes, Docker, Helm, Rancher, Jenkins, GitLab CI, Ansible, Terraform, Prometheus, Grafana, ELK, Linux, Bash, Python, Nginx, vSphere"
- After:
  - Containers and orchestration: Kubernetes, Helm, Rancher, Docker
  - Infrastructure as code: Terraform, Ansible
  - CI/CD: Jenkins, GitLab CI
  - Monitoring and logging: Prometheus, Grafana, ELK
  - Systems and scripting: Linux, Nginx, vSphere, Bash, Python

**Languages and References**
- Before: "English: IELTS 7.5 (Academic, 2023)" and the References section with a named referee
- After: remove both sections (or "English: fluent" if a languages line is kept).

## What already works
- Most recent role leads with measurable results: "cutting release time from two days to three hours" and "mean time to recovery fell from 90 to 25 minutes" (ACH-1, ACH-6, ACH-10).
- Scale is visible: "40 services", "12-node Kubernetes cluster", "150 Linux servers" (ACH-7).
- Kubernetes, Helm, Terraform, CI/CD, Prometheus, Grafana and Python, six of the job's listed items, are named in the context of real work (SKL-12, SKL-3 for all but ELK).
- Plain, one-page layout with no graphics or photo (STR-3, REG-7), fitting JA's one-page view for 6 years (STR-2).
- Experience in reverse date order with months, job title first and employer location on each role (SCR-2, STR-24, STR-14, STR-19); no gaps between roles (GAP-2, GAP-3).
- City stated truthfully, email, phone with country code and a LinkedIn URL in the header (REG-14, REG-3, CHN-5).
- Education with university and degree (STR-27); bullets start with varied action verbs and stay to one line (ACH-13, STR-22); no em-dashes (RED-5).

## Beyond the CV
- **CHN-15** (Consensus 3): Ask for a referral into Halvard Logistics or similar AWS teams; a referral gets the CV read more carefully, which matters when one gap would otherwise end the first pass. JB reports 70 percent of his placements came through referrals (CHN-4, Single source 1).
- **CHN-17** (Supported 2): Send the hiring manager a short message on why the candidate fits: the Kubernetes, Terraform and on-call results, and any real AWS work.
- **CHN-16** (Supported 2): Network alongside applications rather than relying on cold applications from abroad.
- **CHN-18** (Consensus 3) and **CHN-20** (Single source 1, TW, Medium): Keep LinkedIn complete and consistent with the CV, including the same title ("Senior DevOps Engineer") and dates.

## Not covered by the evidence
- **Market.** No recruiter in the evidence hires in the Netherlands or mainland Europe; Dutch CV conventions and how Amsterdam employers weigh applicants from Nigeria are not covered.
- **How to gain AWS experience.** Which certifications or project types Dutch employers credit is not in the evidence. General advice: an AWS certification together with a small, real EKS project built with Terraform's AWS provider is a common way to show the skill honestly.
- **Visa routes.** Dutch highly skilled migrant rules and relocation timing are out of scope; general advice only, confirm with the employer.
- **On-premise to cloud framing.** Whether recruiters credit on-premise Kubernetes and Terraform as transferable to AWS is only partly covered (SKL-5 is contested and about different clouds, not no cloud).
