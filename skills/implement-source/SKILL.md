---
name: implement-source
description: Generate dlt pipeline code and dbt source definitions from a source evaluation scorecard. Validates upstream artifacts before code generation, handles CDC boundary detection, and updates the scorecard to reflect implementation state.
---

# dos:implement-source

Generate dlt pipeline code and dbt source definitions for a single data source. This skill reads a Source Evaluation Scorecard and translates its classification, auth mechanism, and ingestion approach into working extraction code. It implements one source at a time — run it multiple times for data products with multiple sources.

## Preamble

Before starting, establish context and validate inputs:

1. **Which source?** Ask the user for the source name (e.g., `postgres-orders-db`, `stripe-api`). This determines the scorecard path: `docs/sources/<source-name>/evaluation.md`.

2. **Validate upstream artifact.** Run the validation script:

   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/validate-upstream.py <source-name>
   ```

   If validation fails, report what's missing and suggest: "Run `/dos:evaluate-source` to create or complete the scorecard for this source." Do not proceed with code generation until the scorecard passes validation.

3. **Read the scorecard.** Extract: source type, classification, auth mechanism, ingestion approach, dimension scores, and profiling baselines.

4. **Optional input detection.** Ask which data product this source is for (if any). If a data product is named, check for:
   - `docs/data-products/<name>/pipeline-architecture.md` — if present, extract layering strategy and incremental pattern to align generated code.
   - `docs/data-products/<name>/contract.md` — if present, extract schema for dbt source column definitions.

   Report each as "available" or "not found — will proceed without enrichment."

5. **Check for existing code.** Search the project for existing dlt pipeline code and dbt source definitions for this source. If code exists, read it, summarize the current state, and ask what's changing. Propose updates to align existing code with the current scorecard rather than regenerating from scratch. If no code exists, proceed with generation.

6. **Detect project layout.** Look for `dbt_project.yml` to determine where dbt source YAML should be placed. Ask the user for the dlt pipeline location if no convention is detectable from the project structure.

## Workflow

### Step 1: Validate Ingestion Approach Against Tooling

Review the scorecard's recommended ingestion approach and validate it against dlt's capabilities.

**Critical CDC boundary:** dlt is a polling/extraction tool. It does NOT read transaction logs. If the scorecard recommends CDC (log-based change capture), guide the user to Debezium or platform-native CDC instead of dlt.

| Scorecard Recommends | dlt Appropriate? | Action |
|---------------------|-----------------|--------|
| Full load | Yes | Generate with `write_disposition="replace"` |
| Incremental (cursor-based) | Yes | Generate with incremental cursor config |
| Incremental (merge) | Yes | Generate with `write_disposition="merge"` |
| CDC (log-based) | **No** | Recommend Debezium; do not generate dlt pipeline |

If dlt is not appropriate, explain why and suggest alternatives. Do not generate dlt code for CDC use cases.

### Step 2: Generate dlt Pipeline

Generate pipeline code matching the source classification and ingestion approach. Refer to [dlt-pipeline-patterns.md](references/dlt-pipeline-patterns.md) for write dispositions, merge strategies, incremental configuration, and type fidelity warnings.

For each source, generate:

1. **Source and resource definitions** matching the source classification (transactional DB, SaaS API, file-based).

2. **Connection configuration** referencing the documented auth mechanism. Refer to [auth-config-patterns.md](references/auth-config-patterns.md) for auth patterns by source type and dlt config/secrets separation.

3. **Write disposition** matching the ingestion approach:
   - `replace` — Flag risk: truncates before loading, leaving empty/partial tables on failure. Recommend staging with atomic swap where supported.
   - `append` — Flag risk: duplicate accumulation if source replays events.
   - `merge` — Specify merge key(s) and merge strategy. Flag risk: full-table scan without partition pruning.

4. **Incremental loading configuration** if applicable:
   - Cursor field (e.g., `updated_at`)
   - Merge key (e.g., `id`)
   - Initial value for first run

### Step 3: Flag dlt Configuration Pitfalls

Surface these known issues in comments within the generated code or as warnings to the user. Refer to [dlt-pipeline-patterns.md](references/dlt-pipeline-patterns.md) for full details.

- **Bug #2782:** `dlt.config.get()` reads from `secrets.toml` instead of `config.toml`. Test config/secrets separation explicitly.
- **Silent env var failures:** Double-underscore nesting errors in env var names produce no warning. dlt silently falls back to TOML.
- **Silent destination fallback:** Misnamed destinations silently fall back to shorthand type string.
- **Nested data divergence at `max_table_nesting=0`:** Behavior differs silently across DuckDB, Snowflake, Databricks, and ClickHouse. Test on the target platform.

### Step 4: Generate dbt Source YAML

Generate dbt source configuration for the tables loaded by the dlt pipeline. Refer to [dbt-source-config.md](references/dbt-source-config.md) for YAML structure, freshness configuration, and column definition patterns.

Include:
- Source and table definitions matching the dlt pipeline output
- `loaded_at_field` and freshness thresholds derived from the scorecard's freshness dimension and scope SLA (if available)
- Column definitions from the contract schema (if available)

Use the `{{ source('<source_name>', '<table_name>') }}` function reference format for downstream model consumption.

### Step 5: Wire dbt Source Freshness

Remind the user: `dbt source freshness` is **NOT** included in `dbt build`. It must be wired as a separate orchestrator step:

```
Step 1: dbt source freshness  → fail pipeline if stale
Step 2: dbt build              → run only if sources are fresh
```

If no orchestrator is in place, note this as a TODO for production readiness.

### Step 6: Update Source Evaluation Scorecard

After successful code generation, update the source evaluation scorecard to reflect implementation state:

1. Set `status` field in frontmatter to `implemented` (or update from `draft` to `active`).
2. Update `last_modified` date.
3. Add a changelog entry noting:
   - What was generated (dlt pipeline, dbt source YAML)
   - File paths of generated code
   - Date of implementation

### Step 7: Next Steps

End with recommendations for downstream skills:

1. **`/dos:implement-models`** — Generate dbt models that transform the raw data loaded by this pipeline. The dbt source definitions created here are consumed by staging models.
2. **`/dos:review-pipeline`** — Audit the pipeline implementation against best practices once models are also in place.

Present these options and explain what each downstream skill will use from this implementation.

## Iteration Bounds

If generated code fails validation or the user requests changes:

- **Cap at 3-5 iterations** per step. If valid output cannot be produced within this bound, surface the failure with diagnostics rather than retrying.
- **Loop detection:** If three consecutive iterations produce >90% similar output, stop and explain what's blocking progress. The problem likely exceeds this skill's capability.
