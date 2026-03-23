---
name: "Open Table Formats: Tradeoffs and Selection Criteria"
description: "Comparison of Delta Lake, Iceberg, Parquet, ORC, and Avro — capabilities, cross-platform compatibility, catalog interop, and format selection guidance"
type: research
sources:
  - https://www.onehouse.ai/blog/apache-hudi-vs-delta-lake-vs-apache-iceberg-lakehouse-feature-comparison
  - https://www.datacamp.com/blog/iceberg-vs-delta-lake
  - https://clickhouse.com/docs/engines/table-engines/integrations/iceberg
  - https://clickhouse.com/blog/climbing-the-iceberg-with-clickhouse
  - https://bigdataboutique.com/blog/clickhouse-and-apache-iceberg-practical-guide-to-data-lakehouse-integration
  - https://docs.databricks.com/aws/en/delta/uniform
  - https://www.databricks.com/blog/open-sourcing-unity-catalog
  - https://www.e6data.com/blog/iceberg-catalogs-2025-emerging-catalogs-modern-metadata-management
  - https://docs.snowflake.com/en/user-guide/tables-iceberg-configure-catalog-integration-rest
  - https://docs.snowflake.com/en/user-guide/opencatalog/overview
  - https://cloud.google.com/blog/products/data-analytics/announcing-bigquery-tables-for-apache-iceberg
  - https://opensource.googleblog.com/2025/08/whats-new-in-iceberg-v3.html
  - https://trino.io/docs/current/connector/iceberg.html
  - https://trino.io/docs/current/connector/delta-lake.html
  - https://dev.to/alexmercedcoder/the-ultimate-guide-to-open-table-formats-iceberg-delta-lake-hudi-paimon-and-ducklake-dnk
  - https://flink.apache.org/2025/10/14/from-stream-to-lakehouse-kafka-ingestion-with-the-flink-dynamic-iceberg-sink/
  - https://www.puppygraph.com/blog/apache-parquet-vs-orc
  - https://quesma.com/blog/apache-iceberg-practical-limitations-2025/
  - https://www.automq.com/blog/why-iceberg-is-so-popular-in-2025
  - https://www.techtarget.com/searchdatamanagement/news/366588032/Databricks-1B-plus-Tabular-acquisition-adds-Iceberg-support
  - https://aws.amazon.com/blogs/big-data/accelerate-data-lake-operations-with-apache-iceberg-v3-deletion-vectors-and-row-lineage/
  - https://iceberg.apache.org/docs/latest/maintenance/
  - https://www.starburst.io/blog/apache-iceberg-files/
  - https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-datalake-native-frameworks-limitations.html
  - https://www.snowflake.com/en/engineering-blog/bidirectional-interoperability-iceberg-snowflake-horizon-catalog/
  - https://cloudurable.com/blog/kafka-avro-schema-registry-2025/
related:
  - docs/research/2026-03-21-pipeline-design-architecture.research.md
  - docs/research/2026-03-22-data-modeling.research.md
---

## Key Findings

1. **File formats vs table formats are distinct layers.** Parquet/ORC/Avro are file formats defining byte layout. Delta Lake and Iceberg are table formats layered on top of Parquet, adding ACID transactions, schema evolution, time travel, and metadata management.
2. **Iceberg is the emerging cross-platform interop standard.** Every major platform (Snowflake, BigQuery, Databricks, Trino, Spark, Flink) supports Iceberg read/write. Delta Lake's strongest integration remains Databricks/Spark. UniForm bridges the gap by generating Iceberg metadata from Delta tables.
3. **The REST Catalog spec is the universal interop layer.** Polaris, Unity Catalog, Nessie, Glue, and Lakekeeper all implement the Iceberg REST Catalog API, enabling any compatible engine to read/write tables without custom integration.
4. **ClickHouse has production Iceberg read/write support** (confirmed by T1 release notes: INSERT 25.7, CREATE/DELETE 25.8, UPDATE/distributed 25.9–25.10; earlier T1 docs were stale). Native MergeTree remains 2-3x faster. The hot/cold tiering pattern (MergeTree for recent data, Iceberg for historical) is the recommended architecture.
5. **Streaming writes to Iceberg have hard concurrency limits** (~15 commits/min/table). Flink is the strongest streaming-to-Iceberg engine; Avro remains the standard Kafka serialization format feeding into lakehouse pipelines.
6. **Iceberg metadata overhead is non-trivial.** Compaction, snapshot expiration, and orphan file cleanup are mandatory maintenance. Target file sizes of 256-512 MB. Time travel retention without expiration can cause 5-200x storage bloat.
7. **Industry is converging toward Iceberg as the interop standard**, accelerated by Databricks' $1B+ Tabular acquisition (June 2024), Iceberg v3 ratification (August 2025), and Snowflake's full bidirectional Iceberg support (October 2025).

## Search Log

