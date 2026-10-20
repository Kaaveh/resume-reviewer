# CV review: Daniel Okonkwo-Brandt for Senior DevOps Engineer, Halvard Logistics (Amsterdam)

## Verdict: Reject (for this role, as the CV stands)

This is a solid on-premise DevOps CV with real numbers, but the role is built around AWS and the CV has no AWS, and no public cloud at all. "Production experience with AWS (EKS, IAM, VPC, RDS)" and "Terraform for AWS" are two of five must-haves, and both are missing. The candidate's Terraform is the vSphere provider. A recruiter screening against the must-have list stops here, however good the rest is.

If the candidate does have AWS experience that is simply not written down, the verdict moves to **borderline or invite**. Every other must-have is covered well. Without AWS, the honest advice is to target on-prem, hybrid or Kubernetes platform roles, or to get real AWS exposure first, and not to stretch this CV to fit.

### Must-have match

| Requirement | Evidence in CV | Status |
|---|---|---|
| 5+ years DevOps / platform | Jun 2019 to present (about 7 years DevOps), plus 1.5 years sysadmin | Met |
| Production AWS (EKS, IAM, VPC, RDS) | None. Summary says "on-premise data centres" | **Missing** |
| Terraform for AWS | Terraform with vSphere provider only | **Partial** (tool yes, cloud no) |
| Kubernetes and Helm | 12-node bare-metal cluster with Rancher, Helm charts for all services | Met |
| CI/CD (GitHub Actions or similar) | Jenkins for 40 services, GitLab CI | Met |
| Nice: Prometheus, Grafana | Set up with on-call alerts, MTTR 90 to 25 min | Met |
| Nice: Python or Go | Python scripts for backups and log rotation | Met (light) |

## Problems by severity

### Critical
1. **No AWS anywhere.** The JD opens with "We run our platform on AWS." The CV never mentions AWS, EKS, IAM, VPC, RDS or any cloud. This alone gets it rejected at screening.
2. **Terraform is on vSphere, not AWS.** Good that the tool is there, but the JD asks specifically for Terraform for AWS. The current wording makes the gap obvious.
3. **The summary works against the application.** "monitoring for on-premise data centres" tells an AWS shop in the first line that the candidate is not what they want. It is accurate, so do not delete the fact, but lead with what transfers (Kubernetes, IaC, CI/CD, reliability).

### Major
4. **No location or work-authorisation line for the Netherlands.** The candidate is in Lagos; the role is in Amsterdam with relocation offered. Say plainly that you are relocating and whether you need sponsorship (for example the Dutch highly skilled migrant route). Recruiters skip non-EU CVs that leave this open.
5. **Third-party personal data in References.** Naming Mr. Tunde Bakare with his email on a CV sent to strangers shares his details without need. Replace the whole section with nothing; references are asked for later.
6. **Brightmere and Kolade bullets are duties, not results.** "Maintained GitLab CI runners", "Wrote Bash and Python scripts" say what the job was, not what changed. The Tarnwick bullets show the candidate can quantify; the older roles should too.

### Minor
7. **Skills list is flat and unordered.** Group it (Containers, IaC, CI/CD, Observability, Languages) and put the JD's terms first.
8. **Security and access control are invisible.** IAM is a must-have topic. Any work on RBAC in Kubernetes, secrets management (Vault, sealed secrets), network policies or least-privilege access should be shown; it is the closest transferable evidence for IAM/VPC.
9. **Python is undersold.** "scripts for backups and log rotation" reads as junior. If there is tooling, automation or internal CLIs in Python, say so.
10. **Header job title.** "DevOps Engineer" while the current title is Senior DevOps Engineer. Use "Senior DevOps Engineer" to match the role.
11. **IELTS line is fine** but can be shortened; for a Dutch employer, mentioning any Dutch (even none) is not needed for an English-language tech role.

## Rewrites

Only use the AWS-flavoured lines if they are true. Do not add cloud experience the candidate does not have.

### Header
> Senior DevOps Engineer | Lagos, Nigeria (relocating to Amsterdam; requires visa sponsorship) | daniel.ob@example.com | +234 801 555 0142 | linkedin.com/in/example-dob

### Summary (honest, no AWS)
> Senior DevOps engineer with 7 years running production Kubernetes, infrastructure as code and CI/CD for a payments platform. Built and operate a 12-node Kubernetes cluster with Helm, Terraform and Ansible; cut release time from two days to three hours and recovery time from 90 to 25 minutes. Moving from on-premise to AWS.

### Summary (only if the candidate has real AWS work)
> Senior DevOps engineer with 7 years in Kubernetes, Terraform and CI/CD, including [X years / project] on AWS ([EKS, IAM, VPC, RDS: list only what was used]). ...

### Tarnwick Payments bullets
- Built Jenkins pipelines for 40 services, cutting release time from two days to three hours.
- Run a 12-node production Kubernetes cluster (Rancher, bare metal) serving [N] payment services; wrote and maintain Helm charts for all 40.
- Set up Prometheus and Grafana monitoring and on-call alerting; mean time to recovery fell from 90 to 25 minutes.
- Manage infrastructure as code with Terraform (vSphere provider) and Ansible: [N] servers provisioned in [time] instead of [time].
- *(If true)* Configured Kubernetes RBAC, network policies and secrets management for PCI-scoped services.

### Brightmere Telecom bullets
- Moved 25 applications from VMs to Docker containers, [result: e.g. deploy time, server count or cost saved].
- Ran GitLab CI runners and a private Docker registry for [N] engineers / [N] pipelines per day.
- Wrote Python and Bash automation for backups and log rotation, [result: e.g. removed N hours of manual work a week, zero lost backups].

### Skills
> **Containers and orchestration:** Kubernetes, Helm, Docker, Rancher
> **Infrastructure as code:** Terraform, Ansible, vSphere
> **CI/CD:** Jenkins, GitLab CI
> **Observability:** Prometheus, Grafana, ELK
> **Languages and OS:** Python, Bash, Linux (Ubuntu, CentOS), Nginx

### References
Delete the section.

## What would actually change the verdict
- Real AWS work, even a side project or certification backed by a public Terraform repo that stands up EKS with IAM roles, a VPC and RDS. A certification (AWS Solutions Architect Associate) alone helps a little; a working, linked repo helps more. Either way it shows effort, not production experience, so expect "borderline" at best until there is production AWS on the CV.
