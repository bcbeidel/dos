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

| Skill | Phase | Description |
|-------|-------|-------------|
| `dos:scope-source` | Discover | Assess a data source's technical characteristics before pipeline construction. |
| `dos:scope-data-product` | Scope | Populate a `data-product.md` living document section by section — Overview, Sources, Contract, Quality, Architecture. |
| `dos:implement-source` | Build | Generate dlt pipeline code and dbt source definitions from a data product's Sources section. |
| `dos:implement-data-product` | Build | Generate dbt models, schema YAMLs, tests, contract enforcement, and orchestration artifacts from `data-product.md`. |

## Workflow

Skills chain together — each produces artifacts that downstream skills consume. Start anywhere; skills work independently but are most effective in sequence.

```
  Discover           Scope                    Build
┌─────────────┐  ┌──────────────────┐  ┌──────────────────────┐
│ scope-      │─▶│ scope-data-      │─▶│ implement-source (EL)│
│ source      │  │ product          │  │                      │
│             │  │                  │─▶│ implement-data-      │
│             │  │ data-product.md  │  │ product (T + orch)   │
└─────────────┘  └──────────────────┘  └──────────────────────┘
```

**Typical flow:**

1. `/dos:scope-source` — assess a source system (e.g., `postgres-orders-db`)
2. `/dos:scope-data-product` — populate `data-product.md` section by section (Overview → Sources → Contract → Quality → Architecture)
3. `/dos:implement-source` — generate dlt pipeline + dbt source YAML from the Sources section
4. `/dos:implement-data-product` — generate dbt models, tests, contract enforcement, and orchestration artifacts

Each skill checks for existing artifacts and adjusts its workflow accordingly. `scope-data-product` supports re-runs — it rebuilds only pending or potentially-affected sections.

## Artifact Structure

Each data product produces a single living document:

```
docs/data-products/<name>/
  data-product.md    # Overview, Sources, Contract, Quality, Architecture, Changelog
docs/sources/<name>/
  evaluation.md      # Source scorecard (from scope-source)
```

## Feedback

After using a skill, [file feedback](../../issues/new?template=skill-feedback.yml) to help improve it. Report what worked, what didn't, and suggestions.

## Development

Skills live in `skills/<skill-name>/SKILL.md`. Each skill directory may also contain supporting scripts and reference docs.