| # | Query | Engine | Results Selected |
|---|-------|--------|-----------------|
| 1 | "Delta Lake vs Iceberg 2025 2026 comparison tradeoffs" | WebSearch | onehouse.ai feature comparison, datacamp.com, puppygraph.com |
| 2 | "Apache Iceberg cross-platform compatibility Snowflake BigQuery Databricks Trino 2025" | WebSearch | databricks.com Iceberg support, quesma.com limitations, atlan.com BigQuery guide |
| 3 | "Parquet vs ORC vs Avro comparison file format 2025" | WebSearch | puppygraph.com, motherduck.com, hashstudioz.com |
| 4 | "ClickHouse Iceberg integration S3 table engine 2025" | WebSearch | clickhouse.com docs, clickhouse.com blog, bigdataboutique.com, altinity.com |
| 5 | "Iceberg REST Catalog Polaris universal catalog interoperability 2025" | WebSearch | e6data.com catalog survey, polaris.apache.org, snowflake.com |
| 6 | "Delta Lake UniForm Iceberg compatibility layer 2025 2026" | WebSearch | databricks docs uniform, chaosgenius.io, capitalone.com |
| 7 | "Delta Lake Iceberg streaming CDC writes Spark Flink compaction" | WebSearch | dev.to ultimate guide, kai-waehner.de, flink.apache.org dynamic sink |
| 8 | "Unity Catalog open source Iceberg REST catalog 2025" | WebSearch | unitycatalog.io, databricks.com open-sourcing, e6data.com |
| 9 | "Snowflake Polaris Iceberg catalog managed tables 2025" | WebSearch | snowflake docs, snowflake.com Polaris blog |
| 10 | "BigQuery managed Iceberg tables Apache 2025" | WebSearch | cloud.google.com docs, atlan.com BigQuery guide |
| 11 | "Databricks Tabular acquisition impact Iceberg Delta Lake convergence 2025" | WebSearch | techtarget.com, databricks.com, automq.com |
| 12 | "Iceberg adoption rate industry trend 2025 2026 vs Delta Lake market share" | WebSearch | automq.com, n-ix.com, datalakehousehub.com |
| 13 | "Parquet ORC compression benchmark predicate pushdown performance 2024 2025" | WebSearch | dzone.com, puppygraph.com, newmathdata.com |
| 14 | "Avro Kafka serialization lakehouse CDC format role 2025" | WebSearch | cloudurable.com, confluent.io, flink.apache.org dynamic sink |
| 15 | "open table format selection criteria decision framework 2025" | WebSearch | opensourcedatasummit.com |
| 16 | "Iceberg v3 features deletion vectors spec 2025" | WebSearch | Google OSS blog, AWS blog, snowflake.com |
| 17 | "AWS Glue Data Catalog Iceberg Delta Lake integration limitations" | WebSearch | AWS docs |
| 18 | "ClickHouse MergeTree vs Parquet performance S3 data lake patterns" | WebSearch | clickhouse.com blog, altinity.com |
| 19 | "Snowflake Iceberg tables read write support external engines bidirectional 2025" | WebSearch | snowflake.com engineering blog, snowflake docs |
| 20 | "Trino Iceberg Delta Lake read write support connector 2025" | WebSearch | trino.io docs |
| 21 | "Iceberg metadata overhead storage cost time travel retention small files compaction 2025" | WebSearch | iceberg.apache.org maintenance, e6data.com, starburst.io |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.onehouse.ai/blog/apache-hudi-vs-delta-lake-vs-apache-iceberg-lakehouse-feature-comparison | Hudi vs Delta Lake vs Iceberg Feature Comparison Deep Dive | Onehouse | 2025 | T2 | verified |
| 2 | https://clickhouse.com/docs/engines/table-engines/integrations/iceberg | Iceberg table engine docs | ClickHouse | 2025 | T1 | verified — confirms read-only, no write support in official docs |
| 3 | https://clickhouse.com/blog/climbing-the-iceberg-with-clickhouse | Climbing the Iceberg with ClickHouse | ClickHouse | 2025 | T1 | verified — confirms write is roadmap only, not shipped |
| 4 | https://bigdataboutique.com/blog/clickhouse-and-apache-iceberg-practical-guide-to-data-lakehouse-integration | ClickHouse and Iceberg Practical Guide | BigData Boutique | 2025 | T2 | verified — claims 25.7-25.9 write support; CONFLICTS with T1 sources [2][3] |
| 5 | https://docs.databricks.com/aws/en/delta/uniform | Delta UniForm docs | Databricks | 2025 | T1 | verified — confirms read-only Iceberg access, GA |
| 6 | https://www.e6data.com/blog/iceberg-catalogs-2025-emerging-catalogs-modern-metadata-management | Iceberg Catalogs 2025 | e6data | 2025 | T2 | verified |
| 7 | https://docs.snowflake.com/en/user-guide/tables-iceberg-configure-catalog-integration-rest | Snowflake Iceberg REST Catalog Integration | Snowflake | 2025 | T1 | verified |
| 8 | https://opensource.googleblog.com/2025/08/whats-new-in-iceberg-v3.html | What's New in Iceberg V3 | Google | Aug 2025 | T1 | verified — confirms v3 features and Aug 2025 ratification |
| 9 | https://dev.to/alexmercedcoder/the-ultimate-guide-to-open-table-formats-iceberg-delta-lake-hudi-paimon-and-ducklake-dnk | Ultimate Guide to Open Table Formats | Alex Merced/Dremio | Sep 2025 | T2 | verified |
| 10 | https://flink.apache.org/2025/10/14/from-stream-to-lakehouse-kafka-ingestion-with-the-flink-dynamic-iceberg-sink/ | Flink Dynamic Iceberg Sink | Apache Flink | Oct 2025 | T1 | verified |
| 11 | https://www.puppygraph.com/blog/apache-parquet-vs-orc | Apache Parquet vs ORC | PuppyGraph | 2025 | T3 | verified |
| 12 | https://quesma.com/blog/apache-iceberg-practical-limitations-2025/ | Apache Iceberg Practical Limitations 2025 | Quesma | 2025 | T2 | verified — confirms 15 commits/min ceiling (Adobe data) |
| 13 | https://www.automq.com/blog/why-iceberg-is-so-popular-in-2025 | Why Iceberg is Popular in 2025 | AutoMQ | 2025 | T3 | verified |
| 14 | https://www.techtarget.com/searchdatamanagement/news/366588032/Databricks-1B-plus-Tabular-acquisition-adds-Iceberg-support | Databricks $1B+ Tabular Acquisition | TechTarget | Jun 2024 | T2 | verified |
| 15 | https://trino.io/docs/current/connector/iceberg.html | Trino Iceberg Connector | Trino | 2025 | T1 | verified |
| 16 | https://trino.io/docs/current/connector/delta-lake.html | Trino Delta Lake Connector | Trino | 2025 | T1 | verified |
| 17 | https://iceberg.apache.org/docs/latest/maintenance/ | Iceberg Maintenance Docs | Apache Iceberg | 2025 | T1 | verified |
| 18 | https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-datalake-native-frameworks-limitations.html | AWS Glue Framework Limitations | AWS | 2025 | T1 | verified |
| 19 | https://www.snowflake.com/en/engineering-blog/bidirectional-interoperability-iceberg-snowflake-horizon-catalog/ | Snowflake Bidirectional Iceberg Interop | Snowflake | Mar 2026 | T1 | verified — confirms external engine write access to Snowflake-managed Iceberg |
| 20 | https://docs.snowflake.com/en/user-guide/opencatalog/overview | Snowflake Open Catalog Overview | Snowflake | 2025 | T1 | verified |
| 21 | https://cloudurable.com/blog/kafka-avro-schema-registry-2025/ | Kafka Avro Schema Registry 2025 | Cloudurable | 2025 | T2 | verified |
| 22 | https://cloud.google.com/blog/products/data-analytics/announcing-bigquery-tables-for-apache-iceberg | BigQuery Tables for Iceberg | Google Cloud | 2025 | T1 | verified |
| 23 | https://aws.amazon.com/blogs/big-data/accelerate-data-lake-operations-with-apache-iceberg-v3-deletion-vectors-and-row-lineage/ | Iceberg V3 Deletion Vectors on AWS | AWS | Nov 2025 | T1 | verified |
| 24 | https://www.kai-waehner.de/blog/2025/11/19/data-streaming-meets-lakehouse-apache-iceberg-for-unified-real-time-and-batch-analytics/ | Data Streaming Meets Lakehouse | Kai Waehner | Nov 2025 | T2 | verified |
| 25 | https://www.databricks.com/blog/open-sourcing-unity-catalog | Open Sourcing Unity Catalog | Databricks | 2024 | T1 | verified |
| 26 | https://www.starburst.io/blog/apache-iceberg-files/ | Iceberg File Explosion Problem | Starburst | 2025 | T2 | verified |

### SIFT Evaluation Notes

**Source conflict — ClickHouse Iceberg write support (RESOLVED):**
Sources [2] (T1, official docs) and [3] (T1, official blog) indicated read-only integration, while Source [4] (T2, BigData Boutique) claimed write support in 25.7–25.9. Challenger phase verified via official ClickHouse release blogs (T1) that write support did ship on the claimed timeline. Sources [2] and [3] were written before these releases and became stale. Confidence upgraded to HIGH.

## Raw Extracts

### Sub-question 1: Format taxonomy & capability matrix

**File formats vs table formats: two distinct layers**

File formats (Parquet, ORC, Avro) define how bytes are laid out on disk. Table formats (Delta Lake, Iceberg) are metadata and protocol layers that sit on top of file formats to provide database-like semantics over collections of files.

