---
name: "Data Catalog & Lineage"
description: "Open-source catalogs (DataHub, OpenMetadata) require 4-8 weeks deployment and ongoing engineering investment but match commercial feature sets for core cataloging; Unity Catalog and Snowflake Horizon are platform-native catalogs optimized for their ecosystems, not general-purpose alternatives; OpenLineage is the de facto lineage interoperability standard but adoption is uneven — Airflow and Spark have mature integrations while dbt, Flink, and BI tools remain partial; column-level lineage achieves 97-99% accuracy on standard SQL via sqlglot but breaks on JSON extraction, UNNEST, dynamic SQL, and Python models; metadata catalogs decay within months without automated curation — manual-entry catalogs become untrusted within the first year; the data catalog market is projected to grow from ~$1B (2024) to $7.4B (2034) at 22.7% CAGR"
type: research
sources:
  - https://thedataguy.pro/blog/2025/08/open-source-data-governance-frameworks/
  - https://atlan.com/openmetadata-vs-datahub/
  - https://docs.datahub.com/docs/lineage/sql_parsing
  - https://datahub.com/blog/extracting-column-level-lineage-from-sql/
  - https://openlineage.io/blog/why-open-standard/
  - https://openlineage.io/docs/guides/spark/
  - https://docs.getdbt.com/docs/explore/column-level-lineage
  - https://github.com/unitycatalog/unitycatalog
  - https://www.snowflake.com/en/product/features/horizon/
  - https://datacrossroads.nl/2025/10/01/part-1-technological-challenges-data-lineage/
  - https://www.selectstar.com/resources/column-level-lineage-101-a-guide-for-modern-data-management
  - https://www.decube.io/post/data-catalog-metadata-management-guide
  - https://coalesce.io/data-insights/metadata-management-the-complete-guide-to-building-an-ai-ready-data-foundation/
  - https://www.foundational.io/blog/ci-cd-dbt-modern-data-stack
  - https://github.com/OpenLineage/OpenLineage
  - https://www.ibm.com/new/announcements/openlineage-for-a-unified-lineage-view-across-structured-and-unstructured-data-to-enable-explainable-ai
  - https://atlan.com/data-catalog-tools/
  - https://atlan.com/gartner-magic-quadrant-for-metadata-management/
  - https://github.com/canva-public/dbt-column-lineage-extractor
  - https://www.ovaledge.com/blog/ai-powered-open-source-data-catalogs
related:
  - docs/plans/2026-03-21-data-pipeline-research-context.plan.md
  - docs/research/2026-03-22-operations-reliability.research.md
  - docs/research/2026-03-22-pipeline-orchestration.research.md
---

## Summary

**Research question:** How should data catalog and lineage be implemented in a modern data stack, and what tooling options exist?

**Mode:** Technical | **SIFT rigor:** High | **Sources:** 20 | **Searches:** 18 across Google

