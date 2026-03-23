---
name: dos Skill Library Design
description: "Nine foundational skills organized as Discover-Scope-Design-Build-Verify workflow, operating on living data product artifacts stored in docs/data-products/. Skills follow the Agent Skills spec (portable core) with Claude Code extensions. Artifacts are human-readable markdown with YAML frontmatter, evolving over time as specifications that drive code generation."
type: design
related:
  - docs/plans/2026-03-21-data-pipeline-research-context.plan.md
  - docs/research/2026-03-22-skill-design.research.md
  - docs/context/agentic-phase-patterns.md
  - docs/context/deterministic-gates-hooks.md
  - docs/context/cross-provider-skill-portability.md
  - docs/context/data-engineering-lifecycle-model.md
---

# dos Skill Library Design

## Overview

The dos skill library provides guided workflows for data engineering practitioners — solo engineers and small teams who handle both architecture decisions and implementation. Nine foundational skills (Tier 1) cover the full lifecycle from source discovery through pipeline implementation to operational review. Skills operate on living artifacts that persist in the repository, evolve over time, and serve as executable specifications that drive code generation.

## Design Principles

### Skills Are CRUD Operators, Not One-Shot Generators

Each skill checks for existing artifacts before starting. If the artifact exists, the skill reads current state, asks what's changing, and updates the delta. If it doesn't exist, the skill walks through the creation flow. There is no separate "new mode" vs. "change mode" — the artifact's presence determines behavior.

### Artifacts Are Living Specifications

Data product artifacts persist in `docs/data-products/<name>/` and evolve over time. They are:

- **Human-readable first** — a product manager can review a quality config and understand the thresholds
- **Machine-parseable second** — structured enough that skills can read and update them
- **The source of intent** — the formal implementation lives in code; these documents define what the code should do

Format: Markdown with YAML frontmatter. Frontmatter carries metadata skills need (version, owner, status, last_modified). Body carries structured content (tables, lists) and narrative explanation.

### Portable Core, Claude Code Extensions

Skills follow the Agent Skills open standard for cross-provider compatibility (Claude Code, GitHub Copilot, Cursor, OpenAI Codex, Gemini CLI). Provider-specific features (hooks, subagent configs) are layered on top via SKILL.md frontmatter and `scripts/` — they enhance but are not required.

### Curated Knowledge, Not Runtime Dependencies

Each skill embeds the decision frameworks, criteria, and guidance it needs — distilled from the `docs/context/` corpus into focused `references/` files. Context files are authoring inputs, not runtime dependencies. A skill must work without access to `docs/context/`.

## Skill Architecture

### Directory Structure

```
skills/
  evaluate-source/          # Invoked as /dos:evaluate-source (plugin adds namespace)
    SKILL.md                # <500 lines, portable Agent Skills spec
    references/             # Curated knowledge, loaded on demand via relative links
      six-dimension-framework.md
      source-classification-matrix.md
    assets/                 # Output templates, static resources
      source-scorecard.md
    scripts/                # Deterministic validation (shell/python scripts)
      profile-sample.py
```

Directory names omit the `dos-` prefix because the plugin system (`plugin.json` `name: "dos"`) automatically namespaces skills as `dos:<directory-name>`. The SKILL.md `name` field uses lowercase letters, numbers, and hyphens only (no colons) per the Agent Skills spec.

### SKILL.md Conventions

- **Frontmatter**: Only base Agent Skills spec fields for portability (`name`, `description`). Claude Code extensions (`hooks`, `allowed-tools`) added as a separate layer.
- **Size**: Under 500 lines with progressive disclosure to `references/` files.
- **References**: Loaded via relative markdown links from SKILL.md body. Each reference file is focused, under 200 lines, and contains only what the specific skill needs.
- **Preamble check**: Every skill starts by asking which data product the user is working on, checking for existing artifacts, and adjusting behavior accordingly.
- **Next steps**: Every skill's output artifact ends with a "Next Steps" section suggesting the natural downstream skill(s).

### Artifact Conventions

Sources and data products are distinct entities with independent lifecycles. Source evaluations live in `docs/sources/` and are reusable across data products. Data product artifacts live in `docs/data-products/` and reference sources.

```
docs/
  sources/                          # Independent source evaluations
    postgres-orders-db/
      evaluation.md                 # From dos:evaluate-source (one per source)
    stripe-api/
      evaluation.md
  data-products/                    # Data product specifications
    orders/
      scope.md                      # From dos:scope-data-product (references sources)
      contract.md                   # From dos:define-contract (ODCS-aligned)
      quality-config.md             # From dos:assess-quality
      pipeline-architecture.md      # From dos:design-pipeline
      reviews/                      # From dos:review-pipeline (append-only)
        2026-03-23-review.md
```

