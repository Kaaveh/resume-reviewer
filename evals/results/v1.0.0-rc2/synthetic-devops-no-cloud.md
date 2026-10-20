# CV review: Senior DevOps Engineer (Halvard Logistics) for Amsterdam, Netherlands, with relocation from Nigeria

**Verdict:** Reject

**10-second verdict:** The top of page one reads "DevOps Engineer | Lagos, Nigeria", then a summary that ends "for on-premise data centres", then "Senior DevOps Engineer, Tarnwick Payments" with Jenkins, bare-metal Kubernetes on Rancher and "Terraform (vSphere provider)". A screener checking for this job's stack (SCR-7, SCR-2) looks for AWS first, because the ad opens with "We run our platform on AWS" and lists AWS as a must-have. AWS appears nowhere on the CV, and the summary itself tells the reader the work was on-premise. Most screeners stop here (RED-2, SCR-1). The Kubernetes, Helm and monitoring work is relevant and well quantified, but it does not get read.

**Target and weighting:** From the request and job description: Senior DevOps Engineer, Halvard Logistics, Amsterdam (mainland Europe), relocation offered; candidate based in Lagos, so relocation is needed. Match: JA high (hiring manager at a tech product company, reviewed a DevOps CV live, holds the strictest view on cloud providers), TW medium-high (agency, UK and Europe), JB medium-high (cross-border hires across EMEA, infrastructure background), SB low (JavaScript and TypeScript startups only). No recruiter in the evidence hires in the Netherlands, so local conventions there are not covered.

## Findings

### Critical
- **RED-2** (Consensus 3, Critical): The job's core platform is AWS, and "Production experience with AWS (EKS, IAM, VPC, RDS)" and "Terraform for AWS" are must-haves. The CV shows no cloud provider at all: the summary says "on-premise data centres", the cluster is "on bare metal with Rancher", and Terraform is used with the "vSphere provider". Three recruiters report rejecting on a missing core skill. Even SB's view that AWS and GCP are interchangeable (SKL-5) does not help here, because there is no cloud provider to swap. Fix: this cannot be fixed by wording. If the candidate has any real AWS work (a project at work, a migration pilot, a personal lab on EKS, a certification), put it in the most recent role or a projects section with what was built. If not, either build real AWS experience before applying (see ACH-4) or target roles that run Kubernetes on-premise or on bare metal, where this CV is a strong fit. Never add AWS, EKS or RDS without having used them (RED-3).

### High
- **RED-6 / SKL-11** (Single source 1, raised from Medium to High because JA is the high match and this CV is exactly the case JA described): Counting the ad's named skills (AWS, EKS, IAM, VPC, RDS, Terraform, Kubernetes, Helm, CI/CD, GitHub Actions, Prometheus, Grafana, Python, Go), the CV shows about 7 of 14, around 50 percent, against JA's 80 percent. Every missing item is in the AWS group plus GitHub Actions and Go. Fix: the same as RED-2; the gap closes only with real AWS experience.
- **ACH-4** (Consensus 3, High): No side projects or hackathons are listed. For this CV a side project is the most direct honest route to closing the AWS gap. Fix: if the candidate has a personal or open source project on AWS, add it with dates and context (STR-15); if not, a small project that runs the existing skills on AWS (EKS, Terraform with the AWS provider, IAM and VPC set up from code) would give a screener something real to read.
- **ACH-1** (Consensus 4, High): The Tarnwick Payments bullets are good (problem, own work, result). The Brightmere Telecom role is mostly duties: "Maintained GitLab CI runners and a private Docker registry" and "Wrote Bash and Python scripts for backups and log rotation" say what was looked after, not what changed. Fix: for each, add why it was needed and what it changed, with [placeholders] for numbers the candidate can supply (see Rewrites).
- **SKL-4** (Supported 2, High): The CV does not mention any use of AI tools in daily work (also SKL-7, Single source 1). Fix: if the candidate uses AI coding assistants, for example to write Terraform, Helm charts or scripts, add one concrete line about it in the most recent role. If not, leave it out rather than claim it (RED-3).