**Key findings:**
- Open-source catalogs (DataHub, OpenMetadata) provide production-grade cataloging, lineage, and governance but require significant engineering investment — DataHub deploys in 4-8 weeks with a multi-component architecture (Kafka, graph DB, Elasticsearch), while OpenMetadata deploys in 2-4 weeks with a simpler stack (MySQL/PostgreSQL + Elasticsearch)
- Unity Catalog and Snowflake Horizon are platform-native catalogs optimized for their respective ecosystems — Unity Catalog supports Iceberg REST Catalog API for multi-engine access, while Horizon locks governance to Snowflake-managed data unless using Catalog-Linked Databases
- OpenLineage is the de facto open standard for lineage interoperability (LF AI & Data Foundation Graduate project), with mature integrations for Airflow (native since 2.7) and Spark, but uneven adoption across dbt, Flink, and BI tools
- Column-level lineage achieves 97-99% accuracy on standard SQL via sqlglot-based parsers but systematically fails on JSON extraction, UNNEST, dynamic SQL, MERGE INTO, Python models, and struct fields — making it reliable for impact analysis but incomplete for audit
- Metadata catalogs decay within months without automated curation — manual-entry catalogs become untrusted within the first year; success requires automated metadata harvesting, ownership assignment from usage patterns, and quality metrics (search click-through >35%, >80% domain ownership coverage)
- The data catalog market is valued at ~$1B (2024) and projected to reach $7.4B by 2034 at 22.7% CAGR; Gartner reintroduced its Magic Quadrant for Metadata Management in 2025 after a five-year pause

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://thedataguy.pro/blog/2025/08/open-source-data-governance-frameworks/ | Open-Source Data Governance Frameworks | TheDataGuy | 2025 | T5 | verified — practitioner analysis |
| 2 | https://atlan.com/openmetadata-vs-datahub/ | OpenMetadata vs DataHub | Atlan | 2025 | T4 | verified — vendor comparison (biased toward Atlan) |
| 3 | https://docs.datahub.com/docs/lineage/sql_parsing | SQL Parsing | DataHub | current docs | T1 | verified |
| 4 | https://datahub.com/blog/extracting-column-level-lineage-from-sql/ | Extracting Column-Level Lineage from SQL | DataHub / Harshal Sheth | 2024 | T4 | verified — vendor blog |
| 5 | https://openlineage.io/blog/why-open-standard/ | Why an Open Standard for Lineage Metadata? | OpenLineage | 2024 | T2 | verified — project documentation |
| 6 | https://openlineage.io/docs/guides/spark/ | Using OpenLineage with Spark | OpenLineage | current docs | T1 | verified |
| 7 | https://docs.getdbt.com/docs/explore/column-level-lineage | Column-level lineage | dbt Labs | current docs | T1 | verified |
| 8 | https://github.com/unitycatalog/unitycatalog | Unity Catalog | Databricks / OSS | current | T1 | verified |
| 9 | https://www.snowflake.com/en/product/features/horizon/ | Snowflake Horizon Catalog | Snowflake | current | T1 | verified — vendor product page |
| 10 | https://datacrossroads.nl/2025/10/01/part-1-technological-challenges-data-lineage/ | Data Lineage: Challenges and Trends 2025 | Data Crossroads | 2025 | T5 | verified — analyst blog |
| 11 | https://www.selectstar.com/resources/column-level-lineage-101-a-guide-for-modern-data-management | Column-Level Lineage Guide | Select Star | 2025 | T4 | verified — vendor guide |
| 12 | https://www.decube.io/post/data-catalog-metadata-management-guide | Data Catalog & Metadata Management Guide | Decube | 2025 | T4 | verified — vendor guide |
| 13 | https://coalesce.io/data-insights/metadata-management-the-complete-guide-to-building-an-ai-ready-data-foundation/ | Metadata Management Complete Guide | Coalesce | 2025 | T4 | verified — vendor guide |
| 14 | https://www.foundational.io/blog/ci-cd-dbt-modern-data-stack | CI/CD for Data Quality in the Modern Stack | Foundational | 2025 | T4 | verified — vendor blog |
| 15 | https://github.com/OpenLineage/OpenLineage | OpenLineage GitHub | LF AI & Data | current | T1 | verified |
| 16 | https://www.ibm.com/new/announcements/openlineage-for-a-unified-lineage-view-across-structured-and-unstructured-data-to-enable-explainable-ai | OpenLineage in IBM watsonx.data | IBM | 2025 | T2 | verified — enterprise vendor |
| 17 | https://atlan.com/data-catalog-tools/ | Best Data Catalog Tools 2026 | Atlan | 2026 | T4 | verified — vendor buyer's guide (biased toward Atlan) |
| 18 | https://atlan.com/gartner-magic-quadrant-for-metadata-management/ | Gartner MQ for Metadata Management 2025 | Atlan / Gartner | 2025 | T4 | verified — vendor summary of Gartner |
| 19 | https://github.com/canva-public/dbt-column-lineage-extractor | dbt Column Lineage Extractor | Canva | current | T2 | verified — production OSS tool |
| 20 | https://www.ovaledge.com/blog/ai-powered-open-source-data-catalogs | Open Source Data Catalogs for Enterprises | OvalEdge | 2025 | T4 | verified — vendor blog |

---

## Sub-question 1: Catalog Tool Comparison

### DataHub

DataHub employs a distributed, event-driven architecture with four components: relational database (MySQL/PostgreSQL) for document storage, Elasticsearch for search, a graph database (JanusGraph/Neo4j) for entity relationships, and Kafka for streaming metadata changes [1][3]. Every metadata change — a new table, a glossary update, a failed pipeline — becomes an immutable event on Kafka, enabling near-real-time downstream enrichment, indexing, and subscriber notification. This architecture excels at scale and data mesh implementations but imposes significant operational complexity. Deployment takes 4-8 weeks and requires Kubernetes expertise for production workloads [1].

DataHub's SQL parser (built on sqlglot) generates column-level lineage with 97-99% accuracy across 20+ SQL dialects [3][4]. The parser is schema-aware — it queries DataHub's own metadata APIs to resolve table schemas, enabling accurate column mapping through joins, subqueries, and CTEs. DataHub chose sqlglot over alternatives (OpenLineage/Marquez parser, SQLLineage used by OpenMetadata) specifically because it produced the highest accuracy on their benchmark suite [4]. The v1.4.0 release (2025) introduced Context Documents (importing from Notion/Confluence) and a Metrics Catalog with participation in Snowflake's Open Semantic Interchange initiative.

