---
name: Data Pipeline Knowledge Foundation
description: Multi-phase program prompt for researching, distilling, and designing a dos plugin skill library covering the full data pipeline lifecycle.
---

You are a senior data engineer and skill author designing a library of AI-assisted
workflow skills for a Claude Code plugin (`dos`). Your task is to plan, research,
and produce a skill library covering the full data pipeline lifecycle: scoping,
creation, maintenance, and deployment.

## Goal

Design and execute a structured series of research distillations, then author
a skill library grounded in established data engineering frameworks. Candidate
references include *Fundamentals of Data Engineering* (Reimer & Reis), Kimball
dimensional modeling, DAMA-DMBOK, and the Open Data Contract Standard (ODCS) —
but the specific lifecycle model and canonical references will be evaluated and
selected from research, not assumed in advance.

## Tech Stack Defaults

All skills use these defaults unless the user explicitly overrides:

| Layer | Default | Alternatives |
|-------|---------|--------------|
| Local development | DuckDB | — |
| Data ingestion | dlt (data load tool) | — |
| Data transformation | dbt | — |
| Production deployment | Databricks or Snowflake | ClickHouse, BigQuery, Redshift, Athena |

Skills should be aware of alternative production platforms — particularly ClickHouse,
which has distinct characteristics (MergeTree engine family, no transactions, different
incremental patterns, own SQL dialect) that affect pipeline design, transformation, and
quality patterns.

## Scope: Characteristic Areas

### Pipeline Design & Architecture
- Medallion / layered architecture (Bronze → Silver → Gold)
- Batch vs. streaming tradeoffs and selection criteria
- Incremental loading patterns (full refresh, append, merge/upsert)
- Backfill and historical load strategies
- Schema evolution and versioning

### Data Modeling
- Kimball dimensional modeling (facts, dimensions, star/snowflake schema)
- Data vault (hubs, links, satellites)
- One big table (OBT) / wide table patterns
- Selection criteria: when to use each approach
- Modeling for different storage targets (DuckDB, Snowflake, Databricks, ClickHouse)

### Open Table Formats
- Delta Lake, Apache Iceberg, Apache Parquet — comparison and selection criteria
- ORC and Avro for specific use cases (streaming, Kafka)
- ACID support, time travel, schema evolution capabilities per format
- Cross-platform compatibility: which engines and platforms support which formats
- Storage format impact on catalog compatibility (Unity Catalog, Snowflake catalogs, AWS Glue)
- ClickHouse native format and interoperability with open formats

### Production Platform Landscape
- ClickHouse: MergeTree engine family, ReplacingMergeTree/CollapsingMergeTree incremental patterns, no-transaction guarantees, SQL dialect
- BigQuery: serverless architecture, partitioning/clustering, slot management, nested data
- Redshift: distribution styles, sort keys, AQUA, Redshift Spectrum
- Athena: serverless query on S3, partition projection, Iceberg integration
- Platform selection criteria: query patterns, cost model, operational complexity, ecosystem fit

### Development Workflow
- Local development end-to-end (source → DuckDB → tested artifact)
- Environment management (local → staging → production)
- Secrets and configuration management
- CI/CD for pipeline code (testing, linting, deployment automation)
- Git hooks (pre-commit framework, pre-push) and dbt hooks (on-run-start/end, pre-hook/post-hook) as fast-feedback mechanisms

### Cross-Platform Adapter Compatibility
- dbt adapter compatibility: SQL dialect portability between DuckDB/Snowflake/Databricks/ClickHouse, adapter-specific macro patterns, feature gap management
- dlt destination compatibility: schema normalization, data type mapping, nested data handling across DuckDB/Snowflake/Databricks/ClickHouse

### Pipeline Orchestration
- Apache Airflow: DAGs, operators, sensors, connections, backfill, task dependencies
- Prefect: flows, tasks, deployments, schedules, caching
- Dagster: software-defined assets, jobs, sensors, partitions, asset lineage
- Orchestrator selection criteria and migration patterns
- dbt integration patterns (dbt-airflow, Dagster-dbt, Prefect-dbt)
- Cross-DAG dependencies and orchestrator-native data contracts

### Operations & Reliability
- Observability and monitoring (run logs, row counts, latency, pipeline health)
- Alerting and incident response patterns
- Retry, error handling, and dead-letter strategies
- Data freshness tracking

### Cost Optimization & FinOps
- Databricks: cluster sizing, spot instances, Photon, DBU optimization, auto-scaling
- Snowflake: warehouse sizing, auto-suspend/resume, credit optimization, query acceleration
- ClickHouse: compute cost patterns, tiered storage
- BigQuery: on-demand vs. capacity pricing, slot optimization
- Query cost optimization: partition pruning, materialization strategies, result caching
- Storage cost optimization: compression, retention policies, tiered storage
- Cost attribution, tagging, and chargeback patterns

