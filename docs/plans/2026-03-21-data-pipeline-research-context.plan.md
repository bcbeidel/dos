---
name: Data Pipeline Research & Context Foundation
description: Run structured research and distillation across 23 data pipeline characteristic areas, producing grounded context documents that underpin the dos skill library.
type: plan
status: executing
related:
  - docs/prompts/data-pipeline-knowledge-foundation.prompt.md
---

# Data Pipeline Research & Context Foundation

**Goal:** Produce research documents and focused context documents across 23 characteristic areas covering the full data pipeline lifecycle. Areas are deliberately scoped to be focused — each research task covers one coherent domain with a clear investigation question. Research findings determine the final number and boundaries of context files: a task may produce multiple files if sub-topics are distinct, or consolidate with a related task if significant overlap emerges.

**Scope:**

Must have:
- At least one `docs/research/` document per characteristic area, produced by `wos:research`
- At least one `docs/context/` document per characteristic area, produced by `wos:distill`; split or merge as the material warrants
- Each context doc per AGENTS.md conventions: YAML frontmatter, 200–800 words, one concept per file, key insights first and last
- `docs/research/_index.md` and `docs/context/_index.md` listing all produced files with descriptions

Won't have:
- Any `skills/` SKILL.md files (those come after skill discovery and design)
- Code, scripts, or tooling
- Skill design decisions — those emerge in the brainstorm that follows

**Approach:** All 23 research tasks are independent and can be dispatched in parallel. Each task is framed as a focused investigation question to ensure `wos:research` produces coherent sub-questions and SIFT-verified findings. After each research document exists, `wos:distill` determines the right context file structure. Index files are created after all distillation is complete.

**Characteristic Areas:**

| # | Area | Key Concern |
|---|------|-------------|
| 1 | Pipeline Design & Architecture | Medallion layers, incremental patterns, schema evolution |
| 2 | Data Modeling | Kimball dimensional, data vault, OBT — tradeoffs and selection |
| 3 | Open Table Formats | Delta/Iceberg/Parquet/ORC/Avro — tradeoffs and cross-platform compatibility |
| 4 | Production Platform Landscape | ClickHouse, BigQuery, Redshift, Athena characteristics |
| 5 | Development Workflow | Local dev, CI/CD, env management, hooks |
| 6 | Cross-Platform Adapter Compatibility | dbt adapter dialect gaps, dlt destination differences across DuckDB/Snowflake/Databricks/ClickHouse |
| 7 | Pipeline Orchestration | Airflow, Prefect, Dagster — tradeoffs and dbt integration |
| 8 | Operations & Reliability | Observability, alerting, retry, freshness |
| 9 | Cost Optimization & FinOps | Databricks/Snowflake/ClickHouse cost management, query optimization |
| 10 | Governance & Compliance | Audit trails, RLS, entitlement management |
| 11 | Data Catalog & Lineage | DataHub, OpenMetadata, OpenLineage, automated lineage |
| 12 | Privacy Engineering | PII classification, masking, GDPR/CCPA, right-to-erasure |
| 13 | Quality Engineering | Profiling, anomaly detection, quality measurement, SLAs |
| 14 | Validation Frameworks & Testing Tools | dbt tests, GE, Soda, Pandera, pytest-based — tradeoffs |
| 15 | Data Discovery | Source evaluation and onboarding methodologies |
| 16 | Stream Processing | Spark Streaming, DLT, Flink, watermarking, windowing |
| 17 | CDC & Event-Driven Ingestion | CDC, Debezium, dlt CDC, Kafka, event sourcing |
| 18 | Data Platform Engineering | IaC, env provisioning, compute management |
| 19 | Platform Security & Access Control | Network, IAM, secrets, RBAC/ABAC |
| 20 | Data Contracts | ODCS, schema/SLA/quality contracts, enforcement, versioning |
| 21 | Data Product Scoping & Business Requirements | Consumer requirements, use cases, change propagation |
| 22 | Skill Design | Agentic best practices, deterministic gates, hooks |
| 23 | Canonical Frameworks & Lifecycle Models | Evaluate FoDE, DAMA-DMBOK, Kimball, DDIA — select lifecycle model for skill framing |

