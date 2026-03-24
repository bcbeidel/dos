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

## Development

Skills live in `skills/<skill-name>/SKILL.md`. Each skill directory may also contain supporting scripts and reference docs.
