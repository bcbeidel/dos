# Enforcement Layers

Contract enforcement requires three distinct layers. Teams that implement only one layer have blind spots. Cultural adoption -- not tooling -- is the primary barrier.

## Three-Layer Model

### 1. CI-Time: Breaking Change Detection

Catches breaking changes before deployment. Runs during pull request / merge request workflows.

| Tool | Mechanism |
|------|-----------|
| dbt Cloud CI | `contract: { enforced: true }` + `state:modified` selectors detect column removal, type changes, constraint changes |
| Schema registries | Compatibility checks at registration time; incompatible versions rejected before reaching consumers |
| Data Contract CLI | Lints ODCS contracts against previous versions for breaking changes |

Breaking changes tracked: removing columns, changing `data_type`, removing or modifying constraints. The build fails if a breaking change is detected without a new version being created.

### 2. Build-Time: Schema Validation

Prevents structurally incorrect data from being materialized. Runs during transformation execution.

| Tool | Mechanism |
|------|-----------|
| dbt contracts | Preflight check verifies model SQL produces expected columns and types; model not built on failure |
| Schema registries | Serialization-time validation; non-conforming messages never enter the stream |
| dlt contract modes | `freeze` raises exception; `discard_row` drops violating rows; `discard_value` strips bad fields |

Build-time is structural validation only -- it does not catch data quality issues.

### 3. Runtime: Data Quality and SLA Checks

Catches what structural checks cannot: quality violations, freshness breaches, volume anomalies, distribution drift.

| Tool | Mechanism |
|------|-----------|
| Soda / Great Expectations | Execute quality checks within pipeline runs |
| dbt tests | Row-level and aggregate assertions post-materialization |
| Circuit breakers | Stop accepting data from offending producers when violation thresholds are exceeded |

## Tiered Enforcement Actions

| Severity | Trigger | Action |
|----------|---------|--------|
| **Critical** | Schema mismatch, required field null | Block writes, quarantine records |
| **Warning** | Volume anomaly, distribution shift | Allow writes, generate alerts |
| **Informational** | Minor metric deviation | Log to dashboards only |

## Cultural Adoption Is the Bottleneck

GoCardless deployed ~30 contracts in 6 months powering ~60% of async events. Key lesson: the cultural shift was harder than the technical implementation.

**Implementation strategy:** Start with 2-3 high-impact pipelines where contract value is immediately visible (reducing pages, preventing recurring incidents). Demonstrate concrete benefits, then expand. Top-down mandates without demonstrated value generate compliance-oriented adoption that decays over time.

Data contracts require source system owners (typically application engineers) to accept accountability for data they produce -- a fundamental inversion of the traditional model where data teams shoulder this burden alone.