A source evaluation assesses a source system's characteristics — connectivity, auth, schema stability, per-dataset profiling. A data product's scope document declares which sources it consumes. This is a many-to-many relationship: one source can feed multiple data products, and one data product can consume multiple sources.

Every artifact includes YAML frontmatter with:

```yaml
---
name: postgres-orders-db           # Source name (sources) or product name (data products)
artifact_type: source-evaluation   # | scope | contract | quality-config | pipeline-architecture
version: 1.0.0
owner: analytics-engineering
status: active                     # | draft | deprecated
last_modified: 2026-03-23
---
```

Every artifact includes a changelog section at the bottom tracking evolution.

### Artifact Versioning and Concurrency

Git is the concurrency and versioning mechanism. Skills update `last_modified` and `version` in frontmatter as part of their update flow. Version bumping rules are artifact-specific:

- **Contracts** follow semantic versioning: additive changes (new column) → minor bump, breaking changes (removed column, type change) → major bump with expand-contract pattern.
- **Quality configs, scope documents, source evaluations** use simple incrementing versions. Any substantive change bumps the minor version.
- **Pipeline architecture** documents are versioned but changes are typically documented in the changelog rather than requiring formal versioning.

Concurrent updates are handled by git merge. Since artifacts are structured markdown, merge conflicts surface as text conflicts that the user resolves normally. Skills do not attempt locking or conflict detection beyond git.

### Build-Phase Skills: Code Output Pattern

Build-phase skills (`dos:implement-source`, `dos:implement-models`) produce code files, not markdown artifacts. They follow a different preamble pattern than Design-phase skills:

1. Read the relevant specification artifacts (contract, quality config, pipeline architecture).
2. Check if implementation code already exists (dbt models, dlt pipelines) for this data product.
3. If code exists, diff the specification artifacts against the current code and propose updates to align them.
4. If no code exists, generate from the specification artifacts.

To maintain traceability, Build-phase skills update the specification artifacts they consumed — setting the `status` field to indicate implementation state and noting the generated file paths in the changelog.

### Iteration Bounds

Skills must not enter unbounded retry loops. When a skill's output fails validation or the user requests changes:

- **Cap at 3-5 iterations** per step. If the skill cannot produce valid output (e.g., dbt models that pass linting) within this bound, surface the failure to the user with diagnostics rather than retrying.
- **Loop detection**: If three consecutive iterations produce >90% similar output, the problem exceeds the skill's capability — stop and explain what's blocking progress.

### Upstream Artifact Validation

Build-phase skills must deterministically validate that input artifacts are parseable and structurally complete before starting LLM-based code generation. Before any creative work:

1. Verify the artifact file exists and has valid YAML frontmatter.
2. Verify required sections are present (e.g., a contract must have a schema section before `implement-models` can generate code).
3. If validation fails, report what's missing with specific field names and suggest which skill to run to fix it.

This prevents wasted LLM work on incomplete inputs and provides clear self-correction signals.

### Validation Scripts

`scripts/` contains deterministic checks that run as Claude Code hooks or standalone. Scripts are shell or Python, return exit code 0 (pass) or 2 (blocking error), and output structured error messages with specific location, expected-vs-found, and available alternatives for agent self-correction.

Shared project-level validation (linting, formatting) lives at `.claude/hooks/`. Per-skill validation lives in the skill's `scripts/` directory and is wired via SKILL.md frontmatter hooks.

## Tier 1: Nine Foundational Skills

### Lifecycle Phases

```
  Discover          Scope           Design            Build         Verify
┌──────────┐   ┌───────────┐   ┌──────────────┐   ┌──────────┐   ┌────────┐
│ evaluate  │──▶│ scope     │──▶│ select-model │   │implement │   │ review │
│ -source   │   │ -data-    │   │ define-      │──▶│ -source  │──▶│-pipeline│
│           │   │  product  │──▶│  contract    │   │ (EL)     │   │        │
│           │   │           │   │ assess-      │   ├──────────┤   │        │
│           │   │           │──▶│  quality     │──▶│implement │──▶│        │
│           │   │           │   │ design-      │   │ -models  │   │        │
│           │   │           │──▶│  pipeline    │──▶│ (T)      │   │        │
└──────────┘   └───────────┘   └──────────────┘   └──────────┘   └────────┘
```

This diagram shows the primary flow path. The full dependency graph is in the Artifact Chaining table below — additional edges exist (e.g., scope → implement-models, assess-quality → implement-models) that are omitted here for clarity.

Each skill is independently usable. When chained, downstream skills consume upstream artifacts to skip redundant questions and pre-populate known facts.

---

### 1. `dos:evaluate-source`

**Phase:** Discover
**Purpose:** Assess a data source's technical characteristics before pipeline construction.
**Output:** Source Evaluation Scorecard (`docs/sources/<source-name>/evaluation.md`)

**Workflow:**

