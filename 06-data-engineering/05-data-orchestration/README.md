# 05 Data Orchestration

> The central nervous system of Data Engineering: scheduling, triggering, and monitoring complex data workflows.

## Overview

A data pipeline consists of dozens of dependent tasks: extracting data, loading it, running Spark transformations, and updating BI dashboards. If task A fails, task B must not run. If data arrives late, the pipeline must wait. Data Orchestration tools manage this complex web of dependencies.

## Core Concepts

- **DAG (Directed Acyclic Graph)**: A mathematical concept used to represent tasks and their directional dependencies without circular loops.
- **Schedulers vs Orchestrators**: Cron is a scheduler (runs at a specific time). Airflow is an orchestrator (runs based on time AND dependencies).
- **Observability**: Monitoring pipelines to ensure data arrives on time (SLA) and alerting engineers when things break.

## Deep Dives

- [Advanced DAG Patterns & Observability](./advanced-dag-patterns-and-observability.md) — Mastering Apache Airflow, Dynamic DAGs, Backfilling, Deferrable Operators, and Data Observability.
