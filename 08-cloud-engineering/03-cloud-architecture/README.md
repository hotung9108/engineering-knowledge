# 03 - Cloud Architecture

> *"A fool with a tool is still a fool." - Knowing how to use AWS services is not enough; you must know how to combine them securely, reliably, and cost-effectively.*

This section covers the fundamental architectural patterns of Cloud Computing, focusing heavily on the AWS Well-Architected Framework.

## 📂 Contents

### 1. [The Well-Architected Framework](./well-architected-framework.md)
The absolute bible of AWS Cloud Design. Learn the 6 Pillars that dictate how every professional cloud system should be built.
- Operational Excellence
- Security
- Reliability
- Performance Efficiency
- Cost Optimization
- Sustainability

### 2. [High Availability & Disaster Recovery](./ha-and-disaster-recovery.md)
How to survive when entire Data Centers catch fire.
- RTO (Recovery Time Objective) vs RPO (Recovery Point Objective)
- Multi-AZ Deployments
- Multi-Region Active-Active vs Active-Passive setups
- Backup strategies (Pilot Light, Warm Standby)

### 3. [Microservices vs Monoliths](./microservices-architecture.md)
The evolution of application architecture in the cloud.
- Breaking down the Monolith
- The role of Containers (ECS/EKS) in Microservices
- Service Mesh (App Mesh / Istio)
- The CAP Theorem in distributed databases

### 4. [Cost Optimization Strategies](./cost-optimization.md)
How to stop burning VC money on idle cloud resources.
- Reserved Instances & Savings Plans
- Spot Instances for stateless workloads
- Right-sizing resources
- Tagging strategies for financial accountability

---

## 🎯 Learning Objectives

By the end of this section, you will be able to:
1. Design a 3-tier web architecture that can survive the complete destruction of an Availability Zone (Data Center).
2. Justify your architectural choices using the 6 Pillars of the Well-Architected Framework.
3. Strategize a Disaster Recovery plan that balances business requirements (RTO/RPO) with budget constraints.
4. Slash a company's AWS bill by 40% using Spot Instances and Lifecycle Policies.
