---
name: "CDC & Event-Driven Ingestion"
description: "Log-based CDC is the only production-grade mechanism — trigger-based and timestamp-based approaches fail on deletes, add write amplification, or miss changes; Debezium is the dominant open-source CDC platform but requires Kafka Connect operational overhead (Debezium Server trades features for simplicity); AWS DMS is single-threaded for CDC and compounds latency under high change rates; dlt supports merge/SCD2/upsert write dispositions but is not a CDC tool — it polls, not streams; Kafka topic-per-table with primary key partitioning preserves per-entity ordering; Schema Registry with backward compatibility is the production default for CDC topics; the transactional outbox pattern eliminates dual writes by combining business data and events in one database transaction; CDC into Delta Lake uses MERGE INTO (write-amplified but read-optimized) while Iceberg favors merge-on-read with compaction; exactly-once delivery is a Kafka-internal guarantee — end-to-end exactly-once requires idempotent consumers using upsert-on-primary-key; PostgreSQL WAL replication slots risk disk exhaustion if CDC consumers fall behind"
type: research
sources:
  - https://conduktor.io/glossary/implementing-cdc-with-debezium
  - https://debezium.io/documentation/reference/stable/features.html
  - https://debezium.io/blog/2019/02/19/reliable-microservices-data-exchange-with-the-outbox-pattern/
  - https://docs.confluent.io/kafka/design/delivery-semantics.html
  - https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html
  - https://streamkap.com/resources-and-guides/cdc-to-kafka-topics
  - https://streamkap.com/resources-and-guides/idempotency-streaming-pipelines
  - https://www.ryft.io/blog/cdc-strategies-in-apache-iceberg
  - https://dlthub.com/docs/general-usage/incremental-loading
  - https://www.bladepipe.com/blog/data_insights/mysql_cdc_vs_postgres_cdc/
  - https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Troubleshooting_Latency.html
  - https://blog.scottlogic.com/2025/09/08/solving-data-consistency-in-distributed-systems-with-the-transactional-outbox.html
  - https://microservices.io/patterns/data/transactional-outbox.html
  - https://blog.sequinstream.com/the-debezium-trio-comparing-kafka-connect-server-and-engine-run-times/
  - https://delta.io/blog/delta-lake-upsert/
  - https://docs.databricks.com/aws/en/delta/merge
  - https://cloudurable.com/blog/kafka-architecture-log-compaction-2025/
  - https://conduktor.io/blog/kafka-offset-management-consumer-commit-guide
  - https://binaryscripts.com/debezium/2025/04/27/handling-database-failures-and-recoveries-with-debezium-ensuring-reliable-cdc.html
  - https://aws.amazon.com/blogs/big-data/accelerate-data-lake-operations-with-apache-iceberg-v3-deletion-vectors-and-row-lineage/
  - https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/
related:
  - docs/plans/2026-03-21-data-pipeline-research-context.plan.md
  - docs/research/2026-03-22-pipeline-orchestration.research.md
  - docs/research/2026-03-22-operations-reliability.research.md
  - docs/research/2026-03-22-open-table-formats.research.md
  - docs/research/2026-03-21-pipeline-design-architecture.research.md
---

## Summary

**Research question:** What patterns and tooling govern Change Data Capture and event-driven data ingestion?

**Mode:** Technical | **SIFT rigor:** High | **Sources:** 21 | **Searches:** 16 across Google

