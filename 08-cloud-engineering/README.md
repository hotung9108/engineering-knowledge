# 07 — Cloud Engineering

> Learning path cho **Cloud Engineer** — AWS deep dive, cloud architecture, serverless, và multi-cloud.

---

##  Roadmap

```mermaid
graph TD
    FUND["01 Cloud Fundamentals<br/>IaaS, PaaS, SaaS, Networking, Security"] --> AWS["02 AWS Deep Dive<br/>Compute, Storage, DB, Messaging"]
    AWS --> ARCH["03 Cloud Architecture<br/>Well-Architected, Multi-region, Cost"]
    ARCH --> SLS["04 Serverless<br/>Lambda, DynamoDB, SAM"]
    SLS --> MC["05 Multi-Cloud<br/>AWS vs GCP vs Azure"]

    style FUND fill:#4CAF50,color:#fff
    style AWS fill:#FF9900,color:#fff
    style ARCH fill:#2196F3,color:#fff
    style SLS fill:#9C27B0,color:#fff
    style MC fill:#607D8B,color:#fff
```

---

##  Prerequisites

- [01 — Fundamentals](../01-fundamentals/) — Networking, Linux, Security
- [06 — DevOps](../06-devops-engineering/) — Docker, Kubernetes, IaC (recommended)

---

##  Nội dung

| Subsection | Files | Mô tả |
|---|---|---|
| [01 Cloud Fundamentals](./01-cloud-fundamentals/) | Concepts, Networking, Security | IaaS/PaaS/SaaS, VPC, IAM |
| [02 AWS Deep Dive](./02-aws-deep-dive/) | Compute, Storage, Database, Networking, Messaging, Serverless | AWS services mastery |
| [03 Cloud Architecture](./03-cloud-architecture/) | Well-Architected, Multi-region, Cost optimization, Migration | Enterprise cloud design |
| [04 Serverless](./04-serverless/) | Architecture, Lambda, Serverless DB | Event-driven serverless |
| [05 Multi-Cloud](./05-multi-cloud/) | Comparison, Cloud-agnostic patterns | Cross-cloud strategies |

---

##  Sections liên quan

- [03 — AWS](../03-technologies/aws/) — AWS services details
- [06 — DevOps](../06-devops-engineering/) — Deployment & infrastructure
