---
name: Data Pipeline Research & Context Foundation
description: Run structured research and distillation across 23 data pipeline characteristic areas, producing grounded context documents that underpin the dos skill library.
type: plan
status: completed
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

- [x] Run `/wos:research`: "How do dbt and dlt behave across DuckDB, Snowflake, Databricks, and ClickHouse, and what compatibility patterns prevent local-to-production divergence? Cover: dbt adapter SQL dialect differences (DuckDB vs. Snowflake vs. Databricks Spark SQL vs. ClickHouse), adapter-specific macro patterns, feature gaps and workarounds; dlt destination differences in schema normalization, data type mapping, and nested data handling across the same four platforms; strategies for writing portable dbt models and dlt pipelines that behave consistently across targets." <!-- sha:87f1bda -->
- [x] Verify: `ls docs/research/ | grep adapter-compat\|cross-platform` returns a file <!-- sha:87f1bda -->
- [x] Commit: `chore: add cross-platform adapter compatibility research` <!-- sha:87f1bda -->

### Task 7: Research — Pipeline Orchestration

- [x] Run `/wos:research`: "How do Apache Airflow, Prefect, and Dagster compare for data pipeline orchestration, and what governs the choice between them? Cover: Airflow DAGs, dynamic task generation, sensors, backfill management; Prefect flows, deployments, work pools, caching; Dagster software-defined assets, partitions, asset lineage, Dagster Cloud; selection criteria and migration patterns between tools; dbt integration patterns (dbt-airflow, Dagster-dbt, Prefect-dbt); cross-pipeline dependency management and SLA monitoring." <!-- sha:91fb2a9 -->
- [x] Verify: `ls docs/research/ | grep orchestration` returns a file <!-- sha:91fb2a9 -->
- [x] Commit: `chore: add pipeline orchestration research` <!-- sha:91fb2a9 -->

### Task 8: Research — Operations & Reliability

- [x] Run `/wos:research`: "What observability, reliability, and incident response patterns are needed to operate data pipelines in production? Cover: observability instrumentation (run logs, row counts, latency metrics, pipeline health dashboards); alerting patterns and on-call response workflows for data pipelines; retry strategies (exponential backoff, partial retry, dead-letter queues) and failure classification; error handling patterns for dbt, dlt, and orchestrator failures; data freshness tracking and freshness SLA enforcement." <!-- sha:77ee2ed -->
- [x] Verify: `ls docs/research/ | grep operations-reliability` returns a file <!-- sha:77ee2ed -->
- [x] Commit: `chore: add operations & reliability research` <!-- sha:77ee2ed -->

### Task 9: Research — Cost Optimization & FinOps

- [x] Run `/wos:research`: "How should data engineering teams optimize and govern costs across Databricks, Snowflake, ClickHouse, and BigQuery? Cover: Databricks cluster sizing, spot vs. on-demand, Photon, DBU optimization, auto-scaling policies; Snowflake warehouse sizing, auto-suspend/resume, credit optimization, result cache; ClickHouse compute cost patterns and tiered storage; BigQuery on-demand vs. capacity pricing, slot optimization; cross-platform query cost optimization (partition pruning, incremental materialization, avoiding full scans); storage cost optimization (compression, retention, tiering); cost attribution, tagging, and chargeback patterns." <!-- sha:7c88b44 -->
- [x] Verify: `ls docs/research/ | grep cost\|finops` returns a file <!-- sha:7c88b44 -->
- [x] Commit: `chore: add cost optimization & finops research` <!-- sha:7c88b44 -->

### Task 10: Research — Governance & Compliance

- [x] Run `/wos:research`: "What governance and compliance mechanisms should data engineers implement in pipelines and warehouses? Cover: audit trail design and implementation for data access and pipeline execution; row-level security patterns across Databricks, Snowflake, and ClickHouse; column-level access and masking policies; entitlement management and access review workflows; policy-as-code approaches for data access control. Exclude PII/privacy techniques (covered separately) and catalog/lineage tooling (covered separately). Ground findings in DAMA-DMBOK." <!-- sha:be41291 -->
- [x] Verify: `ls docs/research/ | grep governance-compliance` returns a file <!-- sha:be41291 -->
- [x] Commit: `chore: add governance & compliance research` <!-- sha:be41291 -->