**Key findings:**
- Log-based CDC is the only production-grade mechanism — it reads the database transaction log (PostgreSQL WAL, MySQL binlog) with minimal source impact, captures all change types including deletes, and preserves commit ordering; trigger-based CDC adds write amplification to every DML operation; timestamp-based CDC cannot detect hard deletes and requires schema changes
- Debezium is the dominant open-source CDC platform, built on Kafka Connect, with connectors for PostgreSQL, MySQL, MongoDB, SQL Server, and Oracle — but it requires significant operational overhead; Debezium Server offers a lightweight alternative that trades multi-task support and dynamic management for simpler deployment
- AWS DMS CDC is single-threaded by default with no option for parallel CDC threads to relational targets — under high change rates, replication lag compounds over time and has been observed peaking at 600 seconds
- dlt is not a CDC tool — it supports merge, SCD2, and upsert write dispositions for incremental loading via polling, but does not stream from transaction logs
- Kafka topic-per-table with primary-key message keys is the standard CDC topology — it preserves per-entity ordering within partitions and enables independent consumer group progress
- The transactional outbox pattern eliminates dual writes by writing business data and event payloads in a single database transaction, with Debezium tailing the outbox table via CDC
- Exactly-once delivery is a Kafka-internal guarantee (idempotent producers + transactions + read_committed consumers) — end-to-end exactly-once requires idempotent consumers, most practically achieved via upsert-on-primary-key at the destination
- CDC into Delta Lake uses MERGE INTO (copy-on-write, read-optimized but write-amplified); CDC into Iceberg favors merge-on-read with delete files (write-optimized but requires compaction); Iceberg V3 deletion vectors reduce delete file overhead
- PostgreSQL replication slots prevent WAL deletion until the CDC consumer confirms receipt — if the consumer falls behind, WAL files accumulate and can cause disk exhaustion and a total production outage

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://conduktor.io/glossary/implementing-cdc-with-debezium | Implementing CDC with Debezium | Conduktor | 2025 | T4 | verified — vendor education |
| 2 | https://debezium.io/documentation/reference/stable/features.html | Debezium Features | Debezium/Red Hat | current docs | T1 | verified |
| 3 | https://debezium.io/blog/2019/02/19/reliable-microservices-data-exchange-with-the-outbox-pattern/ | Reliable Microservices Data Exchange with the Outbox Pattern | Debezium/Red Hat | 2019 | T2 | verified — canonical reference |
| 4 | https://docs.confluent.io/kafka/design/delivery-semantics.html | Message Delivery Guarantees | Confluent | current docs | T1 | verified |
| 5 | https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html | Schema Evolution and Compatibility | Confluent | current docs | T1 | verified |
| 6 | https://streamkap.com/resources-and-guides/cdc-to-kafka-topics | CDC to Kafka: Building an Event Backbone | Streamkap | 2025 | T4 | verified — vendor guide |
| 7 | https://streamkap.com/resources-and-guides/idempotency-streaming-pipelines | Idempotency in Streaming Pipelines | Streamkap | 2025 | T4 | verified — vendor guide |
| 8 | https://www.ryft.io/blog/cdc-strategies-in-apache-iceberg | CDC Strategies in Apache Iceberg | Ryft | 2025 | T5 | verified — practitioner blog |
| 9 | https://dlthub.com/docs/general-usage/incremental-loading | Incremental Loading | dlt | current docs | T1 | verified |
| 10 | https://www.bladepipe.com/blog/data_insights/mysql_cdc_vs_postgres_cdc/ | MySQL CDC vs PostgreSQL CDC | BladePipe | 2025 | T4 | verified — vendor comparison |
| 11 | https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Troubleshooting_Latency.html | Troubleshooting latency issues in AWS DMS | AWS | current docs | T1 | verified |
| 12 | https://blog.scottlogic.com/2025/09/08/solving-data-consistency-in-distributed-systems-with-the-transactional-outbox.html | Solving Data Consistency with the Transactional Outbox | Scott Logic | 2025 | T3 | verified — consultancy blog |
| 13 | https://microservices.io/patterns/data/transactional-outbox.html | Transactional Outbox Pattern | microservices.io (Chris Richardson) | current | T2 | verified — canonical reference |
| 14 | https://blog.sequinstream.com/the-debezium-trio-comparing-kafka-connect-server-and-engine-run-times/ | The Debezium Trio: Kafka Connect, Server, and Engine | Sequin | 2025 | T4 | verified — vendor comparison |
| 15 | https://delta.io/blog/delta-lake-upsert/ | Delta Lake Upsert | Delta Lake | current | T1 | verified |
| 16 | https://docs.databricks.com/aws/en/delta/merge | Upsert into a Delta Lake table using merge | Databricks | current docs | T1 | verified |
| 17 | https://cloudurable.com/blog/kafka-architecture-log-compaction-2025/ | Kafka Architecture: Log Compaction | Cloudurable | 2025 | T5 | verified — practitioner blog |
| 18 | https://conduktor.io/blog/kafka-offset-management-consumer-commit-guide | Kafka Offset Management | Conduktor | 2025 | T4 | verified — vendor education |
| 19 | https://binaryscripts.com/debezium/2025/04/27/handling-database-failures-and-recoveries-with-debezium-ensuring-reliable-cdc.html | Handling Database Failures with Debezium | BinaryScripts | 2025 | T5 | verified — practitioner blog |
| 20 | https://aws.amazon.com/blogs/big-data/accelerate-data-lake-operations-with-apache-iceberg-v3-deletion-vectors-and-row-lineage/ | Iceberg V3 Deletion Vectors and Row Lineage | AWS | 2025 | T2 | verified — AWS engineering blog |
| 21 | https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/ | Exactly-Once Semantics Are Possible | Confluent | 2017/2025 | T2 | verified — canonical reference (updated 2025) |

---

## Sub-question 1: CDC Mechanisms — Log-Based, Trigger-Based, and Timestamp-Based

### Log-based CDC

