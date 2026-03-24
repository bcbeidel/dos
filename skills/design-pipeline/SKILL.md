---
name: design-pipeline
description: Architecture a data pipeline from source to serving layer. Produces a Pipeline Architecture document with per-source ingestion patterns, layering strategy, incremental loading with silent failure modes, idempotency strategy, schema evolution approach, and platform-specific considerations.
---

# dos:design-pipeline

Architecture a data pipeline from source to serving layer. Walk through source inventory, consumption-driven heuristics, layering selection, incremental pattern selection, idempotency design, schema evolution, and anti-pattern review -- producing a persistent Pipeline Architecture document.

## Preamble

Before starting, establish context:

1. **Which data product?** Ask the user for a data product name (e.g., `orders`, `customer-360`). This determines the artifact path: `docs/data-products/<name>/pipeline-architecture.md`.
2. **Check for existing artifact.** If `docs/data-products/<name>/pipeline-architecture.md` exists, read it, summarize the current state, and ask what's changing. Update the existing artifact rather than creating a new one.
3. **Check for scope document.** If `docs/data-products/<name>/scope.md` exists, load it. Extract: source inventory, freshness requirements, SLA tier, quality dimensions, and modeling recommendation. These pre-populate several workflow steps.
4. **Check for source evaluations.** If source evaluations exist in `docs/sources/`, list them. Load each referenced scorecard to pre-populate source classifications, ingestion approaches, dimension scores (especially freshness, schema stability, volume), and profiling baselines.

If the artifact exists, adjust the workflow: skip sections that haven't changed, focus on what the user wants to update, and bump the version in frontmatter.

## Workflow

### Step 1: Load Existing Context

If a pipeline architecture already exists, read it and ask the user what's changing. Common update scenarios:
- Adding a new source to an existing pipeline
- Changing the layering strategy
- Updating incremental patterns based on production experience
- Adjusting schema evolution approach after encountering drift

If updating, skip unchanged sections and focus on the delta.

### Step 2: Source Inventory

If a scope document exists, load the source inventory from it. For each source, also load the source evaluation scorecard from `docs/sources/<source-name>/evaluation.md` if available. Pre-populate:
- Source classification (transactional DB, event stream, SaaS API, file-based)
- Ingestion approach recommendation
- Freshness score and requirement
- Schema stability score
- Volume characteristics

If no scope document exists, ask the user which sources this pipeline will consume. For each source, gather:
- Source name and type
- Datasets to ingest
- Approximate volume and change rate
- Freshness requirement
- Whether hard deletes must be tracked

### Step 3: Gather Missing Consumption Requirements

If not already captured in the scope document, gather the three consumption dimensions:

- **Query shape:** What is the dominant query pattern? (join-heavy, scan-heavy, entity lookup, ad-hoc)
- **Freshness:** What is the required data freshness in specific time units? ("What business decision changes if the data is 5 minutes old instead of 5 seconds old?")
- **SLA tier:** Is this prototype or production-grade? What is the consumer dependency?

Refer to [consumption-to-architecture.md](references/consumption-to-architecture.md) for the full decision tables.

### Step 4: Apply Consumption-Driven Heuristics

Using the three consumption dimensions, derive architecture defaults:

Refer to [consumption-to-architecture.md](references/consumption-to-architecture.md) for heuristic mappings.

| Dimension | Input | Architecture Default |
|-----------|-------|---------------------|
| Query shape | {{dominant pattern}} | {{modeling recommendation}} |
| Freshness | {{quantified need}} | {{ingestion strategy}} |
| SLA tier | {{prototype / production-grade}} | {{pipeline investment level}} |

Present the derived defaults to the user. These are strong defaults, not final decisions -- the user may override based on constraints not captured by the heuristics (e.g., team familiarity, existing infrastructure, budget).

### Step 5: Select Layering Strategy

Choose the data layering approach based on the number of sources, quality requirements, platform, and team size.

Refer to [layering-strategy.md](references/layering-strategy.md) for medallion pattern details, alternatives, and platform differences.

Decision framework:

| Condition | Recommended Layering |
|-----------|---------------------|
| Multiple sources, quality stages needed, Databricks | Medallion (Bronze/Silver/Gold) |
| Single source, clean data, minimal transformation | 2-layer (staging + marts) or single-layer |
| Multiple business domains with independent ownership | Domain-partitioned |
| Already clean data, low volume | Direct / OneBigTable |

For each selected layer, define:
- Purpose and responsibility
- Storage format
- Key transformations applied

### Step 6: Select Incremental Loading Pattern per Source

For each source, select the incremental loading pattern based on source characteristics.

Refer to [incremental-patterns.md](references/incremental-patterns.md) for the five patterns, selection framework, and tool support.

For each source, determine:
- Which pattern fits (full refresh, append, merge, delete+insert, microbatch)
- The incremental key (timestamp column, sequence, or N/A)
- Lookback window for late-arriving data
- Tool implementation (dbt materialization, dlt write disposition, Delta MERGE)

