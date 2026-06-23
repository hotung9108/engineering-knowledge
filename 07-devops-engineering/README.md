# 07 — DevOps Engineering

> Learning path cho **DevOps Engineer** — CI/CD, containerization, IaC, monitoring, và SRE.

---

##  Roadmap

```mermaid
graph TD
    CICD["01 CI/CD<br/>GitHub Actions, Jenkins"] --> CONT["02 Containerization<br/>Docker, Kubernetes, Helm"]
    CONT --> IAC["03 Infrastructure as Code<br/>Terraform, Ansible"]
    IAC --> MON["04 Monitoring & Alerting<br/>Prometheus, Grafana, ELK"]
    MON --> SEC["05 Security DevOps<br/>DevSecOps, Secrets, Container Security"]
    SEC --> SRE["06 Site Reliability<br/>SRE, Incident Management"]

    style CICD fill:#4CAF50,color:#fff
    style CONT fill:#2196F3,color:#fff
    style IAC fill:#FF9800,color:#fff
    style MON fill:#9C27B0,color:#fff
    style SEC fill:#F44336,color:#fff
    style SRE fill:#607D8B,color:#fff
```

---

##  Prerequisites

- [01 — Fundamentals](../01-fundamentals/) — Linux, Git, Networking
- [03 — Technologies](../03-technologies/) — Docker basics

---

##  Nội dung

| Subsection | Files | Mô tả |
|---|---|---|
| [01 CI/CD](./01-ci-cd/) | Fundamentals, GitHub Actions, Jenkins, GitLab CI | Build, test, deploy automation |
| [02 Containerization](./02-containerization/) | Docker advanced, K8s fundamentals/advanced, Helm, Service Mesh | Container orchestration |
| [03 Infrastructure as Code](./03-infrastructure-as-code/) | Terraform, Ansible, Pulumi | Automated infrastructure provisioning |
| [04 Monitoring & Alerting](./04-monitoring-alerting/) | Prometheus/Grafana, ELK Stack, Alerting strategy | System observability |
| [05 Security DevOps](./05-security-devops/) | DevSecOps, Secrets management, Container security | Security automation |
| [06 Site Reliability](./06-site-reliability/) | SRE fundamentals, Incident management, Capacity planning | Reliability engineering |

---

##  Sections liên quan

- [03 — Docker](../03-technologies/docker/) — Container fundamentals
- [08 — Cloud Engineering](../08-cloud-engineering/) — Cloud platform deployment
- [02 — Observability](../02-concepts/observability/) — Monitoring concepts