**File Changes:**
- Create: one or more `docs/research/YYYY-MM-DD-<area>.research.md` per characteristic area
- Create: one or more `docs/context/<topic>.md` per characteristic area (boundaries set during distillation)
- Create: `docs/research/_index.md`
- Create: `docs/context/_index.md`

**Branch:** `feat-data-pipeline-research-context`
**PR:** https://github.com/bcbeidel/dos/pull/2 (appended after each task)

---

## Chunk 1: Research

All 23 research tasks are independent and can be dispatched in parallel.

### Task 1: Research — Pipeline Design & Architecture

- [x] Run `/wos:research`: "How should batch data pipelines be structured and architected in a modern data stack? Cover: medallion/layered architecture (Bronze→Silver→Gold) and when to add or skip layers; batch vs. streaming selection criteria and decision framework; incremental loading patterns (full refresh, append, merge/upsert) and when to use each; backfill and historical load strategies; schema evolution and versioning approaches. Exclude data modeling approaches (covered separately) and storage format selection (covered separately)." <!-- sha:f79be50 -->
- [x] Verify: `ls docs/research/ | grep pipeline-design` returns a file <!-- sha:f79be50 -->
- [x] Commit: `chore: add pipeline design & architecture research` <!-- sha:f79be50 -->

### Task 2: Research — Data Modeling

- [x] Run `/wos:research`: "What are the tradeoffs between Kimball dimensional modeling, data vault, and wide table (OBT) approaches for analytics engineering, and how should the choice be made? Cover: Kimball star/snowflake schema, facts, dimensions, slowly changing dimensions; data vault hubs/links/satellites and business key design; OBT/wide table patterns and their query implications; selection criteria by use case, team maturity, and change frequency; how each approach adapts to DuckDB, Snowflake, Databricks, and ClickHouse storage targets. Ground findings in Kimball's *The Data Warehouse Toolkit* and DAMA-DMBOK." <!-- sha:90ea158 -->
- [x] Verify: `ls docs/research/ | grep data-modeling` returns a file <!-- sha:90ea158 -->
- [x] Commit: `chore: add data modeling research` <!-- sha:90ea158 -->

### Task 3: Research — Open Table Formats

- [x] Run `/wos:research`: "What are the tradeoffs between Delta Lake, Apache Iceberg, Apache Parquet, ORC, and Avro as data lake and lakehouse storage formats, and how should a format be chosen? Cover: ACID transaction support, time travel, schema evolution, and partition evolution per format; cross-platform read/write compatibility across Databricks, Snowflake, ClickHouse, BigQuery, Trino, and Spark; catalog compatibility implications (Unity Catalog, Snowflake catalogs, AWS Glue); ClickHouse native format interoperability with open formats; format selection criteria by use case (batch, streaming, CDC, cross-platform sharing)." <!-- sha:5adc78c -->
- [x] Verify: `ls docs/research/ | grep table-formats\|open-formats` returns a file <!-- sha:5adc78c -->
- [x] Commit: `chore: add open table formats research` <!-- sha:5adc78c -->

### Task 4: Research — Production Platform Landscape

- [x] Run `/wos:research`: "How do ClickHouse, BigQuery, Redshift, Athena, Databricks, and Snowflake compare as analytical data platforms, and what are the pipeline design implications of each?" (expanded from 4 to 6 platforms per user request) <!-- sha:b52689d -->
- [x] Verify: `ls docs/research/ | grep platform-landscape\|production-platform` returns a file <!-- sha:b52689d -->
- [x] Commit: `chore: add production platform landscape research` <!-- sha:b52689d -->

### Task 5: Research — Development Workflow

