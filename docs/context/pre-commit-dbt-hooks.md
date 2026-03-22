---
name: Pre-commit and dbt Hooks
description: Git hooks (pre-commit framework) and dbt hooks serve different feedback loops — one validates code quality at commit time, the other manages database state at runtime; both are needed
type: context
related:
  - docs/research/2026-03-22-development-workflow.research.md
  - docs/context/ci-cd-pipeline-design.md
---

## Key Insight

Git hooks and dbt hooks are complementary, not alternatives. Git hooks (pre-commit) validate code quality through static analysis at commit time. dbt hooks manage database state through runtime actions at build time. Conflating them leads to gaps in both code quality and operational reliability.

## Git Hooks (pre-commit framework)

The pre-commit framework runs checks before each commit. Three essential hooks for dbt+dlt projects:

**Ruff** (Python linting and formatting for dlt pipelines, macros):
- Two hook IDs: `ruff-check` (linter) and `ruff-format` (formatter)
- When using `--fix`, position the linting hook before formatting

**SQLFluff** (SQL linting):
- Two hook IDs: `sqlfluff-lint` (returns errors) and `sqlfluff-fix` (auto-corrects)
- The fix hook refuses to modify files with templating or parse errors by default
- Use Jinja templater for pre-commit hooks (~2s per file); reserve dbt templater for CI (~20s per file, 10x slower)
- dbt templater parallelism (`--processes > 1`) is broken — causes hangs and crashes
- dbt templater requires installing the dbt adapter as an additional dependency

```yaml
- id: sqlfluff-lint
  additional_dependencies: ['<dbt-adapter>', 'sqlfluff-templater-dbt']
```

**dbt-checkpoint** (dbt governance):
- Successor to the original `pre-commit-dbt` package (which was renamed and transferred)
- Provides 20+ checks: `check-model-has-tests`, `check-model-has-properties-file`, `check-model-name-contract`, `dbt-docs-generate`
- Four-step implementation: (1) define rules, (2) audit existing models with `--all-files`, (3) prioritize fixes, (4) deploy in both hooks and CI

Additional tools worth knowing about (not pre-commit hooks):
- **dbt-bouncer**: governance checks against artifacts, no pre-commit required
- **sqlfmt**: opinionated zero-config SQL formatter, default in dbt Cloud IDE
- **dbt-project-evaluator**: first-party governance package

## dbt Hooks (runtime)

dbt hooks execute SQL at specific points in the dbt execution lifecycle. They manage database state, not code quality.

Four hook types:

| Hook | Scope | When |
|------|-------|------|
| `on-run-start` | Project | Beginning of `dbt build`, `run`, `test`, `seed`, `snapshot`, `compile`, `docs generate` |
| `on-run-end` | Project | End of same commands |
| `pre-hook` | Model/seed/snapshot | Before individual resource builds |
| `post-hook` | Model/seed/snapshot | After individual resource builds |

Common use cases: creating UDFs, managing permissions (GRANT), vacuuming tables, analyzing tables, resuming/pausing warehouses, creating Snowflake shares.

**Operations** (`dbt run-operation`) provide standalone SQL execution via macros for administrative tasks outside the normal build cycle.

## dbt Unit Tests (the Middle Layer)

dbt unit tests (1.8+) sit between static analysis and runtime hooks — they validate transformation logic with mocked inputs.

Strengths:
- Run extremely fast on DuckDB (milliseconds)
- No cloud credentials needed
- Validate business logic with controlled inputs

Severe limitations:
- No macro testing (only SQL models)
- No incremental logic testing
- No complex type support
- High authoring friction
- Expected coverage is ~1% of columns

Best used for complex business logic in critical models only. They are not a substitute for integration testing against the production warehouse.

## Takeaway

Deploy all three layers: pre-commit hooks for fast static checks at commit time, dbt hooks for runtime database management, and dbt unit tests (selectively) for critical business logic. The pre-commit hooks pay for themselves immediately by catching issues before they reach CI. The dbt hooks pay for themselves by automating operational tasks that would otherwise be manual or forgotten.
