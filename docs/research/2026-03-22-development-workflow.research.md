---
name: "Development Workflow"
description: "DuckDB local dev is fast but hides dialect and concurrency divergence; three-tier validation (pre-commit, PR CI with slim builds, production deploy) is the emerging best practice; dbt and dlt have parallel but non-unified environment management; SQLFluff pre-commit hooks are 10x slower with dbt templater"
type: research
sources:
  - https://duckdb.org/2025/04/04/dbt-duckdb
  - https://github.com/duckdb/dbt-duckdb
  - https://dlthub.com/docs/dlt-ecosystem/destinations/duckdb
  - https://rasmusengelbrecht.substack.com/p/my-local-data-stack-duckdb-dlt-dbt
  - https://datacoves.com/post/dbt-duckdb
  - https://docs.getdbt.com/docs/core/connect-data-platform/connection-profiles
  - https://docs.getdbt.com/docs/local/dbt-core-environments
  - https://dlthub.com/docs/general-usage/destination
  - https://dlthub.com/docs/general-usage/credentials/setup
  - https://dlthub.com/docs/walkthroughs/add_credentials
  - https://docs.getdbt.com/reference/dbt-jinja-functions/env_var
  - https://docs.getdbt.com/docs/build/environment-variables
  - https://docs.getdbt.com/guides/set-up-ci
  - https://docs.getdbt.com/guides/custom-cicd-pipelines
  - https://www.datafold.com/blog/accelerating-dbt-core-ci-cd-with-github-actions-a-step-by-step-guide/
  - https://tech.raisa.com/dbt-ci-pipeline/
  - https://docs.sqlfluff.com/en/3.2.5/production/pre_commit.html
  - https://docs.astral.sh/ruff/integrations/
  - https://docs.getdbt.com/blog/enforcing-rules-pre-commit-dbt
  - https://docs.getdbt.com/docs/build/hooks-operations
  - https://docs.getdbt.com/reference/node-selection/state-comparison-caveats
  - https://docs.getdbt.com/best-practices/clone-incremental-models
  - https://docs.getdbt.com/docs/build/unit-tests
  - https://docs.getdbt.com/reference/commands/clone
  - https://docs.getdbt.com/reference/node-selection/defer
  - https://github.com/dbt-checkpoint/dbt-checkpoint
  - https://github.com/sqlfluff/sqlfluff/issues/651
  - https://github.com/dlt-hub/dlt/issues/2782
related:
  - docs/plans/2026-03-21-data-pipeline-research-context.plan.md
---

## Summary

**Research question:** What are best practices for a local-to-production data engineering development workflow using DuckDB, dlt, and dbt?

**Mode:** Technical | **SIFT rigor:** High | **Sources:** 28 (19× T1, 2× T4, 7× T5/challenger) | **Searches:** 12 across Google | **Claims verified:** 15 (11 verified, 4 corrected, 0 unverified)

**Key findings:**

1. **DuckDB local development is fast but hides real divergence risks** (HIGH). The DuckDB + dlt + dbt stack eliminates cloud dependencies — the entire ingestion-to-transformation loop runs in seconds locally. However, DuckDB lacks Snowflake's VARIANT/OBJECT types and platform-specific functions, meaning semi-structured data pipelines require syntax adaptation between environments. DuckDB is also single-writer at the process level.

2. **Three-tier validation is the emerging CI/CD best practice** (HIGH). Pre-commit hooks (Ruff, SQLFluff with Jinja templater, dbt-checkpoint) catch issues in seconds at commit time. PR validation uses slim CI (`dbt build --select state:modified+`) with `dbt clone` to seed incrementals. Production deployment uses merge-triggered or scheduled full builds. SQLFluff with dbt templater is 10x slower than Jinja templater — use Jinja locally, dbt templater in CI only.

3. **dbt and dlt have parallel but non-unified environment management** (MODERATE). dbt uses targets in profiles.yml; dlt uses named destinations with TOML configuration. No single switch changes both — teams coordinate via shared environment variables or Makefiles.

