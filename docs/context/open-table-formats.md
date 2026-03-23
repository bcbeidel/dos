---
name: "Open Table Formats: Delta Lake vs Iceberg vs File Formats"
description: "File formats (Parquet, ORC, Avro) vs table formats (Delta Lake, Iceberg) — what they are, how they differ, and when to use each"
type: context
related:
  - docs/context/iceberg-cross-platform-compatibility.md
  - docs/context/iceberg-catalog-interoperability.md
  - docs/research/2026-03-22-open-table-formats.research.md
---

## Key Insight

File formats and table formats are distinct layers solving different problems. Parquet, ORC, and Avro define byte layout on disk. Delta Lake and Iceberg are metadata and protocol layers on top of file formats that add ACID transactions, schema evolution, time travel, and partition management. Both Delta Lake and Iceberg default to Parquet as their underlying file format.

## File Formats

**Parquet** is the dominant default for analytics and lakehouse storage. It is the only file format supported by BigQuery managed Iceberg tables, Snowflake Iceberg tables, and most modern lakehouse engines. Columnar layout with page-level statistics enables efficient predicate pushdown for analytical queries.

**ORC** retains genuine advantages over Parquet in two areas: Hive ACID transactions (which require ORC) and selective queries where ORC's built-in bloom filter indexes eliminate I/O faster than Parquet's min/max statistics. ORC often achieves better compression ratios (up to 75% reduction in some benchmarks). Outside Hive-centric environments, ORC is not the right default.

**Avro** is a row-based format serving multiple roles: Kafka serialization (the standard via Schema Registry), Iceberg internal metadata format (manifest lists and manifest files are Avro), and CDC wire format (Debezium serializes change events as Avro by default). Avro is the transport format; Parquet is the storage format. In a streaming-to-lakehouse pipeline, Avro-serialized Kafka messages are deserialized and written to Iceberg tables as Parquet files.

## Table Formats

**Apache Iceberg** is the cross-platform write interoperability standard. Every major engine (Databricks, Snowflake, BigQuery, ClickHouse, Trino, Spark, Flink) supports Iceberg read/write. Iceberg's partition evolution lets you change partitioning strategies without rewriting data — old data retains old partitions, new data gets new ones. Hidden partitioning abstracts partition details from users. Iceberg v3 (ratified August 2025) added deletion vectors, row-level lineage, VARIANT type for semi-structured data, and nanosecond timestamps.

**Delta Lake** is the optimized default for Databricks and Microsoft Fabric ecosystems. UniForm (GA) generates Iceberg metadata alongside Delta writes without rewriting data, enabling Iceberg clients (Snowflake, BigQuery, Athena) to read Delta tables — but this access is read-only. Delta's transaction log (`_delta_log/`) is simpler than Iceberg's three-level metadata hierarchy. Databricks provides proprietary auto-optimize and auto-compaction that reduce operational burden.

## Selection Guidance

- **Cross-engine interchange:** Iceberg. It is the format every engine commits to supporting for both read and write.
- **Databricks or Microsoft Fabric primary platform:** Delta Lake, with UniForm for external read access. Managed Iceberg tables in Unity Catalog offer a bidirectional alternative.
- **Both formats will persist.** The industry is converging on dual-format coexistence (Iceberg as interchange, Delta as Databricks/Fabric write format), not single-format dominance. Databricks' $1B+ Tabular acquisition (June 2024), Iceberg v3 ratification, and Snowflake's full bidirectional support all reinforce Iceberg as the interchange standard without eliminating Delta.

## Takeaway

Choose the table format based on your primary platform, not abstract feature comparisons. Iceberg is the correct default for cross-engine interoperability. Delta Lake is the correct default within Databricks/Fabric. Parquet is the file format underneath both. The REST Catalog API is the actual convergence point — it matters more than which table format you pick.