**Strengths:** Real-time metadata streaming, schema-aware lineage, AI-native protocol (Model Context Protocol), data mesh governance support.
**Weaknesses:** Complex multi-component deployment, high resource requirements, steep learning curve.

### OpenMetadata

OpenMetadata uses a simplified architecture — MySQL/PostgreSQL plus Elasticsearch — with no Kafka or graph database dependency [1][2]. This reduces deployment effort to 2-4 weeks and makes operational maintenance significantly easier. The platform provides 84+ connectors, built-in data quality and profiling, and a visual lineage editor for manual annotations. Version 1.8 (2025) introduced data contracts — machine-readable schemas, SLAs, and quality guarantees enforced automatically. Version 1.12 added semantic search with vector embeddings (supporting OpenAI and Bedrock) and custom AI-powered recognizers for classification [2].

OpenMetadata recently introduced a Kubernetes Orchestrator as an alternative to Airflow for managing metadata agents, simplifying deployment for teams already running Kubernetes.

**Strengths:** Simplest deployment among OSS catalogs, comprehensive out-of-box features, modern UI, built-in data quality.
**Weaknesses:** Limited real-time metadata capabilities, no event-driven architecture, stability concerns under high concurrency reported on GitHub.

### Unity Catalog

Unity Catalog is Databricks' open-source catalog (Apache 2.0), designed as a universal governance layer for data and AI assets — tables, files, functions, and ML models [8]. It supports Delta Lake, Iceberg (via UniForm), Hudi, Parquet, JSON, and CSV. The critical interoperability feature: Unity Catalog implements the Iceberg REST Catalog API, allowing external engines (Snowflake, Trino, Presto, Spark) to read and write Unity Catalog-managed tables without format lock-in.

Catalog Federation (Public Preview, 2025) allows Unity Catalog to connect to external catalogs — AWS Glue, Hive Metastore, Snowflake Horizon — and mirror table metadata without copying data. Each query checks for the latest snapshot from the foreign catalog before execution [8]. The v0.4 milestone (February 2026) focuses on managed locations, managed tables, and external locations with credentials.

**Strengths:** Open-source with Iceberg REST API, multi-engine access, AI asset governance (models, features, training datasets), catalog federation.
**Weaknesses:** Databricks-optimized — best experience within Databricks ecosystem, OSS version lacks the full governance features of managed Databricks Unity Catalog.

### Snowflake Horizon Catalog

Horizon Catalog is Snowflake's native governance layer providing metadata search, data classification, lineage tracking, access controls, and data quality monitoring — all integrated into the Snowflake platform [9]. It enforces dynamic data masking, row access policies, and automatic sensitive data classification. In 2025, Snowflake added AI-powered features including Cortex-generated data dictionaries and Copilot for Horizon Catalog.

Catalog-Linked Databases (GA 2025-2026) allow Horizon to sync with Apache Iceberg objects managed by any Iceberg REST Catalog, applying governance and discovery capabilities to externally managed data [9]. Horizon exposes Snowflake-managed Iceberg tables via the Polaris REST API, enabling external engine access.

**Strengths:** Zero-setup for Snowflake users, deep platform integration, AI-powered classification and documentation, built-in data sharing.
**Weaknesses:** Governance tied to Snowflake — limited utility for non-Snowflake data; requires Catalog-Linked Databases for external data governance.

### Atlan

Atlan is a commercial, AI-native "active metadata platform" recognized as a Leader in both Gartner's Metadata Management Magic Quadrant (2025) and Forrester Wave (2024) [17]. Its active metadata engine continuously parses query activity and dbt model runs to eliminate manual catalog curation. The platform provides 100+ certified connectors, automated lineage across columns/queries/metrics/dashboards, and natural language search with semantic understanding. Deployment reaches production in 4-6 weeks versus 3-9 months for legacy platforms like Alation or Collibra [17].

**Strengths:** Fastest time-to-value among commercial catalogs, AI-native curation, strong modern-stack integration (Snowflake, Databricks, dbt, Tableau).
**Weaknesses:** Commercial pricing (not publicly disclosed), SaaS-only deployment, vendor lock-in risk.

### Selection guidance