Log-based CDC reads the database's transaction log — PostgreSQL's Write-Ahead Log (WAL), MySQL's binary log (binlog), SQL Server's transaction log — and converts committed changes into structured events. This is the only mechanism that captures all change types (INSERT, UPDATE, DELETE) in their exact commit order without modifying the source schema or adding write overhead to OLTP operations [1][2].

The architecture is straightforward: databases already write every change to a transaction log for crash recovery and replication. Log-based CDC reads this existing log as a secondary consumer. The source database sees minimal additional load — reading the replication log is a lightweight operation that does not execute queries against the database [3].

Key implementation requirements differ by database [10]:

- **PostgreSQL:** Set `wal_level = logical`, create a replication slot, and configure a logical decoding output plugin (pgoutput ships with PostgreSQL 10+). `max_replication_slots` must equal or exceed the number of CDC connectors. Critical risk: replication slots prevent WAL deletion until the CDC consumer confirms receipt — if the consumer falls behind, WAL files accumulate on the primary server and can fill the disk, causing a total production outage.
- **MySQL:** Set `binlog_format = ROW` and `binlog_row_image = FULL` to capture complete before/after row images. Enable GTIDs (`gtid_mode = ON`, `enforce_gtid_consistency = ON`) for reliable position tracking. Performance overhead is estimated at approximately 15% due to the additional row-level logging.

### Trigger-based CDC

Trigger-based CDC installs database triggers on INSERT, UPDATE, and DELETE operations that write change records into shadow/audit tables. Downstream systems then poll or read these tables.

Trigger-based CDC has three significant drawbacks: (1) every DML operation triggers an additional write, adding measurable write amplification to high-throughput OLTP systems; (2) managing triggers across many tables through schema changes is brittle; (3) if the trigger or audit table mechanism fails, it can create cascading write issues that affect the source application. Trigger-based CDC was common before log-based tools matured and is now used primarily in legacy systems where transaction log access is not available.

### Timestamp-based (query-based) CDC

Timestamp-based CDC adds a `last_modified` or `updated_at` column to each table. A polling process queries for rows where the timestamp exceeds the last checkpoint. This is the simplest mechanism to implement but has fundamental limitations: it cannot detect hard DELETE operations (only soft deletes via a status column), it adds computational overhead by scanning every row to identify changes, and it requires schema modifications to add the timestamp column. For polling-based incremental loading — as opposed to true CDC — dlt uses this pattern with cursor-based tracking [9].

### Mechanism comparison

| Aspect | Log-based | Trigger-based | Timestamp-based |
|--------|-----------|---------------|-----------------|
| Captures DELETEs | Yes | Yes | No (soft only) |
| Source schema changes | None | Triggers on tables | Adds column |
| Source write overhead | None | 1 extra write per DML | None |
| Source read overhead | Minimal (log read) | None | Full table scan |
| Latency | Sub-second | Near real-time | Polling interval |
| Ordering fidelity | Commit order | Trigger execution order | Approximate |

---

## Sub-question 2: CDC Tooling — Debezium, AWS DMS, and dlt

### Debezium

Debezium is the dominant open-source CDC platform, built on Apache Kafka Connect [1][2]. It reads database transaction logs and emits structured change events to Kafka topics. Debezium supports connectors for PostgreSQL, MySQL, MongoDB, SQL Server, Oracle, and Db2.

**Architecture:** Three deployment models exist [14]:
1. **Kafka Connect** (recommended for Kafka targets): Debezium connectors run as Kafka Connect source connectors. Provides multi-task parallelism, REST API management, offset storage in Kafka, and dynamic configuration. Requires managing a Kafka Connect cluster.
2. **Debezium Server** (lightweight alternative): Standalone Quarkus application that streams to non-Kafka targets (Kinesis, Pub/Sub, Pulsar, Redis). Single process, low resource requirements, but no multi-task support, no dynamic management, and configuration changes require restarts.
3. **Debezium Engine** (embedded): Library embedded in custom applications. Maximum flexibility but requires implementing your own fault tolerance.

**Event structure:** Each change event contains `before` and `after` row states, operation type (`c` for create, `u` for update, `d` for delete, `r` for read/snapshot), source metadata (database, table, transaction ID, LSN/binlog position), and processing timestamps [1].

**Snapshot modes:** `initial` (snapshot on first run, default), `never` (stream only), `when_needed` (snapshot if no offset exists), and incremental snapshots (Debezium 2.0+) that re-snapshot tables without stopping the connector or locking tables [1][19].

**Production reliability concerns (2025):** Debezium 3.x resolved several critical issues: blocking snapshots that previously could lose streaming events during snapshot failures now preserve the pre-snapshot position and resume correctly; offset validation that failed prematurely during connector startup was fixed; incremental snapshot restarts on SQL Server were corrected [19].

### AWS DMS

AWS Database Migration Service supports CDC via continuous replication. Its primary advantage is managed infrastructure — no Kafka cluster required. Its limitations are significant for high-volume CDC [11]:

- **Single-threaded CDC:** DMS tasks use a single thread for CDC to relational targets with no option for parallel CDC threads. Under high change rates, replication lag compounds over time.
- **Latency:** CDC latency at the target has been observed peaking at approximately 600 seconds during periods of intense activity.
- **LOB handling:** Large Object data types hinder replication performance due to how DMS processes large binary data.
- **Resource bottlenecks:** High-frequency CDC stresses both the target database and the DMS replication instance, requiring careful CloudWatch monitoring of CPU, memory, I/O, and storage.

DMS is appropriate for managed migration scenarios and low-to-moderate change volumes. For high-throughput production CDC, Debezium on Kafka Connect provides significantly better control and performance.

### dlt incremental loading

dlt is not a CDC tool — it does not read transaction logs. It supports incremental loading via polling with cursor-based tracking [9]. Three write dispositions handle different patterns:

- **Append:** New records added without deduplication. Suitable for immutable event streams.
- **Merge:** Upserts using `primary_key` and optional `merge_key`. Supports three strategies: delete-insert, upsert, and SCD2 (Slowly Changing Dimensions Type 2) for historical tracking.
- **Replace:** Full table reload, truncating the destination before loading.

dlt stores incremental state (the last cursor value) in the destination database alongside loaded data. Between pipeline runs, the cursor advances so only new/changed records are fetched. This is timestamp-based/query-based incremental loading — effective for APIs and databases without log access, but fundamentally different from log-based CDC in latency, completeness, and ordering guarantees.

---

## Sub-question 3: Kafka-Backed Pipeline Design

### Topic design

The standard CDC topology uses **one Kafka topic per source table** [6]. This provides clear ownership, independent retention policies per table, simple ACL administration, and consumer subscription granularity — downstream teams subscribe to exactly the tables they need without filtering.

Topic naming should encode origin: `<environment>.<database>.<schema>.<table>` (e.g., `prod.ecommerce.public.orders`). This prevents collisions across multiple databases and simplifies operations when dozens or hundreds of tables are streaming [6].

### Partition strategy and ordering

Messages should use the table's **primary key as the Kafka message key** [6]. This guarantees that all changes for a given entity (e.g., a specific order) land in the same partition and are processed in order. Kafka guarantees ordering within a partition but not across partitions.

Partition count should initially match expected consumer parallelism. A topic with 12 partitions supports up to 12 concurrent consumers in a single consumer group. Increasing partition count later redistributes keys across partitions, which temporarily breaks per-key ordering [6].

### Consumer groups and offset management

Each downstream system should use a distinct consumer group ID (`analytics-warehouse`, `search-indexer`, `fraud-detection`). Multiple consumer groups read the same topic concurrently and track progress independently [6].

**Offset commit strategies** [18]:
- **Auto-commit** (`enable.auto.commit=true`): Offsets committed at a fixed interval (default 5 seconds). Provides at-most-once semantics — if a consumer crashes after auto-commit but before processing completes, the message is lost. Suitable for non-critical workloads only.
- **Manual commit** (`enable.auto.commit=false`): Offsets committed explicitly after successful processing. Enables at-least-once semantics — if a consumer crashes after processing but before committing, the message will be reprocessed on restart. Required for production CDC pipelines.

Best practice: commit offsets **after** successfully processing a batch, not before. For exactly-once semantics, store offsets alongside processed data in a transactional system (e.g., write both the data and the offset to the same database in one transaction) [18].

### Schema Registry

Avro with Confluent Schema Registry is the standard serialization choice for CDC-to-Kafka pipelines [5][6]. It provides compact binary encoding, mandatory schema definitions, and compatibility enforcement that prevents producers from publishing breaking changes.

**Compatibility modes** [5]:
- **Backward** (default, recommended for CDC): New schema can read data written with the previous schema. Allows adding fields with defaults and removing optional fields.
- **Forward:** Previous schema can read data written with the new schema. Allows removing fields and adding optional fields.
- **Full:** Both backward and forward compatible. Most restrictive — only allows adding/removing optional fields with defaults.
- **Transitive variants** (BACKWARD_TRANSITIVE, etc.): Extend compatibility checks to all previous schema versions, not just the immediately prior one.

A single `ALTER TABLE` upstream can halt deserialization for every downstream consumer if schema compatibility is not enforced. Register schemas in CI/CD and give producer/consumer clients read-only access to the registry, treating schemas as data contracts [5].

### Log compaction

For CDC topics where consumers need the current state of each entity rather than full change history, enable Kafka log compaction (`cleanup.policy=compact`) [17]. Compaction retains only the latest message per key within each partition, keeping topic storage bounded while preserving the most recent state. For CDC, combine compaction with time-based retention (e.g., 7 days) to preserve recent history for replay scenarios while eventually compacting to current-state-only [17].

