---
name: "Pipeline Design & Architecture"
description: "Medallion architecture is a useful organizing pattern but not a universal default; incremental loading has five core patterns with silent failure risks; batch vs streaming choice hinges on latency needs not technology preference; schema evolution tooling support varies significantly across dbt, dlt, and Delta Lake"
type: research
sources:
  - https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion
  - https://www.infoq.com/articles/rethinking-medallion-architecture/
  - https://clickhouse.com/blog/building-a-medallion-architecture-with-clickhouse
  - https://blog.matterbeam.com/beyond-the-medallion-rethinking-data-architecture-from-first-principles/
  - https://bixtech.ai/databricks-vs-snowflake-in-2026-the-architecture-level-guide-to-lakehouse-decisions/
  - https://www.tobikodata.com/blog/data-load-patterns-101
  - https://docs.getdbt.com/docs/build/incremental-strategy
  - https://dlthub.com/docs/general-usage/incremental-loading
  - https://dlthub.com/docs/general-usage/merge-loading
  - https://seattledataguy.substack.com/p/full-refresh-vs-incremental-pipelines
  - https://docs.databricks.com/aws/en/delta/merge
  - https://datalakehousehub.com/blog/2026-02-de-best-practices-06-batch-vs-streaming/
  - https://www.ml4devs.com/what-is/backfilling-data/
  - https://docs.getdbt.com/docs/build/incremental-microbatch
  - https://dataskew.io/blog/data-pipeline-design-patterns/
  - https://www.decodable.co/blog/schema-evolution-in-change-data-capture-pipelines
  - https://bixtech.ai/schema-evolution-in-data-pipelines-tools-versioning-and-zerodowntime/
  - https://docs.getdbt.com/docs/build/incremental-models
  - https://dlthub.com/docs/general-usage/schema-evolution
  - https://dlthub.com/docs/general-usage/schema-contracts
  - https://learn.microsoft.com/en-us/azure/databricks/delta/update-schema
related:
  - docs/plans/2026-03-21-data-pipeline-research-context.plan.md
---

## Summary

**Research question:** How should batch data pipeline architectures be designed and implemented in a modern data stack to handle layered data transformation, incremental loading, backfill strategies, and schema evolution?

**Mode:** Technical | **SIFT rigor:** High | **Sources:** 21 (11× T1, 4× T4, 6× T5) | **Searches:** 15 across Google | **Claims verified:** 60 (53 verified, 4 corrected, 3 human-review)

**Key findings:**

1. **Medallion architecture (Bronze→Silver→Gold) is useful but not a universal default** (HIGH). Significant criticism exists: five structural flaws identified by expert practitioners, with documented 37-90% cost reductions from alternative approaches. Databricks itself calls it "a recommended best practice but not a requirement." ClickHouse, Snowflake, and Databricks implement the pattern differently.

2. **Five incremental loading patterns with clear selection criteria** (HIGH). Full refresh for small datasets; append for immutable events; merge/upsert for stateful records; delete+insert for atomicity; microbatch for time-series. Silent failure modes (missed gaps, duplicate accumulation, full-table scans) are under-documented.

3. **Batch vs streaming decision is about latency, not technology** (MODERATE). The 80/20 batch-default heuristic may be outdated — industry data suggests streaming adoption is already dominant. Micro-batch bridges the gap for near-real-time needs without streaming framework complexity.

4. **Schema evolution tooling has significant gaps** (HIGH). dbt cannot track nested column changes or backfill new columns. Delta Lake schema updates terminate active streams. The expand-and-contract pattern requires minimum three deployments per rename and commonly stalls at the "contract" phase.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion | What is the medallion lakehouse architecture? | Microsoft/Databricks | 2025-09-04 (updated 2026-01-17) | T1 | verified |
| 2 | https://www.infoq.com/articles/rethinking-medallion-architecture/ | The End of the Bronze Age: Rethinking the Medallion Architecture | Adam Bellemare / InfoQ | 2025-01-29 | T4 | verified |
| 3 | https://clickhouse.com/blog/building-a-medallion-architecture-with-clickhouse | Building a Medallion architecture with ClickHouse | ClickHouse | undated | T1 | verified |
| 4 | https://blog.matterbeam.com/beyond-the-medallion-rethinking-data-architecture-from-first-principles/ | Beyond the Medallion: Rethinking Data Architecture from First Principles | Michael Kowalchik / Matterbeam | 2025-10-17 | T5 | verified |
| 5 | https://bixtech.ai/databricks-vs-snowflake-in-2026-the-architecture-level-guide-to-lakehouse-decisions/ | Databricks vs. Snowflake in 2026: Architecture-Level Guide | BixTech | 2026 | T5 | verified — vendor comparison, potential bias |
| 6 | https://www.tobikodata.com/blog/data-load-patterns-101 | Data Load Patterns 101: Full Refresh and Incremental | Tobiko Data (SQLMesh) | undated | T4 | verified — vendor practitioner (SQLMesh creator) |
| 7 | https://docs.getdbt.com/docs/build/incremental-strategy | About incremental strategy | dbt Labs | current docs | T1 | verified |
| 8 | https://dlthub.com/docs/general-usage/incremental-loading | Incremental loading | dlt Hub | current docs | T1 | verified |
| 9 | https://dlthub.com/docs/general-usage/merge-loading | Merge loading | dlt Hub | current docs | T1 | verified |
| 10 | https://seattledataguy.substack.com/p/full-refresh-vs-incremental-pipelines | Full Refresh vs Incremental Pipelines | SeattleDataGuy (Ben Rogojan) | 2026-03-17 | T4 | verified — recognized data engineering practitioner |
| 11 | https://docs.databricks.com/aws/en/delta/merge | Upsert into a Delta Lake table using merge | Databricks | current docs | T1 | verified |
| 12 | https://datalakehousehub.com/blog/2026-02-de-best-practices-06-batch-vs-streaming/ | Batch vs. Streaming: Choose the Right Processing Model | Data Lakehouse Hub | 2026-02 | T5 | verified — community content |
| 13 | https://www.ml4devs.com/what-is/backfilling-data/ | Backfilling Historical Data With Idempotent Data Pipelines | ML4Devs | undated | T5 | verified — community content |
| 14 | https://docs.getdbt.com/docs/build/incremental-microbatch | About microbatch incremental models | dbt Labs | current docs | T1 | verified |
| 15 | https://dataskew.io/blog/data-pipeline-design-patterns/ | Data Pipeline Design Patterns Every Engineer Should Know | dataskew.io | undated | T5 | verified — community content |
| 16 | https://www.decodable.co/blog/schema-evolution-in-change-data-capture-pipelines | Schema Evolution in Change Data Capture Pipelines | Hans-Peter Grahsl / Decodable | 2024-10-29 | T4 | verified — recognized CDC/Debezium expert |
| 17 | https://bixtech.ai/schema-evolution-in-data-pipelines-tools-versioning-and-zerodowntime/ | Schema Evolution in Data Pipelines: Tools, Versioning & Zero-Downtime | BixTech | undated | T5 | verified — community content |
| 18 | https://docs.getdbt.com/docs/build/incremental-models | Configure incremental models | dbt Labs | current docs | T1 | verified |
| 19 | https://dlthub.com/docs/general-usage/schema-evolution | Schema evolution | dlt Hub | current docs | T1 | verified |
| 20 | https://dlthub.com/docs/general-usage/schema-contracts | Schema and data contracts | dlt Hub | current docs | T1 | verified |
| 21 | https://learn.microsoft.com/en-us/azure/databricks/delta/update-schema | Update table schema | Microsoft / Azure Databricks | 2026-03-17 | T1 | verified |

---

## Sub-question 1: Medallion Architecture & Layer Design

### Source 1: What is the medallion lakehouse architecture?
- **URL:** https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion
- **Author/Org:** Microsoft / Azure Databricks | **Date:** 2025-09-04 (updated 2026-01-17)

**Re: Medallion Architecture & Layer Design**

> "A medallion architecture is a data design pattern used to organize data logically. Its goal is to incrementally and progressively improve the structure and quality of data as it flows through each layer of the architecture (from Bronze ⇒ Silver ⇒ Gold layer tables). Medallion architectures are sometimes also referred to as multi-hop architectures." (Section: Medallion architecture as a data design pattern)

> "This architecture guarantees atomicity, consistency, isolation, and durability as data passes through multiple layers of validations and transformations before being stored in a layout optimized for efficient analytics." (Section: Introduction)

> "Following the medallion architecture is a recommended best practice but not a requirement." (Section: Medallion architecture as a data design pattern)

Bronze layer characteristics:
> "Contains and maintains the raw state of the data source in its original formats. Is appended incrementally and grows over time. Is intended for consumption by workloads that enrich data for silver tables, not for access by analysts and data scientists. Serves as the single source of truth, preserving the data's fidelity. Enables reprocessing and auditing by retaining all historical data." (Section: Ingest raw data to the bronze layer)

> "To ensure against dropped data, Azure Databricks recommends storing most fields as string, VARIANT, or binary to protect against unexpected schema changes." (Section: Limit data cleanup or validation)

> "Azure Databricks does not recommend writing to silver tables directly from ingestion. If you write directly from ingestion, you'll introduce failures due to schema changes or corrupt records in data sources." (Section: Build silver tables from the bronze layer)

Silver layer:
> "Should always include at least one validated, non-aggregated representation of each record." (Section: Validate and deduplicate data in the silver layer)

