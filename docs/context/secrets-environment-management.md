---
name: Secrets and Environment Management
description: How dbt and dlt handle environment switching and secrets, the gap between them, and the operational pitfalls in dlt's configuration system
type: context
related:
  - docs/research/2026-03-22-development-workflow.research.md
  - docs/context/local-duckdb-development.md
  - docs/context/ci-cd-pipeline-design.md
---

## Key Insight

dbt and dlt both have well-designed environment and secrets management, but they are parallel systems with no unified switch. Teams must coordinate environment switching manually via shared environment variables, Makefiles, or direnv. dlt's configuration system has confirmed bugs that break its advertised config/secrets separation.

## dbt Environment Management

dbt separates environments via **targets** in `profiles.yml`. Each target specifies database type, connection, and schema. Switching is via `dbt run --target prod`.

```yaml
my_project:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: data/project.duckdb
      schema: dev_schema
    prod:
      type: snowflake
      schema: analytics
```

Development schemas follow `dbt_<username>` to prevent developers overwriting each other's work. The recommended `profiles.yml` location is `~/.dbt/` to keep credentials out of version control.

## dlt Environment Management

dlt uses **named destinations** that abstract the destination type behind a configuration key. The same pipeline code runs against DuckDB locally and BigQuery in production by swapping TOML configuration:

```toml
# Local: .dlt/config.toml
[destination.my_destination]
destination_type = "duckdb"

# Production: different config.toml
[destination.my_destination]
destination_type = "bigquery"
location = "US"
```

Gotcha: if the destination name doesn't match a configured destination, dlt silently falls back to treating it as a shorthand type string. No error, no warning.

## The Gap Between Them

There is no single configuration that switches both dbt and dlt between environments simultaneously. In practice, teams use one of:

- **Environment variables** (e.g., `TARGET=dev`) consumed by both tools
- **Makefile targets** that pass the right flags to each tool
- **direnv** with `.envrc` files that auto-load/unload env vars per directory

## dbt Secrets

dbt uses `{{ env_var('DBT_KEY') }}` in profiles.yml. Three naming conventions:

- `DBT_` — standard variables
- `DBT_ENV_SECRET_` — scrubbed from logs, restricted to profiles.yml and packages.yml only, cannot be passed to macros or used in model SQL
- `DBT_ENV_CUSTOM_ENV_` — custom variables

All environment variables are strings. Use `| int`, `| as_number`, `| as_bool` for type conversion.

Precedence (lowest to highest): default argument in `env_var()` < project-wide default < environment-level value < job-level override.

## dlt Secrets

dlt has a 5-level priority hierarchy:

1. Environment variables (highest)
2. `secrets.toml` and `config.toml`
3. Vaults (GCP Secret Manager, AWS, Azure, Airflow)
4. Custom providers via `register_provider`
5. Default argument values (lowest)

`config.toml` is for non-sensitive data (safe to commit). `secrets.toml` is for sensitive data (never commit). dlt raises an exception if it detects secrets in config.toml.

Environment variable naming uses uppercase with double underscores: `DESTINATION__POSTGRES__CREDENTIALS__USER`.

dlt also uses progressive section elimination in lookup: for `sources.notion.notion_databases.api_key`, it searches progressively shorter paths down to just `api_key`.

## Operational Pitfalls

**dlt bug #2782: config/secrets separation is broken.** `dlt.config.get()` reads from `secrets.toml` instead of only `config.toml`. The advertised separation doesn't work as documented. This is a confirmed, open bug.

**Silent env var failures in dlt.** Getting the double-underscore nesting wrong produces no error — dlt ignores unrecognized env vars and falls back to TOML files without warning.

**Concurrent pipeline state corruption.** Running two dlt pipelines concurrently against the same dataset corrupts `_dlt_pipeline_state`. Works fine locally (separate directories) but breaks in production.

## Takeaway

For local development, use direnv with `.envrc` files (keep in `.gitignore`). For CI, use platform-native secret stores (GitHub Secrets, GitLab CI Variables). Be aware of dlt's config bugs and test that environment variable overrides actually take effect — don't trust silent fallback behavior.