---

## Sub-question 4: Event Sourcing and the Transactional Outbox Pattern

### The dual-write problem

When a microservice needs to both update its database and publish an event to a message broker, it faces the dual-write problem: there is no transaction manager that spans both systems atomically [3][12][13]. If the database write succeeds but the event publish fails, the system state diverges from the event stream. If the event publishes but the database write fails, consumers act on phantom events.

### The transactional outbox pattern

The outbox pattern solves dual writes by writing both the business data and the event payload to the same database in a single transaction [3][12][13]:

1. A service receives a request (e.g., "place order")
2. In one database transaction, it writes the order to the `orders` table and an event record to the `outbox` table
3. The transaction commits atomically — both writes succeed or both fail
4. A separate relay process reads the outbox table and publishes events to the message broker
5. After successful publication, the outbox record is deleted or marked as processed

The outbox table typically contains: `id` (unique event identifier), `aggregatetype` (entity category, e.g., "Order"), `aggregateid` (entity ID, used as Kafka message key), `type` (event type, e.g., "OrderCreated"), and `payload` (JSON event content) [3].

### CDC-based outbox relay (Debezium)

The relay process can use polling (query the outbox table periodically) or CDC (tail the transaction log). CDC via Debezium is preferred because it provides near-zero latency (events appear in Kafka within milliseconds of commit), adds zero additional database query load, and eliminates polling logic [3].

Debezium provides a built-in Outbox Event Router SMT (Single Message Transform) that routes events to Kafka topics based on `aggregatetype`, uses `aggregateid` as the Kafka message key (ensuring per-entity ordering), and propagates the event UUID in Kafka headers for downstream duplicate detection [3].

**Idempotency requirement:** The relay may publish an event more than once if it fails after publishing but before marking the outbox record as processed. Consumers must be idempotent — checking a local record of processed event IDs before taking action [12].

### Event sourcing vs. CDC

Event sourcing and CDC solve different problems but are often conflated. Event sourcing treats events as the primary source of truth — the current state is derived by replaying events. CDC captures changes from a state-oriented database and emits them as events. The choice depends on context: legacy systems with existing databases favor CDC; new applications with strong audit/replay requirements may benefit from event sourcing. Hybrid approaches use the outbox pattern for critical operations and CDC for auxiliary data replication [13].

---

## Sub-question 5: CDC Writes into Delta Lake and Iceberg

### Delta Lake: MERGE INTO (copy-on-write)

Delta Lake's primary CDC ingestion mechanism is MERGE INTO, which performs a copy-on-write operation [15][16]. When a merge executes, Delta Lake:

1. Identifies target files that may contain matching rows (using data-skipping statistics and partition pruning)
2. Reads those files and joins them against the source (CDC) batch
3. Rewrites matched files with the merged result
4. Commits the new file set atomically via the transaction log

Delta Lake 3.0 improved MERGE performance by up to 56% [15]. However, MERGE remains fundamentally write-amplified: updating 10 rows scattered across 10 Parquet files means rewriting all 10 files. For high-frequency micro-batch CDC, this creates many small files that require periodic OPTIMIZE (compaction) and ZORDER (clustering) to maintain read performance.

**Streaming CDC pattern:** Use Spark Structured Streaming with `foreachBatch` to apply MERGE against incoming CDC micro-batches [16]. Partition the Delta table by date and restrict the merge condition to recent partitions to reduce the scan/rewrite surface.

**Databricks AUTO CDC:** A declarative API (`APPLY CHANGES INTO`) that automatically merges CDC events into Delta tables, handling out-of-order data and SCD2 semantics without manual MERGE statements [16].

### Iceberg: merge-on-read with compaction

Iceberg's CDC strategy differs fundamentally from Delta Lake [8][20]:

**Merge-on-Read (MoR):** Instead of rewriting data files on every update, Iceberg writes a small delete file that marks which rows in existing data files are invalidated. At read time, the engine merges delete files with data files to produce the correct result. This keeps write latency low but shifts cost to reads.

**Compaction requirement:** Delete files accumulate in high-frequency CDC scenarios, causing read amplification — queries must scan both data files and delete files, filtering out invalidated rows. Without regular compaction, query latency degrades significantly [8]. Recommended compaction cadence for CDC tables: at least daily, with `delete-file-threshold` set to trigger earlier compaction when delete files pile up (50 is a common threshold). Pair with `rewrite_manifests`, `expire_snapshots`, and `remove_orphan_files` for complete table maintenance [8].

**Iceberg V3 deletion vectors (2025):** Replace positional delete files with an efficient binary format stored as Puffin files. Instead of separate delete files per operation, deletion vectors consolidate references to a single vector per data file, reducing metadata overhead and improving read performance [20].

