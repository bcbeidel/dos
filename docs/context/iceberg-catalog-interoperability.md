---
name: "Iceberg Catalog Interoperability"
description: "REST Catalog spec as the interop layer, catalog options with lock-in analysis, and practical selection guidance"
type: context
related:
  - docs/context/open-table-formats.md
  - docs/context/iceberg-cross-platform-compatibility.md
  - docs/research/2026-03-22-open-table-formats.research.md
---

## Key Insight

Catalog choice creates more lock-in than table format choice. The Iceberg REST Catalog API is the convergence point for cross-engine access, but the spec achieves semantic interoperability without guaranteeing operational interoperability. Two "compliant" catalogs can differ by orders of magnitude in response time. Select catalogs based on lock-in tolerance, not feature checklists.

## The REST Catalog Spec

The Iceberg REST Catalog API enables any compatible engine to read/write tables without custom integration. Supported engines include Spark 3.5, Flink 1.19, Trino 448, PyIceberg, and DuckDB. All major catalog implementations (Polaris, Unity Catalog, Nessie, Glue, Lakekeeper, Gravitino) speak this protocol.

**Operational gaps** (identified in a January 2026 critique):
- **No performance SLOs.** The spec is silent on latency expectations, throughput baselines, and response time guarantees.
- **No concurrency control semantics.** 409 Conflict is defined but retry behavior is not. Aggressive streaming writers can starve batch compaction jobs.
- **No multi-catalog sync timing.** Cross-catalog synchronization has no defined SLA. Sync can take minutes at scale.
- **Incomplete implementations.** Catalogs claiming REST compliance often implement only a subset of the spec. Unity Catalog OSS may not support all write endpoints.
- **Java-centric client libraries.** Non-Java engines (ClickHouse in C++, some Rust-based tools) must reimplement catalog clients.

Production deployments must test catalog-specific behavior rather than relying on spec compliance alone.

## Catalog Options

| Catalog | Lock-in | Best For |
|---------|---------|----------|
| **Apache Polaris** (Snowflake, Apache Incubating) | Low | Federated migration from existing metastores, multi-cloud, Snowflake integration |
| **Project Nessie** (Dremio/community) | Low | Git-style data experimentation, cross-table atomicity, pluggable backends (Postgres, RocksDB, DynamoDB) |
| **Lakekeeper** (community) | Low | Lightweight deployment (single Rust binary), container-first (K8s/Helm) |
| **Unity Catalog** (Databricks, open-sourced under Apache 2.0) | Medium | AI/ML asset governance alongside tabular data, Delta Lake interop via UniForm |
| **Gravitino** (Datastrato) | Medium | Multi-format (Iceberg, Hudi, Delta), geo-distributed metadata sync |
| **AWS Glue Data Catalog** | High | AWS-native environments where convenience outweighs portability |
| **Hive Metastore** | Low (OSS) but high operational burden | Legacy environments, broadest tool compatibility (Spark, Presto, Hive, older tools) |

## Lock-in Analysis

**Lowest lock-in:** Polaris, Nessie, Lakekeeper. Open-source, portable, standard REST API, no vendor-specific pricing.

**Medium lock-in:** Unity Catalog is open-sourced under Apache 2.0 and hosted by LF AI and Data Foundation, but its development is Databricks-aligned. It implements the Iceberg REST Catalog API (leveraging Tabular acquisition expertise) and supports Delta, Iceberg, and Parquet. External Iceberg catalogs (Glue, Hive, Snowflake Horizon) are accessible through Lakehouse Federation.

**Highest lock-in:** AWS Glue. AWS-specific pricing, regional limitations, awkward for multi-cloud. Iceberg support is best in Glue 4.0+ (optimistic locking by default). Delta Lake integration has sync issues — manifest tables can become stale when data is updated externally.

**Legacy risk:** Hive Metastore uses Thrift (no REST API), but now offers an Iceberg REST Catalog API facade, meaning HMS environments can speak REST without migrating. HMS remains the broadest legacy-compatible option.

## Selection Guidance

- **Multi-cloud or vendor-neutral:** Polaris or Nessie. Both are open-source with standard REST API.
- **Lightweight, container-first:** Lakekeeper. Single Rust binary, minimal dependencies.
- **AWS-native, convenience-first:** Glue. Accept the lock-in for reduced operational burden.
- **Databricks-centric with governance needs:** Unity Catalog. Best Delta+Iceberg dual-format support.
- **Legacy Hadoop/Hive environment:** Keep Hive Metastore, add REST facade for modern engines.

## Takeaway

The REST Catalog spec is necessary but not sufficient for true portability. It enables semantic interop (any REST client can talk to any REST catalog) but not operational interop (performance, concurrency, and sync behavior vary per implementation). Pick the catalog with the right lock-in profile for your organization, test actual behavior under your workload, and treat the REST API as the escape hatch rather than the guarantee.