1. Apply intake filtering — ask the two qualifying questions before deep assessment: "What decision will you make with this data?" and "What is the real problem you're trying to solve?" If the request lacks a concrete use case, flag it before investing in full evaluation.
2. Gather source metadata — type, ownership, format, location
3. Classify source type (transactional DB, event stream, SaaS API, file-based)
4. Score across six dimensions:
   - Connectivity — how the source exposes data (JDBC, REST, stream, file, webhook)
   - Volume — data size at rest and change rate (use 95th percentile, not averages)
   - Freshness — update frequency and reliable timestamp availability
   - Schema stability — change frequency and notification process over past 6-12 months
   - Data quality — baseline across DAMA dimensions from profiling
   - Access complexity — auth mechanism, rate limits, IP restrictions, token refresh
5. Document authentication mechanism (OAuth M2M, API key, service account, key-pair, JDBC credentials)
6. Assess credential management — where secrets live, rotation cadence, anti-patterns (static PATs, shared credentials)
7. Profile sample data if provided:
   - Structure profiling — column names, types, field lengths, naming consistency
   - Content profiling — null rates, distinct counts, uniqueness ratios, min/max, numeric distribution (mean, stddev, percentiles, IQR, skewness), pattern frequencies
   - Relationship profiling — key candidates, referential integrity, orphan detection (if multi-table)
   - Map profiling results to quality dimension baselines
8. Recommend ingestion approach (full load, incremental, CDC) based on classification and dimension scores. Note: dlt is a polling tool, not CDC — if log-based CDC is needed, recommend Debezium or platform-native CDC.
9. Note profiling baseline date and recommend re-profiling cadence based on schema stability score (high drift = monthly, stable = quarterly). Profiling is continuous, not one-time.
10. Generate scorecard with "Next Steps" suggesting `dos:scope-data-product`

**Curated references (distilled from context corpus):**

| Reference File | Source Context Files |
|---|---|
| `six-dimension-framework.md` | source-system-evaluation, schema-drift-risk |
| `source-classification-matrix.md` | source-system-evaluation, incremental-loading-patterns |
| `access-auth-patterns.md` | secrets-management-rotation, secrets-environment-management |
| `profiling-metrics.md` | data-profiling |

**Scripts:**

| Script | Purpose |
|---|---|
| `profile-sample.py` | Accepts CSV/JSON/Parquet, computes core profiling metrics (completeness, uniqueness, numeric distribution, key candidates), outputs structured markdown tables. Lightweight — Python stdlib + DuckDB. |

---

### 2. `dos:scope-data-product`

**Phase:** Scope
**Purpose:** Define what a data product needs to be, driven by consumption intent.
**Input:** Source Evaluation Scorecards from `docs/sources/` (optional — pre-populates known facts for one or more sources)
**Output:** Data Product Scope Document (`docs/data-products/<name>/scope.md`)

**Workflow:**

1. If source scorecards exist in `docs/sources/`, ask which sources this data product will consume. Load each referenced scorecard. Pre-populate source classifications, profiling baselines, ingestion recommendations. A data product may consume multiple sources — the scope document records which sources and datasets are in play.
2. Walk through the Data Product Canvas blocks in consumption-first order: Consumers/Use Cases → Data Contract → Sources → Architecture → Domain → Ubiquitous Language → Classification. Start from what consumers need, work backward to what sources provide.
3. Interrogate intended use cases — "What decisions will be made with this data?" Supplement stated requirements with empirical evidence: review actual dashboards, SQL queries, or query logs (BigQuery INFORMATION_SCHEMA.JOBS, Snowflake QUERY_HISTORY) to understand how data is actually consumed vs. how stakeholders say it is consumed.
4. Identify consumers and their query patterns (join-heavy, scan-heavy, entity lookup, ad-hoc)
5. Quantify freshness requirements in specific time units (not adjectives). Ask: "What business decision changes if the data is 5 minutes old instead of 5 seconds old?"
6. Classify SLA tier — prototype (no SLA, re-run on failure) vs. production-grade (formal SLA, error budgets)
7. Apply consumption-driven heuristics:
   - Query shape → modeling recommendation
   - Freshness need → ingestion strategy
   - SLA tier → pipeline investment level
8. Select initial quality dimensions and derive thresholds from profiling baselines + consumption tolerances
9. Define initial SLA dimensions (timeliness + completeness as minimum). Use SLI/SLO/SLA hierarchy: define the indicator first, set the objective, then negotiate the agreement.
10. Apply MoSCoW prioritization if multiple consumers have competing requirements
11. Generate scope document with explicit "Won't have in v1" section
12. Suggest next skills: `dos:select-model`, `dos:define-contract`, `dos:assess-quality`, `dos:design-pipeline`

**Curated references:**

| Reference File | Source Context Files |
|---|---|
| `consumption-heuristics.md` | consumption-driven-architecture |
| `interview-questions.md` | requirements-gathering-techniques |
| `sla-hierarchy.md` | data-freshness-slas, data-quality-slas |
| `quality-dimension-selection.md` | data-quality-dimensions |