- [x] Run `/wos:research`: "What are best practices for a local-to-production data engineering development workflow using DuckDB, dlt, and dbt? Cover: local development end-to-end (source→DuckDB→tested artifact); environment management across local/staging/production; secrets and configuration management; CI/CD pipeline design for dbt and dlt projects (linting, testing, deployment); git hooks (pre-commit framework) and dbt hooks (on-run-start/end, pre/post-hook) as fast-feedback mechanisms. Exclude orchestration tooling (covered separately)." <!-- sha:1b1921b -->
- [x] Verify: `ls docs/research/ | grep development-workflow` returns a file <!-- sha:1b1921b -->
- [x] Commit: `chore: add development workflow research` <!-- sha:1b1921b -->

### Task 6: Research — Cross-Platform Adapter Compatibility

- [ ] Run `/wos:research`: "How do dbt and dlt behave across DuckDB, Snowflake, Databricks, and ClickHouse, and what compatibility patterns prevent local-to-production divergence? Cover: dbt adapter SQL dialect differences (DuckDB vs. Snowflake vs. Databricks Spark SQL vs. ClickHouse), adapter-specific macro patterns, feature gaps and workarounds; dlt destination differences in schema normalization, data type mapping, and nested data handling across the same four platforms; strategies for writing portable dbt models and dlt pipelines that behave consistently across targets."
- [ ] Verify: `ls docs/research/ | grep adapter-compat\|cross-platform` returns a file
- [ ] Commit: `chore: add cross-platform adapter compatibility research`

### Task 7: Research — Pipeline Orchestration

- [ ] Run `/wos:research`: "How do Apache Airflow, Prefect, and Dagster compare for data pipeline orchestration, and what governs the choice between them? Cover: Airflow DAGs, dynamic task generation, sensors, backfill management; Prefect flows, deployments, work pools, caching; Dagster software-defined assets, partitions, asset lineage, Dagster Cloud; selection criteria and migration patterns between tools; dbt integration patterns (dbt-airflow, Dagster-dbt, Prefect-dbt); cross-pipeline dependency management and SLA monitoring."
- [ ] Verify: `ls docs/research/ | grep orchestration` returns a file
- [ ] Commit: `chore: add pipeline orchestration research`

### Task 8: Research — Operations & Reliability

- [ ] Run `/wos:research`: "What observability, reliability, and incident response patterns are needed to operate data pipelines in production? Cover: observability instrumentation (run logs, row counts, latency metrics, pipeline health dashboards); alerting patterns and on-call response workflows for data pipelines; retry strategies (exponential backoff, partial retry, dead-letter queues) and failure classification; error handling patterns for dbt, dlt, and orchestrator failures; data freshness tracking and freshness SLA enforcement."
- [ ] Verify: `ls docs/research/ | grep operations-reliability` returns a file
- [ ] Commit: `chore: add operations & reliability research`

### Task 9: Research — Cost Optimization & FinOps

- [ ] Run `/wos:research`: "How should data engineering teams optimize and govern costs across Databricks, Snowflake, ClickHouse, and BigQuery? Cover: Databricks cluster sizing, spot vs. on-demand, Photon, DBU optimization, auto-scaling policies; Snowflake warehouse sizing, auto-suspend/resume, credit optimization, result cache; ClickHouse compute cost patterns and tiered storage; BigQuery on-demand vs. capacity pricing, slot optimization; cross-platform query cost optimization (partition pruning, incremental materialization, avoiding full scans); storage cost optimization (compression, retention, tiering); cost attribution, tagging, and chargeback patterns."
- [ ] Verify: `ls docs/research/ | grep cost\|finops` returns a file
- [ ] Commit: `chore: add cost optimization & finops research`

### Task 10: Research — Governance & Compliance

- [ ] Run `/wos:research`: "What governance and compliance mechanisms should data engineers implement in pipelines and warehouses? Cover: audit trail design and implementation for data access and pipeline execution; row-level security patterns across Databricks, Snowflake, and ClickHouse; column-level access and masking policies; entitlement management and access review workflows; policy-as-code approaches for data access control. Exclude PII/privacy techniques (covered separately) and catalog/lineage tooling (covered separately). Ground findings in DAMA-DMBOK."
- [ ] Verify: `ls docs/research/ | grep governance-compliance` returns a file
- [ ] Commit: `chore: add governance & compliance research`