**Surface silent failure modes.** For each selected pattern, identify the applicable failure modes and define mitigations:

| Failure Mode | Applies When | Mitigation |
|-------------|-------------|------------|
| Missed gaps | Cursor-based incremental with unreliable timestamps | Row count reconciliation, gap detection queries |
| Duplicate accumulation | Append pattern with late-arriving data | Output-range filtering, deduplication at read time |
| Full-table scans | Merge without partition pruning | Partition on date, add lookback window (e.g., 7 days) |
| Non-replayable sources | API rate limits, deleted records, ephemeral streams | Archive raw responses, store extraction metadata |

### Step 7: Ensure Idempotency by Design

Every pipeline must produce the same result when re-executed. Select the idempotency strategy per layer/source.

Refer to [incremental-patterns.md](references/incremental-patterns.md) for the three idempotency strategies.

| Strategy | Best For |
|----------|---------|
| DELETE+INSERT within transaction | Atomicity, non-unique keys, partition-level reprocessing |
| MERGE/UPSERT on key | Stateful records, dimension updates |
| Immutable append + read-time dedup | Event streams, high-write throughput |

Additionally, ensure:
- Every pipeline accepts a date parameter and processes exactly that date's data
- Backfill is supported from day one: parameterized date ranges, partition-aware processing
- Pre/post validation: row counts, checksums, record count reconciliation

### Step 8: Define Schema Evolution Approach

Select the contract strictness level and define how schema changes will be handled.

Refer to [schema-evolution-patterns.md](references/schema-evolution-patterns.md) for compatibility rules, the expand-and-contract pattern, and tool-specific behavior.

Decisions to make:
- **Contract strictness:** `evolve` for development, `freeze` or `discard_row` for production
- **Non-breaking changes** (add optional column): auto-evolve or expand-and-contract
- **Breaking changes** (rename, type change, drop required): always expand-and-contract
- **Monitoring:** schema diff on new batches, contract checks, DLQ for unexpected data

Factor in the schema stability scores from source evaluations. Sources scoring 1-2 on schema stability require defensive design: stricter contracts, quarantine layers, more frequent monitoring.

### Step 9: Flag Platform-Specific Considerations

Based on the target platform, surface relevant capabilities and constraints.

Refer to [layering-strategy.md](references/layering-strategy.md) for platform differences.

| Platform | Key Capabilities | Key Constraints |
|----------|-----------------|----------------|
| Databricks | Delta Live Tables, Auto Loader, Unity Catalog, MERGE WITH SCHEMA EVOLUTION | Schema updates terminate active streams |
| Snowflake | Snowpipe/Streaming, Tasks/Streams for CDC, SQL ELT | No explicit medallion tooling |
| DuckDB | Fast local analytics, Parquet/CSV native | Single-node, no streaming |
| ClickHouse | MergeTree family, Incremental MVs, Refreshable MVs | ReplacingMergeTree is eventually consistent (requires FINAL) |

Surface any platform-specific constraints that affect the architecture decisions made in earlier steps.

### Step 10: Flag Anti-Patterns

Review the architecture against three common anti-patterns:

Refer to [consumption-to-architecture.md](references/consumption-to-architecture.md) for anti-pattern descriptions.

1. **Premature streaming** -- Is the architecture using streaming when batch or micro-batch meets the validated freshness requirement? Streaming costs 5-10x more to build and operate.
2. **Over-normalization** -- Is the architecture building complex dimensional models when consumers run simple queries that a wide table would serve better? Let the query pattern dictate the model.
3. **Universal SLAs** -- Is the same SLA applied to every source and layer regardless of criticality? Tiered SLAs (critical/standard/best-effort) allocate engineering effort proportionally.

For each anti-pattern, explicitly mark it as "not applicable," "mitigated," or "flagged" with explanation. If flagged, propose the correction before generating the architecture document.

### Step 11: Generate Architecture Document

Produce the Pipeline Architecture document using the template structure from [pipeline-architecture-template.md](assets/pipeline-architecture-template.md).

Save to `docs/data-products/<name>/pipeline-architecture.md` with:
- Complete YAML frontmatter (name, artifact_type, version, owner, status, last_modified, sources)
- All sections populated from the workflow above
- Silent failure modes documented per source pattern
- Anti-pattern review completed
- Changelog entry recording the architecture session

If updating an existing artifact:
- Bump the minor version
- Update `last_modified`
- Add a changelog entry describing what changed

### Next Steps

End the architecture document with a "Next Steps" section recommending downstream skills:

1. **`/dos:implement-source`** -- Implement source ingestion based on the per-source patterns, incremental strategies, and schema evolution approach defined in the architecture.
2. **`/dos:implement-models`** -- Implement data models in the target layers using the modeling recommendation from the scope document and the layering strategy defined in the architecture.

Present these options to the user and explain what each downstream skill will do with the architecture decisions.
