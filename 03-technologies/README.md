# 03 — Technologies (Deep Dive)

> Deep dive vào từng công nghệ cụ thể — từ fundamentals đến production best practices.

---

##  Roadmap

```mermaid
graph LR
    subgraph "Languages"
        JAVA["Java 17+"] --> SPRING["Spring Boot 3.x"]
        PY["Python 3.11+"]
    end

    subgraph "Data Stores"
        PG["PostgreSQL"]
        MONGO["MongoDB"]
        REDIS["Redis"]
    end

    subgraph "Messaging"
        KAFKA["Apache Kafka"]
        RMQ["RabbitMQ"]
    end

    subgraph "Infrastructure"
        DOCKER["Docker"]
        AWS["AWS"]
    end

    subgraph "Data Processing"
        SPARK["Apache Spark"]
        AF["Apache Airflow"]
    end

    SPRING --> PG
    SPRING --> REDIS
    SPRING --> KAFKA
    SPRING --> RMQ
    DOCKER --> AWS
    PY --> SPARK
    PY --> AF

    style JAVA fill:#FF5722,color:#fff
    style SPRING fill:#4CAF50,color:#fff
    style REDIS fill:#F44336,color:#fff
    style KAFKA fill:#000,color:#fff
    style PG fill:#336791,color:#fff
    style DOCKER fill:#2496ED,color:#fff
    style AWS fill:#FF9900,color:#fff
```

---

##  Prerequisites

- [01 — Fundamentals](../01-fundamentals/) — CS basics, OOP, SOLID
- [02 — Concepts](../02-concepts/) — Architecture patterns (recommended)

---

##  Nội dung

| Technology | Files | Focus |
|---|---|---|
| [Java](./java/) | Core, Multithreading, Modern Java, Testing | JVM, Collections, Streams, Virtual Threads |
| [Spring](./spring/) | Core, Boot, Data, Security, WebFlux, Cloud, WebSocket, Kafka, Redis, Testing | Full Spring ecosystem deep dive |
| [Redis](./redis/) | Fundamentals, Advanced, Data modeling, Clustering, Performance, Use cases | In-memory data store mastery |
| [Kafka](./kafka/) | Fundamentals, Architecture, Producer, Consumer, Streams, Schema Registry, Operations | Event streaming platform |
| [RabbitMQ](./rabbitmq/) | Fundamentals, Patterns, Reliability, Clustering, Spring AMQP | Message broker |
| [PostgreSQL](./postgresql/) | Fundamentals, Advanced queries, Indexing, Performance, Replication | Relational database |
| [MongoDB](./mongodb/) | Fundamentals, Indexing, Replication/Sharding, Spring Data MongoDB | Document database |
| [Docker](./docker/) | Fundamentals, Dockerfile best practices, Compose, Production | Containerization |
| [Python](./python/) | Core, Async, Data libraries | Python for data/AI |
| [AWS](./aws/) | Core services, Compute, Messaging, Storage/DB, Networking/Security | Cloud platform |
| [Airflow](./airflow/) | Fundamentals, Best practices, Production | Workflow orchestration |
| [Spark](./spark/) | Fundamentals, Streaming, Optimization | Data processing engine |

---

##  Sections liên quan

- [04 — Backend Engineering](../04-backend-engineering/) — Áp dụng technologies cho backend
- [05 — Data Engineering](../05-data-engineering/) — Kafka, Spark, Airflow in context
- [11 — Code Templates](../11-code-templates/) — Runnable boilerplate code