### Task 11: Research — Data Catalog & Lineage

- [ ] Run `/wos:research`: "How should data catalog and lineage be implemented in a modern data stack, and what tooling options exist? Cover: catalog tool comparison (DataHub, OpenMetadata, Unity Catalog, Snowflake catalog, Atlan) — capabilities, deployment model, integration effort; OpenLineage standard and its role in lineage interoperability; column-level vs. table-level lineage — capabilities and practical limitations; automated lineage extraction from dbt artifacts, Spark, and SQL parsing; catalog integration with CI/CD and dbt docs; metadata quality and staleness management."
- [ ] Verify: `ls docs/research/ | grep catalog\|lineage` returns a file
- [ ] Commit: `chore: add data catalog & lineage research`

### Task 12: Research — Privacy Engineering

- [ ] Run `/wos:research`: "What technical patterns and regulatory requirements govern privacy engineering for data pipelines? Cover: PII and sensitive data identification and classification (automated scanning tools, taxonomy design); data masking techniques (static vs. dynamic masking), tokenization, pseudonymization, and format-preserving encryption — tradeoffs and use cases; GDPR, CCPA compliance requirements that affect pipeline architecture; right-to-erasure implementation in data warehouses — deletion propagation through medallion layers in Delta Lake and Iceberg; privacy-by-design principles (data minimization, retention enforcement, encryption at rest/transit)."
- [ ] Verify: `ls docs/research/ | grep privacy\|pii` returns a file
- [ ] Commit: `chore: add privacy engineering research`

### Task 13: Research — Quality Engineering

- [ ] Run `/wos:research`: "What methods and frameworks should data engineers use to measure and monitor data quality? Cover: data profiling techniques (shape, distribution, completeness, uniqueness, cardinality); anomaly and drift detection methods (statistical process control, z-score, IQR, ML-based approaches) and when each applies; data quality dimension taxonomy (completeness, accuracy, consistency, timeliness, validity, uniqueness); quality scoring and measurement frameworks; SLA definition and tracking for data quality. Exclude validation tooling (covered separately). Ground findings in DAMA-DMBOK."
- [ ] Verify: `ls docs/research/ | grep quality-engineering` returns a file
- [ ] Commit: `chore: add quality engineering research`

### Task 14: Research — Validation Frameworks & Testing Tools

- [ ] Run `/wos:research`: "What are the tradeoffs between dbt tests, Great Expectations, Soda, Pandera, and pytest-based data testing, and how should a tiered validation strategy be structured? Cover: dbt schema tests, singular tests, custom generic tests, dbt-utils, dbt-expectations; Great Expectations expectations, suites, checkpoints, and data docs; Soda checks, scans, and agreements; Pandera DataFrame schema validation and pytest-based tests against DuckDB; tiered strategy: local Python checks → dbt CI tests → full GE/Soda suite in production; tool selection criteria, integration complexity, and maintenance burden comparison."
- [ ] Verify: `ls docs/research/ | grep validation\|testing-tools` returns a file
- [ ] Commit: `chore: add validation frameworks & testing tools research`

### Task 15: Research — Data Discovery

- [ ] Run `/wos:research`: "What methodologies should data engineers use to evaluate and onboard new data sources? Cover: source system evaluation criteria (connectivity, volume, freshness, schema stability, data quality, access complexity); source system classification (transactional, event stream, third-party SaaS, file-based) and how classification affects ingestion approach; structured discovery workflows — what to assess before building a pipeline; metadata documentation standards for new sources; integration of discovery findings with catalog tooling."
- [ ] Verify: `ls docs/research/ | grep data-discovery` returns a file
- [ ] Commit: `chore: add data discovery research`

### Task 16: Research — Stream Processing

