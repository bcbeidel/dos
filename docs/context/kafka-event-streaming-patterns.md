---
name: Kafka & Event Streaming Patterns
description: "Kafka topic-per-table with primary-key partitioning preserves per-entity ordering; Schema Registry with backward compatibility is the production default; exactly-once is a Kafka-internal guarantee -- end-to-end requires idempotent consumers via upsert-on-primary-key; the transactional outbox pattern eliminates dual writes by combining business data and events in one database transaction"
type: context
related:
  - docs/research/2026-03-22-cdc-event-driven-ingestion.research.md
  - docs/context/cdc-mechanisms-tooling.md
  - docs/context/cdc-lakehouse-write-strategies.md
  - docs/context/retry-failure-patterns.md
  - docs/context/incremental-loading-patterns.md
---

## Key Insight

Kafka's exactly-once semantics are a Kafka-internal guarantee, not an end-to-end one. CDC pipelines writing to a warehouse or lakehouse operate with at-least-once delivery at the destination boundary. End-to-end exactly-once requires idempotent consumers -- most practically achieved via upsert-on-primary-key at the destination.

## Topic Design & Partitioning

Standard CDC topology: **one Kafka topic per source table**. This provides clear ownership, independent retention policies, simple ACLs, and subscription granularity. Topic naming should encode origin: `<environment>.<database>.<schema>.<table>` (e.g., `prod.ecommerce.public.orders`).

Use the table's **primary key as the Kafka message key**. This guarantees all changes for a given entity land in the same partition and are processed in order. Kafka guarantees ordering within a partition, not across partitions. Cross-entity ordering (parent before child across tables) requires consumer-side logic -- buffering events and sorting by transaction ID or LSN.

## Consumer Groups & Offset Management

Each downstream system uses a distinct consumer group ID. Multiple groups read the same topic concurrently with independent progress tracking.

- **Auto-commit** (`enable.auto.commit=true`): At-most-once semantics. If a consumer crashes after auto-commit but before processing completes, the message is lost. Non-critical workloads only.
- **Manual commit** (`enable.auto.commit=false`): At-least-once semantics. Commit offsets after successfully processing a batch, not before. Required for production CDC.

For CDC topics where consumers need current state rather than full history, enable **log compaction** (`cleanup.policy=compact`). Retains only the latest message per key. Combine with time-based retention (e.g., 7 days) to preserve recent history for replay.

## Schema Registry

Avro with Confluent Schema Registry is the standard serialization for CDC-to-Kafka pipelines. Backward compatibility (the default) is recommended for CDC: new schemas can read data written with the previous schema. A single upstream `ALTER TABLE` can halt deserialization for every downstream consumer if compatibility is not enforced. Register schemas in CI/CD and give clients read-only access -- treat schemas as data contracts.

## Delivery Semantics

- **At-most-once:** Producer fires without acknowledgment. Messages may be lost.
- **At-least-once:** Producer retries on failure. Since Kafka 3.0, default producer config enables idempotent delivery (`acks=all`, `enable.idempotence=true`), preventing duplicates during producer retries.
- **Exactly-once (Kafka-internal):** Transactional delivery allows atomic writes to multiple partitions. Consumers with `isolation.level=read_committed` see only committed transaction data.

Four patterns for idempotent consumers at the destination:

1. **Upsert on primary key** (most practical): `MERGE`, `ON CONFLICT UPDATE`, `ReplacingMergeTree`. Replayed records overwrite rather than duplicate.
2. **Read-time deduplication:** Append all records, deduplicate at query time with `ROW_NUMBER()`. Simple but pushes cost to every query.
3. **Conditional writes:** Update only if incoming version/timestamp is newer.
4. **Seen-set deduplication:** Track processed IDs in Redis or a database. Adds state management burden.

Non-idempotent operations (SUM, running totals) are dangerous in at-least-once pipelines. Store raw facts with upserted primary keys and compute aggregates at query time.

## Transactional Outbox Pattern

The dual-write problem: when a service must update its database and publish an event, no transaction manager spans both systems atomically. The outbox pattern solves this by writing business data and an event record to the same database in one transaction. A relay process (Debezium via CDC on the outbox table) publishes events to Kafka. Debezium's built-in Outbox Event Router SMT routes by aggregate type, uses aggregate ID as the Kafka key, and propagates event UUIDs for downstream dedup. The pattern requires the full CDC infrastructure stack -- significant commitment for teams not already running Debezium and Kafka.

## Takeaway

Design CDC pipelines for at-least-once delivery with idempotent consumers. Upsert-on-primary-key is the practical default. Kafka's exactly-once is valuable within Kafka but does not extend to external destinations. The outbox pattern is the correct solution for dual writes, but only if you already have (or are willing to stand up) the CDC stack.