---

### 3. `dos:select-model`

**Phase:** Design
**Purpose:** Guide the user through choosing a data modeling approach (Kimball, Data Vault, OBT).
**Input:** Data Product Scope Document (optional — pre-populates query pattern and platform)
**Output:** Modeling decision persisted to scope document (updates the modeling recommendation section)

**Workflow:**

1. If scope document exists, extract query pattern, platform, team size, compliance needs.
2. Gather any missing constraints: team size, source count, compliance needs, dominant query pattern, target platform, change velocity.
3. Apply decision matrix:
   - Kimball: default for any team, mixed analytics, all platforms
   - Data Vault: 5+ engineers, 5+ sources with frequent changes, regulated environments
   - OBT: simple flat queries, few stable sources, BigQuery/Databricks with Liquid Clustering
4. Surface platform-specific guidance (DuckDB joins are cheap; Snowflake separates storage/compute; Databricks optimization > model choice; ClickHouse favors star schema).
5. Flag counter-evidence (Fivetran OBT benchmarks, semantic layer implications).
6. Deliver recommendation with reasoning. Update scope document modeling section (always persist — conversational-only output breaks the artifact chain).
7. Suggest next skills: `dos:define-contract`, `dos:implement-models`

**Curated references:**

| Reference File | Source Context Files |
|---|---|
| `model-decision-matrix.md` | data-model-selection |
| `platform-modeling-guidance.md` | data-model-selection, kimball-dimensional-modeling, obt-wide-table-patterns, data-vault-modeling |

---

### 4. `dos:define-contract`

**Phase:** Design
**Purpose:** Define or evolve a data contract for a data product.
**Input:** Data Product Scope Document (optional — pre-populates SLAs, quality dimensions, consumers)
**Output:** Data contract (`docs/data-products/<name>/contract.md`)

**Workflow:**

1. If contract exists, read it, summarize current state, ask what's changing.
2. If scope document exists, pre-populate consumers, SLAs, quality dimensions.
3. Define or update schema — objects, properties, types, constraints.
4. Define or update quality rules per property (from quality dimensions in scope).
5. Define or update SLAs — freshness, availability, retention.
6. Define ownership, support channels, escalation paths.
7. Apply versioning:
   - Additive changes (new column, relaxed constraint) → minor version bump
   - Breaking changes (removed column, type change, tightened constraint) → major version bump with expand-contract pattern
8. Define enforcement strategy across three layers:
   - **CI-time**: breaking change detection via `dbt state:modified+` comparison
   - **Build-time**: schema validation via dbt contract preflight (`contract: { enforced: true }`)
   - **Runtime**: data quality and SLA checks via Soda/Great Expectations or dbt tests
9. Generate ODCS v3.1-aligned contract document covering all 11 sections (Fundamentals, Schema, References, Data Quality, Support, Pricing, Team, Roles, SLA, Infrastructure, Custom Properties).
10. Optionally generate dbt contract configuration snippet (`contract: { enforced: true }`, column definitions).
11. Suggest next skills: `dos:assess-quality`, `dos:implement-models`

**Curated references:**

| Reference File | Source Context Files |
|---|---|
| `odcs-structure.md` | data-contract-structure, data-contracts |
| `enforcement-layers.md` | data-contract-enforcement-versioning |
| `versioning-patterns.md` | data-contract-enforcement-versioning, schema-evolution |

---

### 5. `dos:assess-quality`

**Phase:** Design
**Purpose:** Set up or update quality engineering for a data product.
**Input:** Data Product Scope Document and/or contract (optional — pre-populate dimensions and thresholds)
**Output:** Quality configuration (`docs/data-products/<name>/quality-config.md`)

**Workflow:**

1. If quality config exists, read it, summarize current state, ask what's changing.
2. If scope or contract exists, pre-populate quality dimensions and initial thresholds.
3. Select relevant quality dimensions (from six-dimension consensus, extend as needed).
4. Define measurement methods and thresholds per dimension.
5. Choose scoring method — test fail rate (binary per test) vs. failed row count (proportion of affected rows). Recommend failed row count for finer granularity.
6. Assign weights (business-driven, stakeholders must participate).
7. Define action thresholds (green/yellow/red) with assigned owners per threshold breach.
8. Recommend validation tooling by tier:
   - Local: Pandera + pytest
   - CI: dbt data tests + dbt-expectations
   - Production: Soda / Great Expectations