### Medium
- **STR-4, STR-21, STR-6** (Supported 2, Medium; STR-21 and STR-6 Single source 1, raised from Low to Medium because JA is the high match): The summary is one line and frames the candidate against this job: "DevOps engineer with 6 years of experience building CI/CD pipelines, container platforms and monitoring for on-premise data centres." JA expects 3 to 4 lines that say who the candidate is, the specialism and why they fit. Fix: a 3 to 4 line summary that leads with Kubernetes, Helm, Terraform, CI/CD and monitoring results, names any real AWS work, and states relocation (see Rewrites). Also check the year count: the DevOps roles run from Jun 2019 to now, which is more than 6 years, so confirm the figure.
- **STR-25** (Single source 1, raised from Low to Medium, JA high match): The title under the name is "DevOps Engineer", while the job is "Senior DevOps Engineer" and the candidate's current title is "Senior DevOps Engineer". Fix: use "Senior DevOps Engineer" under the name.
- **SKL-3** (Supported 2, Medium): "ELK" is in the skills list but no role says where it was used. Fix: add it to the role where it was used (for example alongside the Prometheus and Grafana bullet), or drop it.
- **SKL-8** (Single source 1, raised from Low to Medium, JA high match): The skills section is one flat line of 16 items. Fix: group it, for example containers and orchestration, infrastructure as code, CI/CD, monitoring and logging, languages and OS.
- **REG-8 / REG-9** (Single source 1 each, raised from Low to Medium, JA high match): "English: IELTS 7.5 (Academic, 2023)" lists an English test score and English itself on an English CV. JA says recruiters do not know what the scores mean and listing English adds nothing. Fix: remove the Languages section; the CV itself shows working English (REG-6).
- **STR-12** (Single source 1, raised from Low to Medium, JA high match): There is a References section that also gives a named person's contact details. Fix: delete the section; it adds nothing and shares a third party's details with every reader.
- **SEN-7** (Single source 1, raised from Low to Medium, JA high match): Every bullet reads as solo work ("Built", "Ran", "Set up"), with no team or collaborators. Fix: where true, say who the work was done with or for, for example "with [N] developers" or "for [N] product teams".
- **SKL-10** (Single source 1, 1 report rejecting, Medium; not raised, since JA described developer CVs and the fit to a DevOps CV is partial): No testing tools are named. Fix: if the pipelines ran automated tests, security scans or infrastructure tests, name the tools in the Jenkins bullet.
- **ACH-9** (Single source 1, raised from Low to Medium, JA high match): Nothing shows recent learning. Given the AWS gap, any real recent learning (an AWS course applied in a project, a certification) belongs on the CV. Fix: add it only if it exists.

### Low
- **ATS-1** (Single source 1, Low): The ad's wording "infrastructure as code", "platform engineering", "AWS", "EKS" and "GitHub Actions" do not appear. Fix: use "infrastructure as code" for the Terraform and Ansible work, which is true. Add the AWS terms and GitHub Actions only where the candidate has used them.
- **STR-7 / ACH-2** (Single source 1 each, Low): Roles have no company context: "Tarnwick Payments" and "Brightmere Telecom" do not say what the company does, its size or who the customers are. Fix: one or two lines under each recent role heading (TW suggests 2 to 4, STR-8).
- **REG-5 / REG-15** (Single source 1 each, Low): A candidate in Lagos applying to Amsterdam does not say they will relocate. Fix: add "Open to relocating to Amsterdam" to the header or summary. Do not state a need for sponsorship (REG-2); the job already offers relocation.

### Judgment calls
- **SKL-5** (Contested 1-1): For: SB says leaders treat AWS and GCP as interchangeable and weigh the core stack (SB-36). Against: JA says cloud providers are not interchangeable (JA-56). Recommendation: follow JA, the high match. In this case the question barely arises, because the CV has no cloud provider at all, so RED-2 stands either way.
- **REG-16** (Contested 1-1): For: TW says location filters and client ATS systems screen out applicants from abroad (TW-59, TW-60). Against: JA says skill gaps, not location, cause the rejections (JA-40). Recommendation: fix the AWS gap first, since that is what decides this application. Then keep "Lagos, Nigeria" (REG-14) and add the relocation line, so location is a known fact. The ad offers relocation, which lowers the location risk.

## Rewrites