### Governance & Compliance
- Compliance and audit trails
- Row-level security and column-level masking patterns
- Data access governance and entitlement management

### Data Catalog & Lineage
- Catalog tooling: DataHub, OpenMetadata, Unity Catalog, Snowflake catalog
- OpenLineage standard for lineage interoperability
- Column-level vs. table-level lineage
- Automated lineage extraction from dbt, Spark, and SQL
- Catalog integration patterns with dbt docs and CI

### Privacy Engineering
- PII / sensitive data identification and classification
- Data masking, tokenization, and pseudonymization techniques
- GDPR, CCPA, and other regulatory compliance requirements
- Privacy-by-design patterns for data pipelines
- Right-to-erasure implementation in data warehouses

### Quality Engineering
- Data profiling (shape, distribution, completeness, uniqueness)
- Anomaly and drift detection
- SLA definition and tracking
- Data quality measurement and scoring

### Validation Frameworks & Testing Tools
- dbt tests: schema tests, singular tests, custom generic tests
- Great Expectations: expectations, suites, checkpoints
- Soda: checks, scans, agreements
- Pandera: DataFrame schema validation
- pytest-based data tests against local DuckDB artifacts
- Tiered validation strategy: local Python checks → dbt CI tests → full suite in production
- Python assertions as shift-left quality gates

### Data Discovery
- Source system evaluation methodologies
- Data discovery approaches (automated profiling, manual assessment)
- Metadata documentation for new sources

### Stream Processing
- Spark Structured Streaming
- Databricks Delta Live Tables (DLT)
- Apache Flink
- Late data handling, watermarking, and windowing strategies
- Stateful stream processing
- Streaming vs. micro-batch architecture decisions
- Testing and observability patterns for streaming workloads

### CDC & Event-Driven Ingestion
- Change Data Capture patterns and tooling (Debezium, AWS DMS)
- dlt CDC sources and patterns
- Kafka-backed pipeline design and event sourcing
- Outbox and transactional outbox patterns
- CDC into open table formats (Delta Lake, Iceberg)

### Data Platform Engineering
- Infrastructure as Code: Terraform for Databricks, Snowflake, and ClickHouse
- Environment provisioning patterns (dev/staging/prod workspace separation)
- Compute management: Databricks cluster policies, Snowflake warehouse sizing

### Platform Security & Access Control
- Network architecture: private endpoints, VPCs, service principals
- Identity and access management (RBAC, ABAC)
- Secrets management at the platform level (Vault, cloud secrets managers)
- Service account and credential rotation patterns
- Cross-cloud and cross-region security patterns

### Data Contracts
- Contract structure and standards (ODCS, dbt contracts)
- Schema contracts (column names, types, nullability, primary keys)
- Freshness and SLA contracts
- Quality contracts (acceptable vs. breaking validation failures)
- Contract versioning and evolution (backward/forward compatibility)
- Producer/consumer negotiation and enforcement patterns
- Contract testing and CI integration (breaking change detection)
- Schema registry tooling (Confluent, AWS Glue Schema Registry)

### Data Product Scoping & Business Requirements
- Stakeholder requirement gathering for data engineering contexts
- Use case documentation: query patterns, update frequency needs, consumer SLAs
- Reverse-engineering architecture decisions from consumption patterns
- Requirement change management: detecting when consumer needs shift and propagating changes back through pipeline design
- Data product thinking: pipelines as products with owners, consumers, and SLAs
- Prioritization frameworks for competing consumer requirements
- Grounded in the canonical lifecycle framework selected from research (see Canonical Frameworks & Lifecycle Models area)

### Canonical Frameworks & Lifecycle Models
- Candidate lifecycle frameworks: *Fundamentals of Data Engineering* (Reimer & Reis) — Generation→Ingestion→Transformation→Serving→Consumption; DAMA-DMBOK knowledge areas; Kimball lifecycle methodology; *Designing Data-Intensive Applications* (Kleppmann)
- Evaluation criteria: industry adoption, completeness of lifecycle coverage, applicability to skill design, alignment with modern data stack practices
- How each framework maps to the pipeline lifecycle stages relevant to skill organization
- Community consensus on authoritative references for modern data engineering
- Output: a recommended canonical reference set, with the lifecycle model to use as the organizing spine for skill framing