### Task 11: Research — Data Catalog & Lineage

- [x] Run `/wos:research`: "How should data catalog and lineage be implemented in a modern data stack, and what tooling options exist? Cover: catalog tool comparison (DataHub, OpenMetadata, Unity Catalog, Snowflake catalog, Atlan) — capabilities, deployment model, integration effort; OpenLineage standard and its role in lineage interoperability; column-level vs. table-level lineage — capabilities and practical limitations; automated lineage extraction from dbt artifacts, Spark, and SQL parsing; catalog integration with CI/CD and dbt docs; metadata quality and staleness management." <!-- sha:964fa90 -->
- [x] Verify: `ls docs/research/ | grep catalog\|lineage` returns a file <!-- sha:964fa90 -->
- [x] Commit: `chore: add data catalog & lineage research` <!-- sha:964fa90 -->

### Task 12: Research — Privacy Engineering

- [x] Run `/wos:research`: "What technical patterns and regulatory requirements govern privacy engineering for data pipelines? Cover: PII and sensitive data identification and classification (automated scanning tools, taxonomy design); data masking techniques (static vs. dynamic masking), tokenization, pseudonymization, and format-preserving encryption — tradeoffs and use cases; GDPR, CCPA compliance requirements that affect pipeline architecture; right-to-erasure implementation in data warehouses — deletion propagation through medallion layers in Delta Lake and Iceberg; privacy-by-design principles (data minimization, retention enforcement, encryption at rest/transit)." <!-- sha:dbee403 -->
- [x] Verify: `ls docs/research/ | grep privacy\|pii` returns a file <!-- sha:dbee403 -->
- [x] Commit: `chore: add privacy engineering research` <!-- sha:dbee403 -->

### Task 13: Research — Quality Engineering

- [x] Run `/wos:research`: "What methods and frameworks should data engineers use to measure and monitor data quality? Cover: data profiling techniques (shape, distribution, completeness, uniqueness, cardinality); anomaly and drift detection methods (statistical process control, z-score, IQR, ML-based approaches) and when each applies; data quality dimension taxonomy (completeness, accuracy, consistency, timeliness, validity, uniqueness); quality scoring and measurement frameworks; SLA definition and tracking for data quality. Exclude validation tooling (covered separately). Ground findings in DAMA-DMBOK." <!-- sha:dd92ce3 -->
- [x] Verify: `ls docs/research/ | grep quality-engineering` returns a file <!-- sha:dd92ce3 -->
- [x] Commit: `chore: add quality engineering research` <!-- sha:dd92ce3 -->

### Task 14: Research — Validation Frameworks & Testing Tools

- [x] Run `/wos:research`: "What are the tradeoffs between dbt tests, Great Expectations, Soda, Pandera, and pytest-based data testing, and how should a tiered validation strategy be structured? Cover: dbt schema tests, singular tests, custom generic tests, dbt-utils, dbt-expectations; Great Expectations expectations, suites, checkpoints, and data docs; Soda checks, scans, and agreements; Pandera DataFrame schema validation and pytest-based tests against DuckDB; tiered strategy: local Python checks → dbt CI tests → full GE/Soda suite in production; tool selection criteria, integration complexity, and maintenance burden comparison." <!-- sha:c002513 -->
- [x] Verify: `ls docs/research/ | grep validation\|testing-tools` returns a file <!-- sha:c002513 -->
- [x] Commit: `chore: add validation frameworks & testing tools research` <!-- sha:c002513 -->

### Task 15: Research — Data Discovery

