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

## Development

Skills live in `skills/<skill-name>/SKILL.md`. Each skill directory may also contain supporting scripts and reference docs.
