# Changelog

All notable changes to the dos plugin are documented here.

## [0.2.0] — 2026-04-06

### Added
- `marketplace.json` for plugin registry installation (#8)

### Fixed
- Use `${CLAUDE_SKILL_DIR}` for `validate-upstream.py` path resolution in build-phase skills (#18)

## [0.1.0] — 2026-03-23

First release. All 9 Tier 1 skills implemented covering the full data engineering lifecycle.

### Added

**Discover phase**
- `dos:evaluate-source` — assess source systems with six-dimension scoring, data profiling, and ingestion recommendations

**Scope phase**
- `dos:scope-data-product` — define data products driven by consumption intent with SLA tiers and quality dimensions

**Design phase**
- `dos:select-model` — choose a data modeling approach (Kimball, Data Vault, OBT) based on constraints
- `dos:define-contract` — define ODCS v3.1-aligned data contracts with three-layer enforcement
- `dos:assess-quality` — set up quality dimensions, scoring methods, and tiered validation tooling
- `dos:design-pipeline` — architecture pipelines with layering strategy, incremental patterns, and idempotency

**Build phase**
- `dos:implement-source` — generate dlt pipeline code and dbt source definitions with CDC boundary detection
- `dos:implement-models` — generate dbt models, schema YAMLs, tests, and contract enforcement with platform detection

**Verify phase**
- `dos:review-pipeline` — audit pipelines across observability, validation, CI/CD, SLAs, and retry handling

**Foundation**
- 66 research-backed context files across 23 data engineering characteristic areas
- Skill library design document defining the 9-skill architecture
- Plugin scaffold with `plugin.json`, directory conventions, and portable Agent Skills spec
- `CLAUDE.md` with project conventions and skill architecture reference
- README with workflow diagram, skill chain, and getting started guidance
- GitHub Issue template for skill feedback collection
