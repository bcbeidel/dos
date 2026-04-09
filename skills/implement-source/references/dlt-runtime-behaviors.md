# dlt Runtime Behaviors

## Array Fields and Child Tables

When a source field contains a list/array value, dlt extracts it to a separate child table named `<resource_name>__<field_name>`. Under `merge` write disposition this causes unbounded child table growth and makes the field inaccessible from the parent table.

### Decision Table

| Field Type | Write Disposition | Risk | Action |
|------------|-------------------|------|--------|
| Scalar | Any | None | No action needed |
| Array/List | `replace` | Low — child table rebuilt each run | Advisory: consider serializing for simpler downstream queries |
| Array/List | `append` | Medium — child table grows, no dedup | Advisory: consider serializing |
| Array/List | `merge` | **High — child table unbounded, field inaccessible** | **Blocking: must serialize to text** |

### Detection

During code generation, check if any source field can contain a list/array AND write disposition is `merge`.

### Remediation

Both steps are required together.

**1. Declare the field as text in the dlt columns dict:**

```python
@dlt.resource(
    write_disposition="merge",
    merge_key="id",
    columns={"preciptype": {"data_type": "text"}},
)
```

**2. Serialize the list to a JSON string in processing_steps:**

```python
def process_record(record: dict) -> dict:
    for field in ["preciptype"]:
        value = record.get(field)
        record[field] = json.dumps(value) if isinstance(value, list) else value
    return record
```

## Schema Caching on Field Changes

dlt caches the pipeline schema in `~/.dlt/pipelines/<pipeline_name>/`. When fields are removed or renamed in resource code, the cached schema retains old column names. The pipeline runs silently with no error; downstream models break expecting the new names. This is expected dlt behavior, not a bug.

### Decision Table

| Change Type | Cache Impact | Action Required |
|-------------|-------------|-----------------|
| Add new field | None — schema extends automatically | No action |
| Remove field | Stale column persists in cache | Reset: delete `~/.dlt/pipelines/<name>/` |
| Rename field | Old name persists, new name added | Reset: delete `~/.dlt/pipelines/<name>/` |
| Change field type | dlt creates versioned column (e.g., `field__v_text`) | Reset or accept versioned column |

### Detection

When modifying existing pipeline code that removes or renames fields from a resource.

### Remediation

Include a comment in generated pipeline code:

```python
# IMPORTANT: If you remove or rename fields from this resource,
# delete ~/.dlt/pipelines/<pipeline_name>/ and any local database
# files before re-running.
```

When reviewing existing code changes that alter field names, flag this as an advisory finding.

## Cross-Reference

Nested data divergence across platforms (DuckDB, Snowflake, Databricks, ClickHouse) at `max_table_nesting=0` is documented in `dlt-pipeline-patterns.md` under "Nested data divergence." Refer there for platform-specific behavior; do not duplicate.