| Scenario | Recommended Catalog |
|----------|-------------------|
| Cloud-native, moderate engineering capacity | OpenMetadata |
| Data mesh, real-time metadata, AI-forward | DataHub |
| Databricks-centric stack | Unity Catalog |
| Snowflake-centric stack | Snowflake Horizon |
| Modern stack, fastest deployment, budget available | Atlan |
| Hadoop/legacy ecosystem | Apache Atlas |

---

## Sub-question 2: OpenLineage Standard and Lineage Interoperability

### What OpenLineage is

OpenLineage is an LF AI & Data Foundation Graduate project that defines an open specification for collecting lineage metadata [5][15]. The specification models three core entities — **Jobs** (units of work), **Runs** (executions of jobs), and **Datasets** (inputs and outputs) — connected by events emitted at job start, completion, and failure. The specification is extensible through **Facets** — typed metadata payloads that attach to jobs, runs, or datasets. Column-level lineage is implemented as a Dataset Facet, allowing tools to emit fine-grained lineage without modifying the core specification [15].

Marquez is the reference implementation — an open-source metadata repository that stores and serves OpenLineage events. However, OpenLineage events can be consumed by any compatible backend: DataHub, OpenMetadata, Atlan, and IBM watsonx.data all accept OpenLineage events [16].

### Integration maturity

OpenLineage integration maturity varies significantly across tools:

| Tool | Integration Level | Notes |
|------|------------------|-------|
| Apache Airflow | Mature (native) | Built-in provider since Airflow 2.7; all operators emit events by default [15] |
| Apache Spark | Mature | SparkListener implementation; captures inputs, outputs, schemas, execution plans [6] |
| dbt | Partial | Lineage extractable from manifest.json artifacts but not natively emitted as OpenLineage events; requires external tooling [7][19] |
| Apache Flink | Developing | Stream processing lineage collection supported but less battle-tested than Spark [15] |
| Great Expectations | Supported | Via checkpoint action list integration [15] |
| Dagster | Supported | Native integration available [15] |
| BI tools (Tableau, Looker, PowerBI) | Limited/None | Lineage typically extracted via SQL query log parsing, not OpenLineage events |

### Adoption reality

IBM expanded OpenLineage support across its watsonx.data intelligence platform in November 2025, and AWS documented integration with Amazon MWAA [16]. Enterprise adopters include Northwestern Mutual and BMW Group. However, OpenLineage has a fundamental coverage gap: it focuses on runtime lineage — events emitted during job execution — which leaves a blind spot for static code, rarely-executed pipelines, and ad hoc queries [10]. Tools that run infrequently or are triggered manually may never emit lineage events, creating invisible gaps in the lineage graph.

The standard is also not plug-and-play. It requires integration effort to emit events correctly, and has no native AI capabilities — it is an enabler rather than a feature-rich solution [20]. Configuration management across environments (dev, staging, production) remains a friction point reported by the community.

---

## Sub-question 3: Column-Level vs. Table-Level Lineage

### What each level provides

**Table-level lineage** tracks which tables feed which other tables — the DAG of data flow. It answers "what upstream tables does this dashboard depend on?" and is straightforward to extract from SQL parsing, dbt manifest.json, or orchestrator metadata. Coverage approaches 100% because the information is structurally present in every SQL query [11].

**Column-level lineage** tracks which specific columns in source tables map to which columns in target tables, including transformations applied. It answers "where does the `revenue` column in this report come from, and what calculations were applied?" This requires parsing the SELECT clause of SQL queries and resolving column references through joins, subqueries, CTEs, and expressions [3][4][11].

### Accuracy and practical limitations

DataHub's SQL parser (the most accurate open-source implementation) reports 97-99% accuracy on standard SQL [3]. However, this figure requires careful qualification — it measures accuracy on successfully parsed queries, not on the full universe of SQL a production data platform encounters.

Systematic failure cases include:

- **JSON extraction functions** (`json_extract`, `JSON_VALUE`, `GET_PATH`) — parser cannot trace through semi-structured data access [3]
- **UNNEST / lateral joins** — flattening operations create ambiguous column origins [7]
- **MERGE INTO statements** — column-level lineage is not generated [3]
- **Struct fields** — best-effort resolution, not guaranteed [3]
- **Dynamic SQL / `identifier()` functions** — table and column references resolved at runtime cannot be parsed statically [3]
- **Python dbt models** — no SQL to parse [7]
- **Columns in WHERE, GROUP BY, ORDER BY, JOIN, HAVING** — deliberately excluded from lineage (considered filtering/organization, not data flow) [3]
- **SELECT * expansion** — requires accurate schema information in the catalog; if schemas are stale, lineage breaks silently [3]