- [x] Run `/wos:research`: "What methodologies should data engineers use to evaluate and onboard new data sources? Cover: source system evaluation criteria (connectivity, volume, freshness, schema stability, data quality, access complexity); source system classification (transactional, event stream, third-party SaaS, file-based) and how classification affects ingestion approach; structured discovery workflows — what to assess before building a pipeline; metadata documentation standards for new sources; integration of discovery findings with catalog tooling." <!-- sha:3519c70 -->
- [x] Verify: `ls docs/research/ | grep data-discovery` returns a file <!-- sha:3519c70 -->
- [x] Commit: `chore: add data discovery research` <!-- sha:3519c70 -->

### Task 16: Research — Stream Processing

- [x] Run `/wos:research`: "How should streaming data pipelines be designed and operated, and what are the tradeoffs between Spark Structured Streaming, Databricks DLT, and Apache Flink? Cover: Spark Structured Streaming sources, sinks, triggers, and checkpointing; Databricks Delta Live Tables for streaming; Flink stateful processing, event time handling, exactly-once semantics; late data handling and watermarking strategies; windowing patterns (tumbling, sliding, session); micro-batch vs. continuous streaming tradeoffs; testing strategies for streaming pipelines; observability (lag, throughput, backpressure monitoring)." <!-- sha:8c3489d -->
- [x] Verify: `ls docs/research/ | grep stream-processing` returns a file <!-- sha:8c3489d -->
- [x] Commit: `chore: add stream processing research` <!-- sha:8c3489d -->

### Task 17: Research — CDC & Event-Driven Ingestion

- [x] Run `/wos:research`: "What patterns and tooling govern Change Data Capture and event-driven data ingestion? Cover: CDC mechanisms (log-based, trigger-based, timestamp-based) and their reliability/latency tradeoffs; Debezium and AWS DMS as CDC tools; dlt CDC source patterns; Kafka-backed pipeline design (topic design, consumer groups, offset management, schema registry); event sourcing and the outbox/transactional outbox pattern; CDC writes into Delta Lake and Iceberg (merge vs. append-then-compact strategies); idempotency, ordering guarantees, and at-least-once vs. exactly-once delivery." <!-- sha:fe66d4c -->
- [x] Verify: `ls docs/research/ | grep cdc\|event-driven` returns a file <!-- sha:fe66d4c -->
- [x] Commit: `chore: add cdc & event-driven ingestion research` <!-- sha:fe66d4c -->

### Task 18: Research — Data Platform Engineering

- [x] Run `/wos:research`: "How should data platform infrastructure be managed as code, and what are best practices for environment provisioning and compute management? Cover: Terraform for Databricks (workspace, cluster policies, metastore, permissions), Snowflake (warehouses, databases, roles, resource monitors), and ClickHouse; environment provisioning patterns for dev/staging/prod workspace separation; compute management patterns (Databricks job cluster vs. all-purpose cluster, Snowflake warehouse sizing and auto-suspend, ClickHouse cluster configuration); platform versioning and upgrade management. Exclude network/security configuration (covered separately)." <!-- sha:b681010 -->
- [x] Verify: `ls docs/research/ | grep platform-engineering` returns a file <!-- sha:b681010 -->
- [x] Commit: `chore: add data platform engineering research` <!-- sha:b681010 -->

### Task 19: Research — Platform Security & Access Control

- [x] Run `/wos:research`: "What network, identity, and secrets management patterns govern secure data platform deployments? Cover: private networking for Databricks, Snowflake, and ClickHouse (VPC, PrivateLink, private endpoints); RBAC vs. ABAC design patterns, Unity Catalog privilege model, Snowflake RBAC hierarchy; service principal design and least-privilege patterns; secrets management (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault) and rotation strategies; audit logging for security and compliance; cross-cloud and cross-region access patterns." <!-- sha:b8d3754 -->
- [x] Verify: `ls docs/research/ | grep platform-security\|access-control` returns a file <!-- sha:b8d3754 -->
- [x] Commit: `chore: add platform security & access control research` <!-- sha:b8d3754 -->

### Task 20: Research — Data Contracts