- [ ] Run `/wos:research`: "How should streaming data pipelines be designed and operated, and what are the tradeoffs between Spark Structured Streaming, Databricks DLT, and Apache Flink? Cover: Spark Structured Streaming sources, sinks, triggers, and checkpointing; Databricks Delta Live Tables for streaming; Flink stateful processing, event time handling, exactly-once semantics; late data handling and watermarking strategies; windowing patterns (tumbling, sliding, session); micro-batch vs. continuous streaming tradeoffs; testing strategies for streaming pipelines; observability (lag, throughput, backpressure monitoring)."
- [ ] Verify: `ls docs/research/ | grep stream-processing` returns a file
- [ ] Commit: `chore: add stream processing research`

### Task 17: Research — CDC & Event-Driven Ingestion

- [ ] Run `/wos:research`: "What patterns and tooling govern Change Data Capture and event-driven data ingestion? Cover: CDC mechanisms (log-based, trigger-based, timestamp-based) and their reliability/latency tradeoffs; Debezium and AWS DMS as CDC tools; dlt CDC source patterns; Kafka-backed pipeline design (topic design, consumer groups, offset management, schema registry); event sourcing and the outbox/transactional outbox pattern; CDC writes into Delta Lake and Iceberg (merge vs. append-then-compact strategies); idempotency, ordering guarantees, and at-least-once vs. exactly-once delivery."
- [ ] Verify: `ls docs/research/ | grep cdc\|event-driven` returns a file
- [ ] Commit: `chore: add cdc & event-driven ingestion research`

### Task 18: Research — Data Platform Engineering

- [ ] Run `/wos:research`: "How should data platform infrastructure be managed as code, and what are best practices for environment provisioning and compute management? Cover: Terraform for Databricks (workspace, cluster policies, metastore, permissions), Snowflake (warehouses, databases, roles, resource monitors), and ClickHouse; environment provisioning patterns for dev/staging/prod workspace separation; compute management patterns (Databricks job cluster vs. all-purpose cluster, Snowflake warehouse sizing and auto-suspend, ClickHouse cluster configuration); platform versioning and upgrade management. Exclude network/security configuration (covered separately)."
- [ ] Verify: `ls docs/research/ | grep platform-engineering` returns a file
- [ ] Commit: `chore: add data platform engineering research`

### Task 19: Research — Platform Security & Access Control

- [ ] Run `/wos:research`: "What network, identity, and secrets management patterns govern secure data platform deployments? Cover: private networking for Databricks, Snowflake, and ClickHouse (VPC, PrivateLink, private endpoints); RBAC vs. ABAC design patterns, Unity Catalog privilege model, Snowflake RBAC hierarchy; service principal design and least-privilege patterns; secrets management (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault) and rotation strategies; audit logging for security and compliance; cross-cloud and cross-region access patterns."
- [ ] Verify: `ls docs/research/ | grep platform-security\|access-control` returns a file
- [ ] Commit: `chore: add platform security & access control research`

### Task 20: Research — Data Contracts

- [ ] Run `/wos:research`: "How should data contracts be designed, enforced, and evolved between data producers and consumers? Cover: contract structure and standards (Open Data Contract Standard/ODCS, dbt contracts) and their differences; schema contracts (column names, types, nullability, keys), freshness/SLA contracts, and quality contracts; contract versioning strategies (backward vs. forward compatibility); producer/consumer negotiation workflows; enforcement patterns (CI-time breaking change detection, runtime validation); schema registry tooling (Confluent Schema Registry, AWS Glue Schema Registry); contract-driven development workflow."
- [ ] Verify: `ls docs/research/ | grep data-contracts` returns a file
- [ ] Commit: `chore: add data contracts research`

### Task 21: Research — Data Product Scoping & Business Requirements

- [ ] Run `/wos:research`: "How should data engineers scope, document, and manage business requirements for data products — and how do requirements drive architecture decisions? Cover: stakeholder requirement gathering techniques for data contexts; use case documentation (query patterns, update frequency, consumer SLAs); reverse-engineering architecture choices from consumption patterns (query shape → modeling choice, freshness needs → incremental strategy); requirement change management — detecting when consumer needs shift and propagating changes back through pipeline design; data product thinking (ownership, SLAs, versioning); prioritization of competing consumer requirements. Frame within the lifecycle model established in the Canonical Frameworks & Lifecycle Models research."
- [ ] Verify: `ls docs/research/ | grep scoping\|business-requirements` returns a file
- [ ] Commit: `chore: add data product scoping & business requirements research`

