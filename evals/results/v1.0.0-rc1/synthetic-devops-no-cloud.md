# CV review: Senior DevOps Engineer for Halvard Logistics, Amsterdam (relocation offered)

**Verdict:** Reject

**10-second verdict:** The top of page one shows "DevOps Engineer | Lagos, Nigeria", a summary that ends in "on-premise data centres", and a most recent role as Senior DevOps Engineer at Tarnwick Payments with Jenkins, Kubernetes "on bare metal with Rancher" and "Terraform (vSphere provider)". A screener checking for this job's stack finds Kubernetes, Helm, Terraform and CI/CD quickly, then looks for AWS and finds none anywhere on the page. The job says "We run our platform on AWS" and lists production AWS (EKS, IAM, VPC, RDS) as a must-have, so most screeners stop here. This is one screener's likely view (SCR-16), but the gap is a stated hard requirement, not a preference.

**Target and weighting:** From the request and job description: Senior DevOps Engineer, 5+ years, AWS-based platform, Amsterdam, relocation offered; candidate based in Lagos, so an application from outside the EU. Match: JA high (hiring manager at a cloud-based tech product company, reviewed a DevOps CV live), TW medium-high (agency, UK and Europe, tech), JB medium-high (infrastructure background, cross-border hires across EMEA), SB low (JavaScript and TypeScript startups, UK only). Single source rules from JA are raised one level where the CV is in the situation JA described.

## Findings

### Critical
- **RED-2** (Consensus 3, Critical): The job's core platform is AWS ("Production experience with AWS (EKS, IAM, VPC, RDS)", "Terraform for AWS"), and the CV shows no cloud provider at all: the summary says "on-premise data centres", Kubernetes ran "on bare metal with Rancher" and Terraform used the "vSphere provider". All three recruiters who addressed this report rejecting on a missing core skill, and the posting makes it a must-have (ATS-3: a hard requirement can also be filtered out automatically). Fix: if the candidate has any real AWS use (a work project, a migration pilot, a certification, a personal project), name it with the specific services in the most recent role or a Projects section. If there is none, do not add AWS anywhere: a claim that falls apart in the first technical question is an instant rejection (RED-3). In that case the honest options are to build a small AWS project first (see ACH-4) or to target on-premise and hybrid roles, where this CV is strong.

### High
- **SCR-7** (Consensus 3, High): The stack is easy to find, which is good, but the first stack a reader meets is the wrong one for this job: "on-premise data centres", "bare metal", "vSphere". Fix: lead with the parts that match the job (Kubernetes, Helm, Terraform, CI/CD, Prometheus and Grafana) and present the on-premise setting as context, not as the headline. Do not hide it.
- **ACH-4** (Consensus 3, High): No side projects or hackathons are listed. For this candidate a side project is the only truthful way to show AWS before getting a job that uses it. Fix: if the candidate builds or has built one, add a Projects section with the dates, context and what was built, for example "[EKS cluster provisioned with Terraform, with a GitHub Actions pipeline]", and link the repository (CHN-6: only if it shows real activity).
- **ACH-1** (Consensus 4, High): The Tarnwick Payments bullets describe work and results well, but at Brightmere Telecom two of three bullets are duties: "Maintained GitLab CI runners and a private Docker registry" and "Wrote Bash and Python scripts for backups and log rotation". Fix: say what changed because of this work (see Rewrites).
- **ACH-6** (Consensus 3, High): The most recent role is well quantified ("40 services", "two days to three hours", "90 to 25 minutes"). The Brightmere bullets after the first carry no numbers. Fix: add the real figures where they exist, using the placeholders in Rewrites.
- **SKL-4** (Supported 2, High): The CV shows no use of AI tools in daily work. Fix: if the candidate uses AI coding or ops tools (for writing Terraform, Helm charts, scripts or runbooks), add one concrete line in the most recent role. Do not add it if it is not true. SKL-7 (Single source 1, TW) makes the same point.
- **CHN-15** (Consensus 3, High): Not a CV fix. A candidate applying from abroad for a role with a hard requirement he does not yet meet should not rely on a cold application alone: ask for a referral into Halvard Logistics if any contact exists, and send the hiring manager a short note on why he fits (CHN-17, Supported 2).

