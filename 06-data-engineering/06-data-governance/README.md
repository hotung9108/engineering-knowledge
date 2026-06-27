# 06 Data Governance

> Ensuring data is trustworthy, secure, compliant, and clearly understood across the entire organization.

## Overview

Having petabytes of data is useless if no one trusts it or knows what it means. Data Governance ensures that data is of high quality, its origins are trackable (Data Lineage), and access is securely managed. It bridges the gap between the engineers who produce data and the analysts who consume it.

## Core Concepts

- **Data Contracts**: Formal agreements between software engineers (producers) and data engineers (consumers) to prevent upstream database changes from breaking downstream pipelines.
- **Data Quality**: Automated testing for data (e.g., using Great Expectations) to catch nulls, anomalies, and schema drifts before they reach dashboards.
- **Data Lineage & Cataloging**: Mapping out the entire journey of a data point from the raw database to the final Tableau dashboard, allowing users to discover and trust the data.

## Deep Dives

- [Data Contracts & Quality](./data-contracts-and-quality.md) — Implementing Data Contracts using Schema Registries, automated Data Quality checks, and an introduction to the Data Mesh paradigm.