**Header title**
- Before: "DevOps Engineer | Lagos, Nigeria"
- After: "Senior DevOps Engineer | Lagos, Nigeria | Open to relocating to Amsterdam"

**Summary**
- Before: "DevOps engineer with 6 years of experience building CI/CD pipelines, container platforms and monitoring for on-premise data centres."
- After: "Senior DevOps engineer with [N] years in DevOps and platform work at a payments company and a telecom. Runs Kubernetes and Helm in production (12-node cluster, 40 services) and manages infrastructure as code with Terraform and Ansible. Cut release time from two days to three hours with Jenkins pipelines and cut mean time to recovery from 90 to 25 minutes with Prometheus and Grafana alerting. [Only if real: AWS work, for example a project on EKS with Terraform.]"

**Brightmere Telecom, CI bullet**
- Before: "Maintained GitLab CI runners and a private Docker registry."
- After: "Ran GitLab CI runners and a private Docker registry for [N] teams and [N] builds a day, [result, for example cutting build queue time from X to Y minutes]."

**Brightmere Telecom, scripts bullet**
- Before: "Wrote Bash and Python scripts for backups and log rotation."
- After: "Automated backups and log rotation for [N] servers with Bash and Python, [result, for example removing X hours of manual work a week or preventing disk-full incidents]."

**Skills**
- Before: "Kubernetes, Docker, Helm, Rancher, Jenkins, GitLab CI, Ansible, Terraform, Prometheus, Grafana, ELK, Linux, Bash, Python, Nginx, vSphere"
- After:
  - Containers and orchestration: Kubernetes, Helm, Rancher, Docker
  - Infrastructure as code: Terraform (vSphere), Ansible
  - CI/CD: Jenkins, GitLab CI
  - Monitoring and logging: Prometheus, Grafana, ELK
  - Languages and systems: Python, Bash, Linux, Nginx, vSphere

**Company context (under the Tarnwick Payments heading)**
- After: "[What Tarnwick Payments does, for example a payments provider for N merchants], [team size]. Owned the delivery pipelines and the Kubernetes platform."

**Languages and References**
- Delete both sections.

## What already works
- The most recent role has measured results: "cutting release time from two days to three hours" and "mean time to recovery fell from 90 to 25 minutes" (ACH-6, ACH-1), and the numbers are not all round percentages (ACH-8).
- Scale is visible: "40 services", "12-node Kubernetes cluster", "150 Linux servers" (ACH-7).
- Kubernetes, Helm, Terraform, CI/CD, Prometheus, Grafana and Python, all asked for in the ad, are named and tied to roles (SKL-1, SKL-3, SKL-12).
- Plain one-page layout, no photo, reverse date order, title first in each role heading, months on all dates, employer locations given (STR-3, REG-7, SCR-2, STR-14, STR-24, STR-19).
- Header gives the real city, email, phone with country code and a LinkedIn URL (REG-14, REG-3, CHN-5).
- Education names the university and degree (STR-27).
- Bullets start with varied action verbs and stay to one line (ACH-13, STR-22). No em-dashes (RED-5).

## Beyond the CV
- **CHN-15** (Consensus 3): Ask for a referral into Halvard Logistics if anyone in the candidate's network works there; a referred CV gets a closer read.
- **CHN-17** (Supported 2): Send the hiring manager a short note on why the candidate fits, for example the release time and recovery time results.
- **CHN-16** (Supported 2): Build relationships with DevOps people and recruiters hiring in the Netherlands alongside applications.
- **CHN-18** (Consensus 3) and **CHN-20** (Single source 1): Make sure LinkedIn has a photo, the full job history with what was done in each role, and dates that match the CV.

## Not covered by the evidence
- Netherlands conventions: no recruiter in the evidence hires in the Netherlands or mainland Europe, so local CV norms there are not covered.
- Relocation and visa routes to the Netherlands (for example the highly skilled migrant scheme) are outside the CV rules; general advice only: check with the employer what they sponsor.
- General advice, not from the rules: an AWS certification on its own is unlikely to count as "production experience"; hands-on work described with results will carry more weight.
- Whether to apply at all: general advice, not from the rules. With no AWS experience, applications to roles that run Kubernetes on-premise, on bare metal or in hybrid setups are likely to convert far better than AWS-first roles.
