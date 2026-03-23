---
name: Data Contract Enforcement and Versioning
description: "Enforcement must happen at three layers (CI-time breaking change detection, build-time schema validation, runtime quality checks); contract versioning follows semantic versioning with the expand-contract pattern for breaking changes; consumer-driven contracts are theoretically superior but producer-driven is the practical starting point; cultural adoption is the actual bottleneck"
type: context
related:
  - docs/research/2026-03-22-data-contracts.research.md
  - docs/context/data-contract-structure.md
  - docs/context/schema-evolution.md
  - docs/context/ci-cd-pipeline-design.md
  - docs/context/data-freshness-slas.md
  - docs/context/retry-failure-patterns.md
  - docs/context/data-observability-pillars.md
---

## Key Takeaway

Contract enforcement requires three distinct layers: CI-time (catch breaking changes before deploy), build-time (prevent structurally incorrect data), and runtime (catch data quality issues). Teams that implement only one layer have blind spots. Versioning follows semantic versioning with the expand-contract pattern for breaking changes. Cultural adoption -- not tooling -- is the primary barrier.

## Three-Layer Enforcement

### CI-Time: Breaking Change Detection

dbt Cloud detects breaking changes when `contract: { enforced: true }` and `state:modified` selectors are used in CI. Breaking changes tracked: removing columns, changing `data_type`, removing or modifying constraints. The build fails if a breaking change is detected without a new version being created. `dbt build --select state:modified+` catches cascading breakage.

Schema registries perform compatibility checks at registration time -- producers attempting to register incompatible schema versions are rejected before the schema ever reaches consumers.

### Build-Time: Schema Validation

dbt contract preflight checks run before materialization, verifying the model's SQL will produce expected columns and types. If the check fails, the model is not built. This is structural validation only.

Schema registries validate at serialization time -- producers cannot serialize messages that do not conform. This is the strongest enforcement point for streaming because non-conforming data never enters the stream.

### Runtime: Data Quality and SLA Checks

Runtime validation catches what structural checks cannot: quality violations, freshness breaches, volume anomalies, distribution drift. Enforcement actions are tiered:

- **Critical** (schema mismatch, required field null) -- block writes, quarantine records
- **Warning** (volume anomaly, distribution shift) -- allow writes, generate alerts
- **Informational** (minor metrics) -- log to dashboards only

Soda and Great Expectations execute checks within pipelines. Circuit breaker patterns stop accepting data from offending producers when violation thresholds are exceeded, preventing corrupt data from cascading downstream.

## Contract Versioning

### Semantic Versioning

Contracts follow MAJOR.MINOR.PATCH:

- **MAJOR** -- breaking changes (removing columns, changing types, tightening constraints)
- **MINOR** -- backward-compatible additions (new optional columns, new quality checks)
- **PATCH** -- documentation, metadata, non-functional changes

### Compatibility Modes

- **BACKWARD** (Confluent default) -- consumers using new schema read old data. Consumers upgrade first. Best for data warehousing where topic rewind matters.
- **FORWARD** -- consumers using old schema read new data. Producers upgrade first.
- **FULL** -- both directions. Most restrictive: only add/remove optional fields with defaults.
- **TRANSITIVE** variants -- checked against all previous versions, not just the last. BACKWARD_TRANSITIVE is essential for data warehousing.

### Expand-Contract Pattern for Breaking Changes

Three phases for unavoidable breaking changes:

1. **Expand** -- introduce new elements alongside existing ones. No consumers break.
2. **Migrate** -- update consumers to use new elements. Both versions active.
3. **Contract** -- remove old elements once all consumers have migrated.

dbt model versions implement this explicitly: create `v2`, set `latest_version`, define `deprecation_date` on `v1`, consumers migrate from `ref('model', v=1)` to `ref('model')`. Recommended cadence: version bumps once or twice a year.

## Producer vs Consumer-Driven Contracts

**Producer-driven** (practical default): the producer defines the contract, consumers accept or negotiate. Simpler to implement. Sufficient for most organizations.

**Consumer-driven** (theoretically stronger): consumer expectations aggregate into provider obligations. Providers see exactly which consumers depend on which elements, making safe evolution straightforward. But consumers must formally document expectations -- overhead most data teams resist.

The pragmatic path: start producer-driven, instrument consumer usage patterns (which columns are actually queried), and evolve toward consumer-driven as the organization matures.

## Cultural Adoption Is the Bottleneck

GoCardless deployed ~30 contracts in 6 months powering ~60% of async events. Their key lesson: the cultural shift was harder than the technical implementation. Teams needed regular reminders of why contracts existed. Contracts represent a shift in accountability -- data producers must take responsibility for data quality, inverting the model where data teams shoulder this burden alone.

Implementation strategy: start with 2-3 high-impact pipelines where contract value is immediately visible (reducing pages, preventing recurring incidents). Demonstrate concrete benefits, then expand. Top-down mandates without demonstrated value generate compliance-oriented adoption that decays over time.
