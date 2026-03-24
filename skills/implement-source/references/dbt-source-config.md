# dbt Source Configuration

## Source YAML Structure

```yaml
sources:
  - name: <source_name>           # Matches dlt destination dataset
    description: <from scorecard>
    database: <target database>    # Optional, depends on project setup
    schema: <target schema>        # Where dlt loads raw data
    tables:
      - name: <table_name>
        description: <from scorecard or contract>
        loaded_at_field: <timestamp column>  # Column tracking load time
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
        columns:
          - name: <column_name>
            description: <from contract if available>
            data_type: <type>
            tests:
              - not_null
              - unique
```

## Freshness Configuration

Set `loaded_at_field` to a column that tracks when records were loaded. Common choices:

| Source Type | Typical loaded_at_field |
|-------------|------------------------|
| dlt-managed | `_dlt_load_id` or custom `_loaded_at` |
| Transactional DB | `updated_at`, `modified_date` |
| SaaS API | `_extracted_at` (dlt adds this) |
| File-based | `_file_last_modified` |

Set thresholds based on the source evaluation's freshness dimension score and the scope document's SLA requirements:

| Freshness Need | warn_after | error_after |
|----------------|------------|-------------|
| Near-real-time | 1 hour | 2 hours |
| Intraday | 4 hours | 8 hours |
| Daily batch | 18 hours | 36 hours |
| Weekly | 5 days | 8 days |

## Critical: dbt source freshness Wiring

`dbt source freshness` is **NOT** included in `dbt build`. This is by design — freshness queries hit the source database. Teams who run only `dbt build` in their orchestrator have no freshness monitoring.

Wire as a separate orchestrator step:

```
Step 1: dbt source freshness  → fail pipeline if stale
Step 2: dbt build              → run only if sources are fresh
```

## Column Definitions from Contract

If a contract exists, map contract schema properties to dbt source columns:

| Contract Field | dbt Source Field |
|----------------|-----------------|
| Property name | `name` |
| Property description | `description` |
| Property type | `data_type` |
| Required constraint | `not_null` test |
| Unique constraint | `unique` test |
| Accepted values | `accepted_values` test |
| Foreign key | `relationships` test |