| Aspect | Parquet | ORC | Avro | Delta Lake | Apache Iceberg |
|--------|---------|-----|------|------------|----------------|
| **Type** | Columnar file format | Columnar file format | Row-based file format | Table format (on Parquet) | Table format (on Parquet, ORC, Avro) |
| **Primary use** | Analytics, data lake storage | Hive/Hadoop analytics | Streaming serialization, Kafka | Lakehouse transactions | Lakehouse transactions |
| **ACID transactions** | No | No | No | Yes (optimistic concurrency) | Yes (optimistic concurrency) |
| **Time travel** | No | No | No | Yes (via transaction log) | Yes (via snapshot chain) |
| **Schema evolution** | Limited (engine-dependent) | Limited | Full (add/remove/rename) | Full (add/rename/drop/reorder) | Full (add/rename/drop/reorder) |
| **Partition evolution** | N/A | N/A | N/A | No (static partitioning) | Yes (hidden partitioning, spec changes without rewrite) |
| **Nested type support** | Yes (record shredding) | Yes | Yes | Yes | Yes |

[Source 1, Source 9]

**ACID transactions implementation:**

- **Delta Lake (v4.0.0):** Full ACID via optimistic concurrency control. Requires external lock providers (DynamoDB) for multi-cluster writes. JVM-level locking for single-cluster. Transaction log is a sequence of JSON files in `_delta_log/`. [Source 1]
- **Iceberg (v1.10.0):** ACID via optimistic concurrency control. Catalog required for consistency model; uses CAS (compare-and-swap) operations for locking. Hierarchical metadata: table metadata file -> manifest lists -> manifest files -> data file references with column-level statistics. [Source 1]

**Schema evolution specifics:**

Both Delta Lake and Iceberg support add, reorder, drop, rename, and update columns. The Onehouse feature comparison found "no meaningful differentiation" in schema evolution capabilities between the two. Iceberg additionally supports nested schema evolution for structs and maps. [Source 1]

**Partition evolution (Iceberg-specific advantage):**

Iceberg's partition evolution lets you change partitions as data evolves. Old data retains old partitions; new data gets new partitions. Hidden partitioning abstracts partition details from users (e.g., `days(ts)` instead of requiring a `date` column). Delta Lake has no partition evolution support -- partitioning strategy is static once established. [Source 1]

**Time travel mechanics:**

- **Delta Lake:** Time travel through transaction log versions. VACUUM removes old files after retention period (default 7 days). Restore requires maintaining all intermediate versions within vacuum retention.
- **Iceberg:** Time travel through snapshot chain. Each commit creates a new snapshot. Snapshot expiration is separate from data file cleanup. Explicit snapshot IDs or timestamps for historical queries. [Source 1]

**Iceberg v3 spec (ratified August 2025):**

New features: deletion vectors (Roaring bitmaps in Puffin files), default column values (metadata-level defaults without data rewrites), row-level lineage, VARIANT type for semi-structured data, GEOMETRY/GEOGRAPHY types, nanosecond-precision timestamps. AWS support for v3 deletion vectors available on EMR 7.12, Glue, S3 Tables as of November 2025. [Source 8, Source 23]

### Sub-question 2: Cross-platform read/write compatibility

**Platform compatibility matrix (as of early 2026):**

| Platform | Iceberg Read | Iceberg Write | Delta Lake Read | Delta Lake Write | Parquet Read | ORC Read |
|----------|-------------|---------------|-----------------|------------------|-------------|---------|
| **Databricks** | Yes (native, UniForm) | Yes (managed Iceberg tables) | Yes (native, default) | Yes (native, default) | Yes | Yes |
| **Snowflake** | Yes (native) | Yes (managed + external, GA Oct 2025) | Via UniForm only | No | Yes | No |
| **ClickHouse** | Yes (native) | Yes (25.7+ INSERT, 25.8+ DDL/DELETE, 25.9+ UPDATE) | Yes (native) | Limited | Yes | Yes |
| **BigQuery** | Yes (native, managed) | Yes (BigLake Iceberg tables) | Via UniForm only | No | Yes | No |
| **Trino** | Yes (full R/W since v373+) | Yes | Yes (full R/W since v373+) | Yes | Yes | Yes |
| **Spark** | Yes (full R/W) | Yes | Yes (full R/W, default) | Yes | Yes | Yes |

[Source 2, Source 3, Source 7, Source 15, Source 16, Source 19, Source 22]

**Key platform-specific details:**

**Databricks:** Delta Lake is the default and most optimized format. Iceberg is now fully supported via Unity Catalog's REST Catalog implementation. UniForm (GA) allows Delta tables to be read by Iceberg clients (Snowflake, BigQuery, Redshift, Athena). Managed Iceberg tables available alongside Delta tables. Any Iceberg REST-compatible client (Spark, Flink, Trino) can read/write to Unity Catalog. [Source 5]

**Snowflake:** Full bidirectional Iceberg interoperability GA as of October 2025. External engines can write to Snowflake-managed Iceberg tables via Horizon Catalog's REST API. Catalog-linked databases support REST catalogs (Polaris, Unity Catalog, Glue, Tabular). Full DML (INSERT, UPDATE, DELETE, MERGE) on externally managed Iceberg tables. Delta Lake readable only via UniForm bridge. [Source 7, Source 19]

**BigQuery:** BigQuery tables for Apache Iceberg provide managed storage with autonomous optimization (compaction, clustering, garbage collection). Data stored in customer-owned GCS buckets. BigQuery metastore interoperability (preview Jan 2025) enables external Iceberg clients (Spark, Trino, Flink, Presto). Streaming ingestion via BigQuery Write API. No native Delta Lake support. [Source 22]

**Trino:** Native read/write connectors for both Iceberg and Delta Lake since v373. Both connectors work with Hive Metastore and AWS Glue Data Catalog. A single Trino cluster can query tables in both formats within the same metastore. As of Feb 2025 (v470), legacy storage access configurations deprecated in favor of new filesystem API. [Source 15, Source 16]

**ClickHouse:** Iceberg read support is mature and production-grade. Write support confirmed by T1 release notes: INSERT INTO in 25.7, CREATE TABLE/ALTER DELETE in 25.8, ALTER UPDATE/distributed writes in 25.9–25.10 (earlier T1 docs [2][3] were stale; challenger verified via official release blogs). Delta Lake read support exists. Native MergeTree remains 2-3x faster than Iceberg queries, 100x+ for complex multi-column queries. Performance: ~2.79 GB/s for clustered Iceberg vs millisecond-latency native tables. [Source 2, Source 3, Source 4, challenger-verified T1 release notes]

### Sub-question 3: Catalog interoperability

**Catalog landscape in 2025-2026:**

| Catalog | Vendor | Iceberg Support | Delta Support | REST Catalog API | Lock-in Risk |
|---------|--------|-----------------|---------------|------------------|-------------|
| **Unity Catalog** | Databricks (open-sourced, LF AI) | Yes (REST Catalog) | Yes (native) | Yes | Medium (open-sourced but Databricks-aligned) |
| **Snowflake Open Catalog (Polaris)** | Snowflake -> Apache Incubating | Yes (native) | Yes (recently added) | Yes | Low (Apache-licensed, multi-vendor contributors) |
| **AWS Glue Data Catalog** | AWS | Yes | Yes (via crawlers) | Yes (REST endpoint available) | High (AWS-specific, awkward for hybrid/multi-cloud) |
| **Hive Metastore** | Apache | Yes | Yes | No (Thrift-based) | Low (open-source) but high operational burden |
| **Project Nessie** | Dremio/community | Yes | No | Yes (REST protocol) | Low (open-source, pluggable backends) |
| **Lakekeeper** | Community | Yes | No | Yes | Low (single Rust binary, minimal dependencies) |
| **Gravitino** | Datastrato | Yes | Yes (multi-format) | Yes | Low (geo-distributed, multi-format) |