**Two CDC ingestion patterns for Iceberg** [8]:
1. **Direct materialization:** Tools like Flink CDC write directly to final Iceberg tables, handling merge logic internally. Simpler to operate but less flexible.
2. **Raw change log + ETL:** Append all CDC events to a bronze table, then run a separate MERGE INTO process to materialize the final mirror table. Preserves complete history and enables replay, but requires maintaining two tables and a merge pipeline.

### Strategy comparison

| Aspect | Delta Lake (MERGE INTO) | Iceberg (Merge-on-Read) |
|--------|------------------------|------------------------|
| Write cost | High (file rewrite) | Low (small delete files) |
| Read cost | Low (pre-merged) | Higher (merge at read) |
| Compaction need | OPTIMIZE for small files | Critical for delete files |
| Streaming fit | foreachBatch + MERGE | Flink CDC direct write |
| Out-of-order handling | Manual or AUTO CDC | Manual or Flink |
| V3 improvements | — | Deletion vectors reduce overhead |

---

## Sub-question 6: Delivery Semantics — Idempotency, Ordering, and Exactly-Once

### Kafka delivery guarantees

Kafka provides three delivery semantics [4][21]:

- **At-most-once:** Producer sends without waiting for acknowledgment. Messages may be lost but are never duplicated. Lowest latency, lowest reliability.
- **At-least-once:** Producer retries on failure. Messages are never lost but may be duplicated. Since Kafka 3.0, the default producer configuration enables idempotent delivery (`acks=all`, `enable.idempotence=true`), which prevents duplicates during producer retries by assigning each producer an ID and deduplicating messages using sequence numbers [4].
- **Exactly-once (Kafka internal):** Transactional delivery (Kafka 0.11.0.0+) allows a producer to atomically write to multiple partitions. Consumers using `isolation.level=read_committed` only see data from committed transactions. Kafka 4.0+ in KRaft mode provides faster transaction commits and reduced coordinator overhead [21].

### Exactly-once is a Kafka-internal guarantee, not end-to-end

Kafka's exactly-once semantics apply to data within Kafka — producing to topics and consuming from topics within the Kafka ecosystem [21]. When a pipeline writes to an external system (a data warehouse, a lakehouse, an API), Kafka cannot enforce exactly-once at the destination. The external system must participate.

The practical implication: **end-to-end exactly-once requires idempotent consumers** [7]. Four patterns achieve this:

1. **Upsert on primary key** (most practical): Use `INSERT...ON CONFLICT UPDATE`, `MERGE`, or destination-native upsert. When a record is replayed, the existing row is overwritten rather than duplicated. Works for Snowflake (MERGE), PostgreSQL (ON CONFLICT), ClickHouse (ReplacingMergeTree), Delta Lake (MERGE INTO) [7].
2. **Read-time deduplication:** Append all records (including duplicates) and deduplicate at query time using `ROW_NUMBER()` over primary key ordered by timestamp. Simple to implement but pushes cost to every query.
3. **Conditional writes:** Only update if the incoming version/timestamp is newer than the existing record. Prevents stale replays from overwriting current data.
4. **Seen-set deduplication:** Track processed record IDs in Redis, a database table, or in-memory state. Adds operational complexity and state management burden.

### Non-idempotent operations are dangerous

Aggregations like SUM are not idempotent — if a record replays, the total increases again [7]. Store raw facts with upserted primary keys and compute aggregates at query time. Never maintain running totals in a streaming pipeline that operates with at-least-once delivery.

### Ordering guarantees

Kafka guarantees message ordering within a single partition [6]. Debezium partitions CDC events by primary key, so all changes to a specific entity land on the same Kafka partition and are ordered by commit time. Cross-partition ordering is not guaranteed — if two tables have a foreign key relationship, changes to a parent row and changes to child rows may be processed in different order because they are on different topics/partitions.

For pipelines that require cross-entity ordering (e.g., applying parent before child), consumers must implement ordering logic: buffer events, sort by transaction ID or LSN, and apply in order. Debezium's transaction metadata feature groups events by database transaction, enabling consumers to reconstruct transaction boundaries.

---

## Challenge

Challenger research targeted the reliability of CDC mechanisms, the operational realities of Debezium and DMS, the practicality of exactly-once semantics, and the write strategy tradeoffs for lakehouse targets.

### Log-based CDC is not zero-impact on the source

Multiple sources describe log-based CDC as having "minimal impact" on the source database [1][2]. This is directionally correct — reading the transaction log does not execute queries against user tables. But it is not zero-impact. PostgreSQL's logical decoding must reconstruct transactions, and if decoding exceeds `logical_decoding_work_mem`, it spills to disk, creating I/O and CPU pressure on the primary [10]. MySQL's row-based binlog logging adds approximately 15% write overhead versus statement-based logging [10]. Replication slots in PostgreSQL prevent WAL segment cleanup, risking disk exhaustion. The "minimal impact" framing is accurate for normal operations but understates tail-case risks.

