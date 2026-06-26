# 04 — Distributed Async

> Strategies for asynchronous communication, event-driven architectures, and guaranteed message delivery between microservices.

---

## Content

| # | File | Description |
|---|---|---|
| 1 | [Transactional Outbox Pattern](./transactional-outbox-pattern.md) | Guaranteeing message delivery without distributed transactions using the Outbox pattern and Debezium (CDC). |
| 2 | [Kafka vs RabbitMQ at Scale](./kafka-vs-rabbitmq-at-scale.md) | Deep comparison of messaging semantics, consumer group scaling, and dead-letter queue strategies. |

---

## Related Sections

- [02 — Software Architecture / Distributed Transactions](../02-software-architecture/distributed-transactions.md) — How the Outbox pattern supports the Saga pattern.
- [05 — Resilience & Testing](../05-resilience-and-testing/) — Testing asynchronous messaging with Testcontainers.