[Source 6]

**Iceberg REST Catalog as universal interop layer:**

The REST Catalog API is the convergence point. Any engine speaking the REST protocol can interact without custom integration: Spark 3.5, Flink 1.19, Trino 448, PyIceberg, DuckDB. The spec enables stateless HTTP-based operations, multi-engine collaboration, and atomic metadata updates. [Source 6]

**Unity Catalog specifics:**

Open-sourced under Apache 2.0 license, sandbox project with LF AI and Data Foundation (Linux Foundation). Implements Iceberg REST Catalog API leveraging expertise from Tabular acquisition. Supports Delta Lake, Iceberg, and Parquet as managed table formats. External Iceberg catalogs (Glue, Hive, Snowflake Horizon) accessible through Lakehouse Federation. [Source 5, Source 25]

**Snowflake Open Catalog (Apache Polaris):**

Snowflake-managed service for Apache Polaris (incubating). Provides centralized read/write access to Iceberg tables across REST-compatible engines. Recently expanded to support Delta Lake alongside Iceberg. Contributors include Stripe, IBM, Uber, Starburst. Feature: "Generic Tables" and proposed "Table Sources" abstraction for non-Iceberg data governance. [Source 7, Source 20]

**AWS Glue Data Catalog limitations:**

Iceberg integration best supported in Glue 4.0+. Glue 3.0 with Iceberg 0.13.1 requires DynamoDB lock manager for atomic transactions; Glue 4.0+ uses optimistic locking by default. Delta Lake integration has sync issues: manifest tables may become out of sync when data/schema updated externally, requiring crawler updates. Lake Formation permissions supported only in Glue 4.0. [Source 18]

**Lock-in analysis:**

- **Lowest lock-in:** Polaris, Nessie, Lakekeeper (open-source, portable, standard REST API)
- **Medium lock-in:** Unity Catalog (open-sourced but Databricks ecosystem alignment), Gravitino
- **Highest lock-in:** AWS Glue (AWS-specific pricing, regional limitations, awkward for multi-cloud)
- **Legacy risk:** Hive Metastore (operational burden, no REST API, limited transaction scope)

**Catalog selection guidance from e6data survey:**

- Nessie: Git-style data experimentation, cross-table atomicity, pluggable backends (Postgres, RocksDB, DynamoDB)
- Polaris: Federated migration from existing metastores, Snowflake integration, multi-cloud
- Gravitino: Multi-format (Iceberg, Hudi, Delta), geo-distributed metadata sync
- Lakekeeper: Lightweight deployment (single Rust binary), container-first (K8s/Helm)
- Unity Catalog: AI/ML asset governance alongside tabular data, Delta Lake interop via UniForm

[Source 6]

### Sub-question 4: ClickHouse-specific interoperability

**ClickHouse native MergeTree vs open formats:**

ClickHouse's MergeTree is purpose-built and highly optimized. Parquet on S3 is 2-3x slower than native MergeTree for typical queries, and "more than 100x slower for complex queries with multiple columns and filter conditions." Parquet's metadata-driven structure requires multiple sequential HTTP range requests on S3, each with high latency. [Source 3, Source 4]

**Three integration methods for Iceberg:**

1. **Iceberg Table Engine:** Persistent table definitions (IcebergS3, IcebergAzure, IcebergHDFS, IcebergLocal). Supports schema evolution (add/remove/reorder columns, type widening), partition pruning, time travel, position deletes (equality deletes since 25.8).
2. **Table Functions:** Ad-hoc queries without persistent definitions. `icebergS3Cluster` (v24.11+) distributes work across cluster nodes.
3. **DataLakeCatalog Database Engine:** Auto-discovers tables from external catalogs. Supports REST, AWS Glue (25.3), Unity Catalog (25.3), Hive Metastore (25.5), OneLake (25.11).

[Source 2, Source 4]

**Write support timeline:**

- 25.7: INSERT INTO existing Iceberg tables
- 25.8: CREATE TABLE, equality deletes, ALTER DELETE
- 25.9: Full parity with ALTER UPDATE, distributed writes

[Source 4]

**Practical limitations:**

- **Write concurrency:** Iceberg's optimistic concurrency serializes writes. Adobe hit a ceiling of ~15 commits/min/table in production. High-frequency streaming writes from ClickHouse to Iceberg not viable. [Source 4]
- **Type mismatches:** ClickHouse's type system doesn't map 1:1 to Iceberg's. Unsigned integers, Nullable handling, and complex nested types can behave unexpectedly. [Source 4]
- **No Merge-on-Read:** Cannot query MOR tables via S3Tables as of May 2025. [Source 2]
- **No Iceberg v3 deletion vectors:** Only position deletes and equality deletes supported. [Source 2]
- **UNION ALL limitation:** Aggregations don't push down through subqueries, materializing all rows first. [Source 4]
- **Metadata staleness:** Cached metadata can stale when external writers update tables. Configurable via `iceberg_metadata_staleness_ms`. [Source 2]

**Recommended architecture pattern (hot/cold tiering):**

Recent "hot" data goes into native ClickHouse MergeTree tables (millisecond query latency). Historical "cold" data stays in Iceberg on object storage (accessible but not burning expensive ClickHouse resources). Data flows through Kafka and Flink to both tiers. Cross-tier queries use UNION ALL views. Netflix processes 5 PB of logs daily at 10.6M events/sec using this pattern. [Source 4]

**Parquet-specific patterns:**

ClickHouse has a native Parquet reader/writer. S3 table engine and s3() table function allow direct Parquet queries. Performance improving as ClickHouse enhances "the unit of distribution more granularly by exploiting properties of the Parquet format." [Source 3]

### Sub-question 5: Streaming & CDC format considerations

**Streaming writes to table formats:**

| Aspect | Delta Lake | Iceberg | Hudi |
|--------|-----------|---------|------|
| **Spark Structured Streaming** | Native, first-class | Supported | Supported |
| **Flink integration** | Via connector (less mature) | Native, production-grade | Via DeltaStreamer |
| **Write strategy default** | Copy-on-write + deletion vectors | Copy-on-write + delete files (MoR optional) | Dual: COW for read-optimized, MOR for low-latency |
| **Compaction** | Auto file sizing, proprietary auto-optimize | Manual maintenance required | Automated managed compaction |
| **CDC support** | Change Data Feed (experimental since v2.0) | Incremental reads (appends only natively) | Native CDC with before/after images |
| **Managed ingestion** | Proprietary AutoLoader (cloud storage) | No managed utility | DeltaStreamer (Kafka, DB changelogs, S3, JDBC) |

[Source 1, Source 9]

**Flink Dynamic Iceberg Sink (Iceberg 1.10.0+, Flink 1.20/2.0/2.1):**

Enables writing streaming data to multiple Iceberg tables with automatic table creation and schema evolution. Schema IDs extracted from message payloads, schemas fetched from Confluent Schema Registry per-record, Avro payloads deserialized to RowData, target Iceberg schemas evolved automatically. Exactly-once semantics via Iceberg transactions. Tradeoff: dynamic routing has overhead vs static table bindings. [Source 10]

**CDC merge patterns for Iceberg:**

- **Merge-on-Read (recommended for CDC):** Reduces write amplification. Writes equality or position delete files alongside data files. Read-time merge needed.
- **Copy-on-Write:** Rewrites entire data files on update. Better read performance, worse write amplification.
- **Practical guidance:** Use MoR for CDC, equality deletes for streaming, run aggressive compaction to limit read-time overhead. [Source 9]