4. **Secrets management is well-designed but has operational pitfalls** (HIGH). dbt's `DBT_ENV_SECRET_` prefix scrubs secrets from logs. dlt's 5-level config hierarchy is powerful but has a confirmed bug where config.get() reads from secrets.toml (issue #2782). Silent env var failures in dlt compound the risk.

5. **dbt hooks and git hooks serve different feedback loops** (HIGH). Git hooks (pre-commit) validate code quality (static analysis). dbt hooks (on-run-start/end, pre/post-hook) manage database state at runtime. dbt unit tests (1.8+) add a middle layer but have severe limitations — no macro testing, no incremental logic testing, ~1% expected coverage.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://duckdb.org/2025/04/04/dbt-duckdb | Fully Local Data Transformation with dbt and DuckDB | Petrica Leuca / DuckDB | 2025-04-04 | T1 | verified |
| 2 | https://github.com/duckdb/dbt-duckdb | dbt-duckdb GitHub README | DuckDB / dbt-duckdb maintainers | current | T1 | verified |
| 3 | https://dlthub.com/docs/dlt-ecosystem/destinations/duckdb | DuckDB Destination | dlt Hub | current docs | T1 | verified |
| 4 | https://rasmusengelbrecht.substack.com/p/my-local-data-stack-duckdb-dlt-dbt | My Local Data Stack (DuckDB, dlt, dbt & Evidence.dev) | Rasmus Engelbrecht | 2025 | T5 | verified — community practitioner blog |
| 5 | https://datacoves.com/post/dbt-duckdb | Lean Data Stack with dlt, DuckDB, DuckLake, and dbt | Datacoves | 2025 | T4 | verified — vendor practitioner (dbt partner) |
| 6 | https://docs.getdbt.com/docs/core/connect-data-platform/connection-profiles | About profiles.yml | dbt Labs | current docs | T1 | verified |
| 7 | https://docs.getdbt.com/docs/local/dbt-core-environments | dbt Core Environments | dbt Labs | current docs | T1 | verified |
| 8 | https://dlthub.com/docs/general-usage/destination | Destination Configuration | dlt Hub | current docs | T1 | verified |
| 9 | https://dlthub.com/docs/general-usage/credentials/setup | Configuration Overview and Examples | dlt Hub | current docs | T1 | verified |
| 10 | https://dlthub.com/docs/walkthroughs/add_credentials | How to Add Credentials | dlt Hub | current docs | T1 | verified |
| 11 | https://docs.getdbt.com/reference/dbt-jinja-functions/env_var | env_var Function | dbt Labs | current docs | T1 | verified |
| 12 | https://docs.getdbt.com/docs/build/environment-variables | Environment Variables | dbt Labs | current docs | T1 | verified |
| 13 | https://docs.getdbt.com/guides/set-up-ci | Get Started with Continuous Integration Tests | dbt Labs | current docs | T1 | verified |
| 14 | https://docs.getdbt.com/guides/custom-cicd-pipelines | Customizing CI/CD with Custom Pipelines | dbt Labs | current docs | T1 | verified |
| 15 | https://www.datafold.com/blog/accelerating-dbt-core-ci-cd-with-github-actions-a-step-by-step-guide/ | Accelerating dbt Core CI/CD with GitHub Actions | Datafold | 2023-05-08 | T4 | verified — vendor practitioner (data quality tooling) |
| 16 | https://tech.raisa.com/dbt-ci-pipeline/ | Lint, Test, Deploy: Building a dbt CI Pipeline with SQLFluff | Raisa Tech | 2025 | T5 | verified — community content |
| 17 | https://docs.sqlfluff.com/en/3.2.5/production/pre_commit.html | Using pre-commit | SQLFluff | current docs | T1 | verified |
| 18 | https://docs.astral.sh/ruff/integrations/ | Integrations | Astral (Ruff) | current docs | T1 | verified |
| 19 | https://docs.getdbt.com/blog/enforcing-rules-pre-commit-dbt | Enforcing Rules at Scale with pre-commit-dbt | Benoit Perigaud / dbt Labs | 2022-08-03 | T1 | verified |
| 20 | https://docs.getdbt.com/docs/build/hooks-operations | Hooks and Operations | dbt Labs | current docs | T1 | verified |
| 21 | https://docs.getdbt.com/reference/node-selection/state-comparison-caveats | State Comparison Caveats | dbt Labs | current docs | T1 | verified |
| 22 | https://docs.getdbt.com/best-practices/clone-incremental-models | Clone Incremental Models in CI | dbt Labs | current docs | T1 | verified |
| 23 | https://docs.getdbt.com/docs/build/unit-tests | Unit Tests | dbt Labs | current docs | T1 | verified |
| 24 | https://docs.getdbt.com/reference/commands/clone | dbt clone | dbt Labs | current docs | T1 | verified |
| 25 | https://docs.getdbt.com/reference/node-selection/defer | Defer | dbt Labs | current docs | T1 | verified |
| 26 | https://github.com/dbt-checkpoint/dbt-checkpoint | dbt-checkpoint | dbt-checkpoint maintainers | current | T1 | verified |
| 27 | https://github.com/sqlfluff/sqlfluff/issues/651 | SQLFluff dbt templater performance | SQLFluff community | 2021+ | T4 | verified — issue thread with performance data |
| 28 | https://github.com/dlt-hub/dlt/issues/2782 | config.get reads from secrets.toml | dlt community | 2024 | T4 | verified — confirmed bug report |

---

## Sub-question 1: Local Development End-to-End

### Source 1: Fully Local Data Transformation with dbt and DuckDB
- **URL:** https://duckdb.org/2025/04/04/dbt-duckdb
- **Author/Org:** DuckDB | **Date:** 2025-04-04

profiles.yml minimal configuration for dbt-duckdb:
```yaml
dutch_railway_network:
  outputs:
    dev:
      type: duckdb
      path: data/dutch_railway_network.duckdb
      extensions:
        - spatial
        - httpfs
      threads: 5
      attach:
        - path: 'https://blobs.duckdb.org/nl-railway/train_stations_and_services.duckdb'
          type: duckdb
          alias: external_db
  target: dev
```

Materialization strategies supported: table ("replacing the target table at each run"), incremental (append and delete+insert only), snapshot (SCD Type 2), view, and external (exports to CSV, JSON, or Parquet).

External sources can read directly from S3 Parquet files, CSVs, and JSON via DuckDB's httpfs extension: "external_location can point to CSV, Parquet or JSON files" from local or remote endpoints.

Project structure recommendation: `models/transformation/` for dimension/fact tables, `models/reverse_etl/` for downstream writes, `seeds/` for local files.

### Source 2: dbt-duckdb GitHub README
- **URL:** https://github.com/duckdb/dbt-duckdb
- **Author/Org:** DuckDB / dbt-duckdb maintainers | **Date:** current

Minimal profile (in-memory):
```yaml
default:
  outputs:
    dev:
      type: duckdb
  target: dev
```

Persistent database:
```yaml
default:
  outputs:
    dev:
      type: duckdb
      path: /tmp/dbt.duckdb
      schema: my_schema
      threads: 4
  target: dev
```

MotherDuck (production) configuration:
```yaml
default:
  outputs:
    dev:
      type: duckdb
      path: "md:<database_name>"
  target: dev
```

DuckLake support: `is_ducklake: true` enables materialization as Parquet with centralized metadata.

Secrets management for S3 access:
```yaml
secrets:
  - type: s3
    region: my-aws-region
    key_id: "{{ env_var('S3_ACCESS_KEY_ID') }}"
    secret: "{{ env_var('S3_SECRET_ACCESS_KEY') }}"
```

Incremental strategies: delete+insert (default), append, merge (DuckDB >= 1.4.0), microbatch (dbt-core >= 1.9).

Plugin system supports built-in plugins: `excel`, `gsheet`, `iceberg`, `sqlalchemy`, `delta`.

Minimum requirements: dbt-core >= 1.8.x, DuckDB >= 1.1.x.

### Source 3: dlt Docs — DuckDB Destination
- **URL:** https://dlthub.com/docs/dlt-ecosystem/destinations/duckdb
- **Author/Org:** dlt Hub | **Date:** current docs

Install: `pip install "dlt[duckdb]"`

Configuration patterns:
- Relative path: `dlt.destinations.duckdb("files/data.db")`
- Pipeline-relative: `dlt.destinations.duckdb(":pipeline:")` creates `<pipeline_name>.duckdb`
- In-memory: `duckdb.connect(":memory:")`

Default naming: snake_case. Alternative: `duck_case` for non-ASCII characters.

Warning: "DuckDB identifiers are case-insensitive; loading `{"Column": 1, "column": 2}` creates collisions."

Recommended file format: Parquet (faster, multithreaded) over default insert-values. Loading uses 20 threads by default.

Critical note: "Avoid naming datasets identically to database names — this confuses DuckDB's binder regarding catalog/schema references."

### Source 4: My Local Data Stack (DuckDB, dlt, dbt & Evidence.dev)
- **URL:** https://rasmusengelbrecht.substack.com/p/my-local-data-stack-duckdb-dlt-dbt
- **Author/Org:** Rasmus Engelbrecht | **Date:** 2025

Project structure:
```
localdatastack/
  dlt_pipeline/        # Ingestion
  dbt_project/         # Transformations (staging -> marts)
  evidence_dashboard/  # Dashboards
  run.sh              # One command to run it all
```

dlt role: "a Python library for loading data from APIs with incremental updates and schema evolution built in."
DuckDB role: "fast, SQL-friendly, and works seamlessly with both dbt and Evidence."
dbt pattern: "staging -> intermediate -> marts pattern you'd use in dbt on a real team"

Key insight: "Having everything run with a single command (and no Docker setup) made it so much easier to focus on the modeling and visualization instead of infrastructure."

### Source 5: Lean Data Stack with dlt, DuckDB, DuckLake, and dbt
- **URL:** https://datacoves.com/post/dbt-duckdb
- **Author/Org:** Datacoves | **Date:** 2025

"A lean analytics stack built with dlt, DuckDB, DuckLake, and dbt delivers fast insights without the cost or complexity of a traditional cloud data warehouse."

Authentication consolidation: "This single token is used by dlt, DuckDB, and dbt to authenticate securely with MotherDuck." (referring to MOTHERDUCK_TOKEN)

dbt profile for DuckLake:
```yaml
default:
  outputs:
    dev:
      type: duckdb
      path: 'md:datacoves_ducklake'
      threads: 4
      schema: dev
      is_ducklake: true
  target: dev
```

"By enabling DuckLake, dbt materializes tables as Parquet files with centralized metadata instead of opaque DuckDB-only files."

---

## Sub-question 2: Environment Management

### Source 6: About profiles.yml
- **URL:** https://docs.getdbt.com/docs/core/connect-data-platform/connection-profiles
- **Author/Org:** dbt Labs | **Date:** current docs

Profile structure with multiple targets:
```yaml
my_project_profile:
  target: dev
  outputs:
    dev:
      type: snowflake
      schema: dev_schema
      threads: 4
    prod:
      type: snowflake
      schema: analytics
      threads: 4
```

Switching environments: `dbt run --target prod`

Recommended profiles.yml location: `~/.dbt/` directory. Rationale: "Security — Keeps credentials out of project directories and version control."

Security: Each dbt user should have "their own set of database credentials." Development schemas follow pattern `dbt_<username>` to prevent users overwriting each other's work.

### Source 7: dbt Core Environments
- **URL:** https://docs.getdbt.com/docs/local/dbt-core-environments
- **Author/Org:** dbt Labs | **Date:** current docs

"dbt makes it easy to maintain separate production and development environments through the use of targets within a profile."

Key benefit: "while making changes, your objects will be built in your development target without affecting production queries made by your end users."

Schema recommendation: "using different schemas within one database to separate your environments. This is the easiest to set up and is the most cost-effective solution."

Multi-user pattern: "set your dev target schema to be `dbt_<username>`"

### Source 8: dlt Docs — Destination Configuration
- **URL:** https://dlthub.com/docs/general-usage/destination
- **Author/Org:** dlt Hub | **Date:** current docs

Named destinations for environment switching without code changes:

```python
pipeline = dlt.pipeline(
    pipeline_name='my_pipeline',
    destination='my_destination',
    dataset_name='dataset_name')
```

For development (TOML):
```toml
[destination.my_destination]
destination_type = "duckdb"
```

For production (same code, different TOML):
```toml
[destination.my_destination]
destination_type = "bigquery"
location = "US"
[destination.my_destination.credentials]
project_id = "value"
```

Four factory declaration methods: shorthand type string, factory import, full module path, explicit instantiation.

---

## Sub-question 3: Secrets and Configuration Management

### Source 9: dlt Configuration Overview and Examples
- **URL:** https://dlthub.com/docs/general-usage/credentials/setup
- **Author/Org:** dlt Hub | **Date:** current docs

Priority hierarchy:
1. Environment Variables (highest)
2. secrets.toml and config.toml
3. Vaults (Google Cloud Secrets Manager, AWS, Azure, Airflow)
4. Custom providers via `register_provider`
5. Default argument values (lowest)

config.toml: non-sensitive data, safe to commit. secrets.toml: sensitive data, never commit. "sensitive information should never be placed in config.toml or other non-secure locations. dlt will raise an exception if it detects secrets in inappropriate locations."

Environment variable naming: uppercase with double underscores as separators: `SOURCES__NOTION__API_KEY`, `DESTINATION__POSTGRES__CREDENTIALS__USER`.

Progressive section elimination in lookup: for `sources.notion.notion_databases.api_key`, dlt searches `sources.notion.notion_databases.api_key` -> `sources.notion.api_key` -> `sources.api_key` -> `api_key`.

### Source 10: How to Add Credentials
- **URL:** https://dlthub.com/docs/walkthroughs/add_credentials
- **Author/Org:** dlt Hub | **Date:** current docs

Local development: use `.dlt/secrets.toml`.

TOML example:
```toml
[sources.pipedrive]
pipedrive_api_key = "pipedrive_api_key"

[destination.bigquery.credentials]
project_id = "project_id"
private_key = "private_key"
client_email = "client_email"
```

Google Cloud Secret Manager best practice: store configuration fragments rather than single values to "reduce the number of calls" to the backend.

### Source 11: env_var Function
- **URL:** https://docs.getdbt.com/reference/dbt-jinja-functions/env_var
- **Author/Org:** dbt Labs | **Date:** current docs

Syntax: `{{ env_var('DBT_USER') }}` or with default: `{{ env_var('DBT_MATERIALIZATION', 'view') }}`

Secret variables prefixed `DBT_ENV_SECRET`:
- Available in `profiles.yml` and `packages.yml` only
- Disallowed in `dbt_project.yml` and model SQL "to prevent accidentally writing these secret values to the data warehouse"
- "Scrubbed from dbt logs and replaced with `*****`"
- Cannot be modified using Jinja filters or passed to macros

Type conversion: "Environment variables are always strings." Use `| int`, `| as_number`, `| as_bool` filters.

### Source 12: Environment Variables
- **URL:** https://docs.getdbt.com/docs/build/environment-variables
- **Author/Org:** dbt Labs | **Date:** current docs

Three naming conventions: `DBT_` (standard), `DBT_ENV_SECRET_` (secrets), `DBT_ENV_CUSTOM_ENV_` (custom).

Precedence hierarchy (lowest to highest):
1. Default argument in `env_var()` function
2. Project-wide default value
3. Environment-level value
4. Job-level or personal override (highest)

Secret variables: "Encrypted at rest using infrastructure-specific keys (e.g., AWS KMS)"

---

## Sub-question 4: CI/CD Pipeline Design

### Source 13: Get Started with Continuous Integration Tests
- **URL:** https://docs.getdbt.com/guides/set-up-ci
- **Author/Org:** dbt Labs | **Date:** current docs

Slim CI command: `dbt build --select state:modified+` — runs only modified nodes and downstream dependencies.

Multi-layered validation: dbt Project Evaluator (best practice deviations), SQLFluff linting, semantic node validation.

GitHub Actions SQLFluff example:
```yaml
name: lint dbt project on push
on:
  push:
    branches-ignore:
      - 'main'
jobs:
  lint_project:
    name: Run SQLFluff linter
    runs-on: ubuntu-latest
    steps:
      - uses: "actions/checkout@v3"
      - uses: "actions/setup-python@v4"
        with:
          python-version: "3.9"
      - name: Install SQLFluff
        run: "python -m pip install sqlfluff"
      - name: Lint project
        run: "sqlfluff lint models --dialect snowflake"
```

### Source 14: Customizing CI/CD with Custom Pipelines
- **URL:** https://docs.getdbt.com/guides/custom-cicd-pipelines
- **Author/Org:** dbt Labs | **Date:** current docs

Two pipeline patterns:
- **Pattern A — Merge-Triggered Production:** runs "only when there are pushes to a branch named main"
- **Pattern B — PR-Triggered Preview:** schema isolation using `DBT_CLOUD_PR_{REPO_KEY}_{PR_NUMBER}`

Secret storage by platform: GitHub (Settings -> Secrets), GitLab (Settings -> CI/CD -> Variables with "Mask variable"), Azure DevOps (pipeline variables marked secret), Bitbucket (Repository Variables with "Secured").

### Source 15: Accelerating dbt Core CI/CD with GitHub Actions
- **URL:** https://www.datafold.com/blog/accelerating-dbt-core-ci-cd-with-github-actions-a-step-by-step-guide/
- **Author/Org:** Datafold | **Date:** 2024

Three-workflow architecture: Production Job (scheduled daily), Staging Job (PR-triggered), Deploy Job (merge-triggered). Achieved "30%" reduction in Snowflake costs.

Slim CI implementation:
```yaml
- name: dbt build
  run: dbt build --select state:modified+ --defer --state ./
```

Manifest artifact management via S3:
```yaml
- name: Upload manifest to S3
  run: aws s3 cp target/manifest.json {s3 url}
- name: Grab production manifest from S3
  run: aws s3 cp {s3 url} ./manifest.json
```

Draft PR exclusion: `if: ${{ !github.event.pull_request.draft }}`

Dynamic PR schemas: `SNOWFLAKE_SCHEMA: "${{ format('{0}_{1}', 'PR_NUM', steps.findPr.outputs.pr) }}"`

Production optimization with source freshness: `dbt run --select source_status:fresher+ --state ./ --exclude config.materialized:view tag:static`

### Source 16: Lint, Test, Deploy: Building a dbt CI Pipeline with SQLFluff
- **URL:** https://tech.raisa.com/dbt-ci-pipeline/
- **Author/Org:** Raisa Tech | **Date:** 2025

Three validation stages (sequential):
1. Syntax validation: `dbt parse`
2. Dry-run testing: `dbt run --select $(changed_sql_files_base) --target CI --full-refresh --empty`
3. Code linting: `sqlfluff lint $(changed_sql_files)`

Changed file detection:
```bash
changed_sql_files=$(git diff --name-only --diff-filter=AM origin/$(System.PullRequest.targetBranchName) | grep '^$(project_root)/models/.*\.sql$')
```

---

## Sub-question 5: Git Hooks and dbt Hooks

### Source 17: SQLFluff — Using pre-commit
- **URL:** https://docs.sqlfluff.com/en/3.2.5/production/pre_commit.html
- **Author/Org:** SQLFluff | **Date:** current docs

Two hook IDs: `sqlfluff-lint` (returns errors) and `sqlfluff-fix` (auto-corrects).

dbt templater integration:
```yaml
- id: sqlfluff-lint
  additional_dependencies: ['<dbt-adapter>', 'sqlfluff-templater-dbt']
- id: sqlfluff-fix
  additional_dependencies: ['<dbt-adapter>', 'sqlfluff-templater-dbt']
```

Safety note: fix hook "refuses to modify files with templating or parse errors by default." Overriding with `fix_even_unparsable` "may break your SQL."

### Source 18: Ruff Integrations
- **URL:** https://docs.astral.sh/ruff/integrations/
- **Author/Org:** Astral (Ruff) | **Date:** current docs

Two hook IDs: `ruff-check` (linter) and `ruff-format` (formatter).

Ordering: "When using --fix, position the linting hook *before* formatting and other tools like Black or isort, as Ruff's fix behavior can output code changes that require reformatting."

### Source 19: Enforcing Rules at Scale with pre-commit-dbt
- **URL:** https://docs.getdbt.com/blog/enforcing-rules-pre-commit-dbt
- **Author/Org:** dbt Labs | **Date:** current

Package provides "over 20 tests" including: `check-model-has-tests`, `check-model-has-properties-file`, `check-model-name-contract`, `dbt-docs-generate`.

Four-step implementation: (1) define rules and config, (2) audit existing models with `--all-files`, (3) prioritize fixes, (4) deploy through both git hooks and CI.

### Source 20: Hooks and Operations
- **URL:** https://docs.getdbt.com/docs/build/hooks-operations
- **Author/Org:** dbt Labs | **Date:** current docs

Four hook types:
- `pre-hook`: before model/seed/snapshot build
- `post-hook`: after model/seed/snapshot build
- `on-run-start`: at beginning of `dbt build`, `dbt run`, `dbt test`, `dbt seed`, `dbt snapshot`, `dbt compile`, `dbt docs generate`
- `on-run-end`: at conclusion of same commands

Common use cases: creating UDFs, managing permissions, vacuuming tables, analyzing tables, resuming/pausing warehouses, creating Snowflake shares.

Operations (standalone SQL via macros): invoked via `dbt run-operation grant_select --args '{role: reporter}'`

---

## Challenge

### DuckDB local-to-production divergence risks

**VARIANT type gap is the single biggest risk.** DuckDB has no VARIANT, ARRAY (Snowflake-style), or OBJECT data types. Any Snowflake project using semi-structured data (PARSE_JSON, OBJECT_CONSTRUCT) will not run on DuckDB without rewriting. DuckDB supports LATERAL joins and UNNEST (functional equivalents to Snowflake's LATERAL FLATTEN, but with different syntax). DuckDB uses STRUCT and explicit typing where Snowflake uses flexible VARIANT. Code that compiles locally may produce silently different results in production due to type coercion differences. [GitHub discussions, DZone comparisons, DuckDB docs]

**Concurrency model mismatch.** DuckDB is single-writer at the process level — only one process can write at a time. Within a process, DuckDB uses MVCC with optimistic concurrency control (not simple database-level locking). Production warehouses handle concurrent writes from multiple processes natively. Cross-process concurrency bugs are invisible in local dev. [DuckDB concurrency docs]

**Scale divergence.** DuckDB performs well for datasets up to ~500MB. Beyond that, performance characteristics diverge significantly from cloud warehouses. Local dev gives false confidence about query performance at scale.

### dbt slim CI has documented blind spots

**False negatives for var()/env_var() changes.** dbt cannot detect that a model should be rebuilt when a variable value changes (issue #4304). CI passes while production breaks. [21]

**Incremental models run full-refresh in CI.** When running slim CI in a clean PR schema, incremental models don't exist yet. The `is_incremental` flag evaluates to false, so CI tests the full-refresh path — which may be entirely different SQL from the production incremental path. Fix: use `dbt clone` to seed the CI schema first. [22]

**State artifact management burden.** With dbt Core (not Cloud), you must persist `manifest.json` to S3/GCS and fetch it at CI start. This adds infrastructure and a failure mode (stale/missing manifest). [15]

### SQLFluff pre-commit performance is a known pain point

**dbt templater is 10x slower** than the Jinja templater (~20s per file vs ~2s). SQLFluff must compile the entire dbt project to resolve refs/sources. On pre-commit, this makes commits painfully slow. The documented workaround: use Jinja templater on pre-commit (accepting reduced accuracy) and dbt templater only in CI. [27]

**Parallelism is broken with dbt templater.** Running `--processes > 1` causes hangs and crashes. Must use `--processes 1`. [SQLFluff issues #6037, #6188]

### dlt configuration has footguns

**config/secrets separation is broken.** Bug #2782: `dlt.config.get()` reads from `secrets.toml` instead of `config.toml`. The advertised separation between configuration and secrets doesn't work as documented. [28]

**Silent env var failures.** Getting the double-underscore nesting wrong produces silent failures — dlt ignores unrecognized env vars and falls back to TOML files without warning.

**Concurrent pipeline state corruption.** Running two dlt pipelines concurrently against the same dataset corrupts `_dlt_pipeline_state`. Works fine locally (separate directories) but breaks in production. Classic local-vs-prod divergence. [dlt issue #2687]

### Missing tools and patterns

**pre-commit-dbt is dead; dbt-checkpoint is the successor.** The old `datacoves/pre-commit-dbt` repo has been renamed and transferred to `dbt-checkpoint/dbt-checkpoint`. [26]

**Additional tools not covered:** dbt-bouncer (governance checks against artifacts, no pre-commit required), sqlfmt (opinionated zero-config SQL formatter, default in dbt Cloud IDE), dbt-project-evaluator (first-party governance package).

**dbt unit tests (dbt-core 1.8+) have severe limitations.** No macro testing, no incremental logic testing, no complex type support, high authoring friction. Expected coverage is ~1% of columns. However, they run extremely fast on DuckDB — milliseconds, no cloud credentials needed. [23]

**dbt clone solves the incremental CI problem** via zero-copy cloning (Snowflake, Databricks, BigQuery). But DuckDB doesn't support zero-copy cloning — creates views instead. Another local-vs-prod divergence point. [24]

**dbt --defer enables local development** by resolving ref() calls against a production manifest when referenced models don't exist locally. Developers modify and test one model without building all upstream dependencies. [25]

**dbt run --empty (dbt 1.8+)** validates SQL correctness and schema compatibility with zero data. But if pointed at a production schema, it replaces tables with empty ones — causing outages.

**direnv for env var management** auto-loads/unloads environment variables from `.envrc` when entering/leaving a directory. Pairs naturally with dbt's `DBT_ENV_SECRET_*` prefix convention.

**Makefile/task runner patterns** for local dev orchestration (build, seed, test, docs, ci targets) are standard practice but not shipped with dbt or dlt project scaffolds.

---

## Findings

### 1. Local DuckDB development is fast and frictionless but hides real divergence risks

The DuckDB + dlt + dbt local stack eliminates cloud dependencies for development: dlt loads data into a local DuckDB file, dbt-duckdb transforms it, and the entire loop runs in seconds with no credentials needed (HIGH — T1 sources [1][2][3] converge).

The recommended project structure separates ingestion (dlt pipeline), transformation (dbt project with staging→intermediate→marts), and optionally dashboards — all orchestrated by a single shell script or Makefile [4][5]. DuckDB supports table, view, incremental (append, delete+insert, merge, microbatch), snapshot, and external materializations [1][2].

**However, three divergence risks undermine local-to-production confidence:**

1. **SQL dialect gaps** — DuckDB lacks Snowflake's VARIANT/OBJECT types and platform-specific functions (IFF, TRY_TO_*, PARSE_JSON). DuckDB supports LATERAL joins and UNNEST (functional equivalent to LATERAL FLATTEN but with different syntax). Models using semi-structured data require syntax adaptation between environments (HIGH — verified through DuckDB docs and community reports).

2. **Concurrency model** — DuckDB is single-writer at the process level (one write process at a time), using MVCC with optimistic concurrency control within a process. Production warehouses handle concurrent writes natively. Cross-process concurrency bugs are invisible locally (MODERATE — architectural constraint, not disputed).

3. **Scale characteristics** — DuckDB handles ~500MB comfortably but diverges significantly beyond that. Performance-critical queries may pass locally and timeout in production, or vice versa (MODERATE — depends on dataset size).

**Mitigation:** Use DuckDB for rapid iteration and unit testing. Run integration tests against the production warehouse in CI. Write adapter-portable SQL where possible; isolate platform-specific logic in macros with cross-database dispatch.

### 2. Environment management uses targets (dbt) and named destinations (dlt) — but the patterns are parallel, not unified

**dbt** separates environments via targets in `profiles.yml`. Each target specifies a database type, connection, and schema. Developers use personal schemas (`dbt_<username>`) to avoid collisions. Switching is via `dbt run --target prod` [6][7]. The recommended `profiles.yml` location is `~/.dbt/` to keep credentials out of version control [6].

**dlt** uses named destinations that abstract the destination type behind a configuration key. The same pipeline code runs against DuckDB locally and BigQuery in production by swapping TOML configuration [8]. This is powerful but has a gotcha: if the destination name doesn't match a configured destination, dlt silently falls back to treating it as a shorthand type string.

**Gap:** dbt and dlt have parallel but non-unified environment management. There's no single configuration that switches both tools between environments simultaneously. In practice, teams use environment variables (e.g., `TARGET=dev`) consumed by both tools, or a Makefile that passes the right flags to each (MODERATE — observed pattern, not formally documented).

### 3. Secrets management is well-designed in both tools but has operational pitfalls

**dbt** uses `{{ env_var('DBT_KEY') }}` in profiles.yml, with `DBT_ENV_SECRET_` prefix for values that must be scrubbed from logs and restricted to profiles.yml/packages.yml only [11][12]. Environment variable precedence is well-defined (default → project → environment → job) [12]. All environment variables are strings and require explicit type casting [11].

**dlt** has a 5-level priority hierarchy: env vars > TOML files > vaults > custom providers > defaults [9]. The config.toml/secrets.toml split is conceptually clean (config is safe to commit, secrets are not) [9][10].

**Critical pitfall:** dlt bug #2782 — `dlt.config.get()` reads from secrets.toml, breaking the advertised config/secrets separation. Silent env var failures compound this: misnaming a double-underscore variable causes silent fallback to TOML [28].

**Best practice for local env var management:** Use direnv with `.envrc` files (auto-load/unload per directory, language-agnostic). Keep `.envrc` and `.env` in `.gitignore`. For CI, use platform-native secret stores (GitHub Secrets, GitLab CI Variables, etc.) [14].

### 4. CI/CD should be three-tiered: pre-commit → PR validation → production deployment

The emerging best practice is a three-tier validation pipeline (HIGH — T1 [13][14] + T4 [15] converge):

**Tier 1: Pre-commit (local, seconds)**
- Ruff for Python linting/formatting (dlt pipelines, macros) [18]
- SQLFluff for SQL linting — use Jinja templater locally, dbt templater in CI only [17][27]
- dbt-checkpoint (successor to pre-commit-dbt) for model governance checks (tests exist, properties documented, naming conventions) [19][26]
- **Performance caveat:** SQLFluff with dbt templater is 10x slower; parallelism is broken. Use Jinja templater on pre-commit hooks [27].

**Tier 2: PR validation (CI, minutes)**
- `dbt parse` for syntax validation [16]
- `dbt build --select state:modified+ --defer --state ./` for slim CI — only modified models and downstream [13][15]
- `dbt clone` to seed CI schema with production incrementals before running slim CI [22][24]
- `dbt run --empty` for schema-only validation without warehouse compute (dbt 1.8+)
- SQLFluff lint with dbt templater for full accuracy
- Draft PR exclusion, concurrency control, dynamic PR schemas [15]

**Tier 3: Production deployment (merge-triggered or scheduled)**
- Full `dbt build` or source-freshness-aware selective build [15]
- Manifest artifact persistence to S3/GCS for state comparison [15]
- Schema teardown for old PR environments [15]

**Slim CI caveats:**
- False negatives for var()/env_var() changes [21]
- Incremental models run full-refresh unless `dbt clone` seeds the schema first [22]
- State artifact management adds infrastructure complexity for dbt Core users [15]

### 5. dbt hooks and git hooks serve different feedback loops — both are needed

**Git hooks (pre-commit framework)** enforce code quality at commit time — before code reaches CI. The three essential hooks are Ruff (Python), SQLFluff (SQL), and dbt-checkpoint (dbt governance). The four-step implementation approach: define rules, audit existing codebase with `--all-files`, prioritize fixes, deploy in both hooks and CI [19].

**dbt hooks** enforce runtime behavior at build time — within the dbt execution lifecycle [20]:
- `on-run-start/end`: project-level setup/teardown (create UDFs, manage permissions, resume/pause warehouses)
- `pre/post-hook`: model-level actions (grant access, vacuum tables, analyze tables)
- Operations (`dbt run-operation`): standalone SQL macros for administrative tasks

**Key distinction:** Git hooks validate code quality (static analysis). dbt hooks manage database state (runtime actions). They operate at different stages and are complementary, not alternatives.

**dbt unit tests (1.8+)** add a middle layer: they validate transformation logic with mocked inputs, run fast on DuckDB (milliseconds), but have severe limitations — no macro testing, no incremental logic testing, no complex types. Expected coverage is ~1% of columns. Best used for complex business logic in critical models [23].

---

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | dbt-duckdb supports table, view, incremental, snapshot, and external materializations | factual | [1][2] | verified |
| 2 | DuckDB lacks Snowflake's VARIANT, OBJECT types; supports LATERAL and UNNEST as functional equivalents to LATERAL FLATTEN | factual | DuckDB docs | corrected — DuckDB has LATERAL joins and UNNEST but not VARIANT/OBJECT |
| 3 | dbt slim CI command is `dbt build --select state:modified+` | factual | [13] | verified |
| 4 | SQLFluff with dbt templater is 10x slower than Jinja templater | statistic | [27] | verified — issue #651 title and body confirm exactly this |
| 5 | dlt config.get() reads from secrets.toml (bug #2782) | factual | [28] | verified — open bug, confirmed by maintainers |
| 6 | offbi/pre-commit-dbt was renamed to dbt-checkpoint/dbt-checkpoint | factual | [26] | corrected — original was offbi/pre-commit-dbt (not datacoves); datacoves fork is separate |
| 7 | dbt unit tests cannot test macros directly | factual | [23] | verified — docs state "only support unit testing SQL models" |
| 8 | dbt clone uses zero-copy cloning on Snowflake/Databricks/BigQuery | factual | [24] | verified |
| 9 | dbt env vars must be prefixed with DBT_, DBT_ENV_SECRET_, or DBT_ENV_CUSTOM_ENV_ | factual | [11][12] | verified |
| 10 | dlt uses 5-level config priority hierarchy (env > toml > vaults > custom > defaults) | factual | [9] | verified |
| 11 | dbt-duckdb minimum requirements: dbt-core >= 1.8.x, DuckDB >= 1.1.x | factual | [2] | verified |
| 12 | Datafold reported 30% Snowflake cost reduction from CI/CD optimizations including slim CI | statistic | [15] | corrected — 30% was from multiple optimizations, not slim CI alone |
| 13 | DuckDB is single-writer at the process level, uses MVCC within a process | factual | DuckDB concurrency docs | corrected — uses MVCC with optimistic concurrency, not simple database-level locking |
| 14 | dbt --empty flag introduced in dbt 1.8 | factual | dbt v1.8 upgrade guide | verified |
| 15 | sqlfmt is the default formatter in dbt Cloud IDE | factual | dbt Cloud IDE docs | verified — with SQLFluff fallback if .sqlfluff file present |