### Task 22: Research — Skill Design

- [ ] Run `/wos:research`: "What are best practices for designing AI agentic skills with deterministic feedback loops and phased execution? Cover: phased skill structure (plan→execute→resume→verify) with inspectable artifacts at each phase; deterministic phase gate patterns — structuring Python/CLI checks to validate artifacts without LLM judgment; Claude Code hooks ecosystem (PostToolUse, PreToolUse, Stop) for automatically triggering checks on agent tool events; shared vs. per-skill check library composition; error output design for agent self-correction; atomic vs. composite skill decomposition; cross-provider compatibility (Claude, GitHub Copilot, OpenAI); resumability patterns after interruption."
- [ ] Verify: `ls docs/research/ | grep skill-design` returns a file
- [ ] Commit: `chore: add skill design research`

### Task 23: Research — Canonical Frameworks & Lifecycle Models

- [ ] Run `/wos:research`: "What books, standards, and conceptual frameworks are considered most authoritative for modern data engineering practice, and which best serves as a lifecycle model for organizing AI-assisted workflow skills? Cover: *Fundamentals of Data Engineering* (Reimer & Reis) — the Generation→Ingestion→Transformation→Serving→Consumption lifecycle, its scope, and industry adoption; DAMA-DMBOK knowledge area taxonomy and its coverage of data engineering concerns; Kimball's dimensional lifecycle methodology; *Designing Data-Intensive Applications* (Kleppmann) and its focus areas; any other widely-cited modern references; evaluation criteria: lifecycle completeness, alignment with modern data stack tooling, community consensus, applicability to skill design. Output: a clear recommendation for the canonical lifecycle model and reference set to use as the organizing spine for this skill library."
- [ ] Verify: `ls docs/research/ | grep framework\|lifecycle-canon` returns a file
- [ ] Commit: `chore: add canonical frameworks & lifecycle models research`

---

## Chunk 2: Distillation

**Depends on:** Each research file must exist before its corresponding distillation task. Tasks within this chunk are otherwise independent and can run in parallel.

For each area: produce multiple focused context files if sub-topics are distinct (one concept per file, 200–800 words each). Consolidate with a related area only if significant overlap is found. Document splits and merges in commit messages.

### Task 24: Distill — Pipeline Design & Architecture
- [ ] Run `/wos:distill`
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter (`name`, `description`, `type: context`)
- [ ] Commit: `docs: add pipeline design context`

### Task 25: Distill — Data Modeling
- [ ] Run `/wos:distill`; consider splitting Kimball, data vault, and OBT if each is substantive
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add data modeling context`

### Task 26: Distill — Open Table Formats
- [ ] Run `/wos:distill`; consider splitting format comparison from cross-platform compatibility
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add open table formats context`

### Task 27: Distill — Production Platform Landscape
- [ ] Run `/wos:distill`; consider one comparative overview vs. per-platform files
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add production platform landscape context`

### Task 28: Distill — Development Workflow
- [ ] Run `/wos:distill`
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add development workflow context`

### Task 29: Distill — Cross-Platform Adapter Compatibility
- [ ] Run `/wos:distill`; consider splitting dbt adapter from dlt destination if both are rich
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add cross-platform adapter compatibility context`

### Task 30: Distill — Pipeline Orchestration
- [ ] Run `/wos:distill`; consider one comparative overview vs. per-tool files
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add pipeline orchestration context`

### Task 31: Distill — Operations & Reliability
- [ ] Run `/wos:distill`
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add operations & reliability context`

### Task 32: Distill — Cost Optimization & FinOps
- [ ] Run `/wos:distill`; consider splitting platform-specific cost from query/storage optimization
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add cost optimization & finops context`

### Task 33: Distill — Governance & Compliance
- [ ] Run `/wos:distill`
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add governance & compliance context`

### Task 34: Distill — Data Catalog & Lineage
- [ ] Run `/wos:distill`; consider splitting catalog tooling comparison from lineage standards
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add data catalog & lineage context`