### AWS DMS single-threaded limitation is underemphasized in documentation

AWS documentation describes DMS latency troubleshooting but does not prominently surface the single-threaded CDC constraint for relational targets [11]. This limitation means that under high change rates, DMS cannot parallelize CDC processing, and lag compounds over time. The observed 600-second peak latency under intense activity is a real-world data point but is workload-dependent. Teams evaluating DMS for CDC should performance-test with production-representative change volumes before committing.

### Exactly-once delivery vs. exactly-once processing

Confluent's 2017/2025 post titled "Exactly-Once Semantics Are Possible" [21] refers specifically to Kafka-internal semantics — producing to and consuming from Kafka topics. Many practitioners interpret this as end-to-end exactly-once, which it is not. True end-to-end exactly-once requires the destination to participate (via upsert, conditional write, or transactional offset storage). The Kafka community has clarified this distinction, but the original framing continues to cause confusion. For CDC pipelines landing in a data warehouse or lakehouse, at-least-once delivery with idempotent consumers (upsert-on-primary-key) is the standard and most practical pattern [7].

### Delta Lake MERGE write amplification is workload-dependent

The claim that MERGE is "write-amplified" is true in the general case — updating scattered rows requires rewriting entire Parquet files [15]. But the degree of amplification depends on data distribution: if CDC updates are concentrated in recent partitions (common for time-series data), partitioning by date restricts the merge surface to a small number of files. The 56% performance improvement in Delta Lake 3.0 further narrows the gap. For entity tables where updates touch any partition, write amplification remains significant.

### Iceberg merge-on-read compaction is not optional

Sources recommend compaction "at least daily" for CDC tables [8]. This understates the operational burden for high-frequency CDC. Without aggressive compaction, delete files accumulate rapidly, and read performance degrades non-linearly. Iceberg V3 deletion vectors [20] mitigate this by consolidating delete references per data file, but compaction remains a hard operational requirement, not a nice-to-have. Teams adopting Iceberg for CDC workloads must budget for compaction infrastructure and monitoring as a first-class operational concern.

### The outbox pattern adds complexity even as it solves dual writes

The transactional outbox pattern is presented as an elegant solution to dual writes [3][12][13]. It is — but the operational complexity is non-trivial: you need to deploy and manage Debezium (or a polling relay), configure logical replication on the database, monitor consumer lag, handle connector restarts, and manage schema evolution of the outbox table itself. For teams already running Kafka and Debezium, adding an outbox table is incremental. For teams without this infrastructure, the outbox pattern requires standing up the entire CDC stack to solve what appears to be a simple consistency problem.

---

## Findings

### Finding 1: Log-based CDC is the only production-grade mechanism for reliable change capture
**Confidence: HIGH**

Log-based CDC reads the database's existing transaction log, capturing all change types (INSERT, UPDATE, DELETE) in commit order with minimal source database impact. Trigger-based CDC adds write amplification to every DML operation — unacceptable for high-throughput OLTP systems. Timestamp-based CDC fundamentally cannot capture hard deletes and requires schema modifications. The choice is not between three equal alternatives; it is between one production mechanism (log-based) and two legacy approaches with known deficiencies. All major CDC tools (Debezium, AWS DMS, Fivetran, Airbyte) use log-based capture as their primary mechanism.

### Finding 2: Debezium requires significant operational investment but is the correct default for open-source CDC
**Confidence: HIGH**

Debezium on Kafka Connect is the dominant open-source CDC platform for good reason: it supports all major databases, emits structured events with before/after state, handles snapshots and incremental re-snapshots, and integrates natively with Schema Registry. But it requires managing a Kafka Connect cluster (or at minimum a Kafka cluster), monitoring connector health, handling offset management, and dealing with database-specific configuration (WAL levels, replication slots, binlog formats). Debezium Server offers a lighter alternative for non-Kafka targets, trading multi-task support and dynamic management for simpler deployment. AWS DMS is appropriate for managed migration scenarios and moderate CDC volumes but is single-threaded for relational targets and inappropriate for high-throughput production CDC.

### Finding 3: End-to-end exactly-once requires idempotent consumers, not just Kafka transactions
**Confidence: HIGH**

Kafka's exactly-once semantics (idempotent producers + transactions + read_committed consumers) prevent duplicates within Kafka. They do not prevent duplicates at the destination. CDC pipelines that write to a warehouse or lakehouse operate with at-least-once delivery at the destination boundary. The most practical pattern for end-to-end exactly-once processing is upsert-on-primary-key at the destination (MERGE, ON CONFLICT, ReplacingMergeTree). This is simpler, more robust, and more widely supported than alternatives like seen-set deduplication or conditional writes. Non-idempotent operations (running totals, SUM) must be avoided in at-least-once pipelines — store raw facts and compute aggregates at query time.