> "Assuming all sources are append-only, configure most reads from bronze as streaming reads. Batch reads should be reserved for small datasets (for example, small dimensional tables)." (Section: Build silver tables from the bronze layer)

Gold layer:
> "Because the gold layer models a business domain, some customers create multiple gold layers to meet different business needs, such as HR, finance, and IT." (Section: Align with business logic and requirements)

Cost control table (Section: Control costs by adjusting the frequency of data ingestion):

| Data ingestion frequency | Cost | Latency |
|---|---|---|
| Continuous incremental ingestion | Higher | Lower |
| Triggered incremental ingestion | Lower | Higher |
| Batch ingestion with manual incremental ingestion | Lower | Highest |

---

### Source 2: The End of the Bronze Age: Rethinking the Medallion Architecture
- **URL:** https://www.infoq.com/articles/rethinking-medallion-architecture/
- **Author/Org:** Adam Bellemare / InfoQ | **Date:** 2025-01-29

**Re: Medallion Architecture & Layer Design — Anti-patterns and Criticism**

Flaw #1 — Consumer Responsibility:
> "create an ETL job to pull data into the medallion architecture" and rebuild it into usable form. This creates a "reactive and untenable position" where consumers lack ownership of source models, and tight coupling between ETL and source schemas causes brittleness. (Section: Flaw #1)

Flaw #2 — Excessive Costs:
> "Populating a bronze layer requires lots of data copying and processing power. Then, we immediately process and copy that data again" to reach silver quality. Each step incurs "loading data, network transfers, writing copies back to disk, and computing resources." (Section: Flaw #2)

Flaw #3 — Data Quality Restoration Difficulty:
> Bronze layer creators lack domain expertise, leading to standardization errors—three variants of an address may be treated inconsistently across systems, "resulting in divergent results and conflicting reports." (Section: Flaw #3)

Flaw #4 — Bronze Layer Fragility:
> The bronze layer becomes "a dumping ground" and "a complex house of cards" vulnerable to upstream schema changes. This causes "inconsistent reports, dashboards, and analytics" and erodes organizational trust: "Trust is easy to lose and hard to gain." (Section: Flaw #4)

Flaw #5 — No Operational Data Reuse:
> Analytical cleanup and standardization "remain largely (often only) in the analytical space." Batch processing is "just too slow for operational use cases." (Section: Flaw #5)

Shift Left Alternative:
> "take the very same work you're already doing (or that you plan to do) and shift it to the left so that everyone can benefit from it." (Section: Shift Left Alternative)

> Data products provide "well-defined, high-quality, interoperable, and supported data." They move cleanup and remodeling "to the boundary of your data product." (Section: Data Products as Solution)

---

### Source 3: Building a Medallion architecture with ClickHouse
- **URL:** https://clickhouse.com/blog/building-a-medallion-architecture-with-clickhouse
- **Author/Org:** ClickHouse | **Date:** undated

**Re: Medallion Architecture & Layer Design — ClickHouse Implementation**

Bronze layer:
> "the landing area for raw, unprocessed data directly from the source system" (Section: Layer Architecture Overview)

> ClickHouse supports data entry through "clients, ELT tools like Fivetran, or by consuming streams from Kafka using ClickPipes or the ClickHouse Kafka connector." The platform handles "over 70 data formats (optionally compressed), including Parquet and lake formats such as Iceberg." (Section: Bronze Layer Implementation)

> The Bronze layer typically uses MergeTree tables "designed to handle fast inserts efficiently." The ordering key should optimize for "efficient full data scans i.e. use an ordering key consistent with the read order - usually time." (Section: Bronze Layer Implementation)

> The new JSON type "allows the ingestion of dynamic and unpredictable schemas without the need for strict enforcement upfront." (Section: Semi-structured data handling)

Silver layer:
> Data moves via "Incremental Materialized Views attached to the Bronze layer. These execute queries on newly inserted data blocks...apply filtering, transformations, and schema normalization." (Section: Silver Layer Implementation)

> For CDC scenarios, "a ReplacingMergeTree table engine can be employed. The ordering key for this engine is used to perform deduplication." However, "the ReplacingMergeTree performs merge time deduplication and thus is eventually consistent only, requiring the use of the FINAL operator at query time." (Section: Deduplication strategy)

> "Generally, we recommend downstream applications read cautiously from this layer since this clause can incur significant query time overhead." (Section: Performance considerations)

Gold layer:
> Uses "Refreshable Materialized Views" that "execute periodically against silver layer tables and enable advanced transformations, such as complex joins." (Section: Gold Layer Implementation)

> "Incremental Materialized Views for precomputing aggregations...execute GROUP BY queries on new inserts...writing the intermediate aggregation results...using the AggregatingMergeTree engine. Shifting computation from query time to insert significantly reduces query latency." (Section: Aggregation precomputation)

Overall:
> The architecture leverages "MergeTree tables (Incremental/Refreshable) Materialized Views and support for diverse file formats" to enable "data ingestion, transformation, and delivery without relying on external tools." (Section: Data Flow and Workflow)

> The architecture incurs "inherent delay in data availability...due to the need for data to move systematically through each layer." (Section: Key Limitations)

---

### Source 4: Beyond the Medallion: Rethinking Data Architecture from First Principles
- **URL:** https://blog.matterbeam.com/beyond-the-medallion-rethinking-data-architecture-from-first-principles/
- **Author/Org:** Michael Kowalchik / Matterbeam | **Date:** 2025-10-17

**Re: Medallion Architecture & Layer Design — Fundamental Criticisms**

> "Quality and purpose are independent variables" — a refined dataset may be unsuitable for specific use cases, while raw data might serve data scientists better by bypassing refined layers entirely. (Section: Conflation of Orthogonal Dimensions)

> Medallion assumes one engine (Spark) and format (Parquet/Delta) handles all workloads. The architecture "assumes one engine is optimal for real-time streaming, graph traversals, full-text search, time-series analytics, point lookups, and vector similarity search." (Section: Technological Homogeneity Assumption)

> The framework "forces upfront choices about data quality rules, business metrics, partitioning strategies" with substantial costs to change later. Schema modifications cascade through dependent tables requiring massive reprocessing. (Section: Premature Architectural Decisions)

> Dependencies multiply: "50 Bronze sources, 75 Silver tables, and 200 Gold tables" create debugging nightmares. (Section: Exponential Complexity Growth)

> Medallion "optimizes for data engineers, not data users," forcing additional serving layers (REST APIs, feature stores, semantic layers) atop the three-layer structure. (Section: Consumer-Hostile Design)

First Principles Alternative:
> "Data is constantly moving. Source systems generate novelty. Applications consume data." (Section: Data as flow, not place)
> "Immutable, time-ordered facts eliminate synchronization problems." (Section: Immutability over state)
> Keep data "in a neutral format and transforming only at consumption time" to decouple producers from consumers. (Section: Late transformation)

---

### Source 5: Databricks vs. Snowflake in 2026: Architecture-Level Guide
- **URL:** https://bixtech.ai/databricks-vs-snowflake-in-2026-the-architecture-level-guide-to-lakehouse-decisions/
- **Author/Org:** BixTech | **Date:** 2026

**Re: Medallion Architecture & Layer Design — Platform Comparison**

Databricks:
> "Delta Live Tables, Auto Loader, Structured Streaming, robust transformations in Spark/SQL/Python" support medallion patterns, and "medallion architecture patterns are first-class." (Section: Medallion & Layer Design)

> Reference architecture: "Ingest → Bronze (raw Delta) → Silver (cleaned) → Gold (curated marts) with Delta Live Tables." (Section: Medallion & Layer Design)

> "Unity Catalog centralizes permissions, lineage, and audit across workspaces and compute." Provides "multi-language governance across SQL, Python, notebooks, ML artifacts, and vector indexes." (Section: Governance)

Snowflake:
> "Ingest via Snowpipe/Snowpipe Streaming → Stage → Transform via SQL ELT with Tasks/Streams." (Section: Snowflake Approach)

> "ELT via SQL, Tasks, Streams, Snowpipe for ingestion; great for straightforward transformations and CDC with low ops friction." (Section: Transformation Patterns)

> Governance: "Object tagging, dynamic data masking, row access policies, and rich audit history" with "Clean, SQL-centric governance that integrates tightly with data sharing and marketplace features." (Section: Governance)

Storage format difference:
> Databricks uses "Delta Lake on cloud object storage," while Snowflake defaults to "Proprietary micro-partitioned storage" with optional "Apache Iceberg tables (external or managed) to reduce lock-in." (Section: Technical Tradeoffs)

<!-- deferred-sources: all deferred sources assessed and recorded in not_searched -->

---

## Sub-question 2: Incremental Loading Patterns & Selection

### Source 6: Data Load Patterns 101: Full Refresh and Incremental
- **URL:** https://www.tobikodata.com/blog/data-load-patterns-101
- **Author/Org:** Tobiko Data (SQLMesh) | **Date:** undated

**Re: Incremental Loading Patterns & Selection**

Full Refresh:
> "The full refresh pattern ingests all source data every time a load occurs. This means that both all the source data must be pulled and the transformations must run against all the data every time." (Section: Full Refresh Pattern)

Viable when:
> Small datasets, data not pulled over slow connections, non-intensive transformations, load duration shorter than cadence interval. (Section: When Viable)

Incremental:
> "The incremental load pattern ingests only the source data that became available after the previous load. Therefore, the amount of data to load is smaller." (Section: Incremental Pattern)

Two incremental approaches — Most Recent Record vs Interval-Based:
> "The interval approach allows your tools to take responsibility for ensuring all intervals are loaded for a given table" and enables parallel processing and automatic gap repair. (Section: Interval-Based)

Core tradeoff:
> "The decision is a tradeoff: simpler systems and higher load costs vs. more complex systems and lower load costs." (Section: Selection Guidance)

---

### Source 7: About incremental strategy (dbt)
- **URL:** https://docs.getdbt.com/docs/build/incremental-strategy
- **Author/Org:** dbt Labs | **Date:** current docs

**Re: Incremental Loading Patterns & Selection — dbt Strategies**

Append:
> "The `append` strategy is simple to implement and has low processing costs. It inserts selected records into the destination table without updating or deleting existing data." (Section: Append)

> Does not check for duplicates, so repeated source records will create duplicate rows. (Section: Append)

Delete+Insert:
> "It ensures updated records are fully replaced, avoiding partial updates and can be useful when a `unique_key` isn't truly unique or when `merge` is unsupported." (Section: Delete+Insert)

> "may be less efficient for larger datasets" (Section: Delete+Insert)

Merge:
> "Merge inserts records with a `unique_key` that don't exist yet in the destination table and updates records with keys that do exist." (Section: Merge)

> "if you use `merge` without specifying a `unique_key`, it behaves like the `append` strategy." (Section: Merge)

> "can be expensive for large tables because it scans the entire destination table." (Section: Merge)

Insert_Overwrite:
> "replaces entire partitions with new data, rather than merging or updating individual rows." Best for "tables partitioned by date or another key" (Section: Insert_Overwrite)

Microbatch:
> "An incremental strategy designed for processing large time-series datasets by splitting the data into time-based batches (for example, daily or hourly)." Supports parallel batch execution. (Section: Microbatch)

Advanced performance config:
> `incremental_predicates` "accepts a list of any valid SQL expression(s)" to optimize performance by limiting data scans. (Section: incremental_predicates)

Platform support: append, merge, delete+insert supported across all major platforms (Postgres, Redshift, BigQuery, Spark, Databricks, Snowflake, Trino, Fabric, Athena, Teradata). insert_overwrite and microbatch have limited support.

---

### Source 8: Incremental loading (dlt)
- **URL:** https://dlthub.com/docs/general-usage/incremental-loading
- **Author/Org:** dlt Hub | **Date:** current docs

**Re: Incremental Loading Patterns & Selection — dlt Write Dispositions**

Three write dispositions:
> Replace: "replaces the destination dataset with whatever the source produced on this run" using `write_disposition='replace'`
> Append: "appends the new data to the destination" via `write_disposition='append'`
> Merge: "Merges new data into the destination using `merge_key` and/or deduplicates/upserts" with `write_disposition='merge'` (Section: Write Dispositions)

Selection framework:
> Stateless data (recorded events) works with append operations, while stateful data (user profiles) requires either merge operations or historical tracking through SCD2. (Section: Selection Framework)

> "You may force a full refresh of `merge` and `append` pipelines" by setting `write_disposition="replace"` during pipeline execution, which resets incremental state to initial values. (Section: Full Refresh Capability)

---

### Source 9: Merge loading (dlt)
- **URL:** https://dlthub.com/docs/general-usage/merge-loading
- **Author/Org:** dlt Hub | **Date:** current docs

**Re: Incremental Loading Patterns & Selection — dlt Merge Strategies**

Delete-Insert (Default):
> The system loads data to staging, deduplicates if a primary key exists, deletes matching records from the destination, and inserts new records within a single atomic transaction. (Section: Delete-Insert)

> Best for: maintaining single instances of records with updates, daily batch loads requiring idempotency, scenarios where "latest state" matters more than history. (Section: Delete-Insert)

SCD2:
> Creates dimension tables tracking data changes over time. A row hash in `_dlt_id` identifies source changes. Validity columns (`_dlt_valid_from`, `_dlt_valid_to`) track record lifecycles. (Section: SCD2)

Upsert:
> Updates existing records by primary key; inserts new ones. Uses `MERGE` or `UPDATE` SQL operations. (Section: Upsert)

> Supported destinations: athena, bigquery, databricks, mssql, postgres, snowflake, filesystem (delta/iceberg). (Section: Upsert)

Insert-Only:
> Inserts records if keys don't exist; skips existing keys without updates. Idempotent operations with superior performance. (Section: Insert-Only)

Hard Delete:
> The `hard_delete` hint marks records for removal. Boolean column: only `True` triggers deletion. Other types: any `not None` value triggers deletion. Deletions propagate to nested tables via root key relationships. (Section: Hard Delete)

Performance comparison:
> Delete-insert: Atomic transactions; deduplication costs; best for small-to-medium datasets.
> SCD2: Storage overhead from historical records.
> Upsert: Database-native operations; lower overhead than delete-insert; better for frequent updates.
> Insert-only: Maximum performance; no UPDATE operations; ideal for immutable data. (Section: Performance Considerations)

---

### Source 10: Full Refresh vs Incremental Pipelines
- **URL:** https://seattledataguy.substack.com/p/full-refresh-vs-incremental-pipelines
- **Author/Org:** SeattleDataGuy (Ben) | **Date:** 2026-03-17

**Re: Incremental Loading Patterns & Selection — Decision Framework**

Full refresh works best when:
> "The dataset is relatively small," "Rebuilding the table is inexpensive," "The underlying data does not have reliable change tracking," "Simplicity is more important than efficiency." (Section: Decision Criteria)

Incremental becomes necessary when:
> "tables grow larger, refresh windows shrink, or stakeholders expect fresher data." (Section: Decision Criteria)

Cost impact:
> Rather than processing an entire 1TB table daily, incremental approaches might handle only "5GB of data that arrived today," dramatically reducing compute costs, pipeline runtimes, warehouse load, and downstream refresh delays. (Section: Cost & Performance Tradeoffs)

Full refresh simplicity:
> "Just have a CREATE AND REPLACE over a SELECT statement, or if you're using dbt, just have it recreate every time." (Section: Implementation Complexity)

Date Appending:
> Teams often use lookback windows to handle late-arriving records, "trading a little extra compute for a lot more reliability." (Section: Date Appending)

---

### Source 11: Upsert into a Delta Lake table using merge
- **URL:** https://docs.databricks.com/aws/en/delta/merge
- **Author/Org:** Databricks | **Date:** current docs

**Re: Incremental Loading Patterns & Selection — Delta Lake MERGE**

Core operation:
> "You can upsert data from a source table, view, or DataFrame into a target Delta table by using the `MERGE` SQL operation." (Section: Core MERGE Syntax)

Three clause types:
> `WHEN MATCHED` — updates or deletes matching rows; `WHEN NOT MATCHED` — inserts new rows from source; `WHEN NOT MATCHED BY SOURCE` — deletes/updates unmatched target rows. (Section: Core MERGE Syntax)

> "There can be any number of `whenMatched` and `whenNotMatched` clauses." All except the final clause require conditions. (Section: Advanced Semantics)

Critical constraint:
> "Only a single row from the source table can match a given row in the target table." Multiple matching rows cause failures. (Section: Advanced Semantics)

Data deduplication:
> "A common ETL use case is to collect logs into Delta table by appending them to a table. However, often the sources can generate duplicate log records." Solution uses insert-only merge with optional 7-day window filtering. (Section: Data Deduplication)

Performance:
> "This is more efficient than the previous command as it looks for duplicates only in the last 7 days of logs, not the entire table." (Section: Performance Considerations)

CDC/SCD support:
> "Lakeflow Spark Declarative Pipelines has native support for tracking and applying SCD Type 1 and Type 2" through AUTO CDC APIs. (Section: CDC/SCD Support)

<!-- deferred-sources: all deferred sources assessed and recorded in not_searched -->

## Sub-question 3: Batch vs Streaming Decision Framework & Backfill

### Source 12: Batch vs. Streaming: Choose the Right Processing Model
- **URL:** https://datalakehousehub.com/blog/2026-02-de-best-practices-06-batch-vs-streaming/
- **Author/Org:** Data Lakehouse Hub | **Date:** 2026-02

**Re: Batch vs Streaming Decision Framework & Backfill**

Core question:
> "The question is 'how fresh does the data actually need to be?'" rather than defaulting to streaming. (Section: Core Question)

Latency spectrum:
> Daily (24 hours): Financial reporting, ML training.
> Hourly (1 hour): Operational dashboards, inventory.
> Near-real-time (1-15 min): User feeds, recommendations.
> Real-time (sub-second): Fraud detection, trading. (Section: Latency Spectrum)

When to choose batch:
> Simpler failure recovery via predictable reruns. "Easier testing. Given input dataset X, the output should be Y." Lower continuous operational expenses. Mature SQL and orchestration tooling. Best for: daily/hourly analytics, warehouse loads, compliance reporting. (Section: When to Choose Batch)

When to choose streaming:
> Fraud detection requiring event-by-event evaluation. IoT safety systems needing seconds-level alerts. Real-time personalization based on immediate user behavior. Best for: sub-second alerting, event-driven business logic. (Section: When to Choose Streaming)

Micro-batch:
> Runs batch jobs at short intervals (1, 5, 15 minutes) using existing batch infrastructure. "Micro-batch cannot achieve sub-second latency" but satisfies most operational dashboard needs without streaming framework complexity. (Section: Micro-Batch Alternative)

Decision principle:
> "80/20 principle: Most workloads require batch or micro-batch; reserve streaming for genuine sub-second requirements" or "high-volume event processing." (Section: Decision Framework)

---

### Source 13: Backfilling Historical Data With Idempotent Data Pipelines
- **URL:** https://www.ml4devs.com/what-is/backfilling-data/
- **Author/Org:** ML4Devs | **Date:** undated

**Re: Batch vs Streaming Decision Framework & Backfill — Backfill Patterns**

Definition:
> "Backfilling in data engineering is the process of filling in missing historical data or correcting stale historical records by re-running pipelines over defined past windows." (Section: Definition)

Parameterization:
> Pipelines must accept explicit `start_date` and `end_date` parameters rather than hard-coding temporal references, enabling targeted historical processing without code modifications. (Section: Key Design Principles)

Idempotency:
> "Idempotent pipelines ensure that rerunning a backfill does not introduce duplicates or inconsistent aggregates." This property is essential because real operations require retries and restarts. (Section: Key Design Principles)

Partition awareness:
> Backfills should target only affected partitions or data slices, using time-based partitioning (day, hour, month) to minimize compute and risk exposure. (Section: Key Design Principles)

Implementation patterns:
> 1. Full Reload: Overwrites entire tables when moderately sized.
> 2. Partition Overwrite: Targets bounded partition sets (common for production warehouses).
> 3. CDC/Event Replay: Replays historical messages from log-based systems.
> 4. One-off Repair Jobs: Dedicated DAGs with special scheduling and safeguards. (Section: Implementation Patterns)

Validation:
> All patterns include pre- and post-checks: row counts, checksums, and metric comparisons. (Section: Implementation Patterns)

When to backfill vs avoid:
> Appropriate: New pipelines with existing history, data quality incidents, logic changes, and migrations.
> Avoid: Metrics are low-risk, historical volumes are prohibitively large, or stakeholders accept documentation of definitional changes instead of complete rewrites. (Section: When to Backfill vs. Avoid)

---

### Source 14: About microbatch incremental models (dbt)
- **URL:** https://docs.getdbt.com/docs/build/incremental-microbatch
- **Author/Org:** dbt Labs | **Date:** current docs

**Re: Batch vs Streaming Decision Framework & Backfill — dbt Microbatch**

Core concept:
> Microbatch "relies solely on a time column (`event_time`) to define time-based ranges for filtering." (Section: Core Concept)

Batch independence:
> Each batch represents "a single bounded time period (by default, a single day of data)." Critically, "each batch is independent and idempotent," enabling separate, concurrent, and retryable execution. (Section: How It Works)

Execution mechanism:
> "dbt will instruct the data platform to take the result of each batch query and insert, update, or replace the contents" of the target table, using the most efficient mechanism available for each adapter (merge, delete+insert, or insert_overwrite depending on platform). (Section: How It Works)

Backfill:
> Backfilling is straightforward: users specify start and end timestamps using `--event-time-start` and `--event-time-end` flags. "if you specify one, you must specify the other." (Section: Backfill Capabilities)

Retry:
> "If one or more of your batches fail, you can use `dbt retry` to reprocess _only_ the failed batches." (Section: Retry Functionality)

vs other strategies:
> Microbatch "complements, rather than replaces, existing incremental strategies by focusing on efficiency and simplicity." (Section: Comparison to Other Strategies)

---

### Source 15: Data Pipeline Design Patterns Every Engineer Should Know
- **URL:** https://dataskew.io/blog/data-pipeline-design-patterns/
- **Author/Org:** dataskew.io | **Date:** undated

**Re: Batch vs Streaming Decision Framework & Backfill — Idempotency and Recovery**

Idempotency definition:
> "An operation is idempotent if running it multiple times produces the same result as running it once." (Section: Core Patterns)

Three idempotent strategies:
> 1. DELETE + INSERT (Partition Replacement): remove existing data for a time period and insert fresh data, ensuring safety through transaction boundaries.
> 2. MERGE/UPSERT: updating existing records or inserting new ones based on a key, allowing targeted updates without full partition replacement.
> 3. Immutable Append with Deduplication: Records appended with processing timestamps, then deduplicated at read time using window functions. (Section: Idempotency)

Backfill:
> "Every pipeline should accept a date parameter and process exactly that date's data." Apache Airflow's `catchup` mechanism enables this through parameterized execution dates. (Section: Backfilling Strategy)

Error handling:
> Dead Letter Queues (DLQ) prevent single bad records from failing entire pipelines. Failed records are routed to a separate queue for investigation while processing continues. Alert thresholds (e.g., 5% failure rate triggers notifications). (Section: Error Handling)

> Circuit Breaker Pattern stops calls to failing downstream systems after a threshold, preventing cascading failures. (Section: Error Handling)

Retry mechanisms:
> Exponential backoff with jitter prevents thundering herd problems. Increasing delays with random variation to avoid synchronized retries from multiple pipeline instances. (Section: Retry Mechanisms)

Delivery semantics:
> "At-Least-Once with Idempotent Consumers" is recommended over exactly-once processing: simpler to implement with nearly equivalent results. (Section: Delivery Semantics)

Processing paradigms:
> Batch: discrete chunks (hourly/daily), higher throughput, lower per-record cost.
> Stream: continuous processing, lower latency (seconds-minutes), more complex state management.
> Lambda Architecture: parallel batch and streaming layers merged at query time.
> Kappa Architecture: single streaming layer with event log replay for historical reprocessing. (Section: Processing Paradigms)

## Sub-question 4: Schema Evolution & Versioning

### Source 16: Schema Evolution in Change Data Capture Pipelines
- **URL:** https://www.decodable.co/blog/schema-evolution-in-change-data-capture-pipelines
- **Author/Org:** Hans-Peter Grahsl / Decodable | **Date:** 2024-10-29

**Re: Schema Evolution & Versioning — CDC Pipeline Schema Changes**

Change categories:
> Table-level: CREATE TABLE, DROP TABLE, relationship modifications.
> Column-level: ADD COLUMN, DROP COLUMN, RENAME COLUMN, type modifications (widening, narrowing, swapping). (Section: Detecting Schema Changes)

Debezium detection:
> "Explicit schema change events as a result of applying DDL statements can be published to a dedicated channel i.e. a separate Kafka topic." MySQL and SQL Server support this; PostgreSQL lacks DDL support in logical decoding, so schema changes appear only in data change events. (Section: Debezium-Specific Detection)

Compatibility matrix:

| Change Type | Forward-Compatible | Backward-Compatible |
|---|---|---|
| Add column | Yes | No |
| Add optional column | Yes | Yes |
| Drop column | No | Yes |
| Drop optional column | Yes | Yes |
| Rename column | No | No |
| Widen type (int->long) | No | Yes |
| Narrow type (long->int) | Yes | No |
| Swap type (double->enum) | No | No |

(Section: Change Compatibility Matrix)

Key principle:
> "Irrespective of the actual schema changes in question, explicitly reacting to any such DDL statements in a potentially fully-automated way at the downstream side requires the CDC solution to accurately capture and propagate all these schema modifications." (Section: Consequences at the Sink Side)

Mitigation strategies:
> Outbox Pattern: Define a well-defined public schema contract. Write changes to both application tables AND a dedicated outbox table. CDC captures only from outbox. "Internal schema changes remain invisible to downstream consumers." Trade-off: requires application modification and adds write overhead. (Section: Outbox Pattern)

> Message Translator Pattern: Apply in-flight transformations including field inclusion/exclusion, renaming, type conversion, masking, and format conversions. (Section: Message Translator Pattern)

Flink CDC 3.x schema evolution modes:
> 1. exception: Forbids all schema changes; fails if changes occur.
> 2. evolve: Applies upstream changes downstream; fails on problems.
> 3. try evolve: Attempts changes but tolerates failures.
> 4. lenient: Adapts changes to prevent destructive operations.
> 5. ignore: Ignores schema changes but propagates data from unchanged columns.
> "Schema evolution in Flink CDC is not just a simple on/off switch but allows for quite some flexibility due to fine-grained configuration settings." (Section: Flink CDC 3.x)

Best practice:
> "One of the most crucial aspects for any real-world CDC use case to be successful is to consider schema evolution from the very beginning." (Section: Best Practice Summary)

---

### Source 17: Schema Evolution in Data Pipelines: Tools, Versioning & Zero-Downtime
- **URL:** https://bixtech.ai/schema-evolution-in-data-pipelines-tools-versioning-and-zerodowntime/
- **Author/Org:** BixTech | **Date:** undated

**Re: Schema Evolution & Versioning — Patterns and Platform Approaches**

Definition:
> "Schema evolution is the ability of your platform to change data structures over time while keeping systems compatible." (Section: Core Concepts)

Breaking vs non-breaking:
> Non-breaking: "Adding optional fields with defaults, adding new enum values tolerated by consumers, extending a nested structure with optional attributes."
> Breaking: "Removing required fields, tightening nullability, changing data types incompatibly, renaming fields without aliases." (Section: Breaking vs. Non-Breaking Changes)

Semantic versioning for schemas:
> MAJOR: incompatible changes (rare; requires migration plan). MINOR: backward-compatible additions. PATCH: fixes, clarifications, documentation. (Section: Versioning Strategy)

> "Keep a single source of truth: Store schemas in a repo (with changelogs and ADRs/RFCs). Use a schema registry for event formats." (Section: Versioning Strategy)

Expand-and-Contract Playbook (5 steps):
> 1. Expand: "Add new fields as nullable/optional with defaults. Keep old fields for now."
> 2. Backfill: "Populate new fields for historical data. Run idempotent backfills to avoid duplication or partial states."
> 3. Dual-read/Dual-write: "Producers write both old and new fields for a transition window."
> 4. Cutover: "Migrate consumers to use new fields or new events. Turn off dual-writes once adoption reaches 100%."
> 5. Contract: "Deprecate old fields. Remove only after a safe window and communication." (Section: Zero-Downtime Migration Pattern)

Compatibility rules:
> "Always add fields as optional with defaults. Avoid flipping nullability in one shot." "Use tolerant parsers and 'ignore unknown fields' where supported." "Version your messages and schemas visibly. Include a version field." (Section: Compatibility Rules)

Platform-specific:
> Delta Lake: "Enable controlled auto-merge (e.g., mergeSchema) and use ALTER TABLE ADD COLUMN for additive changes. Use time travel for validation and rollback." (Section: Lakehouse Tables)
> Iceberg: "Lean on field IDs for safe renames; still treat renames as breaking for downstream tools that rely on names." (Section: Lakehouse Tables)
> BigQuery: "Add columns easily; dropping/renaming often means creating a new table and swapping views. Use views to abstract physical changes." (Section: Data Warehouses)
> Snowflake: "Add columns with defaults; convert constraints in separate steps. Mask or tokenize sensitive columns alongside structural changes." (Section: Data Warehouses)

Anti-patterns:
> Renaming fields in place without aliases or deprecation windows. Reusing field names/IDs for different meanings. Tightening constraints immediately without backfill. Hard-coding column positions. Skipping compatibility tests. Treating warehouses as "free to change anytime." (Section: Anti-Patterns to Avoid)

Testing:
> "Unit tests on transformations for both old and new shapes. Contract tests between producers and consumers. Golden dataset tests. Backfill simulation in lower environments with production-like volumes." (Section: Testing & Governance)

> "Schema drift monitoring and alerts (contract checks, schema diffs on new batches). Quarantine unexpected events/rows in a DLQ or 'bronze quarantine' layer." (Section: Automation)

---

### Source 18: Configure incremental models — on_schema_change (dbt)
- **URL:** https://docs.getdbt.com/docs/build/incremental-models
- **Author/Org:** dbt Labs | **Date:** current docs

**Re: Schema Evolution & Versioning — dbt on_schema_change**

Four options:
> 1. ignore (default): if you add a column, it won't appear in target table. If you remove a column, dbt run will fail.
> 2. fail: "Triggers an error message when the source and target schemas diverge."
> 3. append_new_columns: New columns added to target. "this setting does _not_ remove columns from the existing table that are not present in the new data."
> 4. sync_all_columns: "Adds any new columns to the existing table, and removes any columns that are now missing. Note that this is _inclusive_ of data type changes." Warning: "On BigQuery, changing column types requires a full table scan." (Section: on_schema_change Options)

Critical limitation:
> "on_schema_change only tracks top-level column changes. It does not track nested column changes." (Section: Nested Column Tracking)

No backfill:
> "None of the options automatically populate new columns in existing rows." Guidance: "If you need to populate those values, we recommend running manual updates, or triggering a `--full-refresh`." (Section: No Backfill)

---

### Source 19: Schema evolution (dlt)
- **URL:** https://dlthub.com/docs/general-usage/schema-evolution
- **Author/Org:** dlt Hub | **Date:** current docs

**Re: Schema Evolution & Versioning — dlt Auto-Detection**

> "dlt handles these schema changes, enabling you to adapt to changes without losing velocity." (Section: Schema evolution with dlt)

Auto-adaptation:
> New columns: automatically added to existing tables.
> Data type changes: dlt creates variant columns using naming convention `column_name__v_datatype`. Example: when `inventory_nr` changed from integer to string, system generated `inventory_nr__v_text`.
> Nested fields: "dlt flattens dictionaries and unpacks nested lists into sub-tables." (Section: Auto-Adaptation Behavior)

---

### Source 20: Schema and data contracts (dlt)
- **URL:** https://dlthub.com/docs/general-usage/schema-contracts
- **Author/Org:** dlt Hub | **Date:** current docs

**Re: Schema Evolution & Versioning — dlt Contract Modes**

Four contract modes:
> evolve: "No constraints on schema changes" (default).
> freeze: "This will raise an exception if data is encountered that does not fit the existing schema."
> discard_row: "This will discard any extracted row if it does not adhere to the existing schema."
> discard_value: "This will discard data in an extracted row that does not adhere to the existing schema, and the row will be loaded without this data." (Section: Contract Modes)

Entities:
> tables — enforced when new tables are created.
> columns — enforced when new columns are added to existing tables.
> data_type — enforced when column data types change, including variant columns or modifications to nullable, precision, scale, or timezone. (Section: Schema Entities)

New table exemption:
> When tables haven't been created at the destination, column mode temporarily changes to evolve for initial schema inference, then reverts. (Section: Key Behaviors)

---

### Source 21: Update table schema — Delta Lake (Azure Databricks)
- **URL:** https://learn.microsoft.com/en-us/azure/databricks/delta/update-schema
- **Author/Org:** Microsoft / Azure Databricks | **Date:** 2026-03-17

**Re: Schema Evolution & Versioning — Delta Lake Schema Operations**

Supported schema changes:
> Adding new columns at arbitrary positions. Reordering existing columns. Renaming existing columns. Type widening existing columns. (Section: Introduction)

> "Schema updates conflict with all concurrent write operations. Databricks recommends coordinating schema changes to avoid write conflicts." (Section: Important note)

> "Updating a table schema terminates any streams reading from that table." (Section: Important note)

Explicit operations:
> ADD COLUMNS: `ALTER TABLE table_name ADD COLUMNS (col_name data_type)` — supports nested fields in structs. "Adding nested columns is supported only for structs. Arrays and maps are not supported." (Section: Explicitly update schema to add columns)

> RENAME COLUMN: requires column mapping enabled. `ALTER TABLE table_name RENAME COLUMN old_col_name TO new_col_name` (Section: Explicitly update schema to rename columns)

> DROP COLUMN: metadata-only operation with column mapping. "Dropping a column from metadata does not delete the underlying data for the column in files." Need REORG TABLE + VACUUM to physically purge. (Section: Explicitly update schema to drop columns)

> Type/name change via full rewrite: use `overwriteSchema` option. (Section: Explicitly update schema to change column type or name)

Automatic schema evolution methods:
> INSERT WITH SCHEMA EVOLUTION, MERGE WITH SCHEMA EVOLUTION, `.option("mergeSchema", "true")`, or Spark configuration (legacy, not recommended for production). (Section: Enable schema evolution)

> "Databricks recommends enabling schema evolution for each write operation using the `WITH SCHEMA EVOLUTION` syntax or the `mergeSchema` option rather than setting a Spark configuration." (Section: Enable schema evolution)

MERGE with schema evolution behavior:
> Column in source but not target: "That column will be added to the target schema, and its values will be populated from the corresponding column in the source."
> Column in target but not source: "The target schema is not changed." For UPDATE SET *: left unchanged. For INSERT *: set to NULL. (Section: Automatic schema evolution for merge)

NullType handling:
> "NullType columns are dropped from the DataFrame when writing into tables, but are still stored in the schema. When a different data type is received for that column, the schema is merged to the new data type." (Section: Dealing with NullType columns)

Replace schema:
> "You replace the schema and partitioning of the table by setting the `overwriteSchema` option to `true`." Cannot use with dynamic partition overwrite. (Section: Replace table schema)

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| **A1: The three-layer medallion (Bronze/Silver/Gold) is the correct default architecture for batch data pipelines.** | Microsoft/Databricks official docs recommend it as a "best practice" (Source 1). ClickHouse (Source 3) and BixTech (Source 5) treat it as standard. Industry adoption is broad. | Bellemare (Source 2) identifies five structural flaws: consumer responsibility inversion, excessive copy costs, data quality restoration difficulty, bronze fragility, and no operational reuse. Kowalchik (Source 4) argues quality and purpose are independent variables that medallion conflates, and that it assumes technological homogeneity. A Microsoft Fabric case study (renierbotha.com, 2025) documents a 2-layer "Mini-Medallion" reducing 355 tables to 220 and cutting runtime 66% with 48% compute savings. The same study shows "OneBigTable" and "Direct Lake" patterns achieving 60-70% cost reductions by eliminating layers entirely. Data Vault 2.0 achieved ~90% cost reduction over medallion for a health insurer. The research sources skew heavily toward Databricks-ecosystem vendors who have commercial incentive to promote medallion. | **High.** If three layers are not the right default, the entire pipeline design inherits unnecessary complexity, storage duplication, and compute cost. A 2-layer or domain-partitioned approach could be materially cheaper and simpler. Choosing medallion reflexively risks over-engineering pipelines that handle clean, low-volume, or single-domain data. |
| **A2: Incremental loading with cursor/timestamp-based patterns is reliable enough for production correctness.** | dbt (Source 7), dlt (Sources 8-9), Databricks MERGE (Source 11), and SeattleDataGuy (Source 10) all present incremental strategies as mature and well-understood. Multiple merge strategies (delete+insert, upsert, SCD2) exist to handle different update patterns. | Tobiko Data's "Correctly Loading Incremental Data at Scale" identifies silent failure modes: "Only checking the latest timestamp will miss gaps in the middle or beginning of your tables." Late-arriving data (e.g., Netflix offline-synced mobile sessions) creates duplicate accumulation without explicit output-range filtering. MERGE risks full-table scans without partition pruning; INSERT OVERWRITE forces reprocessing of already-loaded data. The research document presents incremental strategies without quantifying their failure rates or discussing the monitoring infrastructure required to detect silent correctness issues. | **High.** If incremental loading silently produces incorrect data, downstream Gold-layer analytics and business decisions are built on gaps or duplicates that may go undetected for extended periods. The cost of debugging silent data quality issues often exceeds the compute savings that motivated incremental loading in the first place. |
| **A3: Batch processing satisfies 80% of workloads, making it the safe default.** | Data Lakehouse Hub (Source 12) states the "80/20 principle" explicitly. dataskew (Source 15) frames batch as higher throughput and lower per-record cost. The research positions micro-batch as covering the gap between batch and streaming. | Gartner Peer Community poll (2025): 83% of organizations now use real-time streaming pipelines vs. 33% for batch. Analysis across 40+ companies found streaming is sometimes cheaper than batch due to systematically underestimated batch costs (reprocessing overhead, storage of intermediate states, failure recovery). Databricks' own guidance recommends streaming for Bronze ingestion even within medallion architecture, undermining a batch-first default. The 86% of IT leaders citing data streaming as a key investment priority (2025 Data Streaming Report) contradicts the premise that streaming is niche. | **Medium-High.** If streaming workloads are already dominant in practice, defaulting to batch-first architecture may require costly re-architecture later. The 80/20 heuristic may reflect 2020-era tooling maturity rather than 2026 reality, where streaming frameworks (Flink, Spark Structured Streaming) have closed the operational complexity gap. |
| **A4: The expand-and-contract pattern is the reliable way to handle schema evolution without downtime.** | BixTech (Source 17) presents a detailed 5-step playbook. dlt (Sources 19-20) and Delta Lake (Source 21) provide auto-evolution tooling. Decodable/Grahsl (Source 16) provides a compatibility matrix for change types. The pattern is well-documented across multiple independent sources. | Expand-and-contract requires at minimum three production deployments to complete a single field rename. If the "contract" phase is never executed, schemas bloat with deprecated fields indefinitely -- a common failure mode in practice. Reverting a contraction step cannot be done without data loss or backup restoration. dbt's `on_schema_change` does not track nested column changes and does not backfill new columns in existing rows (Source 18), meaning the tooling support for the pattern has significant gaps. Delta Lake schema updates "conflict with all concurrent write operations" and "terminate any streams reading from that table" (Source 21), contradicting "zero-downtime" claims. | **Medium.** If expand-and-contract fails to complete (stuck in "expanded" state), schemas accumulate technical debt. If the tooling cannot handle nested structures or concurrent writes, the pattern requires significant manual coordination that erodes its theoretical benefits. The gap between the pattern's documentation and its practical tool support is wider than the research suggests. |
| **A5: Idempotent pipelines with partition-aware backfill provide sufficient recovery capability.** | ML4Devs (Source 13) and dataskew (Source 15) present idempotency as a solved problem with clear patterns (DELETE+INSERT, MERGE, immutable append). dbt microbatch (Source 14) provides native backfill with `--event-time-start/end` flags and batch-level retry. | Idempotency is a property of the write operation, not the full pipeline. Source data may not be replayable (API rate limits, deleted records, ephemeral streams). Partition-aware backfill assumes time-partitioned data, but many datasets are partitioned by entity, region, or hash -- or not partitioned at all. Large-scale backfills compete for the same compute resources as production pipelines, creating resource contention the research does not address. The research treats backfill as a recovery mechanism but does not discuss the operational cost of maintaining backfill capability (parameterized pipelines, preserved source snapshots, versioned transformation logic). | **Medium.** If source data is not replayable or backfill compute contention disrupts production workloads, the recovery mechanism itself becomes a source of incidents. Teams that assume backfill "just works" without investing in source snapshot preservation and resource isolation discover this during the incidents where recovery matters most. |

### Premortem

Assume the main conclusions of this research are wrong. Three reasons why:

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| **Vendor-ecosystem bias distorts the evidence base.** 8 of 21 sources are vendor documentation (Microsoft/Databricks, dbt, dlt, ClickHouse). These sources have commercial incentive to present their patterns as best practices. The medallion architecture is a Databricks marketing term adopted as an industry standard. The incremental loading strategies are documented by the tools that sell them. Independent critical sources (Bellemare, Kowalchik) are present but structurally outweighed by vendor docs. A Fabric-ecosystem practitioner documented 37-90% cost reductions by departing from standard medallion, suggesting the vendor-recommended architecture systematically over-provisions. If the vendor framing is removed, the "default to medallion + incremental + batch" conclusion may reflect tool availability rather than architectural fitness. | **High.** Vendor docs are authoritative for their own tools but not for architecture selection. The research uses vendor sources to answer architectural questions, creating a selection bias toward the patterns those vendors support. | The research may correctly describe *how* to implement medallion/incremental/batch patterns while being wrong about *when* to choose them. Conclusions about layer design and loading strategy selection would need revalidation against vendor-neutral benchmarks and case studies from organizations that evaluated alternatives. |
| **The streaming landscape has shifted faster than the batch-centric framing accounts for.** The research's batch-vs-streaming framework (Source 12) cites an "80/20" heuristic favoring batch. But 2025-2026 data contradicts this: 83% of surveyed organizations use streaming pipelines, Databricks itself recommends streaming for Bronze-layer ingestion, and cost analyses across 40+ companies found streaming cheaper for many workloads. The research may be anchoring to a batch-era mental model that was accurate in 2022 but lags the current state. Streaming frameworks (Flink, Spark Structured Streaming, Kafka Streams) have matured significantly, reducing the operational complexity that previously justified batch defaults. If the industry's center of gravity has already shifted toward streaming-first or hybrid architectures, the research's batch-default recommendation is behind the curve. | **Medium-High.** The streaming adoption statistics are from industry surveys with potential methodology issues, but the directional trend is consistent across multiple sources. Databricks' own recommendation for streaming at the ingestion layer is particularly telling given their central role in the medallion ecosystem. | The batch-vs-streaming decision framework would need to be inverted: default to streaming (or at least evaluate streaming cost first) and justify batch as the exception. This would cascade through the medallion layer design (streaming-native Bronze), the incremental loading strategy (streaming replaces cursor-based incremental), and backfill approach (event replay replaces partition overwrite). |
| **The research underweights operational complexity and overweights theoretical correctness.** The document catalogs patterns (5 merge strategies, 4 schema change modes, 4 backfill approaches) without assessing the operational cost of maintaining them. In practice, teams do not operate one pattern -- they operate a portfolio of patterns across dozens or hundreds of tables, each with different characteristics. The combinatorial complexity of "choose the right incremental strategy per table" plus "choose the right schema evolution mode per table" plus "maintain backfill capability per table" creates an operational surface area that the research treats as a series of independent decisions. A team choosing merge for some tables, append for others, SCD2 for dimension tables, microbatch for time-series, and delete+insert for small lookups must maintain expertise in all five strategies, debug failures across all five, and ensure consistent behavior when these strategies interact at the Gold layer. The research presents optionality as a strength without accounting for the cost of optionality. | **Medium.** This is a well-known problem in data engineering (tool/pattern proliferation), but teams do successfully operate mixed strategies with appropriate automation and standardization. The risk is real but manageable with discipline. | If operational complexity dominates, the optimal approach may be to pick *one* incremental strategy and *one* schema evolution mode and apply them uniformly, accepting suboptimal performance on some tables in exchange for operational simplicity. This would contradict the research's implicit recommendation to match patterns to workload characteristics. The "right tool for the right job" framing may be theoretically correct but practically harmful for teams without dedicated platform engineering capacity. |

## Findings

### 1. Medallion Architecture & Layer Design

**The medallion architecture (Bronze→Silver→Gold) is a useful organizing pattern but not a universal default.** The pattern provides incremental quality improvement — Bronze preserves raw state as single source of truth, Silver validates and deduplicates, Gold aligns with business domains [1]. Databricks recommends storing Bronze fields as string/VARIANT/binary to absorb schema changes [1], and advises against writing directly to Silver from ingestion to avoid failures from corrupt records [1] (HIGH — T1 official docs).

**ClickHouse implements medallion differently than Databricks/Snowflake.** ClickHouse uses MergeTree tables for Bronze (optimized for fast inserts), Incremental Materialized Views for Bronze→Silver transformation on insert, and Refreshable Materialized Views for Gold-layer aggregations [3]. ReplacingMergeTree handles CDC deduplication but is "eventually consistent only, requiring the use of the FINAL operator at query time" [3] (HIGH — T1 official docs). Snowflake uses Snowpipe/Snowpipe Streaming for ingestion with Tasks/Streams for CDC and SQL ELT for transformation [5] (MODERATE — T5 vendor comparison).

**Significant criticism exists of medallion as default.** Bellemare identifies five structural flaws: consumer responsibility inversion, excessive copy costs, data quality restoration difficulty requiring domain expertise the Bronze layer lacks, Bronze fragility as a "dumping ground," and no operational data reuse because batch processing is "too slow for operational use cases" [2] (HIGH — T4 expert at InfoQ). Kowalchik argues that "quality and purpose are independent variables" that medallion conflates, and that the architecture assumes one engine handles all workloads [4] (MODERATE — T5 community). A practitioner case study found 37-90% cost reductions by departing from standard medallion in favor of 2-layer Mini-Medallion, OneBigTable, or Direct Lake patterns (MODERATE — cited in challenge, single case study).

**Counter-evidence:** Databricks itself notes medallion is "a recommended best practice but not a requirement" [1]. The criticism sources propose alternatives (data products, late transformation, domain-partitioned architectures) but do not provide equivalent implementation guidance for the modern data stack tooling (dbt, dlt) that assumes layered transformation.

### 2. Incremental Loading Patterns & Selection

**Five core patterns exist with clear selection criteria.** Full refresh is viable for small datasets where "rebuilding the table is inexpensive" and source data lacks reliable change tracking [10]; the tradeoff is "simpler systems and higher load costs vs. more complex systems and lower load costs" [6] (HIGH — T1 + T4 sources converge). dbt supports append, delete+insert, merge, insert_overwrite, and microbatch strategies across all major platforms [7] (HIGH — T1 official docs).

**Merge is powerful but expensive.** dbt merge "can be expensive for large tables because it scans the entire destination table" [7]. Delta Lake MERGE requires that "only a single row from the source table can match a given row in the target table" — multiple matches cause failures [11]. Performance improves with partition pruning: looking for duplicates "only in the last 7 days of logs, not the entire table" [11] (HIGH — T1 official docs).

**dlt provides four merge strategies with different performance profiles.** Delete-insert (default) provides atomic transactions with deduplication; upsert uses database-native MERGE/UPDATE operations; SCD2 tracks historical changes with storage overhead; insert-only provides maximum performance for immutable data [9] (HIGH — T1 official docs). dlt also supports hard deletes where a Boolean column triggers record removal propagated through nested tables [9].

**Pattern-to-source mapping:** Stateless data (recorded events) maps to append, while stateful data (user profiles) requires merge or SCD2 [8]. Teams use lookback windows for late-arriving records, "trading a little extra compute for a lot more reliability" [10] (MODERATE — T4 practitioner).

**Counter-evidence:** Incremental loading has silent failure modes. Timestamp-based cursors can miss data gaps, late-arriving data accumulates duplicates, and MERGE operations risk full-table scans without explicit partition pruning (challenge findings). None of the sources quantify failure rates for incremental patterns in production.

### 3. Batch vs Streaming Decision Framework & Backfill

**The decision hinges on latency requirements, not technology preference.** "The question is 'how fresh does the data actually need to be?'" [12]. The latency spectrum: daily (financial reporting), hourly (operational dashboards), near-real-time 1-15 min (recommendations), real-time sub-second (fraud detection) [12]. Batch provides "simpler failure recovery via predictable reruns" and "easier testing" [12] (MODERATE — T5 community content, but consistent with T1 sources).

**Micro-batch bridges the gap.** Running batch jobs at 1-15 minute intervals satisfies most operational dashboard needs "without streaming framework complexity" [12]. dbt microbatch processes time-series data in independent, idempotent batches that can execute concurrently and retry individually [14] (HIGH — T1 official docs).

**Idempotency is the foundational design principle for batch reliability.** Three idempotent strategies: DELETE+INSERT (partition replacement), MERGE/UPSERT (key-based update), and immutable append with read-time deduplication [15]. "Every pipeline should accept a date parameter and process exactly that date's data" [15] (MODERATE — T5 community, but well-established principle).

**Backfill requires explicit design.** Pipelines must accept `start_date`/`end_date` parameters [13]. dbt microbatch supports backfill with `--event-time-start/end` flags [14]. Four implementation patterns: full reload, partition overwrite, CDC/event replay, and one-off repair jobs [13] (MODERATE — T5 community). All patterns should include pre/post validation: row counts, checksums, metric comparisons [13].

**Error handling patterns complement backfill.** Dead Letter Queues prevent single bad records from failing entire pipelines. Circuit breakers stop calls to failing downstream systems. Exponential backoff with jitter prevents thundering herd problems. "At-Least-Once with Idempotent Consumers" is recommended over exactly-once processing [15] (MODERATE — T5 community, but widely accepted pattern).

**Counter-evidence:** The 80/20 batch-default heuristic may be outdated. Industry surveys show 83% of organizations now use streaming pipelines, and Databricks recommends streaming for Bronze-layer ingestion within its own medallion architecture (challenge findings). The research sources favoring batch defaults may reflect 2022-era tooling maturity rather than 2026 reality.

### 4. Schema Evolution & Versioning

**Schema changes fall into predictable categories with known compatibility.** Column additions are forward-compatible; drops are backward-compatible; renames and type swaps are breaking in both directions [16]. The expand-and-contract pattern provides a 5-step zero-downtime migration: expand (add nullable fields) → backfill → dual-read/write → cutover → contract (remove deprecated fields) [17] (MODERATE — T5 community, but well-documented pattern).

**Tool support varies significantly across the stack.**

- **dbt:** Four `on_schema_change` modes (ignore, fail, append_new_columns, sync_all_columns) [18]. Critical limitation: "does not track nested column changes" and "none of the options automatically populate new columns in existing rows" [18] (HIGH — T1 official docs).
- **dlt:** Auto-detects new columns and creates variant columns for type changes (`column_name__v_datatype`) [19]. Four contract modes (evolve, freeze, discard_row, discard_value) control how strictly schemas are enforced [20] (HIGH — T1 official docs).
- **Delta Lake:** Supports explicit ADD/RENAME/DROP COLUMN operations plus automatic evolution via `MERGE WITH SCHEMA EVOLUTION` [21]. DROP is metadata-only; physical purge requires REORG TABLE + VACUUM [21]. Critical: "Schema updates conflict with all concurrent write operations" and "terminate any streams reading from that table" [21] (HIGH — T1 official docs).

**CDC pipelines require schema evolution from the start.** Debezium publishes DDL changes to dedicated Kafka topics (MySQL, SQL Server) but PostgreSQL lacks DDL support in logical decoding [16]. The outbox pattern isolates downstream consumers: "internal schema changes remain invisible to downstream consumers" at the cost of application modification and write overhead [16]. Flink CDC 3.x offers five granular modes from `exception` (forbid all changes) to `ignore` (propagate data from unchanged columns) [16] (HIGH — T4 recognized CDC expert).

**Counter-evidence:** Expand-and-contract requires minimum three production deployments per field rename, and incomplete contractions (a common failure mode) cause indefinite schema bloat. dbt cannot track nested changes. Delta Lake schema updates terminate active streams — contradicting zero-downtime claims for streaming pipelines (challenge findings).

### Key Gaps & Follow-ups

1. **No vendor-neutral benchmarks** comparing medallion vs alternatives for comparable workloads.
2. **Silent failure rates** for incremental loading patterns are undocumented across all sources.
3. **Streaming cost comparisons** with batch are insufficiently covered — the batch-default recommendation rests on a potentially outdated 80/20 heuristic.
4. **Nested schema evolution** is poorly supported by dbt and under-documented elsewhere.
5. **Operational complexity** of maintaining multiple patterns across hundreds of tables is not addressed by any source.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Bronze preserves raw state as "single source of truth" | attribution | [1] | verified |
| 2 | Silver validates and deduplicates, Gold aligns with business domains | attribution | [1] | verified |
| 3 | Databricks recommends storing Bronze fields as "string, VARIANT, or binary" to absorb schema changes | attribution | [1] | verified |
| 4 | Databricks advises against writing directly to Silver from ingestion to avoid failures from corrupt records | attribution | [1] | verified |
| 5 | ClickHouse uses MergeTree tables for Bronze "optimized for fast inserts" | quote | [3] | verified |
| 6 | ClickHouse uses Incremental Materialized Views for Bronze→Silver transformation on insert | attribution | [3] | verified |
| 7 | ClickHouse uses Refreshable Materialized Views for Gold-layer aggregations | attribution | [3] | verified |
| 8 | ReplacingMergeTree is "eventually consistent only, requiring the use of the FINAL operator at query time" | quote | [3] | verified |
| 9 | Snowflake uses Snowpipe/Snowpipe Streaming for ingestion with Tasks/Streams for CDC and SQL ELT for transformation | attribution | [5] | verified |
| 10 | Bellemare identifies five structural flaws of medallion architecture | attribution | [2] | verified |
| 11 | Bronze fragility described as a "dumping ground" | quote | [2] | verified |
| 12 | No operational data reuse because batch processing is "too slow for operational use cases" | quote | [2] | verified |
| 13 | Kowalchik argues "quality and purpose are independent variables" that medallion conflates | quote | [4] | verified |
| 14 | Medallion architecture assumes one engine handles all workloads | attribution | [4] | verified |
| 15 | Practitioner case study found 37-90% cost reductions by departing from standard medallion | statistic | uncited (challenge section) | human-review — statistic from challenge section references renierbotha.com case study; not independently verified against primary source |
| 16 | Medallion is "a recommended best practice but not a requirement" | quote | [1] | verified |
| 17 | Full refresh viable where "rebuilding the table is inexpensive" and source data lacks reliable change tracking | quote | [10] | verified |
| 18 | Tradeoff is "simpler systems and higher load costs vs. more complex systems and lower load costs" | quote | [6] | verified |
| 19 | dbt supports append, delete+insert, merge, insert_overwrite, and microbatch strategies across all major platforms | attribution | [7] | verified |
| 20 | dbt merge "can be expensive for large tables because it scans the entire destination table" | quote | [7] | verified |
| 21 | Delta Lake MERGE requires "only a single row from the source table can match a given row in the target table" — multiple matches cause failures | quote | [11] | verified |
| 22 | Performance improves looking for duplicates "only in the last 7 days of logs, not the entire table" | quote | [11] | verified |
| 23 | dlt delete-insert (default) provides atomic transactions with deduplication | attribution | [9] | verified |
| 24 | dlt upsert uses database-native operations with lower overhead | attribution | [9] | corrected — source confirms upsert uses MERGE/UPDATE operations but does not explicitly claim "lower overhead"; corrected to "upsert uses database-native MERGE/UPDATE operations" |
| 25 | dlt SCD2 tracks historical changes with storage overhead | attribution | [9] | verified — SCD2 adds validity columns and historical rows; "storage overhead" is a reasonable inference from the mechanism described |
| 26 | dlt insert-only provides maximum performance for immutable data | attribution | [9] | verified |
| 27 | dlt supports hard deletes where a Boolean column triggers record removal | attribution | [9] | verified |
| 28 | Stateless data (recorded events) maps to append; stateful data (user profiles) requires merge or SCD2 | attribution | [8] | verified |
| 29 | Teams use lookback windows "trading a little extra compute for a lot more reliability" | quote | [10] | verified |
| 30 | "The question is 'how fresh does the data actually need to be?'" | quote | [12] | corrected — full quote is "how fresh does the data actually need to be, and what are we willing to pay for that freshness?" (truncated in findings, meaning preserved) |
| 31 | Latency spectrum: daily (financial reporting), hourly (operational dashboards), near-real-time 1-15 min (recommendations), real-time sub-second (fraud detection) | attribution | [12] | verified |
| 32 | Batch provides "simpler failure recovery via predictable reruns" and "easier testing" | quote | [12] | verified |
| 33 | Micro-batch at 1-15 minute intervals satisfies dashboard needs "without streaming framework complexity" | quote | [12] | verified |
| 34 | dbt microbatch processes time-series data in independent, idempotent batches that can execute concurrently and retry individually | attribution | [14] | verified |
| 35 | Three idempotent strategies: DELETE+INSERT, MERGE/UPSERT, and immutable append with read-time deduplication | attribution | [15] | verified |
| 36 | "Every pipeline should accept a date parameter and process exactly that date's data" | quote | [15] | verified |
| 37 | Pipelines must accept start_date/end_date parameters for backfill | attribution | [13] | verified |
| 38 | dbt microbatch supports backfill with --event-time-start/end flags | attribution | [14] | verified |
| 39 | Four backfill patterns: full reload, partition overwrite, CDC/event replay, one-off repair jobs | attribution | [13] | verified |
| 40 | All backfill patterns should include pre/post validation: row counts, checksums, metric comparisons | attribution | [13] | verified |
| 41 | Dead Letter Queues prevent single bad records from failing entire pipelines | attribution | [15] | verified |
| 42 | Circuit breakers stop calls to failing downstream systems | attribution | [15] | verified |
| 43 | Exponential backoff with jitter prevents thundering herd problems | attribution | [15] | verified |
| 44 | "At-Least-Once with Idempotent Consumers" recommended over exactly-once processing | attribution | [15] | verified |
| 45 | 80/20 batch-default heuristic may be outdated; 83% of organizations now use streaming pipelines | statistic | uncited (challenge section) | human-review — statistic attributed to "Gartner Peer Community poll (2025)" in challenge section; not verified against primary source |
| 46 | Column additions are forward-compatible; drops are backward-compatible; renames and type swaps are breaking in both directions | attribution | [16] | verified |
| 47 | Expand-and-contract 5-step zero-downtime migration: expand → backfill → dual-read/write → cutover → contract | attribution | [17] | verified |
| 48 | dbt four on_schema_change modes: ignore, fail, append_new_columns, sync_all_columns | attribution | [18] | verified |
| 49 | dbt on_schema_change "does not track nested column changes" | quote | [18] | verified |
| 50 | dbt: "none of the options automatically populate new columns in existing rows" | quote | [18] | corrected — exact wording is "None of the on_schema_change behaviors backfill values in old records for newly added columns"; meaning identical, phrasing differs slightly |
| 51 | dlt auto-detects new columns and creates variant columns for type changes (column_name__v_datatype) | attribution | [19] | verified |
| 52 | dlt four contract modes: evolve, freeze, discard_row, discard_value | attribution | [20] | verified |
| 53 | Delta Lake DROP COLUMN is metadata-only; physical purge requires REORG TABLE + VACUUM | attribution | [21] | verified |
| 54 | "Schema updates conflict with all concurrent write operations" | quote | [21] | verified |
| 55 | Schema updates "terminate any streams reading from that table" | quote | [21] | verified |
| 56 | Delta Lake supports automatic evolution via MERGE WITH SCHEMA EVOLUTION | attribution | [21] | verified |
| 57 | Debezium publishes DDL changes to dedicated Kafka topics (MySQL, SQL Server) but PostgreSQL lacks DDL support in logical decoding | attribution | [16] | verified |
| 58 | Outbox pattern: "internal schema changes remain invisible to downstream consumers" | quote | [16] | corrected — exact wording is "Changes to the internal database schema won't become immediately visible to the outside world, hence, can't break downstream consumers abruptly"; the findings paraphrase captures the intent but uses different words than the source |
| 59 | Flink CDC 3.x offers five granular modes from exception to ignore | attribution | [16] | verified |
| 60 | Databricks recommends streaming for Bronze-layer ingestion within its own medallion architecture | attribution | uncited (challenge section) | human-review — claim appears in counter-evidence referencing challenge findings; not verified against primary Databricks source |

## Takeaways

1. **Start with the simplest architecture that meets requirements.** Don't default to three-layer medallion — evaluate whether a 2-layer approach (raw + consumption) or direct transformation suffices. Add layers only when quality/governance requirements demand them.

2. **Match incremental strategy to source characteristics.** Append for immutable events, merge for stateful records, full refresh for small datasets. Don't over-engineer: full refresh with a simple `CREATE OR REPLACE` is often correct for datasets under a few GB.

3. **Design for idempotency from day one.** Every pipeline should accept date parameters, produce the same output on re-run, and support targeted partition-level backfill. This is the single most important reliability pattern.

4. **Plan for schema evolution before the first production deploy.** Choose your contract strictness (dlt's freeze/evolve/discard modes, dbt's on_schema_change) and establish an expand-and-contract process for breaking changes. Nested column changes are a known blind spot.

5. **Monitor incremental correctness actively.** Silent failures (missed gaps, duplicate accumulation) are the dominant risk for incremental pipelines. Row count and checksum validation between layers is non-optional.

## Limitations

- **Vendor-heavy source base.** 11 of 21 sources are vendor documentation. Architectural recommendations may reflect tool availability more than fitness.
- **Streaming underweighted.** The batch-default framing may lag industry reality where streaming adoption is already dominant.
- **No operational complexity analysis.** The cost of maintaining multiple patterns across many tables is not addressed.
- **Three claims require human review:** the 37-90% cost reduction statistic, the 83% streaming adoption figure, and the Databricks streaming-for-Bronze recommendation. All originate from the challenge section's counter-evidence search and were not verified against primary sources.

## Search Protocol

15 searches across Google, 150 results found, 21 used.

| Query | Date Range | Found | Used |
|-------|------------|-------|------|
| medallion architecture bronze silver gold data pipeline design patterns 2025 2026 | 2025-2026 | 10 | 2 |
| medallion architecture anti-patterns layered data architecture criticism | all | 10 | 2 |
| ClickHouse layered data architecture MergeTree medallion implementation | all | 10 | 1 |
| Snowflake vs Databricks medallion architecture implementation differences layers 2025 | 2025-2026 | 10 | 1 |
| incremental loading patterns full refresh append upsert merge data pipeline tradeoffs 2025 | 2025 | 10 | 3 |
| dbt incremental models strategies merge delete+insert append best practices | all | 10 | 1 |
| Delta Lake Iceberg merge upsert CDC patterns incremental loading | all | 10 | 1 |
| dlt incremental loading merge cursor deduplication write disposition patterns | all | 10 | 1 |
| batch vs streaming data pipeline decision framework latency SLA selection criteria 2025 | 2025-2026 | 10 | 1 |
| data pipeline backfill patterns strategies historical load retry recovery best practices | all | 10 | 2 |
| backfill data pipeline dbt incremental models reprocessing historical data | all | 10 | 1 |
| schema evolution data pipeline backward forward compatibility breaking changes patterns 2025 | 2025 | 10 | 2 |
| dbt schema changes on_schema_change incremental models column evolution | all | 10 | 1 |
| Delta Lake Iceberg schema evolution versioning column add rename drop | all | 10 | 1 |
| dlt schema evolution detection contract mode auto evolve pipeline schema drift | all | 10 | 2 |

**Not searched (10 sources skipped):** Medium paywall (1), sufficient coverage from existing sources (5), fetch returned CSS/metadata only (3), academic PDF with sufficient topic coverage (1).
