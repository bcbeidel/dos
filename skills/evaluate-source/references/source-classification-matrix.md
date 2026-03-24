# Source Classification Matrix

Source type constrains available ingestion methods — this is not a free choice. Classify first, then select the ingestion approach.

## Classification Table

| Source Type | Examples | Key Constraints | Typical Ingestion |
|-------------|----------|-----------------|-------------------|
| **Transactional DB** | PostgreSQL, MySQL, Oracle, SQL Server | Extraction load on source; need reliable timestamps for incremental | Full load, incremental (cursor), or CDC (log-based) |
| **Event Stream** | Kafka, Kinesis, Pub/Sub | Retention period; schema registry; partition strategy | Streaming consumers |
| **SaaS API** | Salesforce, Stripe, HubSpot, GitHub | Rate limits, pagination, vendor-controlled auth; most schema-volatile type | API extraction (managed connectors preferred) |
| **File-Based** | CSV/JSON via SFTP, S3, GCS, Azure Blob | No query interface; format consistency; silent delivery gaps | Polling or event-driven detection |

## Ingestion Approach Selection

| Question | Full Load | Incremental (Cursor) | CDC (Log-Based) |
|----------|-----------|----------------------|------------------|
| Change frequency? | Rare or small dataset | Moderate, regular | High frequency |
| Must track hard deletes? | No | No | Yes |
| Freshness requirement? | Hours/daily | Hours/daily | Minutes/real-time |
| Source system impact? | Full query load | Filtered query load | Minimal (reads logs) |

**Hybrid is typical:** Full loads for small dimensions, incremental for regular fact tables, CDC for high-value transactional data.

## Incremental Pattern by Source Type

| Source Type | Recommended Pattern | Silent Failure Modes |
|-------------|-------------------|---------------------|
| Transactional DB (small) | Full refresh | None — simplest approach |
| Transactional DB (large) | Merge/upsert on PK | Full-table scan without partition pruning |
| Transactional DB (high-freq) | CDC via Debezium | Slot replication lag; WAL growth |
| Event stream | Append | Duplicate accumulation if source replays |
| SaaS API | Incremental (cursor) or full refresh | Missed gaps if cursor is unreliable; rate limit throttling |
| File-based (immutable) | Append | Silent delivery gaps; duplicate files |
| File-based (mutable) | Full refresh per file | Partial file delivery |

## dlt vs CDC: Critical Distinction

**dlt is a polling/extraction tool, not CDC.** It does not read transaction logs.

| Capability | dlt | Debezium / Platform CDC |
|-----------|-----|------------------------|
| Reads transaction logs | No | Yes |
| Tracks hard deletes | Only via soft-delete columns | Yes (via log events) |
| Source system impact | Query load per extraction | Minimal (log reader) |
| Latency floor | Minutes (polling interval) | Seconds |
| Best for | API extraction, file sources, DB polling | High-frequency transactional sources |

**Decision rule:** If the source is a transactional DB with high change frequency and hard deletes matter, use Debezium or platform-native CDC. dlt is appropriate for API extraction, file-based sources, and database polling with cursor-based incremental loading.

## Idempotency Requirements

Every pipeline must produce the same result if re-executed:

| Strategy | Mechanism |
|----------|-----------|
| Delete+Insert | Remove then insert within transaction boundaries |
| Merge/Upsert | Update existing, insert new, based on key |
| Immutable append | Append with processing timestamps, deduplicate at read time |