### Finding 4: CDC write strategy must match the target format's strengths
**Confidence: HIGH**

Delta Lake uses copy-on-write (MERGE INTO) — writes are expensive (file rewrites) but reads are fast (pre-merged data). Iceberg uses merge-on-read — writes are cheap (small delete files) but reads require merging at query time and degrade without compaction. The choice depends on the workload profile: read-heavy analytics workloads with moderate CDC frequency favor Delta Lake's pre-merged approach; write-heavy CDC workloads with high change rates favor Iceberg's merge-on-read with scheduled compaction. Neither is universally superior. Iceberg V3 deletion vectors narrow the gap by reducing delete file overhead, but compaction remains a hard operational requirement for Iceberg CDC workloads.

### Finding 5: The transactional outbox pattern is the correct solution for dual writes in event-driven architectures
**Confidence: HIGH**

The outbox pattern — writing business data and event payloads in a single database transaction, then relaying events via CDC — is the only pattern that provides atomic consistency between state changes and event publication without distributed transactions. Debezium's built-in Outbox Event Router SMT provides production-ready support. The pattern requires the CDC infrastructure stack (Debezium, Kafka, replication configuration), which makes it a significant commitment for teams not already running this stack. But the alternative — hoping that dual writes to a database and message broker both succeed — is not a pattern; it is a source of eventual data inconsistency.

---

## Claims

| # | Claim | Source | Status | Notes |
|---|-------|--------|--------|-------|
| 1 | Log-based CDC captures all change types (INSERT, UPDATE, DELETE) in commit order with minimal source impact | [1][2][10] | verified | Confirmed across Debezium docs and multiple practitioner sources |
| 2 | Trigger-based CDC adds write amplification to every DML operation | [1] | verified | Each DML triggers an additional write to the shadow/audit table |
| 3 | Timestamp-based CDC cannot detect hard DELETE operations | [1][9] | verified | Only soft deletes via status column; dlt docs confirm cursor-based limitation |
| 4 | PostgreSQL replication slots prevent WAL deletion and can cause disk exhaustion | [10] | verified | Confirmed by BladePipe comparison and PostgreSQL documentation |
| 5 | MySQL row-based binlog adds approximately 15% write overhead | [10] | qualified | BladePipe estimate; actual overhead depends on workload characteristics |
| 6 | AWS DMS uses a single thread for CDC to relational targets with no parallel option | [11] | verified | AWS documentation confirms; CDC latency peaks at ~600s under high load |
| 7 | Debezium Server lacks multi-task support and dynamic management compared to Kafka Connect | [14] | verified | Sequin comparison confirms feature/simplicity tradeoff |
| 8 | Kafka guarantees message ordering within a single partition, not across partitions | [4][6] | verified | Fundamental Kafka design property; confirmed by Confluent docs |
| 9 | Schema Registry backward compatibility is the default and recommended mode for CDC topics | [5] | verified | Confluent docs confirm; allows adding fields with defaults and removing optional fields |
| 10 | The transactional outbox pattern eliminates dual writes via single-transaction atomicity | [3][12][13] | verified | Canonical pattern confirmed by microservices.io, Debezium, and Scott Logic |
| 11 | Debezium provides a built-in Outbox Event Router SMT for outbox pattern support | [3] | verified | Routes events by aggregate type, uses aggregate ID as Kafka key |
| 12 | Delta Lake 3.0 improved MERGE performance by up to 56% | [15] | verified | Delta Lake blog; improvement is workload-dependent |
| 13 | Iceberg merge-on-read requires at least daily compaction for CDC workloads | [8] | verified | Ryft recommendation; frequency depends on change rate |
| 14 | Iceberg V3 deletion vectors consolidate delete references per data file using Puffin format | [20] | verified | AWS engineering blog; replaces positional delete files |
| 15 | Kafka's exactly-once semantics apply within Kafka, not end-to-end to external systems | [4][21] | verified | Confluent docs explicitly state external systems must participate |
| 16 | Upsert-on-primary-key is the most practical pattern for idempotent CDC consumers | [7] | verified | Streamkap guide; works across Snowflake, PostgreSQL, ClickHouse, Delta Lake |
| 17 | dlt supports merge, SCD2, and upsert write dispositions but uses polling, not log-based CDC | [9] | verified | dlt docs confirm cursor-based incremental loading, not transaction log reading |
| 18 | Kafka auto-commit provides at-most-once semantics; manual commit enables at-least-once | [18] | verified | Conduktor guide; auto-commit risks message loss on consumer crash |
