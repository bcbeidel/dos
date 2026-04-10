---
name: implement-data-product
description: Generate dbt models, schema YAMLs, tests, contract enforcement, and orchestration artifacts from a data-product.md living document. Validates all required sections before code generation and appends a Changelog entry on completion.
---

# dos:implement-data-product

Generate dbt models, schema YAMLs, tests, contract enforcement, and orchestration artifacts for a data product. Reads Contract, Quality, and Architecture sections from `data-product.md` as the sole specification input.

## Preamble

Before starting, establish context and validate inputs:

1. **Which data product?** Ask the user for the data product name (e.g., `orders`, `customer-360`). The artifact path is `docs/data-products/<name>/data-product.md`.

2. **Validate the artifact.** Run the validation script:

   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/validate-data-product.py <product-name> --require contract,quality,architecture
   ```

   If validation fails, report the missing sections and suggest: "Run `/dos:scope-data-product` to populate the missing sections." Do not proceed with code generation until the artifact passes validation.

3. **Read the Contract section.** Extract schema: objects (tables), properties (columns), types, constraints, SLA terms, enforcement notes.

4. **Read the Quality section.** Extract quality dimensions, measurement methods, rule types, thresholds, dbt test mappings, scoring weights, and alert thresholds.

5. **Read the Architecture section.** Extract layering strategy, model inventory, incremental pattern, `tool::component.identifier` declarations (orchestration shorthands), and cross-pipeline dependency ordering.

6. **Read the Sources section.** Extract source names and incremental keys to anchor `{{ source() }}` references.

7. **Build model registry.** Search the project for all existing dbt models (`models/**/*.sql`) and record every filename (without `.sql`) as a known `{{ ref() }}` target. Parse `models/**/*.yml` and any `sources.yml` for valid `{{ source() }}` targets.

8. **Check for existing code.** Search the project for existing dbt models for this data product. If models exist, diff against the current Contract and Quality sections, and propose updates. If no models exist, proceed with generation.

   **Composite key detection:** If any existing model uses a list for `unique_key`, flag it and recommend a surrogate key. See [dbt-model-patterns.md](references/dbt-model-patterns.md) for the pattern.

9. **Detect project layout.** Find `dbt_project.yml` to determine model paths, naming conventions, and target platform.

## Workflow

### Step 1: Detect Target Platform

Identify the target platform from `profiles.yml` or ask the user. Flag incompatibilities before generating any code.

Refer to [cross-platform-sql.md](references/cross-platform-sql.md) for the full compatibility matrix and dispatch shim patterns.

**ClickHouse — flag before proceeding:**
- No merge incremental strategy — use `delete+insert` with lightweight deletes
- No Python models — SQL only
- CTEs fail with INSERT — ephemeral models will break in table model SELECT

**Semi-structured data — flag before proceeding:** If the Contract schema includes JSON types, require dispatch shim implementations before generating models that depend on JSON path extraction, regex, or array flattening.

### Step 2: Generate Staging Models

Generate one staging model per source table. Refer to [dbt-model-patterns.md](references/dbt-model-patterns.md) for layer conventions, naming patterns, and surrogate key pattern.

- **Naming:** `stg_<source>__<table>`
- **Materialization:** `view` or `ephemeral`
- **Content:** Rename columns, cast types, basic cleaning. No joins, no business logic.
- **Source reference:** `{{ source('<source_name>', '<table_name>') }}`

**Composite key handling:** If the Contract schema defines a composite primary key, recommend generating a surrogate `id` column via `dbt_utils.generate_surrogate_key`. Switch `unique_key` to `'id'`. Keep the composite uniqueness test as validation.

### Step 3: Generate Intermediate Models

Generate intermediate models for complex business logic reused by multiple marts.

- **Naming:** `int_<entity>__<verb>`
- **Materialization:** `table` or `incremental`
- **Content:** Joins, enrichments, deduplication, pivots.

### Step 4: Generate Mart Models

Generate consumer-facing models based on the Architecture section's model selection rationale. Refer to [dbt-model-patterns.md](references/dbt-model-patterns.md) for modeling approach patterns.

- **Kimball:** `fct_<process>` for fact tables, `dim_<entity>` for denormalized dimensions.
- **OBT/Wide table:** `<entity>_wide` — best as serving layer on Kimball core.
- **Entity-centric:** `<entity>` — one model per business entity.
- **Materialization:** `table` or `incremental`. Enable contract enforcement.

### Step 5: Validate Cross-References

Before generating schema YAMLs, validate every `{{ ref() }}` and `{{ source() }}` target:

1. Combine models being generated with existing models from the Preamble registry.
2. Verify every `{{ ref('model_name') }}` exists in the valid target set.
3. Verify every `{{ source('source_name', 'table_name') }}` against source YAML definitions.
4. Verify column references against schema YAMLs or Contract property definitions.
5. If any reference target is not found, do NOT emit the code. Report the mismatch with the closest valid match and ask for confirmation.

### Step 6: Generate Schema YAMLs

Generate schema YAML alongside each model. Refer to [dbt-testing-patterns.md](references/dbt-testing-patterns.md) for test mapping, severity configuration, and version-appropriate syntax.

For each model:
- Column definitions with descriptions from Contract
- `contract: { enforced: true }` on mart models
- Generic tests derived from Quality section: `not_null`, `unique`, `accepted_values`, `relationships`
- dbt-expectations tests for distribution/range checks if Quality specifies them
- Severity and `store_failures` configuration based on Quality dimension weights

### Step 7: Contract Enforcement

Refer to [contract-enforcement.md](references/contract-enforcement.md) for the false confidence warning and platform-specific enforcement behavior.

**Critical warning:** DuckDB enforces all constraints at build time, but Snowflake and Databricks treat most constraints as metadata-only. For every constraint the production warehouse does not enforce, add an explicit dbt data test.

Apply the three-layer enforcement strategy:
- **CI-time:** `dbt build --select state:modified+` for breaking change detection
- **Build-time:** `contract: { enforced: true }` for schema validation preflight
- **Runtime:** dbt data tests for quality and constraint enforcement

### Step 8: Generate Unit Tests

Generate dbt unit tests (v1.8+) for critical transformation logic. Refer to [dbt-testing-patterns.md](references/dbt-testing-patterns.md) for unit test patterns.

Focus on: complex joins, conditional logic, edge cases (nulls, zero quantities, negative values, boundary conditions). Run in dev/CI only.

### Step 9: Generate Orchestration Artifacts

Read the Architecture section for `tool::component.identifier` declarations.

- **`dbx::job.<name>`** — generate a Databricks Asset Bundles `databricks.yml` job resource block. Use schedule, cluster config, and task dependencies from the Architecture section.
- **`dbx::pipeline.<name>`** — generate a Databricks Asset Bundles DLT pipeline resource block per the Architecture section.
- **Other orchestrator shorthand** — generate the equivalent artifact for the declared tool.
- **No orchestrator declared** — note the absence, skip without error.

### Step 10: Update Specification Artifacts

After successful code generation, append a Changelog entry to `data-product.md`:

```markdown
### v<version> — <date>

| Field | Value |
|-------|-------|
| version | <bumped to MINOR> |
| date | <date> |
| skill | implement-data-product |
| sections updated | Contract, Quality, Architecture |
| change | Generated dbt models, schema YAMLs, tests, orchestration artifacts |
| reason | Initial implementation |
| potentially affected | (none) |
```

Update `version` (MINOR bump) and `last_modified` in frontmatter. Do not update standalone `contract.md` or `quality-config.md` — those are deprecated.

## Iteration Bounds

If generated code fails validation or the user requests changes:

- **Cap at 3-5 iterations** per step. If valid output cannot be produced within this bound, surface the failure with diagnostics rather than retrying.
- **Loop detection:** If three consecutive iterations produce >90% similar output, stop and explain what's blocking progress.
