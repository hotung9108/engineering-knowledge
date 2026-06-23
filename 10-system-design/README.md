# 09 — System Design

> Case studies thiết kế hệ thống lớn — luyện tập tư duy architecting systems at scale.

---

##  Prerequisites

- [01-08](../) — Tất cả sections trước đó (ít nhất Fundamentals + Concepts + 1 learning path)

---

##  System Design Framework

Mỗi case study tuân theo template:

1. **Clarify Requirements** — Functional + Non-functional requirements
2. **Estimate Scale** — QPS, storage, bandwidth
3. **High-Level Design** — Components, data flow
4. **Detailed Design** — Database schema, API design, algorithms
5. **Trade-offs & Bottlenecks** — Identify & resolve

---

##  Case Studies

| # | Case | Công nghệ liên quan | Mô tả |
|---|---|---|---|
| 1 | [URL Shortener](./url-shortener.md) | Redis, PostgreSQL | Base62, distributed ID generation |
| 2 | [Chat System](./chat-system.md) | WebSocket, Kafka, Redis | Real-time messaging at scale |
| 3 | [Notification System](./notification-system.md) | Kafka, Redis, Push/Email/SMS | Multi-channel notifications |
| 4 | [Rate Limiter](./rate-limiter.md) | Redis | Token bucket, sliding window |
| 5 | [News Feed](./news-feed.md) | Redis, Kafka, PostgreSQL | Fan-out, ranking algorithms |
| 6 | [Search Autocomplete](./search-autocomplete.md) | Trie, Redis, Elasticsearch | Type-ahead suggestions |
| 7 | [Payment System](./payment-system.md) | Kafka, PostgreSQL | Idempotency, reconciliation |
| 8 | [E-Commerce](./e-commerce.md) | Spring Boot, Kafka, Redis, PostgreSQL | Order management, inventory |

---

##  Sections liên quan

- [02 — Concepts](../02-concepts/) — Architecture patterns dùng trong system design
- [10 — Projects](../10-projects/) — Hands-on implementation
