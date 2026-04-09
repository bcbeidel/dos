---
name: {{name}}
artifact_type: pipeline-architecture
version: 1.0.0
owner: {{owner}}
status: draft
last_modified: {{date}}
sources:
  - {{source-name}}
---

# Pipeline Architecture: {{name}}

## Source Inventory

Sources and their ingestion approaches. Classifications and recommendations drawn from source evaluations where available.

| Source | Classification | Datasets | Ingestion Approach | Incremental Key | Freshness Requirement | Evaluation |
|--------|---------------|----------|-------------------|----------------|----------------------|------------|
| {{source-name}} | {{transactional DB / event stream / SaaS API / file-based}} | {{dataset list}} | {{full / incremental / CDC}} | {{column or N/A}} | {{e.g., 2 hours, daily}} | [evaluation](../../sources/{{source-name}}/evaluation.md) |

## Cross-Pipeline Dependencies

Models that join across staging domains introduce runtime dependencies on other pipelines. These must be explicitly ordered in the DAG or documented as first-time setup prerequisites.

| Model / Join | Upstream Pipeline | Ordering Guarantee | Notes |
|-------------|------------------|-------------------|-------|
| {{e.g., int_noaa__stations_enriched joins stg_zipcode__zip_codes}} | {{e.g., run_zipcode_pipeline}} | {{DAG dependency / schedule ordering / manual}} | {{e.g., zipcode runs 3rd, noaa runs 15th}} |

{{If no cross-pipeline dependencies: "No cross-pipeline dependencies identified. All staging models source from within this pipeline."}}

**First-time setup checklist:** Before running this pipeline in a new environment, ensure these upstream pipelines have completed at least once: {{list or "N/A"}}.

## Layering Strategy

**Approach:** {{medallion (Bronze/Silver/Gold) / 2-layer (staging+marts) / single-layer / domain-partitioned}}

**Rationale:** {{why this layering approach — number of sources, quality stages needed, platform, team size}}

### Layer Responsibilities

| Layer | Purpose | Storage Format | Key Transformations |
|-------|---------|---------------|-------------------|
| {{layer-name}} | {{what this layer does}} | {{Delta / Parquet / Iceberg / table}} | {{cleaning, dedup, joins, aggregations}} |

## Incremental Loading Patterns

### Per-Source Patterns

| Source | Pattern | Rationale | Lookback Window |
|--------|---------|-----------|----------------|
| {{source-name}} | {{full refresh / append / merge / delete+insert / microbatch}} | {{why this pattern for this source}} | {{e.g., 7 days, N/A}} |

### Silent Failure Modes

Document the failure modes specific to the selected patterns and the mitigation strategy for each.

| Source | Pattern | Failure Mode | Mitigation |
|--------|---------|-------------|------------|
| {{source-name}} | {{pattern}} | {{missed gaps / duplicate accumulation / full-table scans / non-replayable}} | {{monitoring, lookback windows, partition pruning, raw archival}} |

## Idempotency Strategy

Every pipeline must produce the same result if re-executed. Selected strategy per layer:

| Layer / Source | Strategy | Mechanism |
|---------------|----------|-----------|
| {{layer or source}} | {{DELETE+INSERT / MERGE/UPSERT / immutable append + dedup}} | {{transaction boundaries, key-based update, processing timestamps + window functions}} |

**Backfill design:** All pipelines accept a date parameter and process exactly that date's data. Parameterized date ranges, partition-aware processing, pre/post validation (row counts, checksums).

## Schema Evolution Approach

**Contract strictness:** {{evolve / freeze / discard_row / discard_value}}

**Change handling:**

| Change Type | Handling | Tool Support |
|-------------|----------|-------------|
| Add optional column | {{auto-evolve / expand-and-contract}} | {{dbt append_new_columns / dlt evolve / Delta mergeSchema}} |
| Rename column | {{expand-and-contract (treat as breaking)}} | {{manual migration}} |
| Type change | {{variant columns / fail and alert}} | {{dlt variant columns / dbt fail mode}} |
| Drop column | {{deprecation window then contract}} | {{dbt sync_all_columns / Delta DROP COLUMN}} |

**Monitoring:** {{schema diff on new batches, contract checks, DLQ for unexpected data}}

## Platform-Specific Considerations

**Target platform:** {{Databricks / Snowflake / DuckDB / ClickHouse / other}}

| Consideration | Detail |
|--------------|--------|
| {{native feature}} | {{how the platform supports or constrains the architecture — e.g., Delta Live Tables, Snowpipe, MergeTree}} |
| {{limitation}} | {{platform-specific constraint and workaround}} |

## Anti-Patterns Flagged

Review and confirm that the architecture avoids these common pitfalls:

| Anti-Pattern | Risk | Status |
|-------------|------|--------|
| **Premature streaming** | Building streaming when batch meets freshness needs. Costs 5-10x more. | {{not applicable / mitigated / flagged}} |
| **Over-normalization** | Complex dimensional models when consumers need simple wide-table queries. | {{not applicable / mitigated / flagged}} |
| **Universal SLAs** | Same SLA for every pipeline regardless of criticality. | {{not applicable / mitigated / flagged}} |

## Next Steps

Based on this pipeline architecture, the recommended next skills are:

1. **`/dos:implement-source`** -- Implement source ingestion based on the per-source patterns, incremental strategies, and schema evolution approach defined above.
2. **`/dos:implement-models`** -- Implement data models in the target layers using the modeling recommendation from the scope document and the layering strategy defined above.

## Changelog

| Date | Version | Change | Author |
|------|---------|--------|--------|
| {{date}} | 1.0.0 | Initial pipeline architecture | {{author}} |
