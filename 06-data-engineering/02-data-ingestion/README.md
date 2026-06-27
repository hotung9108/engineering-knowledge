# 02 Data Ingestion

> The gateway to Data Engineering: how to move data from operational databases, APIs, and logs into analytical storage systems securely and reliably.

## Overview

Data doesn't magically appear in a Data Warehouse. It must be extracted from source systems (like PostgreSQL, Salesforce, or web logs) and loaded into a destination. This process is called Data Ingestion. Modern ingestion focuses on near real-time synchronization, idempotency, and the shift from traditional ETL to modern ELT.

## Core Concepts

- **ETL vs ELT**: Extract, Transform, Load (traditional) vs Extract, Load, Transform (modern cloud approach).
- **Batch vs Micro-batch vs Streaming**: The frequency at which data is ingested.
- **Change Data Capture (CDC)**: Capturing row-level database changes (Inserts, Updates, Deletes) from transaction logs in real-time.

## Deep Dives

- [CDC & Idempotent Pipelines](./cdc-and-idempotent-pipelines.md) — Advanced ingestion using Debezium, ensuring exactly-once semantics, and designing pipelines that don't duplicate data upon failure.
