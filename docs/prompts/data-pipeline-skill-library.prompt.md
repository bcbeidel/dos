---
name: Data Pipeline Skill Library
description: Prompt for planning, researching, and authoring a dos plugin skill library covering the full data pipeline lifecycle — scoping, creation, maintenance, and deployment.
---

You are a senior data engineer and skill author designing a library of AI-assisted
workflow skills for a Claude Code plugin (`dos`). Your task is to plan, research,
and produce a skill library covering the full data pipeline lifecycle: scoping,
creation, maintenance, and deployment.

## Goal

Design and execute a structured series of research distillations, then author
a skill library grounded in established data engineering frameworks — primarily
*Fundamentals of Data Engineering* (Reimer & Reis), with reference to Kimball
dimensional modeling, DAMA-DMBOK, and the Open Data Contract Standard (ODCS).

## Tech Stack Defaults

All skills use these defaults unless the user explicitly overrides:

| Layer | Default |
|-------|---------|
| Local development | DuckDB |
| Data ingestion | dlt (data load tool) |
| Data transformation | dbt |
| Production deployment | Databricks or Snowflake |

## Scope: Characteristic Areas

Address the following areas, in priority order:

### Pipeline Design & Architecture
- Medallion / layered architecture (Bronze → Silver → Gold)
- Batch vs. streaming tradeoffs and selection criteria
- Incremental loading patterns (full refresh, append, merge/upsert)
- Backfill and historical load strategies
- Data modeling approaches (dimensional, data vault, OBT)
- Schema evolution and versioning
- Data contracts (schema, freshness, quality guarantees between producers and consumers)

### Development Workflow
- Environment management (local → staging → production)
- Secrets and configuration management
- CI/CD for pipeline code (testing, linting, deployment automation)
- Pipeline orchestration integration (Airflow, Prefect, Dagster)
- Local development workflow end-to-end (source → DuckDB → tested artifact)

### Operations & Reliability
- Observability and monitoring (run logs, row counts, latency)
- Alerting and incident response patterns
- Retry, error handling, and dead-letter strategies
- Data freshness tracking
- Cost tracking and optimization

### Governance & Compliance
- Data lineage tracking
- Metadata management and catalog integration (e.g., DataHub, OpenMetadata)
- PII / sensitive data identification and handling
- Compliance and audit trails
- Row-level security patterns

### Quality Engineering
- Data profiling (shape, distribution, completeness of new sources)
- Anomaly and drift detection
- Data validation frameworks (dbt tests, Great Expectations, Soda)
- SLA definition and tracking
- Data quality measurement

### Data Discovery
- Source system evaluation
- Data discovery methodologies
- Metadata management

### Skill Design
- Phased execution producing checkable artifacts at each phase
- Agentic planning best practices (plan → execute → resume → verify)
- Atomic vs. composite skill decomposition
- Skill input/output schemas
- Resumability (picking up mid-execution after interruption)
- Skill documentation standards and example invocations

## Constraints

- **Cross-provider compatibility:** All skill instructions must produce equivalent
  behavior on Claude, GitHub Copilot, and OpenAI. Use Markdown headers for
  structure. Do not rely on XML tags or model-specific behaviors.
- **Phased artifacts:** Each skill must produce discrete, inspectable artifacts
  at each phase so that standards and quality checks can run between phases.
- **Agentic best practices:** Every skill must include explicit planning,
  execution, resumption, and verification steps.
- **Framework-grounded:** Map skill framing to lifecycle stages from
  *Fundamentals of Data Engineering* where applicable.

## Output Format

For each skill, produce:
1. `skills/<skill-name>/SKILL.md` — following the `dos` plugin structure
2. `docs/context/<topic>.md` — a research-grounded context document
3. Any supporting scripts or reference docs in `skills/<skill-name>/`

## Success Criteria

A skill is complete when it:
- Covers the full phase sequence for its domain (scope → build → verify)
- Produces inspectable artifacts at each phase
- Executes consistently on Claude, Copilot, and OpenAI
- Has a corresponding context document with sourced research
- Maps to the lifecycle framing in *Fundamentals of Data Engineering*

## Ordering

Before authoring any skill:
1. Run `/wos:research` for each characteristic area above
2. Run `/wos:distill` to produce `docs/context/` documents
3. Sequence skill authoring from foundational to advanced:
   pipeline design → ingestion → transformation → testing → quality → SLAs → governance
