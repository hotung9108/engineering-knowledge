# 03 Data Processing

> Transforming raw data into valuable insights using distributed computing engines.

## Overview

Once data is ingested into a data lake or warehouse, it's rarely in a state ready for analysis. It needs to be cleaned, joined, aggregated, and enriched. This is the "Transform" step in modern Data Engineering.

## Core Concepts

- **Batch Processing**: Processing large volumes of bounded data at scheduled intervals (e.g., nightly jobs using Apache Spark).
- **Stream Processing**: Processing unbounded data continuously as it arrives in real-time (e.g., using Apache Flink or Kafka Streams).
- **Distributed Computing**: How frameworks like Spark split a massive dataset across hundreds of machines to process it in parallel.

## Deep Dives

- [Streaming vs Batch Architectures](./streaming-vs-batch-architectures.md) — Lambda vs Kappa architectures, state management, and Spark/Flink internals.