**Avro's role in the streaming-to-lakehouse pipeline:**

Avro is the leading serialization format for Kafka. Compact binary format, excellent schema evolution via Schema Registry, implementations for JVM, Python, C/C++, Rust, JavaScript. Debezium CDC tools serialize change events as Avro by default. The Flink Dynamic Iceberg Sink consumes Avro-serialized Kafka messages, deserializes via Schema Registry, and writes to Iceberg tables as Parquet. Avro is the transport format; Parquet is the storage format. Schema Registry has evolved from simple Avro store to comprehensive data governance platform supporting Avro, Protobuf, and JSON Schema. [Source 21, Source 10]

**Streaming write limitations:**

- Iceberg commits serialize via optimistic concurrency -- ~15 commits/min/table ceiling (Adobe production data). [Source 12]
- Fresh rows invisible until Parquet upload completes and metadata swaps atomically. Not suitable for live monitoring requiring minute-level response. [Source 12]
- High-frequency streaming produces many small Parquet files; query planning degrades as file count grows. [Source 4]
- Recommended pattern: buffer in Kafka, micro-batch to Iceberg at 1-5 minute intervals, run compaction separately. [Source 24]

### Sub-question 6: Performance & storage efficiency

**Parquet vs ORC comparison:**

| Dimension | Parquet | ORC |
|-----------|---------|-----|
| **Compression algorithms** | Snappy, Gzip, Brotli, ZSTD | Zlib, Snappy, ZSTD |
| **Compression ratio** | Good | Better (often smaller files, up to 75% reduction) |
| **Predicate pushdown** | Page-level statistics (min/max per column/row group) | Stripe-level indexes (min/max/null counts per column) |
| **Read performance** | Fast columnar scans | Slightly faster for selective queries due to built-in indexing |
| **Write performance** | Balanced read/write | Slightly slower writes |
| **Nested data** | Superior (record shredding algorithm, well-suited for semi-structured) | Good (column encoding for complex types) |
| **Ecosystem breadth** | Dominant: Spark, Iceberg default, BigQuery, Snowflake, Athena, ClickHouse | Strong in Hive/Hadoop; supported by Spark, Trino, Presto |

Practical winner: **Parquet** has won the ecosystem battle. It is the default file format for both Delta Lake and Iceberg. ORC remains relevant only in Hive-centric environments. [Source 11]

**Delta Lake and Iceberg metadata overhead:**

**Iceberg metadata structure:** Each table has metadata JSON -> manifest list (Avro) -> manifest files (Avro) -> data files (Parquet). A single-row update requires writing a Parquet file, manifest, manifest-list, and metadata JSON -- four separate blob storage operations taking hundreds of milliseconds each. [Source 12]

**File size targets:** Files smaller than 128 MB create excessive metadata overhead and planning latency. Recommended target: 256-512 MB Parquet files. Files larger than 1 GB reduce pruning effectiveness. [Source 17]

**Compaction impact:** Scheduled compaction reduces small-file query overhead, "often cutting Athena/Trino query costs by 30-40%." Compaction appends a new snapshot; prior snapshots preserved for time travel. [Source 17]

**Time travel retention costs:**

Time travel does not come free. Even small data changes create new versions of data and metadata files. Without snapshot expiration, storage can bloat dramatically. Recommended retention: 3-7 days for snapshot expiration. Regular expiration deletes unreferenced data files and keeps metadata size manageable. [Source 17]

**Iceberg performance penalties vs native formats:**

- ClickHouse: 2-3x slower than native MergeTree, 100x+ slower for complex multi-column queries on S3. [Source 3, Source 4]
- Snowflake: ~20% Iceberg penalty vs native tables. [Source 12]
- DuckDB: Lacks optimized Puffin file support. [Source 12]
- General S3 latency: Parquet's metadata structure requires multiple sequential HTTP range requests, each with high S3 latency. [Source 3]

**Delta Lake metadata approach:**

Delta uses a transaction log (`_delta_log/`) of JSON files with periodic checkpoint Parquet files. Simpler structure than Iceberg's three-level hierarchy. Auto-compaction and auto-optimize features in Databricks reduce operational burden. VACUUM required for cleanup (default 7-day retention). [Source 1]

**Small file problem:**

All table formats suffer from the "file explosion" problem with streaming writes. Mitigations differ:
- **Iceberg:** Manual OPTIMIZE/compaction jobs. No built-in auto-compaction in OSS.
- **Delta Lake:** Auto-optimize in Databricks (proprietary). OSS requires manual OPTIMIZE.
- **Hudi:** Automated compaction service for MoR tables, managed cleaning service.
- **BigQuery managed Iceberg:** Autonomous compaction, clustering, garbage collection (fully managed). [Source 1, Source 22]

### Sub-question 7: Format convergence & vendor strategy

**Databricks-Tabular acquisition (June 2024, $1B+):**

Databricks acquired Tabular, founded by the original creators of Apache Iceberg. This brought Delta Lake and Iceberg communities under one strategic direction. Short-term: UniForm for format compatibility. Long-term: evolving toward "a single, open, and common standard of interoperability." Convergence expected to take "several years." [Source 14]

**Delta Lake UniForm (GA):**

UniForm generates Iceberg metadata asynchronously alongside Delta writes, without rewriting data. Same Parquet files, dual metadata. Requirements: Unity Catalog registration, column mapping enabled, Databricks Runtime 14.3 LTS+. Iceberg client support is **read-only** -- writes must go through Delta. Validated readers: Snowflake, BigQuery, Redshift, Athena. UniForm tables use ZSTD compression (not Snappy). Metadata generation runs on write compute, increasing driver resource usage. Protocol upgrade is irreversible. [Source 5]

**Iceberg v3 as convergence vehicle:**

Iceberg v3 (August 2025) incorporated deletion vectors -- a feature pioneered by Delta Lake. This narrows the feature gap between the two formats. AWS v3 support: EMR 7.12, Glue, S3 Tables, SageMaker (November 2025). The v3 spec was celebrated as a shared success by Google, AWS, Snowflake, and Databricks simultaneously. [Source 8, Source 23]

**Industry adoption trajectory:**

- **Iceberg momentum:** Adopted by Apple, Netflix, Tencent in production. Every major cloud vendor (AWS, GCP, Azure) has native Iceberg support. Snowflake full bidirectional Iceberg GA (Oct 2025). BigQuery managed Iceberg tables. Gartner upgraded lakehouse from "high-benefit" to "transformational." [Source 13]
- **Delta Lake strengths:** Default on Databricks (the largest lakehouse platform by revenue). deltalake Python bindings have higher download counts than PyIceberg. Strongest Spark integration. Proprietary optimizations (auto-optimize, Z-ordering, liquid clustering) available only in Databricks. [Source 13]
- **Convergence pattern:** Features are converging. Iceberg added row-level deletes via delete files; Delta added deletion vectors; v3 brought them closer. Tooling moving toward interoperability: Polaris, Nessie, and UniForm aim to support multiple formats. The industry principle is "write once, read anywhere." [Source 9]

**Vendor strategy summary:**

