# 05 - Multi-Cloud & Hybrid Cloud

> *"Don't put all your eggs in one basket, unless the cost of two baskets bankrupts you."*

This section explores the realities, benefits, and severe challenges of operating across multiple cloud providers (AWS, Azure, GCP) or mixing Cloud with On-Premise data centers.

## 📂 Contents

### 1. [Multi-Cloud Strategies](./multi-cloud-strategies.md)
The holy grail of vendor independence, or a massive architectural anti-pattern?
- The Vendor Lock-in debate
- Polycloud (Best-of-Breed) vs. Multi-Cloud (Portability)
- Terraform as the multi-cloud equalizer
- The nightmare of egress costs and network latency

### 2. Hybrid Cloud Architectures (Coming Soon)
Connecting your private corporate data center to the public cloud.
- AWS Direct Connect vs Site-to-Site VPN
- Data sovereignty and compliance routing
- AWS Outposts (Bringing AWS into your basement)

---

## 🎯 Learning Objectives

By the end of this section, you will be able to:
1. Articulate the massive trade-offs between "Cloud-Agnostic" architectures and "Cloud-Native" architectures.
2. Understand why egress bandwidth pricing is the silent killer of Multi-Cloud dreams.
3. Use Infrastructure as Code (Terraform) as a strategy to standardize deployments across Azure and AWS.