### Medium
- **SKL-11** (Single source 1, Medium; raised from Low because JA is a high match and the CV is in this situation): JA expects about 80 percent of the listed skills. The CV shows 5+ years, Kubernetes and Helm, CI/CD (Jenkins and GitLab CI as "similar"), Prometheus and Grafana, and Python, but not AWS and only half of "Terraform for AWS": about 75 percent, with the missing share being the most important item. RED-6 (most skills missing) does not apply.
- **STR-4** (Supported 2, Medium): The summary is one sentence and generic: "DevOps engineer with 6 years of experience building CI/CD pipelines, container platforms and monitoring for on-premise data centres." It does not say why the candidate fits this role and does not use his best results. Fix: see Rewrites.
- **STR-21** (Single source 1, Medium; raised, JA high match): JA wants a summary of 3 to 4 lines; this one is about 2. Fix: expand to 3 or 4 lines with the strongest results.
- **STR-25** (Single source 1, Medium; raised, JA high match): The title under the name is "DevOps Engineer"; the job is "Senior DevOps Engineer", and the candidate already holds that title at Tarnwick Payments. Fix: use "Senior DevOps Engineer" in the header and the summary.
- **SKL-3** (Supported 2, Medium): "ELK" is in the skills list but appears in no role. Fix: name the role where ELK was used, or remove it.
- **SKL-8** (Single source 1, Medium; raised, JA high match): The skills section is one flat list of 16 items. Fix: group it (see Rewrites).
- **ACH-7** (Single source 1, Medium; raised, JA high match): Product scale is clear ("40 services", "12-node", "150 Linux servers"), but team and company size are not. Fix: add team size, for example "in a team of [N] engineers".
- **SEN-7** (Single source 1, Medium; raised, JA high match): Every bullet reads as solo work ("Built", "Ran", "Set up"). Fix: show who the work was done with or for, for example the developers who used the pipelines.
- **REG-8** (Single source 1, Medium; raised, JA high match): "IELTS 7.5 (Academic, 2023)" is listed; JA says many recruiters do not know what the score means. Fix: remove it.
- **REG-9** (Single source 1, Medium; raised, JA high match): An English CV with a Languages section listing only English adds nothing. Fix: drop the Languages section. REG-6 is met by the CV itself being in clear English.
- **STR-12** (Single source 1, Medium; raised, JA high match): There is a References section, and it gives a named referee with contact details. Fix: delete the section, which also keeps a third person's details off a CV sent to strangers.

### Low
- **REG-5** (Single source 1, Low): The header gives "Lagos, Nigeria" (good, REG-14) but no word on relocation, for a job in Amsterdam that offers it. Fix: add "ready to relocate to Amsterdam" in the header.
- **REG-15** (Single source 1, Low): Right to work in the Netherlands is not stated. Fix: if the candidate holds a right to work in the EU, say so; if he needs sponsorship, leave it off the CV (REG-2) and let the relocation line carry the point.
- **ATS-1** (Single source 1, Low): The job's terms "AWS", "EKS", "IAM", "VPC", "RDS", "GitHub Actions" and "infrastructure as code" do not appear. Fix: use "infrastructure as code" with Terraform and Ansible, which is true; add the AWS terms only for services actually used.
- **STR-7** (Single source 1, Low): No role opens with company context. Fix: add 2 to 4 lines under Tarnwick Payments and Brightmere Telecom on what the company does, the team and the platform's scale (STR-8).

### Judgment calls
- **SKL-5** (Contested 1-1): For: SB says leaders treat cloud providers as interchangeable and weigh the core stack. Against: JA says cloud providers are not interchangeable. Here the question is sharper, because the CV shows no cloud at all, so even SB's view does not bridge the gap. Recommendation: follow JA (high match) and treat AWS as missing; present the Kubernetes, Terraform and monitoring work as transferable without claiming AWS.
- **REG-16** (Contested 1-1): For: TW says location filters screen out applicants from abroad. Against: JA says skill gaps, not location, cause the rejection. Recommendation: fix the AWS gap first (JA); then state Lagos and readiness to relocate in one line so location is a known fact. Halvard offers relocation, which helps.
- **STR-2** (Contested range 4): The CV is about one page for 6 to 8 years of experience, which fits JA's 1 page and is short of TW and JB's ranges. Recommendation: keep it to one page, or at most two if a Projects section and company context are added.