9. Recommend anomaly detection approach based on data characteristics (rule-based for known constraints, statistical for distributions, ML only at scale).
10. Generate quality configuration artifact.
11. Suggest next skills: `dos:implement-models`, `dos:define-contract` (if contract doesn't include quality rules yet)

**Curated references:**

| Reference File | Source Context Files |
|---|---|
| `quality-dimensions.md` | data-quality-dimensions |
| `scoring-methods.md` | data-quality-scoring |
| `sla-error-budgets.md` | data-quality-slas, data-freshness-slas |
| `validation-tiers.md` | tiered-validation-strategy, data-validation-tool-comparison |
| `anomaly-methods.md` | anomaly-drift-detection |

---

### 6. `dos:design-pipeline`

**Phase:** Design
**Purpose:** Architecture a data pipeline from source to serving layer.
**Input:** Source Evaluation Scorecards from `docs/sources/` and/or Data Product Scope Document (optional)
**Output:** Pipeline architecture document (`docs/data-products/<name>/pipeline-architecture.md`)

**Workflow:**

1. If pipeline architecture exists, read it, ask what's changing.
2. If scope exists, identify referenced sources and load their scorecards from `docs/sources/`. Pre-populate source classifications, ingestion approaches, freshness requirements, SLA tier. If no scope exists but scorecards are available, ask which sources to design for.
3. Gather any missing consumption requirements: query shape, freshness, SLA tier.
4. Apply consumption-driven heuristics to derive architecture decisions.
5. Select layering strategy:
   - Medallion (Bronze → Silver → Gold) when: multiple consumers, different quality tiers, need raw data preservation
   - Simpler (staging → marts) when: single consumer, straightforward transformations
6. Select incremental loading pattern (full refresh, append, merge, delete+insert, microbatch). For each pattern, surface the specific silent failure modes:
   - Append: duplicate accumulation if source replays events
   - Merge: full-table scan on large tables without partition pruning
   - Delete+insert: non-atomic — partial tables visible during execution
   - Microbatch: gaps if batches overlap or skip time ranges
7. Ensure idempotency by design — every pipeline must produce the same result if re-executed. Three strategies: delete+insert with transaction wrapping, merge/upsert on primary key, or immutable append with downstream deduplication.
8. Define schema evolution approach (additive-only, expand-contract, tool-specific handling for dbt/dlt/Delta).
9. Flag platform-specific considerations.
10. Flag three anti-patterns: premature streaming, over-normalization, universal SLAs.
10. Generate architecture document.
11. Suggest next skills: `dos:implement-source`, `dos:implement-models`

**Curated references:**

| Reference File | Source Context Files |
|---|---|
| `consumption-to-architecture.md` | consumption-driven-architecture |
| `incremental-patterns.md` | incremental-loading-patterns |
| `layering-strategy.md` | medallion-architecture |
| `schema-evolution-patterns.md` | schema-evolution |

---

### 7. `dos:implement-source`

**Phase:** Build (EL)
**Purpose:** Generate dlt pipeline code and dbt source definitions from data product artifacts.
**Input:** Source Evaluation Scorecard from `docs/sources/<source>/` (required), pipeline architecture (optional), contract (optional)
**Output:** dlt pipeline code + dbt source YAML in the project codebase

**Workflow:**

1. Ask which source to implement. Read its evaluation scorecard from `docs/sources/<source>/evaluation.md` — extract source type, classification, auth mechanism, ingestion approach. This skill implements one source at a time; run it multiple times for data products with multiple sources.
2. If pipeline architecture exists, extract layering strategy and incremental pattern.
3. If contract exists, extract schema for source definition columns.
4. Validate ingestion approach against tooling capability. dlt is a polling/extraction tool, NOT CDC — it does not read transaction logs. If the scorecard recommends CDC (log-based change capture for high-frequency transactional sources), guide the user to Debezium or platform-native CDC instead of dlt. dlt is appropriate for API extraction, file-based sources, and database polling with cursor-based incremental loading.
5. Generate dlt pipeline:
   - Source/resource definitions matching the source classification
   - Connection configuration referencing the documented auth mechanism
   - Write disposition (replace, append, merge) matching the ingestion approach. Flag `replace` risk: it truncates before loading, leaving empty/partial tables on failure — recommend staging with atomic swap where supported.
   - Incremental loading configuration (cursor fields, merge keys) if applicable
6. Flag dlt configuration pitfalls:
   - Bug #2782: `dlt.config.get()` reads from `secrets.toml` instead of `config.toml` — test config/secrets separation explicitly
   - Silent env var failures: double-underscore nesting errors produce no warning, dlt silently falls back to TOML
   - Silent destination fallback: misnamed destinations silently fall back to shorthand type string
   - Nested data divergence at `max_table_nesting=0`: behavior differs silently across DuckDB, Snowflake, Databricks, ClickHouse
7. Generate dbt source YAML:
   - Source and table definitions
   - `loaded_at_field` and freshness thresholds from scorecard/scope
   - Column definitions from contract if available
8. Remind user to wire `dbt source freshness` as a separate orchestrator step (not included in `dbt build`).
9. Update source evaluation scorecard status to reflect implementation.
10. Suggest next skills: `dos:implement-models` (if not yet done), `dos:review-pipeline`

**Curated references:**

| Reference File | Source Context Files |
|---|---|
| `dlt-pipeline-patterns.md` | cdc-mechanisms-tooling, incremental-loading-patterns, dlt-destination-type-mapping |
| `dbt-source-config.md` | data-freshness-slas, ci-cd-pipeline-design |
| `auth-config-patterns.md` | secrets-environment-management, secrets-management-rotation |

---

### 8. `dos:implement-models`

**Phase:** Build (T)
**Purpose:** Generate dbt models, schema YAMLs, tests, and contract enforcement from data product artifacts.
**Input:** Contract (required), quality config (optional), pipeline architecture (optional), scope (optional)
**Output:** dbt models + schema YAMLs + tests in the project codebase

**Workflow:**

1. Read contract — extract schema (columns, types, constraints).
2. If quality config exists, extract dimensions, thresholds, and scoring for test generation.
3. If pipeline architecture exists, extract layering strategy and incremental configuration.
4. If scope exists, extract modeling recommendation and consumption patterns.
5. Detect target platform and flag incompatibilities before generating code:
   - **ClickHouse**: no merge incremental strategy, no Python models, CTEs fail with INSERT (ephemeral models broken), ReplicatedMergeTree deduplication prevents delete+insert. Recommend append-only patterns with materialized views for pre-aggregation.
   - **Semi-structured data** (JSON types in contract): dbt's 38 cross-database macros have zero coverage for JSON path extraction, regex, and array flattening. Require dispatch shim implementations before proceeding.
6. Generate dbt models by layer:
   - **Staging**: rename, cast, basic cleaning. Materialized as view or ephemeral. One model per source table.
   - **Intermediate**: business logic joins, enrichments, deduplication. Materialized as table or incremental.
   - **Marts**: consumer-facing models matching the modeling recommendation (star schema facts/dims, wide tables, entity-centric). Materialized as table or incremental. Contract enforcement enabled.
7. Generate schema YAMLs alongside each model:
   - Column definitions with descriptions from contract
   - `contract: { enforced: true }` on mart models
   - Generic tests from quality config: `not_null`, `unique`, `accepted_values`, `relationships`
   - dbt-expectations tests for distribution/range checks if quality config specifies them
8. Flag contract enforcement false confidence: DuckDB enforces all constraints at build time, but Snowflake and Databricks treat most constraints as metadata-only. Add explicit dbt tests for every constraint the production warehouse does not enforce — a contract passing locally can silently allow invalid data in production.
9. Generate dbt unit tests for critical transformation logic (dbt v1.8+).
10. Update contract and quality config status to reflect implementation.
11. Suggest next skill: `dos:review-pipeline`

**Curated references:**

| Reference File | Source Context Files |
|---|---|
| `dbt-model-patterns.md` | kimball-dimensional-modeling, medallion-architecture, obt-wide-table-patterns |
| `dbt-testing-patterns.md` | tiered-validation-strategy, data-validation-tool-comparison |
| `contract-enforcement.md` | data-contract-structure, data-contract-enforcement-versioning |
| `cross-platform-sql.md` | dbt-adapter-dialect-gaps, cross-platform-portability-strategy |

---

### 9. `dos:review-pipeline`

**Phase:** Verify
**Purpose:** Audit an existing data pipeline against best practices.
**Input:** All existing data product artifacts (optional — enriches review with artifact context)
**Output:** Review checklist (`docs/data-products/<name>/reviews/<date>-review.md`)

**Workflow:**

1. If data product artifacts exist, load them for context.
2. Inventory the current pipeline: orchestrator, transformation tool, validation tools, monitoring.
3. Assess observability — are five baseline metrics covered? Start with freshness and volume (highest signal-to-investment ratio), then layer distribution, schema, and lineage.
   - Freshness, volume, distribution, schema, lineage
   - Distinguish observability (infer data health from outputs) from monitoring (watch execution metrics). Both are needed: instrument pipeline monitoring first (orchestrator-native), then layer data observability on top.
4. Assess validation — is the three-tier strategy in place?
   - Local dev (Pandera + pytest), CI (dbt tests), production (Soda/GE)
   - Where are the gaps?
5. Assess CI/CD — which tiers exist?
   - Pre-commit, PR validation (slim CI), production deployment
   - Flag three known slim CI blind spots:
     1. False negatives for var()/env_var() changes — CI passes, production breaks
     2. Incremental models run full-refresh in CI — entirely different SQL path from production. Fix: `dbt clone` to seed CI schema first.
     3. State artifact (manifest.json) staleness — if manifest is stale or missing, `state:modified+` comparisons are wrong. The pipeline that persists the manifest is itself a failure mode.
6. Assess SLA compliance across three enforcement layers:
   - **CI-time**: Are breaking changes detected via state comparison?
   - **Build-time**: Are dbt contracts enforced? Are constraints actually enforced by the production warehouse (not just metadata)?
   - **Runtime**: Are quality checks and freshness monitoring in place?
   - Are SLAs quantified with error budgets ("99.5% compliance ≈ 3.6h/month violation allowed") or aspirational ("data should be fresh")?
   - Is `dbt source freshness` wired separately from `dbt build`? If not, there is no freshness monitoring.
7. Assess retry and failure handling:
   - Has every known failure mode been classified as terminal or transient?
   - Exponential backoff with jitter (not fixed-interval retry)
   - Dead letter queue for records that exhaust retries
   - Flag: dlt has no default retry — must use tenacity or equivalent
8. Flag gaps between artifacts and implementation (contract says X, code does Y).
9. Generate review checklist with findings, severity, and recommendations.
10. Append review to `reviews/` directory (reviews are append-only, not overwritten).

**Curated references:**

| Reference File | Source Context Files |
|---|---|
| `observability-pillars.md` | data-observability-pillars |
| `validation-audit.md` | tiered-validation-strategy, ci-cd-pipeline-design |
| `sla-checklist.md` | data-freshness-slas, data-quality-slas |
| `retry-patterns.md` | retry-failure-patterns |

---

## Artifact Chaining

Skills produce artifacts that downstream skills consume. Each skill checks for prior artifacts at startup and adjusts its workflow. Source evaluations live in `docs/sources/` and are independent of data products. All other artifacts live in `docs/data-products/<name>/`. The scope document is the join point — it declares which sources a data product consumes.

| Skill | Produces | Location | Consumed By |
|---|---|---|---|
| `dos:evaluate-source` | Source Evaluation Scorecard | `docs/sources/<source>/` | scope-data-product, implement-source, design-pipeline |
| `dos:scope-data-product` | Data Product Scope Document | `docs/data-products/<name>/` | select-model, define-contract, assess-quality, design-pipeline, implement-models |
| `dos:select-model` | Advisory (updates scope) | `docs/data-products/<name>/` | implement-models |
| `dos:define-contract` | Contract | `docs/data-products/<name>/` | implement-models, assess-quality, review-pipeline |
| `dos:assess-quality` | Quality Config | `docs/data-products/<name>/` | implement-models, review-pipeline |
| `dos:design-pipeline` | Pipeline Architecture | `docs/data-products/<name>/` | implement-source, implement-models, review-pipeline |
| `dos:implement-source` | Code (dlt + dbt source) | project codebase | review-pipeline |
| `dos:implement-models` | Code (dbt models + tests) | project codebase | review-pipeline |
| `dos:review-pipeline` | Review Checklist | `docs/data-products/<name>/reviews/` | (terminal — informs next iteration) |

Every artifact template ends with a "Next Steps" section suggesting downstream skills, guiding the user through the natural workflow chain.

**Graceful degradation:** Every skill works without upstream artifacts. When artifacts are absent, the skill asks the questions those artifacts would have answered. The experience degrades gracefully — the user answers more questions rather than hitting errors. The full chain is the optimized path, not the only path.

## Context Corpus Coverage

Context files may appear in multiple tiers — a file that informs a Tier 1 skill's references may also inform a Tier 2 skill with different emphasis. The counts below reflect unique files per tier; some files appear in more than one.

### Tier 1 Coverage (35 unique context files across 9 skills)

| Skill | Context Files Consumed |
|---|---|
| evaluate-source | source-system-evaluation, data-source-onboarding, data-profiling, schema-drift-risk, secrets-management-rotation, secrets-environment-management, incremental-loading-patterns |
| scope-data-product | consumption-driven-architecture, requirements-gathering-techniques, data-freshness-slas, data-quality-dimensions, data-quality-slas |
| select-model | data-model-selection, kimball-dimensional-modeling, data-vault-modeling, obt-wide-table-patterns |
| define-contract | data-contract-structure, data-contracts, data-contract-enforcement-versioning, schema-evolution |
| assess-quality | data-quality-dimensions, data-quality-scoring, data-quality-slas, tiered-validation-strategy, data-validation-tool-comparison, anomaly-drift-detection, data-freshness-slas |
| design-pipeline | consumption-driven-architecture, incremental-loading-patterns, medallion-architecture, schema-evolution |
| implement-source | cdc-mechanisms-tooling, incremental-loading-patterns, dlt-destination-type-mapping, data-freshness-slas, secrets-environment-management, secrets-management-rotation, ci-cd-pipeline-design |
| implement-models | kimball-dimensional-modeling, medallion-architecture, obt-wide-table-patterns, dbt-adapter-dialect-gaps, cross-platform-portability-strategy, tiered-validation-strategy, data-contract-structure, data-contract-enforcement-versioning, data-validation-tool-comparison |
| review-pipeline | data-observability-pillars, tiered-validation-strategy, ci-cd-pipeline-design, data-freshness-slas, data-quality-slas, retry-failure-patterns |

### Meta/Infrastructure Context Files (5 files)

These files inform skill design itself rather than any individual skill's domain knowledge. They shaped this design document and will guide skill authoring conventions:

- agentic-phase-patterns — phased execution model, artifact boundaries, size constraints
- deterministic-gates-hooks — validation patterns, hook ecosystem, error output design
- cross-provider-skill-portability — Agent Skills spec, portability strategy, provider extensions
- data-engineering-lifecycle-model — Reis lifecycle as organizational spine, framework layering
- data-governance-foundations — governance maturity model, accountability framing

### Tier 2 Candidates (15 additional context files)

| Candidate | Context Files | Workflow |
|---|---|---|
| `dos:impact-analysis` | data-lineage-implementation | Trace a proposed change through downstream consumers and artifacts |
| `dos:select-platform` | production-platform-comparison, platform-cost-optimization, platform-tooling-compatibility, compute-governance-patterns, query-storage-cost-optimization | Compare platforms for a specific workload |
| `dos:configure-ci` | ci-cd-pipeline-design, pre-commit-dbt-hooks, local-duckdb-development | Scaffold three-tier CI/CD pipeline |
| `dos:onboard-source-e2e` | (composes Tier 1 skills) | Full source-to-serving guided session |
| `dos:setup-observability` | data-observability-pillars, streaming-observability-backpressure | Configure monitoring and alerting |
| `dos:govern-access` | access-control-models, row-column-security-comparison, data-masking-tokenization, data-governance-foundations | Define access control and masking policies |
| `dos:evaluate-compliance` | privacy-regulatory-requirements, right-to-erasure-implementation, audit-trail-design | Assess privacy/regulatory pipeline implications |

### Uncovered Context Files (~24%, Tier 3 specializations)

These are deep specializations that become Tier 3 skills or specialist reference material. They cover streaming, cross-cloud, table format internals, and platform provisioning — areas that matter at scale but are not part of the foundational workflow:

- stream-processing-comparison, streaming-windowing-watermarks
- kafka-event-streaming-patterns, cdc-lakehouse-write-strategies
- cross-cloud-data-sharing, iceberg-catalog-interoperability, iceberg-cross-platform-compatibility
- open-table-formats, private-networking-data-platforms
- environment-provisioning-patterns, terraform-data-platform-iac, finops-governance
- pipeline-orchestration-comparison, data-catalog-selection
- data-masking-tokenization, compute-governance-patterns

## Non-Goals

- **No orchestrator integration** — skills do not generate Airflow DAGs, Dagster assets, or Prefect flows. Orchestration is a Tier 2+ concern.
- **No streaming pipeline implementation** — Tier 1 covers batch/incremental. Streaming (Flink, Spark Structured Streaming, DLT) is Tier 3.
- **No platform provisioning** — skills do not generate Terraform. Infrastructure-as-code is a Tier 2 concern.
- **No catalog integration** — skills do not push metadata to DataHub, OpenMetadata, or Unity Catalog. Catalog integration is a Tier 2 concern.

## Implementation Notes

**Skill authoring order:** Start with `dos:evaluate-source` — it is the entry point to the chain, exercises the full skill architecture (SKILL.md, references, assets, scripts), and its profiling script validates the scripts/ pattern. Use it to empirically validate the 500-line SKILL.md constraint. If progressive disclosure to references/ proves insufficient, adjust the constraint before authoring remaining skills.

**Artifact template authoring:** Design the artifact templates (`assets/`) before writing SKILL.md instructions. The template defines the structure that skills read and write — getting it right first prevents rework across multiple skills that consume the same artifact.

**Reference curation:** When distilling context files into skill references, extract only decision matrices, criteria tables, checklists, and platform-specific thresholds. Do not copy explanatory prose — the skill instructions provide the narrative; references provide the data.

## Key Decisions Summary

1. **Practitioner-workflow organization** over lifecycle-stage taxonomy — skills map to what engineers do, not where it falls in a framework.
2. **Living artifacts over one-shot generation** — skills create and update structured specifications that evolve with the data product.
3. **EL/T split at the tool boundary** — `implement-source` (dlt) and `implement-models` (dbt) mirror the ELT pattern.
4. **Human-readable artifacts** — markdown with YAML frontmatter, reviewable by non-technical stakeholders, parseable by skills.
5. **Portable core with Claude Code extensions** — base Agent Skills spec for cross-provider, hooks/scripts layered on top.
6. **Curated references, not runtime dependencies** — context corpus informs authoring; skills carry their own knowledge.
7. **Graceful degradation** — every skill works without upstream artifacts; the chain is optimized path, not required path.
8. **Nine Tier 1 skills** covering Discover → Scope → Design → Build → Verify, with seven Tier 2 candidates mapped for future expansion.