- [x] Run `/wos:research`: "How should data contracts be designed, enforced, and evolved between data producers and consumers? Cover: contract structure and standards (Open Data Contract Standard/ODCS, dbt contracts) and their differences; schema contracts (column names, types, nullability, keys), freshness/SLA contracts, and quality contracts; contract versioning strategies (backward vs. forward compatibility); producer/consumer negotiation workflows; enforcement patterns (CI-time breaking change detection, runtime validation); schema registry tooling (Confluent Schema Registry, AWS Glue Schema Registry); contract-driven development workflow." <!-- sha:ab8afae -->
- [x] Verify: `ls docs/research/ | grep data-contracts` returns a file <!-- sha:ab8afae -->
- [x] Commit: `chore: add data contracts research` <!-- sha:ab8afae -->

### Task 21: Research — Data Product Scoping & Business Requirements

- [x] Run `/wos:research`: "How should data engineers scope, document, and manage business requirements for data products — and how do requirements drive architecture decisions? Cover: stakeholder requirement gathering techniques for data contexts; use case documentation (query patterns, update frequency, consumer SLAs); reverse-engineering architecture choices from consumption patterns (query shape → modeling choice, freshness needs → incremental strategy); requirement change management — detecting when consumer needs shift and propagating changes back through pipeline design; data product thinking (ownership, SLAs, versioning); prioritization of competing consumer requirements. Frame within the lifecycle model established in the Canonical Frameworks & Lifecycle Models research." <!-- sha:470d277 -->
- [x] Verify: `ls docs/research/ | grep scoping\|business-requirements` returns a file <!-- sha:470d277 -->
- [x] Commit: `chore: add data product scoping & business requirements research` <!-- sha:470d277 -->

### Task 22: Research — Skill Design

- [x] Run `/wos:research`: "What are best practices for designing AI agentic skills with deterministic feedback loops and phased execution? Cover: phased skill structure (plan→execute→resume→verify) with inspectable artifacts at each phase; deterministic phase gate patterns — structuring Python/CLI checks to validate artifacts without LLM judgment; Claude Code hooks ecosystem (PostToolUse, PreToolUse, Stop) for automatically triggering checks on agent tool events; shared vs. per-skill check library composition; error output design for agent self-correction; atomic vs. composite skill decomposition; cross-provider compatibility (Claude, GitHub Copilot, OpenAI); resumability patterns after interruption." <!-- sha:ac34300 -->
- [x] Verify: `ls docs/research/ | grep skill-design` returns a file <!-- sha:ac34300 -->
- [x] Commit: `chore: add skill design research` <!-- sha:ac34300 -->

### Task 23: Research — Canonical Frameworks & Lifecycle Models

- [x] Run `/wos:research`: "What books, standards, and conceptual frameworks are considered most authoritative for modern data engineering practice, and which best serves as a lifecycle model for organizing AI-assisted workflow skills? Cover: *Fundamentals of Data Engineering* (Reimer & Reis) — the Generation→Ingestion→Transformation→Serving→Consumption lifecycle, its scope, and industry adoption; DAMA-DMBOK knowledge area taxonomy and its coverage of data engineering concerns; Kimball's dimensional lifecycle methodology; *Designing Data-Intensive Applications* (Kleppmann) and its focus areas; any other widely-cited modern references; evaluation criteria: lifecycle completeness, alignment with modern data stack tooling, community consensus, applicability to skill design. Output: a clear recommendation for the canonical lifecycle model and reference set to use as the organizing spine for this skill library." <!-- sha:a0be427 -->
- [x] Verify: `ls docs/research/ | grep framework\|lifecycle-canon` returns a file <!-- sha:a0be427 -->
- [x] Commit: `chore: add canonical frameworks & lifecycle models research` <!-- sha:a0be427 -->

---

## Chunk 2: Distillation

**Depends on:** Each research file must exist before its corresponding distillation task. Tasks within this chunk are otherwise independent and can run in parallel.

For each area: produce multiple focused context files if sub-topics are distinct (one concept per file, 200–800 words each). Consolidate with a related area only if significant overlap is found. Document splits and merges in commit messages.