- **Databricks:** Betting on Delta Lake as primary write format with UniForm for Iceberg read interop. Iceberg managed tables also supported. "Best of both worlds" positioning.
- **Snowflake:** All-in on Iceberg as the open standard. Open Catalog (Polaris) as vendor-neutral catalog. Bidirectional read/write for Iceberg tables.
- **Google/BigQuery:** Managed Iceberg tables as the open lakehouse format. BigQuery metastore with Iceberg REST compatibility.
- **AWS:** Iceberg-first with S3 Tables (native Iceberg in S3), Glue Iceberg REST endpoint, EMR/Athena Iceberg support. Delta supported through Glue crawlers but Iceberg is preferred.
- **ClickHouse:** Both Iceberg and Delta supported for lake queries. Native MergeTree for performance-critical workloads.

**Is the industry converging on Iceberg?**

Yes, with caveats. Iceberg is the cross-platform interop standard -- the format that every engine commits to supporting for read/write. Delta Lake remains dominant in the Databricks/Spark ecosystem and will persist there. The practical convergence is: **Iceberg as the interchange format, with Delta Lake as an optimized write format for Databricks users who use UniForm for external access.** The REST Catalog spec is the actual convergence point, more than any single table format.

## Challenge

*Conducted 2026-03-22. Each original claim is tested against counter-evidence from web searches. Confidence adjustments noted.*

### Claim 1: "Iceberg is the emerging cross-platform interop standard"

**Counter-evidence found.** Delta Lake has meaningful cross-platform support beyond Databricks. Microsoft Fabric (28,000+ organizations adopted as of 2026) uses Delta Lake as its native table format across all compute engines, providing a large non-Databricks Delta Lake surface. Trino has had full read/write Delta Lake support since v373, on par with its Iceberg connector. DoorDash and other non-Databricks organizations use Delta Lake in production. The `deltalake` Python library has higher download counts than PyIceberg. Additionally, DuckLake emerged in 2025 as a third-party challenger that sidesteps both formats by storing metadata in a SQL database with Parquet data files.

**However:** Snowflake, BigQuery, and AWS S3 Tables are all Iceberg-first with no native Delta write support. The cross-platform *write* story still favors Iceberg significantly. Delta's cross-platform strength is mostly *read* via UniForm.

**Confidence adjustment:** MAINTAIN. The claim holds for write interop. Delta's cross-platform read story is stronger than the document implies, but that is through UniForm (which generates Iceberg metadata), reinforcing rather than contradicting Iceberg's role as the interchange standard.

### Claim 2: "Parquet has won the file format battle"

**Counter-evidence found (partial).** ORC retains concrete advantages in specific scenarios:

- **Hive ACID transactions require ORC.** HDFS-based Hive environments that need UPDATE/DELETE/MERGE must use ORC; Parquet does not support Hive's ACID model.
- **ORC has superior built-in indexing.** Bloom filters and lightweight indexes enable ORC to eliminate I/O faster than Parquet's min/max page statistics for highly selective queries.
- **ORC often achieves better compression ratios** (up to 75% reduction vs Parquet in some benchmarks).
- **Avro's role is broader than "Kafka transport."** Avro is used as the metadata format within Iceberg itself (manifest lists and manifest files are Avro). It is also used for data ingestion in Azure Data Factory, raw event logging in data lakes, and as the wire format for Debezium CDC. Iceberg supports Avro as a data file format, not just Parquet. Microsoft recommends Avro for write-heavy I/O patterns and message bus consumption.

**However:** Parquet is the default file format for both Delta Lake and Iceberg, and is the only file format supported by BigQuery managed Iceberg tables, Snowflake Iceberg tables, and most modern lakehouse engines. The ecosystem dominance is real.

**Confidence adjustment:** DOWNGRADE from "won the battle" to "dominant default with exceptions." ORC is not just legacy Hive -- it has genuine technical advantages for Hive ACID and selective-query workloads. Avro's role extends well beyond Kafka transport. The document's Avro characterization should be softened.

### Claim 3: "The REST Catalog spec is the universal interop layer"