### Task 35: Distill — Privacy Engineering
- [ ] Run `/wos:distill`; consider splitting masking/tokenization techniques from regulatory requirements
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add privacy engineering context`

### Task 36: Distill — Quality Engineering
- [ ] Run `/wos:distill`
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add quality engineering context`

### Task 37: Distill — Validation Frameworks & Testing Tools
- [ ] Run `/wos:distill`; consider splitting tool comparison from tiered strategy guidance
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add validation frameworks context`

### Task 38: Distill — Data Discovery
- [ ] Run `/wos:distill`
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add data discovery context`

### Task 39: Distill — Stream Processing
- [ ] Run `/wos:distill`; consider splitting tool comparison from windowing/watermarking patterns
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add stream processing context`

### Task 40: Distill — CDC & Event-Driven Ingestion
- [ ] Run `/wos:distill`; consider splitting CDC tooling from Kafka/event-sourcing patterns
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add cdc & event-driven ingestion context`

### Task 41: Distill — Data Platform Engineering
- [ ] Run `/wos:distill`
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add data platform engineering context`

### Task 42: Distill — Platform Security & Access Control
- [ ] Run `/wos:distill`; consider splitting network/IAM from secrets management
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add platform security context`

### Task 43: Distill — Data Contracts
- [ ] Run `/wos:distill`; consider splitting contract structure from enforcement/testing and versioning
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add data contracts context`

### Task 44: Distill — Data Product Scoping & Business Requirements
- [ ] Run `/wos:distill`; consider splitting requirement gathering from change propagation
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add data product scoping context`

### Task 45: Distill — Skill Design
- [ ] Run `/wos:distill`; consider splitting agentic phase patterns from deterministic gates/hooks
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add skill design context`

### Task 46: Distill — Canonical Frameworks & Lifecycle Models
- [ ] Run `/wos:distill`; distil into a single context file capturing the selected lifecycle model and canonical reference set with rationale
- [ ] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter
- [ ] Commit: `docs: add canonical frameworks & lifecycle models context`

---

## Chunk 3: Index Files

**Depends on:** All Chunk 2 tasks complete.

### Task 47: Create directory index files

- [ ] Create `docs/research/_index.md` listing all research files with their `name` and `description` fields
- [ ] Create `docs/context/_index.md` listing all context files with their `name` and `description` fields
- [ ] Verify: every file in each directory has an entry; all 23 characteristic areas represented in `docs/context/_index.md`
- [ ] Commit: `docs: add research and context index files`

---

## Validation

- [ ] `ls docs/research/*.research.md` — at least one file per characteristic area (23 areas)
- [ ] `grep -l "type:" docs/context/*.md | wc -l` equals `ls docs/context/*.md | grep -v _index | wc -l` — all context files have frontmatter
- [ ] `cat docs/context/_index.md` — all 23 characteristic areas represented with at least one entry each
- [ ] Manual review: each context file leads with key insights, closes with takeaways, stays under 800 words

## Notes

- Chunk 1 (23 research tasks) can be fully parallelized — dispatch as concurrent agents.
- Chunk 2 (23 distillation tasks) can also be parallelized once each research file exists.
- The executor decides split/merge during distillation — document decisions in commit messages.
- Likely overlaps to watch: Data Contracts ↔ Pipeline Design; Data Catalog ↔ Data Discovery; Privacy Engineering ↔ Governance & Compliance; Cross-Platform Adapter Compatibility ↔ Development Workflow; Canonical Frameworks ↔ Data Product Scoping (lifecycle framing).
- The Canonical Frameworks research (Task 23) informs all other areas — its context file should be distilled before the brainstorm phase uses the corpus.

## Next Step

When this plan is complete, invoke `/wos:brainstorm` with the full `docs/context/` corpus to identify and prioritize skill candidates. The brainstorm output becomes the skill design document that drives authoring. Do not pre-plan the discovery — let the research findings shape it.
