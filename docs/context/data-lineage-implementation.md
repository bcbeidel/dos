---
name: "Data Lineage Implementation"
description: "OpenLineage is the de facto interoperability standard but requires hybrid collection strategies; column-level lineage achieves 97-99% accuracy on standard SQL but systematically fails on JSON extraction, UNNEST, dynamic SQL, and Python models; automated extraction covers 70-85% of data flows"
type: context
related:
  - docs/context/data-catalog-selection.md
  - docs/context/ci-cd-pipeline-design.md
  - docs/research/2026-03-22-data-catalog-lineage.research.md
---

## Key Insight

OpenLineage is the right interoperability standard for lineage metadata, but expecting it alone to provide end-to-end lineage produces a graph with significant blind spots. Airflow and Spark have mature integrations; dbt, Flink, and BI tools do not natively emit OpenLineage events. Column-level lineage is highly practical for dbt-centric SQL transformations (97-99% accuracy) but degrades on semi-structured data, dynamic SQL, and Python models. Plan for hybrid collection: OpenLineage events where available, artifact parsing for dbt, query log analysis for BI tools, and manual annotation for the rest.

## OpenLineage Standard

OpenLineage is an LF AI & Data Foundation Graduate project defining an open spec for lineage metadata. It models three core entities -- **Jobs**, **Runs**, and **Datasets** -- connected by events emitted at job start, completion, and failure. Column-level lineage is implemented as a Dataset Facet. Marquez is the reference implementation, but DataHub, OpenMetadata, Atlan, and IBM watsonx.data all accept OpenLineage events.

### Integration Maturity

| Tool | Level | Notes |
|------|-------|-------|
| Apache Airflow | Mature (native) | Built-in since 2.7; all operators emit events by default |
| Apache Spark | Mature | SparkListener captures inputs, outputs, schemas, execution plans |
| dbt | Partial | Lineage from manifest.json artifacts, not native OpenLineage events |
| Apache Flink | Developing | Supported but less battle-tested than Spark |
| Dagster | Supported | Native integration available |
| BI tools (Tableau, Looker, PowerBI) | Limited/None | Lineage via SQL query log parsing only |

### Fundamental Coverage Gap

OpenLineage focuses on **runtime lineage** -- events emitted during job execution. This leaves blind spots for static code, rarely-executed pipelines, and ad hoc queries. Tools that run infrequently may never emit lineage events, creating invisible gaps.

## Column-Level vs. Table-Level Lineage

**Table-level lineage** tracks which tables feed which other tables. Coverage approaches 100% because the information is structurally present in every SQL query and dbt's manifest.json.

**Column-level lineage** tracks which source columns map to which target columns, including transformations. DataHub's sqlglot-based parser achieves 97-99% accuracy on standard SQL across 20+ dialects. This measures accuracy on successfully parsed queries, not on all SQL a production platform encounters.

### Systematic Failure Cases

- **JSON extraction** (json_extract, JSON_VALUE, GET_PATH) -- cannot trace through semi-structured access
- **UNNEST / lateral joins** -- flattening creates ambiguous column origins
- **MERGE INTO** -- column-level lineage not generated
- **Dynamic SQL / identifier() functions** -- references resolved at runtime, not parseable statically
- **Python dbt models** -- no SQL to parse
- **Struct fields** -- best-effort resolution, not guaranteed
- **SELECT * expansion** -- requires accurate catalog schemas; stale schemas break lineage silently

Column-level lineage is reliable for **impact analysis** and **root cause debugging** on SQL transformation patterns. It is not reliable for **audit** (proving exact provenance of every value) or in environments heavy on semi-structured data and Python transformations.

## Automated Lineage Extraction

**dbt artifacts:** manifest.json provides the complete table-level DAG via ref()/source() declarations. Column-level lineage requires SQL parsing of model code -- dbt Cloud Enterprise provides this natively; for open-source dbt, Canva's dbt-column-lineage-extractor uses sqlglot.

**Spark:** OpenLineage's SparkListener captures input/output datasets, schemas, and execution plans. Works across Databricks, EMR, and Dataproc.

**SQL query log parsing:** Catalogs parse warehouse query history for table-level lineage outside dbt/Spark.

### Coverage Blind Spots

Common gaps:

1. Custom scripts and legacy ETL outside the SQL-parseable ecosystem
2. Cross-system transformations through APIs, message queues, or file transfers
3. Ad hoc analyst queries not running through instrumented pipelines
4. Semantic transformations in BI tools (Tableau calculated fields, Looker LookML)

Teams should expect automated lineage to cover 70-85% of data flows and plan for manual annotation of the remainder.

## Metadata Source of Truth

Three patterns exist: **dbt-first** (descriptions/owners/tags in schema.yml, ingested by catalog -- version-controlled but engineer-only), **catalog-first** (business users curate in catalog UI, changes pushed to dbt via automated PRs -- accessible but sync-complex), and **hybrid** (technical metadata in dbt, business metadata in catalog -- emerging best practice, requires clear ownership boundaries). dbt Cloud CI jobs can validate lineage impact on PRs but do not validate metadata quality without custom checks.

## Takeaway

Adopt OpenLineage as the backbone of lineage architecture but supplement with artifact-based extraction (dbt), query log parsing (warehouses), and manual annotation (legacy/custom). Invest in column-level lineage for core transformation and reporting paths where it provides high value. Accept table-level lineage for ingestion, data science, and semi-structured processing workloads. Treating column-level lineage as a complete audit trail is a mistake.
