# dos

> **Experimental** — this repository is a work in progress and subject to breaking changes.

A Claude Code plugin housing skills for facilitating data engineering work.

## Installation

```bash
claude plugin install dos
```

Or for local development:

```bash
claude --plugin-dir ./dos
```

## Skills

Skills are namespaced under `dos:` and invocable as `/dos:<skill-name>`.

| Skill | Description |
|-------|-------------|
| `dos:evaluate-source` | Assess a data source's technical characteristics before pipeline construction. |
| `dos:scope-data-product` | Define what a data product needs to be, driven by consumption intent. |
| `dos:select-model` | Choose a data modeling approach (Kimball, Data Vault, OBT) based on constraints. |
| `dos:define-contract` | Define or update an ODCS v3.1-aligned data contract for a data product. |
| `dos:assess-quality` | Set up quality engineering with dimensions, scoring, and validation tooling. |
| `dos:design-pipeline` | Architecture a data pipeline from source to serving layer. |
| `dos:implement-source` | Generate dlt pipeline code and dbt source definitions from data product artifacts. |
| `dos:implement-models` | Generate dbt models, schema YAMLs, tests, and contract enforcement from data product artifacts. |
| `dos:review-pipeline` | Audit an existing data pipeline against best practices. |

## Workflow

Skills chain together — each produces artifacts that downstream skills consume. Start anywhere; skills work independently but are most effective in sequence.

```
  Discover          Scope            Design              Build           Verify
┌────────────┐  ┌─────────────┐  ┌───────────────┐  ┌──────────────┐  ┌─────────────┐
│ evaluate-  │─▶│ scope-data- │─▶│ select-model  │  │ implement-   │  │ review-     │
│ source     │  │ product     │  │ define-       │─▶│ source (EL)  │─▶│ pipeline    │
│            │  │             │─▶│  contract     │  │              │  │             │
│            │  │             │  │ assess-       │  ├──────────────┤  │             │
│            │  │             │─▶│  quality      │─▶│ implement-   │─▶│             │
│            │  │             │  │ design-       │  │ models (T)   │  │             │
│            │  │             │─▶│  pipeline     │─▶│              │  │             │
└────────────┘  └─────────────┘  └───────────────┘  └──────────────┘  └─────────────┘
```

**Typical flow:**

1. `/dos:evaluate-source` — assess a source system (e.g., `postgres-orders-db`)
2. `/dos:scope-data-product` — define what the data product needs to be
3. `/dos:define-contract` + `/dos:assess-quality` + `/dos:design-pipeline` — specify the contract, quality rules, and architecture (any order)
4. `/dos:implement-source` — generate dlt pipeline + dbt source YAML
5. `/dos:implement-models` — generate dbt models, tests, and contract enforcement
6. `/dos:review-pipeline` — audit the result; findings loop back to upstream skills

Each skill checks for existing artifacts and adjusts its workflow accordingly. You don't have to start from step 1 — jump in wherever your project is.

## Feedback

After using a skill, [file feedback](../../issues/new?template=skill-feedback.yml) to help improve it. Report what worked, what didn't, and suggestions.

## Development

Skills live in `skills/<skill-name>/SKILL.md`. Each skill directory may also contain supporting scripts and reference docs.