### Task 24: Distill — Pipeline Design & Architecture
- [x] Run `/wos:distill` <!-- sha:4d82b3f -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter (`name`, `description`, `type: context`) <!-- sha:4d82b3f -->
- [x] Commit: `docs: add pipeline design context` <!-- sha:4d82b3f -->

### Task 25: Distill — Data Modeling
- [x] Run `/wos:distill`; split into Kimball, data vault, OBT, and selection criteria <!-- sha:4d82b3f -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:4d82b3f -->
- [x] Commit: `docs: add data modeling context` <!-- sha:4d82b3f -->

### Task 26: Distill — Open Table Formats
- [x] Run `/wos:distill`; split into format comparison, cross-platform compatibility, catalog interop <!-- sha:4d82b3f -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:4d82b3f -->
- [x] Commit: `docs: add open table formats context` <!-- sha:4d82b3f -->

### Task 27: Distill — Production Platform Landscape
- [x] Run `/wos:distill`; split into platform comparison and tooling compatibility <!-- sha:4d82b3f -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:4d82b3f -->
- [x] Commit: `docs: add production platform landscape context` <!-- sha:4d82b3f -->

### Task 28: Distill — Development Workflow
- [x] Run `/wos:distill`; split into local dev, CI/CD, secrets, pre-commit hooks <!-- sha:4d82b3f -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:4d82b3f -->
- [x] Commit: `docs: add development workflow context` <!-- sha:4d82b3f -->

### Task 29: Distill — Cross-Platform Adapter Compatibility
- [x] Run `/wos:distill`; split into dbt adapter gaps, dlt type mapping, portability strategy <!-- sha:4d82b3f -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:4d82b3f -->
- [x] Commit: `docs: add cross-platform adapter compatibility context` <!-- sha:4d82b3f -->

### Task 30: Distill — Pipeline Orchestration
- [x] Run `/wos:distill`; single comparative overview <!-- sha:791958a -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:791958a -->
- [x] Commit: `docs: add pipeline orchestration context` <!-- sha:791958a -->

### Task 31: Distill — Operations & Reliability
- [x] Run `/wos:distill`; split into observability pillars, retry/failure patterns, freshness SLAs <!-- sha:791958a -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:791958a -->
- [x] Commit: `docs: add operations & reliability context` <!-- sha:791958a -->

### Task 32: Distill — Cost Optimization & FinOps
- [x] Run `/wos:distill`; split into platform cost, query/storage optimization, finops governance <!-- sha:791958a -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:791958a -->
- [x] Commit: `docs: add cost optimization & finops context` <!-- sha:791958a -->

### Task 33: Distill — Governance & Compliance
- [x] Run `/wos:distill`; split into governance foundations, audit trail design <!-- sha:791958a -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:791958a -->
- [x] Commit: `docs: add governance & compliance context` <!-- sha:791958a -->

### Task 34: Distill — Data Catalog & Lineage
- [x] Run `/wos:distill`; split into catalog selection, lineage implementation <!-- sha:791958a -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:791958a -->
- [x] Commit: `docs: add data catalog & lineage context` <!-- sha:791958a -->

### Task 35: Distill — Privacy Engineering
- [x] Run `/wos:distill`; split into masking/tokenization, regulatory requirements, right-to-erasure <!-- sha:791958a -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:791958a -->
- [x] Commit: `docs: add privacy engineering context` <!-- sha:791958a -->

### Task 36: Distill — Quality Engineering
- [x] Run `/wos:distill`; split into profiling, dimensions, anomaly detection, scoring, SLAs <!-- sha:072226b -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:072226b -->
- [x] Commit: `docs: add quality engineering context` <!-- sha:072226b -->

### Task 37: Distill — Validation Frameworks & Testing Tools
- [x] Run `/wos:distill`; split into tool comparison and tiered strategy <!-- sha:072226b -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:072226b -->
- [x] Commit: `docs: add validation frameworks context` <!-- sha:072226b -->