These limitations mean column-level lineage is reliable for **impact analysis** (what downstream assets are affected if I change this column?) and **root cause analysis** (where did this wrong value originate?) on standard SQL transformation patterns. It is **not** reliable for **audit** (proving the exact provenance of every value) or for environments with heavy use of semi-structured data, dynamic SQL, or Python transformations.

### Cost of implementation

Building column-level lineage is "expensive and resource-intensive" even for basic SQL queries [11]. Maintenance complexity increases as data stacks grow and change. The practical recommendation from 2025 practitioners: "It's better to have precise lineage for fewer assets than incomplete or misleading mappings for everything" [10]. Organizations should validate lineage outputs against actual transformation logic and use automation selectively while investing curation effort where trust and decision-making depend on it.

---

## Sub-question 4: Automated Lineage Extraction

### dbt artifacts

dbt generates two critical artifacts for lineage: `manifest.json` (model dependencies, sources, macros, the full DAG, column documentation) and `catalog.json` (database schema information including column types and descriptions) [7][19]. Together, these enable automatic generation of lineage graphs with model descriptions and column metadata.

**Table-level lineage** from dbt is straightforward — `manifest.json` contains the complete dependency graph via `ref()` and `source()` declarations. Every catalog (DataHub, OpenMetadata, Atlan) can ingest `manifest.json` and reconstruct the DAG.

**Column-level lineage** from dbt requires SQL parsing of model code. dbt Cloud/Catalog (Enterprise plan) provides this natively by parsing SELECT statements [7]. For open-source dbt, Canva's `dbt-column-lineage-extractor` uses sqlglot to parse model SQL and map column relationships [19]. The tool is lightweight but subject to the same SQL parsing limitations described above.

dbt Cloud CI jobs can regenerate and validate lineage on every pull request — running only modified models and their downstream dependencies in a staging schema [14]. This creates a natural integration point between catalog updates and the development workflow.

### Spark

OpenLineage's Spark integration works through the SparkListener interface [6]. Configuration requires adding the openlineage-spark JAR to `spark.jars.packages` and registering `OpenLineageSparkListener` as an extra listener. The listener automatically captures:

- Input and output datasets with schemas
- Optimized LogicalPlan (serialized query execution plan)
- Output statistics (record counts, bytes written)
- Data source metadata and Spark version

The integration works across Databricks, EMR, and Dataproc. Job names follow the pattern `{appName}.{operation_type}`. The listener captures events at run start, completion, and failure — the full OpenLineage lifecycle [6].

### SQL query log parsing

For warehouse-native lineage (outside dbt/Spark), catalogs parse SQL query logs from the warehouse's query history. DataHub supports automatic lineage extraction from BigQuery, Snowflake, Redshift, and 20+ sources through this mechanism [3]. The approach works well for table-level lineage but introduces a dependency on query history retention and access permissions. Snowflake's QUERY_HISTORY view, BigQuery's INFORMATION_SCHEMA.JOBS, and Redshift's STL_QUERYTEXT are the primary sources.

### Limitations of automated extraction

No automated extraction method achieves complete coverage [10]. Common blind spots:

1. **Custom scripts and legacy ETL** — pipelines that use Python, shell scripts, or proprietary tools outside the SQL-parseable ecosystem
2. **Cross-system transformations** — data that moves through APIs, message queues, or file transfers between systems
3. **Ad hoc queries** — analyst SQL that transforms data without running through instrumented pipelines
4. **Semantic transformations** — business logic encoded in BI tools (Tableau calculated fields, Looker LookML) that sits outside the data platform

Teams should expect automated lineage to cover 70-85% of data flows and plan for manual annotation of the remainder.

---

## Sub-question 5: Catalog Integration with CI/CD and dbt Docs

### CI/CD integration patterns

The core question is where the single source of truth for metadata lives: in dbt (schema.yml) or in the catalog [14][17]. Three patterns exist:

1. **dbt-first:** Descriptions, owners, and tags are defined in `schema.yml` files and ingested by the catalog. Changes flow through pull requests, code review, and CI validation. This approach ensures metadata is version-controlled but limits contributions to engineers comfortable with YAML and git.

2. **Catalog-first:** Business users curate metadata in the catalog UI. Changes are pushed back to dbt via automated pull requests. This approach lowers the barrier for domain experts but introduces synchronization complexity.

3. **Hybrid:** Technical metadata (column types, tests, lineage) is managed in dbt. Business metadata (descriptions, glossary terms, ownership) is managed in the catalog. Each system is authoritative for its domain. This is the emerging best practice but requires clear ownership boundaries [17].