## Rewrites

**Header title line**
- Before: "DevOps Engineer | Lagos, Nigeria | ..."
- After: "Senior DevOps Engineer | Lagos, Nigeria, ready to relocate to Amsterdam | [contact details as now]"

**Summary**
- Before: "DevOps engineer with 6 years of experience building CI/CD pipelines, container platforms and monitoring for on-premise data centres."
- After: "Senior DevOps engineer with 6 years of experience in CI/CD, Kubernetes, Helm and Terraform at Tarnwick Payments and Brightmere Telecom. Built Jenkins pipelines for 40 services, cutting release time from two days to three hours, and cut mean time to recovery from 90 to 25 minutes with Prometheus and Grafana. [AWS experience, only if real: services used and where]."

**Brightmere Telecom bullets**
- Before: "Moved 25 applications from VMs to Docker containers."
- After: "Moved 25 applications from VMs to Docker containers, cutting [deployment time or server count] by [X%]."
- Before: "Maintained GitLab CI runners and a private Docker registry."
- After: "Ran GitLab CI runners and a private Docker registry for [N developers], keeping builds [result, such as under N minutes]."
- Before: "Wrote Bash and Python scripts for backups and log rotation."
- After: "Automated backups and log rotation with Bash and Python, [saving N hours a week or cutting restore time to N minutes]."

**Skills**
- Before: "Kubernetes, Docker, Helm, Rancher, Jenkins, GitLab CI, Ansible, Terraform, Prometheus, Grafana, ELK, Linux, Bash, Python, Nginx, vSphere"
- After:
  - "Containers and orchestration: Kubernetes, Helm, Docker, Rancher"
  - "CI/CD: Jenkins, GitLab CI"
  - "Infrastructure as code: Terraform, Ansible"
  - "Monitoring and logging: Prometheus, Grafana, ELK"
  - "Systems and scripting: Linux, Nginx, vSphere, Bash, Python"
  - "[Cloud: AWS services actually used, only if any]"

**New Projects section (only if the candidate does this work)**
- After: "[Project name], [month and year], personal project: [what was built, such as an EKS cluster provisioned with Terraform and deployed through a CI pipeline], [repository link]"

## What already works
- The most recent role leads the experience section, is in reverse date order and shows a matching core stack apart from the cloud (SCR-2).
- The Tarnwick Payments bullets give what was built and the result, with real numbers: "two days to three hours", "90 to 25 minutes" (ACH-1, ACH-6).
- Bullets start with varied action verbs: Built, Ran, Set up, Automated (ACH-13).
- Plain single-column layout, no photo, no graphics (STR-3, REG-7).
- Role headings lead with the job title, and give the employer's city and start and end months (STR-14, STR-19, STR-24).
- The current city is stated truthfully (REG-14), and the phone country code matches it (REG-17 does not arise).
- Education names the university and degree and sits below experience (STR-27, STR-26).
- A promotion path is visible: Systems Administrator, DevOps Engineer, Senior DevOps Engineer (SEN-2).
- No gaps between roles (GAP-2, GAP-3), and a LinkedIn URL is in the header (CHN-5).

## Not covered by the evidence
- **Market.** No recruiter in the evidence hires in the Netherlands or mainland Europe; Dutch conventions and how Dutch employers screen non-EU applicants are not covered.
- **Visa and relocation routes.** Whether Halvard sponsors a work permit (for example under the Dutch highly skilled migrant scheme) is out of scope for the rules. General advice: confirm sponsorship with the recruiter early.
- **AWS certification.** The evidence does not say whether a certification can stand in for production AWS experience. General advice: a certification alone is unlikely to satisfy "production experience", but paired with a real project it gives the screener something to check.
- **LinkedIn.** The profile could not be checked; keep it complete and consistent with the CV (CHN-18, CHN-20).