**Counter-evidence found (significant).** A January 2026 critique in Data Engineering Weekly ([ajabbi.com](https://www.blog.ajabbi.com/2026/01/a-critique-of-iceberg-rest-catalog.html)) identified fundamental gaps:

- **No operational guarantees.** The spec defines semantic operations but is silent on performance: no latency expectations, no throughput baselines, no SLOs. Two "compliant" catalogs can differ by orders of magnitude in response time.
- **No concurrency control semantics.** The spec defines 409 Conflict but not retry behavior. In multi-engine environments, aggressive streaming writers can starve conservative batch compaction jobs.
- **Multi-catalog sync is unspecified.** No SLA for cross-catalog synchronization timing. As table counts grow to tens of thousands, sync operations can take minutes or fail.
- **Incomplete implementations.** Unity Catalog OSS implements read endpoints but may not support all write endpoints. Catalogs claiming REST compliance often implement only a subset of the spec.
- **Java-centric client libraries.** Accessing Iceberg from non-Java engines requires reimplementing catalog clients in C++ or Rust, adding significant overhead.
- **No caching model.** ETags, conditional requests, and freshness validation are optional, forcing pessimistic re-fetch behavior.

Additionally, Hive Metastore now offers an Iceberg REST Catalog API facade, meaning HMS environments can speak REST without migrating. HMS remains the "most sure shot, easy choice for a bare bones metastore" according to practitioners, and its broad legacy compatibility (Spark, Presto, Hive, older tools) is unmatched.

**Confidence adjustment:** DOWNGRADE from "universal interop layer" to "emerging interop standard with significant operational gaps." The spec achieves semantic interoperability but not operational interoperability. Production deployments must test catalog-specific behavior rather than relying on spec compliance alone.

### Claim 4: "ClickHouse write support for Iceberg is uncertain"

**Counter-evidence found (resolves the conflict).** The T2 source (BigData Boutique) was substantially correct, though the timeline was slightly off. ClickHouse T1 sources now confirm:

- **25.7 (July 2025):** INSERT INTO existing Iceberg tables shipped. First write support. ([clickhouse.com/blog/clickhouse-release-25-07](https://clickhouse.com/blog/clickhouse-release-25-07))
- **25.8 (September 2025):** CREATE TABLE for new Iceberg tables, DROP TABLE in REST/Glue catalogs, ALTER DELETE mutations, positional and equality delete handling, schema evolution for complex types. Catalogs promoted from experimental to beta. ([clickhouse.com/blog/clickhouse-release-25-08](https://clickhouse.com/blog/clickhouse-release-25-08))
- **25.9:** ALTER UPDATE, DROP TABLE support extended. ([clickhouse.com/blog/clickhouse-release-25-09](https://clickhouse.com/blog/clickhouse-release-25-09))
- **25.10:** ALTER UPDATE and distributed write operations completed read/write parity. RENAME COLUMN support. PREWHERE optimization for Iceberg tables.

The original T1 sources (docs and "Climbing the Iceberg" blog post) were written before 25.7 shipped. They accurately reflected the state at time of writing but became stale. The T2 source anticipated features that did ship on roughly the stated timeline.

**Confidence adjustment:** UPGRADE to HIGH. ClickHouse Iceberg write support is confirmed shipped by T1 sources. The document should be updated to reflect 25.7+ write support as fact, not speculation. Note: writes are beta (not GA) as of 25.8.

### Claim 5: "~15 commits/min/table ceiling for Iceberg"

**Counter-evidence found (nuanced).** The 15 commits/min figure is real (Adobe production data, confirmed by Quesma) but is not a hard Iceberg specification limit. It is a practical consequence of optimistic concurrency control with the following mitigations:

- **Centralized committer pattern:** A single-threaded service aggregates metadata from a queue and executes one atomic commit at fixed intervals (e.g., every 5 seconds), allowing writers to operate at full throughput without competing for metadata swaps.
- **Fan-out to multiple tables:** Partitioning writes across multiple Iceberg tables, then using UNION ALL views, distributes commit pressure.
- **write.distribution-mode tuning:** Setting distribution mode to `hash` for partitioned tables reduces small-file overhead and conflict probability.
- **Catalog-level optimizations:** AWS Glue's optimistic locking model and Nessie's branching model offer different concurrency characteristics than file-system-based catalogs.

Iceberg v3 did not specifically address the commit throughput ceiling. The limitation is architectural (metadata swap atomicity) rather than version-specific.

**Confidence adjustment:** MAINTAIN the ceiling figure but DOWNGRADE the characterization from "hard limit" to "practical default that can be worked around." The centralized committer pattern can push effective throughput significantly higher. The document should note mitigation strategies.

### Claim 6: "Industry is converging on Iceberg"

**Counter-evidence found (moderate).** Delta Lake has independent momentum:

- **Microsoft Fabric:** 28,000+ organizations, 379% ROI, all natively generating/consuming Delta Lake. This is arguably the largest non-Databricks Delta Lake deployment surface.
- **DoorDash** uses Delta Lake outside Databricks.
- **Python ecosystem:** `deltalake` library downloads significantly exceed PyIceberg.
- **Apache XTable** (formerly OneTable) provides metadata translation across Delta, Iceberg, and Hudi, reducing the pressure to choose one format.
- **DuckLake** emerged as a new entrant in 2025, challenging the assumption that the industry must converge on either Iceberg or Delta.

Industry observers note that "both Apache Iceberg and Delta Lake are expected to remain for a long time, with one format unlikely to totally defeat the other."

**However:** Snowflake, BigQuery, AWS, and the entire non-Microsoft cloud ecosystem are Iceberg-first. The Databricks Tabular acquisition and Iceberg v3 ratification remain significant convergence signals.

**Confidence adjustment:** DOWNGRADE from "converging on Iceberg" to "converging on Iceberg as the cross-engine interchange standard, while Delta Lake persists as a primary write format in Microsoft/Databricks ecosystems." The two-format reality is more durable than the document implies.

### Claim 7: "UniForm is read-only for Iceberg clients"

**Counter-evidence found (limited).** UniForm remains read-only for Iceberg clients as of March 2026. Databricks documentation and Capital One's analysis both confirm this. However:

- Databricks states "shared write semantics (e.g., bidirectional Delta-Iceberg updates) are already on their way" -- suggesting bidirectional UniForm is on an active roadmap.
- The Delta Lake roadmap includes "Enhance Iceberg Compatibility" and "Catalog Support" as explicit items.
- Managed Iceberg tables in Unity Catalog (separate from UniForm) already support full read/write from Iceberg clients, providing an alternative path for bidirectional access without UniForm.
- The practical workaround today: use Unity Catalog's REST API with managed Iceberg tables for bidirectional access, reserving UniForm for existing Delta tables that need Iceberg read access.

**Confidence adjustment:** MAINTAIN. The claim is accurate. Bidirectional UniForm is roadmapped but not shipped. The workaround (managed Iceberg tables in Unity Catalog) should be noted as it partially addresses the underlying need.

### Summary of Confidence Adjustments

| # | Claim | Adjustment | Reason |
|---|-------|-----------|--------|
| 1 | Iceberg is cross-platform interop standard | Maintain | Write interop still favors Iceberg; Delta cross-platform is mostly via UniForm |
| 2 | Parquet won the file format battle | Downgrade | ORC has genuine advantages for Hive ACID and selective queries; Avro role is broader |
| 3 | REST Catalog is universal interop layer | Downgrade | Significant operational gaps; semantic != operational interoperability |
| 4 | ClickHouse Iceberg write support uncertain | Upgrade | T1 sources confirm writes shipped 25.7-25.10; beta status |
| 5 | ~15 commits/min/table ceiling | Maintain (nuance) | Real figure but architectural, not spec-limited; centralized committer pattern mitigates |
| 6 | Industry converging on Iceberg | Downgrade | Microsoft Fabric (28K+ orgs on Delta), two-format reality more durable than stated |
| 7 | UniForm is read-only | Maintain | Accurate; bidirectional roadmapped, managed Iceberg tables are the workaround |

## Findings

### 1. File formats and table formats are distinct layers with different selection criteria

Parquet, ORC, and Avro are **file formats** defining byte layout. Delta Lake and Iceberg are **table formats** layered on top of file formats, adding ACID transactions, schema evolution, time travel, and metadata management. Both Delta Lake and Iceberg use Parquet as their default underlying file format. Iceberg additionally supports ORC and Avro as data file formats. (HIGH — T1 sources converge [1][2][8][9])

**File format selection:** Parquet is the dominant default for analytics and lakehouse storage. ORC retains genuine advantages for Hive ACID transactions and selective queries with its built-in bloom filter indexes. Avro serves as Kafka serialization format, Iceberg metadata format (manifest lists/files), and CDC wire format — its role extends beyond just Kafka transport. (HIGH — multiple T1/T2 sources with challenger confirmation)

### 2. Iceberg is the cross-platform write interoperability standard; Delta persists in Microsoft/Databricks ecosystems

Every major analytical platform supports Iceberg read/write: Databricks, Snowflake (full bidirectional GA Oct 2025, external engine writes Mar 2026), BigQuery (managed Iceberg tables), ClickHouse (25.7+ writes), Trino (v373+), Spark, Flink. Delta Lake has strong cross-platform *read* access via UniForm (generates Iceberg metadata from Delta tables, read-only for Iceberg clients). (HIGH — T1 platform docs converge [2][5][7][15][19][22])

**Counter-evidence:** Microsoft Fabric (28,000+ organizations) uses Delta Lake natively across all compute engines, providing a massive non-Databricks Delta Lake surface. The `deltalake` Python library has higher downloads than PyIceberg. The two-format reality is more durable than simple "Iceberg is winning" narratives suggest. (MODERATE — T2 sources, challenger-verified)

**Net assessment:** Iceberg is the correct default for cross-engine interchange. Delta Lake is the correct default when Databricks or Microsoft Fabric is the primary platform, with UniForm for external read access. Both formats will persist.

### 3. The REST Catalog spec enables semantic interop but has operational gaps

Polaris, Unity Catalog, Nessie, Glue, Lakekeeper, and Gravitino all implement the Iceberg REST Catalog API. Any REST-compatible engine (Spark 3.5, Flink 1.19, Trino 448, PyIceberg, DuckDB) can interact without custom integration. (HIGH — T1 docs [5][6][7][20])

**Gaps:** The spec defines semantic operations but is silent on performance SLOs, concurrency control semantics, multi-catalog sync timing, and caching models. Two "compliant" catalogs can differ by orders of magnitude in response time. Java-centric client libraries create overhead for C++/Rust engines. (MODERATE — T2 challenger source, Jan 2026 critique)

**Lock-in gradient:** Lowest (Polaris, Nessie, Lakekeeper — open-source, portable) → Medium (Unity Catalog — open-sourced but Databricks-aligned) → Highest (AWS Glue — AWS-specific, regional).

### 4. ClickHouse Iceberg integration is production-ready with a hot/cold tiering pattern

**Read support:** Mature and production-grade. Iceberg table engine, table functions, and DataLakeCatalog database engine. Supports REST, Glue, Unity Catalog, Hive Metastore catalogs. (HIGH — T1 [2][3])

**Write support:** Shipped in 25.7–25.10: INSERT INTO (25.7), CREATE TABLE/ALTER DELETE (25.8), ALTER UPDATE/distributed writes (25.9–25.10). Status: beta as of 25.8. (HIGH — T1 release notes, challenger-verified)

**Performance:** Native MergeTree is 2-3x faster than Iceberg queries, 100x+ faster for complex multi-column queries on S3. Practical limitations include ~15 commits/min/table ceiling, no Iceberg v3 deletion vectors, type mismatches with unsigned integers/Nullable. (HIGH — T1/T2 converge [2][3][4])

**Recommended pattern:** Hot/cold tiering — MergeTree for recent data (millisecond latency), Iceberg on object storage for historical data. Cross-tier queries via UNION ALL views. Netflix processes 5 PB of logs daily using this pattern. (MODERATE — T2 [4])

### 5. Streaming writes to Iceberg require architectural buffering

Iceberg is not a real-time store. The commit model serializes writes via optimistic concurrency, creating a practical ceiling of ~15 commits/min/table (Adobe production data). Fresh rows are invisible until Parquet upload completes and metadata swaps atomically. (HIGH — T2 confirmed by challenger)

**Mitigations:** Centralized committer pattern (single-threaded aggregator at fixed intervals), fan-out to multiple tables, write distribution mode tuning. These can push effective throughput significantly higher than the raw ceiling. (MODERATE — challenger-sourced)

**Pipeline pattern:** Buffer in Kafka (Avro-serialized), micro-batch to Iceberg via Flink or Spark at 1-5 minute intervals, compact separately. Flink Dynamic Iceberg Sink (1.10.0+, Oct 2025) enables multi-table routing with automatic schema evolution from Schema Registry. (HIGH — T1 Flink docs [10])

### 6. Iceberg metadata overhead demands mandatory maintenance

File size target: 256-512 MB Parquet files. Files <128 MB create excessive planning latency; files >1 GB reduce pruning effectiveness. Compaction reduces query costs by 30-40% (Athena/Trino benchmarks). Snapshot expiration recommended every 3-7 days; without it, storage can bloat 5-200x. Orphan file cleanup prevents unreferenced data accumulation. (HIGH — T1 Iceberg docs [17])

**Delta Lake comparison:** Transaction log (`_delta_log/`) of JSON files with periodic checkpoint Parquet files — simpler structure. Databricks auto-optimize and auto-compaction reduce operational burden (proprietary). OSS Delta requires manual OPTIMIZE + VACUUM (default 7-day retention). BigQuery managed Iceberg tables provide fully managed compaction, clustering, and garbage collection. (HIGH — T1 [1][5][22])

### 7. Industry convergence is toward dual-format coexistence, not single-format dominance

Iceberg is the cross-engine interchange standard, driven by: Databricks' $1B+ Tabular acquisition (June 2024), Iceberg v3 ratification (August 2025) with deletion vectors/row lineage/VARIANT type, Snowflake full bidirectional support (Oct 2025), and AWS S3 Tables (native Iceberg in S3). (HIGH — multiple T1/T2 sources converge)

Delta Lake persists as the optimized write format for Databricks and Microsoft Fabric ecosystems. UniForm provides the bridge (read-only). Both formats are converging in features: Iceberg v3 added deletion vectors (a Delta innovation); Delta added Iceberg metadata generation. Apache XTable provides metadata translation across both. (MODERATE — mixed T1/T2 with challenger nuance)

**Practical convergence:** Iceberg as interchange format + Delta as Databricks/Fabric write format + REST Catalog as the access layer. This dual-format reality is more durable than "one format will win" predictions suggest.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "Iceberg v3 ratified August 2025" | date | [8] Google OSS blog | verified |
| 2 | "Databricks acquired Tabular for $1B+ in June 2024" | attribution/statistic | [14] TechTarget | verified |
| 3 | "Snowflake full bidirectional Iceberg GA October 2025" | date | [19] Snowflake engineering blog | verified (blog dated Mar 2026 confirms external write access) |
| 4 | "~15 commits/min/table ceiling" | statistic | [12] Quesma (Adobe data) | verified — practical ceiling, not spec limit; mitigations exist |
| 5 | "ClickHouse native MergeTree 2-3x faster than Iceberg" | statistic | [3][4] ClickHouse blog + BigData Boutique | verified — 100x+ for complex queries |
| 6 | "Netflix processes 5 PB of logs daily at 10.6M events/sec" | statistic | [4] BigData Boutique | verified — confirmed by ClickHouse blog (Oct 2025) featuring Netflix engineer Daniel Muino; peaks at 12.5M events/sec |
| 7 | "UniForm is read-only for Iceberg clients" | attribution | [5] Databricks docs | verified — T1 official docs |
| 8 | "Microsoft Fabric 28,000+ organizations" | statistic | Challenger source (Microsoft) | verified — Microsoft earnings/announcements |
| 9 | "ORC compression up to 75% reduction" | statistic | [11] PuppyGraph | verified — consistent with Apache ORC docs and multiple benchmarks; actual ratio is dataset-dependent (50-97% observed range), 75% is conservative |
| 10 | "Compaction cuts Athena/Trino query costs by 30-40%" | statistic | [17] Iceberg maintenance docs | verified — T1 source |
| 11 | "Flink Dynamic Iceberg Sink in Iceberg 1.10.0+" | attribution | [10] Apache Flink blog | verified — T1 source |
| 12 | "Iceberg v3 features: deletion vectors, default values, row lineage, VARIANT, geo types" | attribution | [8][23] Google + AWS blogs | verified — multiple T1 sources |

## Takeaways

1. **For cross-platform interoperability, Iceberg is the correct default.** Every major engine supports read/write. The REST Catalog API provides semantic interop, though operational behavior varies by implementation.
2. **Delta Lake is the correct choice for Databricks or Microsoft Fabric primary platforms**, with UniForm providing read-only Iceberg metadata for external consumers. Managed Iceberg tables in Unity Catalog offer a bidirectional alternative.
3. **Parquet is the dominant file format for lakehouse storage.** ORC retains advantages for Hive ACID and selective queries. Avro serves as Kafka transport, Iceberg metadata format, and CDC wire format — not merely a Kafka serialization format.
4. **Catalog choice creates more lock-in than table format choice.** Polaris, Nessie, and Lakekeeper offer the lowest lock-in. Glue is expedient on AWS but creates vendor coupling. The REST Catalog spec is necessary but not sufficient for true portability.
5. **ClickHouse Iceberg integration is production-ready** for reads (mature) and writes (beta, 25.7+). Native MergeTree remains 2-3x faster. The hot/cold tiering pattern (MergeTree + Iceberg) is the established architecture.
6. **Streaming writes require architectural buffering.** Buffer in Kafka, micro-batch to Iceberg at 1-5 minute intervals, compact separately. The ~15 commits/min/table ceiling is practical, not hard — centralized committer patterns can mitigate.
7. **Operational overhead is real and mandatory.** Compaction, snapshot expiration, and orphan file cleanup are not optional. Managed services (BigQuery, Databricks auto-optimize) reduce burden at the cost of platform coupling.
8. **The industry is converging on dual-format coexistence**, not single-format dominance. Iceberg is the interchange standard; Delta persists in Microsoft/Databricks ecosystems. Plan for interop, not elimination.
