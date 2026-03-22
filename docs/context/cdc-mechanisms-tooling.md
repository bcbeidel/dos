---
name: CDC Mechanisms & Tooling
description: "Log-based CDC is the only production-grade mechanism -- trigger-based adds write amplification, timestamp-based misses deletes; Debezium on Kafka Connect is the dominant open-source tool but requires significant operational overhead; AWS DMS is single-threaded for CDC and inappropriate for high-throughput; dlt is not CDC -- it polls, it does not stream from transaction logs"
type: context
related:
  - docs/research/2026-03-22-cdc-event-driven-ingestion.research.md
  - docs/context/kafka-event-streaming-patterns.md
  - docs/context/cdc-lakehouse-write-strategies.md
  - docs/context/incremental-loading-patterns.md
  - docs/context/schema-evolution.md
---

## Key Insight

Log-based CDC is the only production-grade mechanism for capturing database changes. It reads the existing transaction log (PostgreSQL WAL, MySQL binlog) with minimal source impact, captures all change types including deletes, and preserves commit ordering. Trigger-based and timestamp-based CDC are legacy approaches with fundamental deficiencies.

## CDC Mechanisms

**Log-based CDC** reads committed changes from the database's transaction log. The database already writes every change for crash recovery -- CDC reads this as a secondary consumer. No schema modifications, no write overhead, sub-second latency. Database-specific setup:

- **PostgreSQL:** `wal_level = logical`, create a replication slot, configure `pgoutput`. Critical risk: replication slots prevent WAL deletion until the consumer confirms receipt. If the consumer falls behind, WAL files accumulate and can fill the disk, causing total production outage.
- **MySQL:** `binlog_format = ROW`, `binlog_row_image = FULL`, GTIDs enabled. Approximately 15% write overhead from row-level logging.

**Trigger-based CDC** installs triggers on DML operations that write to shadow tables. Three problems: write amplification on every operation, brittle trigger management across schema changes, and cascading failure risk. Legacy approach.

**Timestamp-based CDC** polls for rows where `updated_at` exceeds a checkpoint. Cannot detect hard deletes. Requires schema modifications. This is what dlt uses for incremental loading -- effective for APIs and databases without log access, but not CDC.

## Tooling

**Debezium** is the dominant open-source CDC platform, built on Kafka Connect. Supports PostgreSQL, MySQL, MongoDB, SQL Server, Oracle, Db2. Three deployment models:

1. **Kafka Connect** (production default): Multi-task parallelism, REST API management, offset storage in Kafka. Requires managing a Kafka Connect cluster.
2. **Debezium Server** (lightweight): Standalone process streaming to non-Kafka targets (Kinesis, Pub/Sub). No multi-task support, no dynamic management, restarts required for config changes.
3. **Debezium Engine** (embedded): Library for custom applications. Maximum flexibility, zero built-in fault tolerance.

Each change event includes before/after row state, operation type (create/update/delete/snapshot), source metadata (table, transaction ID, LSN/binlog position), and timestamps.

**AWS DMS** provides managed CDC but with severe limitations: single-threaded CDC to relational targets with no parallel option. Under high change rates, replication lag compounds -- observed peaking at 600 seconds. Appropriate for managed migrations and low-to-moderate volumes. Inappropriate for high-throughput production CDC.

**dlt** is not a CDC tool. It supports merge, SCD2, and upsert write dispositions via polling with cursor-based state tracking. Effective for incremental loading from APIs and databases without log access. Fundamentally different from log-based CDC in latency, completeness, and ordering guarantees.

## Takeaway

The decision is not between three equal CDC alternatives. Log-based CDC is the one production mechanism; trigger-based and timestamp-based are compromises for environments where log access is unavailable. Debezium is the correct default for open-source CDC despite its operational weight. AWS DMS is a managed convenience that breaks down under load. dlt fills a different niche entirely -- polling-based incremental loading, not streaming change capture.
