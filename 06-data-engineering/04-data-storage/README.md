# 04 Data Storage

> The evolution of analytical data storage: from structured Data Warehouses to unstructured Data Lakes, culminating in the modern Data Lakehouse.

## Overview

Storing Petabytes of data requires entirely different architectures than storing Gigabytes in a PostgreSQL database. Data Engineering storage is optimized for scanning millions of rows in milliseconds (OLAP), leveraging cheap cloud object storage, and compressing data using columnar formats.

## Core Concepts

- **Data Warehouse**: Highly structured, relational storage optimized for SQL analytics (e.g., Snowflake, BigQuery). Data is loaded via ETL.
- **Data Lake**: A vast repository of raw, unstructured data (images, JSON, CSVs) stored on cheap cloud storage like AWS S3. Data is loaded as-is (ELT).
- **Columnar Formats**: Storing data by columns (Parquet, ORC) instead of rows (CSV) to drastically reduce I/O when aggregating specific fields.

## Deep Dives

- [Lakehouse & ACID Transactions](./lakehouse-and-acid-transactions.md) — The modern paradigm (Delta Lake, Apache Iceberg) that brings Database-like ACID transactions to the raw Data Lake, plus advanced optimizations like Z-Ordering.