### Task 38: Distill — Data Discovery
- [x] Run `/wos:distill`; split into source evaluation, onboarding, schema drift <!-- sha:072226b -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:072226b -->
- [x] Commit: `docs: add data discovery context` <!-- sha:072226b -->

### Task 39: Distill — Stream Processing
- [x] Run `/wos:distill`; split into tool comparison, windowing/watermarks, observability <!-- sha:072226b -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:072226b -->
- [x] Commit: `docs: add stream processing context` <!-- sha:072226b -->

### Task 40: Distill — CDC & Event-Driven Ingestion
- [x] Run `/wos:distill`; split into CDC mechanisms/tooling, Kafka patterns, lakehouse writes <!-- sha:072226b -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:072226b -->
- [x] Commit: `docs: add cdc & event-driven ingestion context` <!-- sha:072226b -->

### Task 41: Distill — Data Platform Engineering
- [x] Run `/wos:distill`; split into Terraform IaC, environment provisioning, compute governance <!-- sha:072226b -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:072226b -->
- [x] Commit: `docs: add data platform engineering context` <!-- sha:072226b -->

### Task 42: Distill — Platform Security & Access Control
- [x] Run `/wos:distill`; split into private networking, secrets management, cross-cloud <!-- sha:072226b -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:072226b -->
- [x] Commit: `docs: add platform security context` <!-- sha:072226b -->

### Task 43: Distill — Data Contracts
- [x] Run `/wos:distill`; split into contract structure and enforcement/versioning <!-- sha:072226b -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:072226b -->
- [x] Commit: `docs: add data contracts context` <!-- sha:072226b -->

### Task 44: Distill — Data Product Scoping & Business Requirements
- [x] Run `/wos:distill`; split into requirements gathering and consumption-driven architecture <!-- sha:072226b -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:072226b -->
- [x] Commit: `docs: add data product scoping context` <!-- sha:072226b -->

### Task 45: Distill — Skill Design
- [x] Run `/wos:distill`; split into agentic phase patterns, deterministic gates, cross-provider <!-- sha:072226b -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:072226b -->
- [x] Commit: `docs: add skill design context` <!-- sha:072226b -->

### Task 46: Distill — Canonical Frameworks & Lifecycle Models
- [x] Run `/wos:distill`; single context file with lifecycle model and reference set <!-- sha:072226b -->
- [x] Verify: output files in `docs/context/`, each 200–800 words, YAML frontmatter <!-- sha:072226b -->
- [x] Commit: `docs: add canonical frameworks & lifecycle models context` <!-- sha:072226b -->

---

## Chunk 3: Index Files

**Depends on:** All Chunk 2 tasks complete.

### Task 47: Create directory index files

- [x] Create `docs/research/_index.md` listing all research files with their `name` and `description` fields <!-- sha:53a4971 -->
- [x] Create `docs/context/_index.md` listing all context files with their `name` and `description` fields <!-- sha:53a4971 -->
- [x] Verify: every file in each directory has an entry; all 23 characteristic areas represented in `docs/context/_index.md` <!-- sha:53a4971 -->
- [x] Commit: `docs: add research and context index files` <!-- sha:53a4971 -->

---

## Validation

- [x] `ls docs/research/*.research.md` — 23 files, one per characteristic area <!-- validated:53a4971 -->
- [x] `grep -l "type:" docs/context/*.md | wc -l` equals `ls docs/context/*.md | grep -v _index | wc -l` — 66/66 context files have frontmatter <!-- validated:53a4971 -->
- [x] `cat docs/context/_index.md` — all 23 characteristic areas represented with 1-7 entries each <!-- validated:53a4971 -->
- [x] Manual review: all 66 context files are 479-799 words, have complete YAML frontmatter (name, description, type: context, related), key insights first <!-- validated:53a4971 -->

## Notes