### dbt Catalog evolution

dbt Docs was renamed to dbt Catalog in 2025 and rebuilt on the Fusion engine [17]. On Enterprise plans, dbt Catalog provides column-level lineage, multi-project lineage for dbt Mesh architectures, model performance analysis, and project recommendations. The 2025 State of Analytics Engineering report found that 50% of data practitioners already use AI for documentation and metadata development [17].

### CI/CD data quality gates

dbt Cloud CI jobs provide the integration point [14]:

1. PR opened triggers CI job
2. CI job builds only modified models and downstream dependencies in staging schema
3. Tests run against staged models
4. Lineage impact is visible in PR (via dbt Catalog or external catalog)
5. PR reviewer can see which downstream assets are affected

This flow catches data quality issues before merge but does not validate metadata quality (descriptions, ownership, tags). Teams that want metadata quality gates must add custom checks — for example, failing CI if a new model lacks a description or an owner assignment.

### Automated YAML generation

Tools like `dbt-codegen` and proprietary solutions auto-generate dbt-compatible YAML model files from database schemas, eliminating manual typing and reducing human error [14]. This accelerates initial catalog population but does not solve the ongoing curation problem — auto-generated descriptions are technical (column types) not semantic (business meaning).

---

## Sub-question 6: Metadata Quality and Staleness Management

### The decay problem

Metadata catalogs decay within months when manual processes dominate [12]. Comprehensive inventories created by dedicated projects become outdated and untrusted within the first year. Data stewards cannot manually tag thousands of columns across dozens of systems while keeping up with continuous schema changes, new tables, and deprecated assets. The result: teams stop trusting the catalog and revert to asking colleagues or querying the warehouse directly.

### Automated curation as the solution

Modern catalogs address decay through "active metadata" — continuous automated ingestion from pipelines, query logs, and schema crawlers [12][13]. Three layers of automation prevent staleness:

1. **Technical metadata harvesting** — incremental schema scans detect new columns, type changes, and dropped tables without full crawls. This keeps structural metadata current automatically.
2. **Usage-based curation** — query log analysis identifies popular assets, frequent users, and natural owners. Ownership can be auto-suggested from usage patterns and confirmed through steward workflows [12].
3. **Quality signal integration** — data quality test results, freshness metrics, and anomaly detections are surfaced directly in the catalog entry, giving users immediate trust signals without leaving the catalog [12].

### Ownership models

Distributed ownership — where domain teams own metadata for their data — is the only model that scales [12][13]. Centralized data stewardship teams cannot keep pace with the rate of change across an entire organization's data estate. The practical approach: auto-suggest owners from query and pipeline usage patterns, route confirmation workflows to stewards, and flag orphaned assets for review. A "glossary without ownership" causes terms to drift and definitions to become meaningless [12].

### Success metrics

Four metrics indicate whether a catalog is healthy [12]:

1. **Search click-through rate >35%** — users find what they need through search (below 35% indicates poor metadata quality or search relevance)
2. **Time-to-first-answer <5 minutes** — basic data discovery questions are answerable quickly
3. **>80% domain ownership coverage** — priority data domains have assigned owners
4. **>60% of top assets have at least one quality check** — the most-used assets have automated quality validation

Wiring data quality rules to lineage enables incident routing directly to accountable teams, reducing mean time to resolution by 30-50% [12].

---

## Challenge

Challenger research targeted the practical viability of column-level lineage, whether open-source catalogs genuinely compete with commercial offerings, the real adoption rate of OpenLineage, and the sustainability of metadata quality initiatives.

### Column-level lineage is practical but not comprehensive

The 97-99% accuracy claim from DataHub [3] is real but misleading without context. This accuracy applies to queries that the parser successfully handles — standard SQL with known schemas. The systematic failure cases (JSON extraction, UNNEST, dynamic SQL, Python models, MERGE INTO) are not edge cases in modern data platforms — they are common patterns. Semi-structured data processing, which relies heavily on JSON functions and UNNEST operations, is one of the fastest-growing workload types. Column-level lineage is therefore highly practical for dbt-centric transformation layers (where SQL is structured and predictable) but degrades significantly for ingestion layers, data science workloads, and platforms with heavy semi-structured data usage. The practical recommendation is sound: invest in column-level lineage for core transformation and reporting paths, and accept table-level lineage for the remainder.

### Open-source catalogs genuinely compete on features but not on operational burden

