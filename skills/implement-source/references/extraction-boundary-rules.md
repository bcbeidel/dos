# Extraction Boundary Rules

## Raw-First Extraction Definition

The extraction layer captures ONLY fields present in the source API/database response.

**Allowed in extraction `processing_steps`:**

| Operation | Rationale |
|-----------|-----------|
| Flattening nested JSON to columnar fields | Structural change only, no data modification |
| Serializing array/list fields to JSON strings | Type coercion for storage, no data modification |
| Adding metadata fields (`_extracted_at`, `_source_version`) | Pipeline-internal metadata, not derived from source data |

**NOT allowed in extraction `processing_steps`:**

| Operation | Belongs In | Layer |
|-----------|-----------|-------|
| Field renames | dbt staging | `stg_` models |
| Type casting beyond storage coercion | dbt staging | `stg_` models |
| Pydantic model validation/reshaping | dbt staging or intermediate | `stg_` / `int_` models |
| Enrichment from a second data source | dbt intermediate | `int_` models |
| Cross-domain lookups | dbt intermediate | `int_` models |

## Violation Patterns to Scan For

| Pattern | How to Detect | Remediation Route |
|---------|--------------|-------------------|
| `processing_steps` lambda calls `.model_dump()` on a Pydantic class | Grep for `model_dump()` in extract files | Remove Pydantic schema from extraction; move field renames/reshaping to dbt staging |
| Schema module imports in extract files (`from extractload.<module>.schema import`) | Grep for `schema import` in extract files | Remove schema dependency; extraction should yield raw dicts |
| Lambda in `processing_steps` renames fields (e.g., `"new_name": record["old_name"]`) | Grep for lambda expressions in `processing_steps` definitions | Move field renames to dbt staging `stg_` model |
| Enrichment logic references a second data source or external lookup (haversine, ZIP code lookup) | Review `processing_steps` for non-source-native logic or imports | Move to dbt intermediate `int_` model |
| Cross-domain joins requiring data from another pipeline | Imports from other extract modules or references to external datasets | Move to dbt intermediate `int_` model |

## Cost-of-Retry Principle

For quota-billed APIs, a full-job retry replays ALL API calls.

### Retry Type Comparison

| Retry Type | Behavior | Safe for quota-billed? |
|------------|----------|------------------------|
| Full-state retry | Replays all API calls from scratch | No — multiplies cost |
| Checkpoint retry | Resumes from last successful cursor position | Yes — only replays failed segment |
| Idempotent retry | Re-requests same data, no side effects | Depends on billing model |

### Retry Cost Decision Table

Calculate: `retry_cost = api_calls_per_run * overage_price_per_call`

| Condition | Severity | Action |
|-----------|----------|--------|
| `retry_cost > $10` | Blocking | Present cost estimate to user; ask before setting `max_retries > 0` |
| `retry_cost <= $10` | Advisory | Recommend retry with cost note in pipeline comments |
| Source is not quota-billed | Standard | Apply normal retry guidance (exponential backoff, max 3 retries) |

Prefer checkpoint retry over full-state retry for all quota-billed sources. If the extraction framework does not support checkpoint retry, document the retry cost in the pipeline configuration comments.

## Remediation Routing Summary

| Violation Type | Route To | Skill |
|----------------|----------|-------|
| Field renames | Staging (`stg_`) | `implement-models` |
| Type casting | Staging (`stg_`) | `implement-models` |
| Pydantic reshaping | Staging (`stg_`) | `implement-models` |
| Enrichment/lookup | Intermediate (`int_`) | `implement-models` |
| Cross-domain joins | Intermediate (`int_`) | `implement-models` |