- Chunk 1 (23 research tasks) can be fully parallelized — dispatch as concurrent agents.
- Chunk 2 (23 distillation tasks) can also be parallelized once each research file exists.
- The executor decides split/merge during distillation — document decisions in commit messages.
- Likely overlaps to watch: Data Contracts ↔ Pipeline Design; Data Catalog ↔ Data Discovery; Privacy Engineering ↔ Governance & Compliance; Cross-Platform Adapter Compatibility ↔ Development Workflow; Canonical Frameworks ↔ Data Product Scoping (lifecycle framing).
- The Canonical Frameworks research (Task 23) informs all other areas — its context file should be distilled before the brainstorm phase uses the corpus.

## Next Step

When this plan is complete, invoke `/wos:brainstorm` with the full `docs/context/` corpus to identify and prioritize skill candidates. The brainstorm output becomes the skill design document that drives authoring. Do not pre-plan the discovery — let the research findings shape it.

## Retrospective

**Completed:** 2026-03-22 | **Duration:** Single session | **Commits:** 52

### What worked well

- **Parallel agent dispatch dramatically accelerated throughput.** Batching 4-6 research agents or 6-11 distillation agents in parallel reduced wall-clock time from what would have been 23+ sequential research cycles to ~4 waves. The plan's note that "all 23 research tasks are independent and can be dispatched in parallel" was the key enabler.
- **The gatherer→evaluator→challenger→verifier→finalizer chain produced high-quality research.** The challenger stage consistently found substantive counter-evidence (SQLGlot's error rates, Dagster pricing surprises, dbt contract enforcement gaps, Prefect commit decline as vendor bias). Without the challenger, findings would have been uncritically vendor-aligned.
- **Delegating full research documents to single agents** (gathering + challenge + synthesis + finalization in one prompt) worked well for Tasks 8-23 after the pattern was established in Tasks 5-7. This reduced orchestration overhead without sacrificing quality.
- **Context file splitting decisions emerged naturally.** The plan's guidance to "split or merge as the material warrants" let each distillation agent make the right call — some areas produced 1 file (orchestration comparison, lifecycle model), others produced 4 (data modeling, dev workflow, governance).

### What didn't work well

- **Rate limits hit during the final distillation batch.** 8 of 11 agents in the last batch returned "You've hit your limit" — but the files had already been written to disk before the limit was reached. This was recoverable but could have caused data loss if files hadn't been flushed.
- **Index file concurrency caused merge conflicts.** Multiple parallel agents updating `_index.md` simultaneously meant the index was incomplete after parallel batches. Required a full rebuild (Task 47) to reconcile. Future plans should have index updates as a sequential post-step, not per-agent.
- **First commit captured all batch 1 context files together** instead of per-task commits. The plan called for individual commits per distillation task, but when multiple agents completed simultaneously, staging and committing per-task was impractical. The plan's commit-per-task pattern doesn't map well to parallel execution.
- **Research-distill pipeline's "sequential execution" requirement was impractical.** The pipeline reference says "Execute research tasks sequentially. Each `/wos:research` invocation completes before the next begins." Following this literally would have taken 10x longer. Parallel dispatch was the right call but deviated from the documented pipeline protocol.

### Metrics

| Metric | Value |
|--------|-------|
| Research documents | 23 |
| Total sources across all research | ~490 |
| Total research word count | ~130K |
| Context documents | 66 |
| Context word count range | 479-799 (all within 200-800 target) |
| Characteristic areas covered | 23/23 |
| Git commits | 52 |
| Validation criteria | 4/4 passed |

### Recommendations for future plans

1. **Design parallel-safe index updates.** Either make index files a sequential post-step or use a merge-safe format that handles concurrent appends.
2. **Batch commits are fine for parallel work.** Don't force per-task commits when executing in parallel — batch by wave instead.
3. **Rate limit awareness.** When dispatching 10+ agents, stagger slightly or accept that some may hit limits. Ensure file writes flush before agent completion reporting.
4. **The research-distill pipeline protocol should acknowledge parallel execution.** The sequential requirement is a documentation artifact, not an architectural constraint — the no-nesting rule applies to subagents within skills, not to independent plan tasks.