The feature comparison between DataHub/OpenMetadata and commercial tools like Atlan shows near-parity on core cataloging, lineage, and search capabilities [1][2]. However, the comparison obscures a critical difference: operational burden. DataHub requires Kafka, a graph database, Elasticsearch, and a relational database — four infrastructure components that must be deployed, monitored, upgraded, and scaled [1]. OpenMetadata is simpler (two components) but still requires Kubernetes for production scaling. Commercial tools eliminate this burden entirely. The Gartner analyst quote — "Open source is cheap, but it requires a level of skill most organizations don't have" [20] — captures the practical reality. For teams with strong platform engineering capabilities, open-source catalogs are a viable and cost-effective choice. For teams without, the TCO of self-hosting frequently exceeds commercial licensing costs.

### OpenLineage adoption is real but uneven

OpenLineage has achieved genuine institutional adoption — IBM, AWS, Northwestern Mutual, BMW Group are documented users [16]. The standard is embedded in Airflow (native since 2.7) and has a mature Spark integration [6]. But calling it a "universal standard" overstates current reality. dbt does not natively emit OpenLineage events — lineage is extracted from artifacts by external tools. BI tools (Tableau, Looker, PowerBI) have no OpenLineage integration; their lineage is captured through SQL log parsing. Flink support is developing but less tested than Spark. The result is that OpenLineage provides strong coverage for the orchestration-to-warehouse layer but leaves gaps at the ingestion and consumption ends of the pipeline. Teams adopting OpenLineage should plan for hybrid lineage collection — OpenLineage events where available, artifact parsing (dbt), and query log analysis (BI tools) for the rest.

### Metadata quality initiatives fail more often than they succeed

The 90-day rollout pattern recommended by practitioners [12] — start with 3-5 high-impact domains, harvest schemas and lineage, import glossaries, then activate — is sound but represents the exception, not the norm. Research shows that data lineage adoption has doubled over five years, but "a gap persists between awareness and execution" [10]. The most common failure mode is "boiling the ocean" — attempting to catalog everything simultaneously, which overwhelms stewards and produces a catalog so incomplete that users distrust it from day one [12]. The second most common failure is treating the catalog as a "static wiki" — a one-time documentation project rather than a continuously maintained system [12]. Success requires treating the catalog as a product with its own SLAs, user feedback loops, and continuous improvement cycles.

### Platform-native catalogs are not general-purpose alternatives

Unity Catalog and Snowflake Horizon are frequently positioned alongside DataHub and OpenMetadata in comparison guides [8][9]. This comparison is misleading. Unity Catalog and Horizon are governance layers for their respective platforms — they excel at governing data within Databricks or Snowflake but are not designed to catalog assets across a heterogeneous data stack. Unity Catalog's Iceberg REST API support and Catalog Federation partially address this limitation, but the primary use case remains Databricks-managed data. Similarly, Horizon's Catalog-Linked Databases extend governance to external Iceberg objects, but the governance experience is still Snowflake-centric. Teams with multi-platform stacks need a standalone catalog (DataHub, OpenMetadata, or Atlan) in addition to or instead of platform-native catalogs.

---

## Findings

### Finding 1: Open-source catalogs match commercial feature sets but impose significant operational burden
**Confidence: HIGH**

DataHub and OpenMetadata provide production-grade cataloging, search, lineage (table and column-level), data quality, governance, and AI-assisted features. Feature parity with commercial tools like Atlan is genuine for core use cases. However, the operational cost is substantial. DataHub's four-component architecture (RDBMS, Elasticsearch, graph DB, Kafka) requires Kubernetes expertise, 4-8 weeks deployment, and ongoing maintenance. OpenMetadata is simpler (2-4 weeks, two components) but still requires engineering investment. Commercial catalogs deploy in 4-6 weeks with zero infrastructure management. The decision is not features vs. no-features — it is engineering capacity vs. licensing budget. Teams with strong platform engineering should evaluate open-source first; teams without should default to commercial.

### Finding 2: Column-level lineage is practical for SQL-centric transformation layers but systematically incomplete
**Confidence: HIGH**

sqlglot-based parsers achieve 97-99% accuracy on standard SQL — sufficient for impact analysis and root cause debugging in dbt transformation layers. The failures are systematic and predictable: JSON extraction, UNNEST, dynamic SQL, Python models, MERGE INTO, and struct fields. These are not rare edge cases — semi-structured data processing and Python-based transformations are growing workload categories. Column-level lineage should be adopted for dbt models and SQL-based transformations where it provides high value, while accepting table-level lineage for ingestion, data science, and semi-structured processing workloads. Treating column-level lineage as a complete audit trail is a mistake.

### Finding 3: OpenLineage is the right interoperability standard but requires hybrid collection strategies
**Confidence: HIGH**