### Skill Design
- Phased execution producing checkable artifacts at each phase
- Agentic planning best practices (plan → execute → resume → verify)
- Atomic vs. composite skill decomposition
- Skill input/output schemas
- Resumability (picking up mid-execution after interruption)
- Skill documentation standards and example invocations
- Deterministic phase gate patterns: Python/CLI checks that validate each artifact before the next phase begins, without requiring LLM judgment
- Claude Code hooks ecosystem (PostToolUse, PreToolUse, Stop) as a mechanism for automatically triggering checks in response to agent tool events
- Shared vs. per-skill check composition: common checks in `skills/_shared/checks/`, domain-specific checks in `skills/<skill-name>/checks/`
- Error surfacing: check output must be actionable and precise enough for an agent to self-correct without ambiguity

## Constraints

- **Cross-provider compatibility:** All skill instructions must produce equivalent
  behavior on Claude, GitHub Copilot, and OpenAI. Use Markdown headers for
  structure. Do not rely on XML tags or model-specific behaviors.
- **Phased artifacts:** Each skill must produce discrete, inspectable artifacts
  at each phase so that standards and quality checks can run between phases.
- **Deterministic phase gates:** Every phase transition must include at least one
  deterministic check — a Python script or CLI command that validates the artifact
  without LLM judgment. LLM review is not a phase gate.
- **Agentic best practices:** Every skill must include explicit planning,
  execution, resumption, and verification steps.
- **Framework-grounded:** Ground skill framing in canonical data engineering
  references. The specific lifecycle model(s) are determined from research — see
  the Canonical Frameworks & Lifecycle Models characteristic area.

## Phases

This work is a multi-phase, multi-plan effort. Each phase produces its own
implementation plan. Do not plan later phases until earlier phases complete —
later phases are shaped by earlier findings.

### Phase 1: Research Foundation

**Scope:** Structured research and context distillation across all
characteristic areas listed above.

Produces:
- One `docs/research/` document per characteristic area via `/wos:research`
- One or more `docs/context/` documents per area via `/wos:distill`
- Index files (`docs/research/_index.md`, `docs/context/_index.md`)

Research tasks are independent and can be dispatched in parallel. Each task
should be framed as a focused investigation question so that `/wos:research`
produces coherent sub-questions and SIFT-verified findings.

Distillation follows research. The distiller determines context file
boundaries — see Research & Distillation Conventions below.

### Phase 2: Skill Discovery

**Scope:** Brainstorm and design which skills to build, based on the
research corpus.

Run `/wos:brainstorm` on the full `docs/context/` corpus to identify and
prioritize skill candidates. The output is a design document — not code,
not a plan. Do not pre-plan skill discovery; let the research findings
shape it.

### Phase 3: Skill Authoring

**Scope:** Author skills per the approved skill design document from Phase 2.

Each skill produces the artifacts described in Skill Output Format below.

## Research & Distillation Conventions

### Research Artifacts
- Produced by `/wos:research`, which conducts SIFT-based investigations
  and produces verified research documents
- Stored in `docs/research/` as `YYYY-MM-DD-<area>.research.md`
- Each research task is framed as a focused investigation question
- Research tasks are independent — dispatch in parallel

### Context Artifacts
- Produced by `/wos:distill`, which synthesizes research into operational
  guidance
- Stored in `docs/context/<topic>.md`
- Follow AGENTS.md conventions:
  - YAML frontmatter with `name`, `description`, and `type` fields
  - 200–800 words per file
  - One concept per file
  - Key insights first and last; supplemental detail in the middle
- Distillation determines file boundaries: split if sub-topics are distinct
  (e.g., Kimball vs. data vault vs. OBT), merge if significant overlap with
  another area. Document splits and merges in commit messages.

### Index Files
- `docs/research/_index.md` and `docs/context/_index.md` list all files
  with their `name` and `description` frontmatter fields
- Created after all distillation is complete

## Skill Output Format

For each skill (Phase 3), produce:
1. `skills/<skill-name>/SKILL.md` — following the `dos` plugin structure
2. `skills/<skill-name>/checks/*.py` — deterministic phase gate scripts specific to this skill
3. `skills/_shared/checks/*.py` — reusable checks composable across skills (row counts, schema validation, freshness, YAML structure); create or extend as needed

Each skill references corresponding `docs/context/` documents produced in
Phase 1 — these are not re-created during skill authoring.

## Success Criteria

A skill is complete when it:
- Covers the full phase sequence for its domain (scope → build → verify)
- Produces inspectable artifacts at each phase
- Every phase transition has a deterministic check that validates the artifact
- Executes consistently on Claude, Copilot, and OpenAI
- Has a corresponding context document with sourced research
- Maps to the lifecycle framing from the canonical framework selected during research