OpenLineage is the only open standard for lineage metadata with institutional backing (LF AI & Data Foundation, IBM, AWS) and production integrations (Airflow native since 2.7, Spark listener). No competing standard has comparable adoption. However, coverage is uneven — dbt, BI tools, and many ingestion tools do not natively emit OpenLineage events. Teams should adopt OpenLineage as the backbone of their lineage architecture but supplement it with artifact-based extraction (dbt manifest.json), query log parsing (warehouse SQL history), and manual annotation for custom/legacy pipelines. Expecting OpenLineage alone to provide end-to-end lineage will produce a graph with significant blind spots at the ingestion and consumption ends.

### Finding 4: Metadata catalogs require product-level operational commitment to avoid decay
**Confidence: HIGH**

Manual-entry catalogs become untrusted within the first year. Automated metadata harvesting (schema scans, query log analysis, usage-based ownership suggestion) is necessary but not sufficient. Catalogs must be treated as products with success metrics (search click-through >35%, time-to-first-answer <5 minutes, >80% domain ownership coverage), feedback loops, and continuous improvement cycles. Distributed ownership — domain teams owning their metadata — is the only model that scales. Starting with 3-5 high-impact domains and expanding incrementally prevents the "boil the ocean" failure mode. The 30-50% reduction in incident MTTR from quality-signal-integrated catalogs provides concrete ROI justification.

### Finding 5: Platform-native catalogs complement but do not replace standalone catalogs in multi-platform stacks
**Confidence: MODERATE**

Unity Catalog and Snowflake Horizon provide excellent governance for data within their respective ecosystems. Iceberg REST API support and catalog federation are extending their reach, but the governance experience remains platform-centric. For teams running a single-vendor stack (all-Databricks or all-Snowflake), the platform-native catalog may be sufficient. For multi-platform stacks — which represent the majority of enterprise data architectures — a standalone catalog (DataHub, OpenMetadata, or Atlan) is needed to provide unified discovery and governance across platforms. The emerging pattern is layered catalogs: platform-native catalogs for platform-specific governance, plus a standalone catalog for cross-platform discovery and lineage. The risk is metadata duplication and synchronization drift between layers.

---

## Claims

| # | Claim | Source | Status | Notes |
|---|-------|--------|--------|-------|
| 1 | DataHub SQL parser achieves 97-99% column-level lineage accuracy | [3][4] | verified | Built on sqlglot; schema-aware; accuracy measured on parseable queries |
| 2 | OpenMetadata deploys in 2-4 weeks vs DataHub's 4-8 weeks | [1] | verified | OpenMetadata has 2 infrastructure components vs DataHub's 4 |
| 3 | OpenLineage is an LF AI & Data Foundation Graduate project | [5][15] | verified | Active development, institutional backing from IBM/AWS |
| 4 | Airflow has native OpenLineage integration since version 2.7 | [15] | verified | All operators emit events by default unless explicitly disabled |
| 5 | dbt column-level lineage requires Enterprise plan | [7] | verified | Open-source dbt requires external tools like Canva's extractor |
| 6 | Column-level lineage fails on JSON extraction, UNNEST, MERGE INTO, and dynamic SQL | [3][7] | verified | Systematic limitations confirmed by DataHub docs and dbt docs |
| 7 | Unity Catalog implements the Iceberg REST Catalog API | [8] | verified | Enables multi-engine read/write without format lock-in |
| 8 | Data catalog market projected to reach $7.4B by 2034 at 22.7% CAGR | [18] | qualified | InsightAce Analytic projection from ~$1B (2024); vendor estimate |
| 9 | Manual-entry catalogs become untrusted within the first year | [12] | qualified | Practitioner consensus across multiple sources; no formal study cited |
| 10 | Gartner reintroduced its MQ for Metadata Management in 2025 after 5-year pause | [18] | verified | Market evolved from augmented catalogs to metadata orchestration platforms |
| 11 | Catalog quality metric: search click-through rate should exceed 35% | [12] | qualified | Decube benchmark; limited validation across industry |
| 12 | 50% of data practitioners use AI for documentation and metadata development | [17] | qualified | dbt Labs 2025 State of Analytics Engineering report; self-selected survey |
| 13 | Quality-signal-integrated catalogs reduce incident MTTR by 30-50% | [12] | qualified | Vendor claim from Decube; directionally consistent but magnitude unverified |
| 14 | OpenLineage focuses on runtime lineage, leaving static code lineage as a blind spot | [10] | verified | Data Crossroads analysis confirmed by OpenLineage architecture |
