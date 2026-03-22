---
name: "Data Source Discovery & Onboarding"
description: "Source system evaluation requires assessment across six dimensions — connectivity, volume, freshness, schema stability, data quality, and access complexity — before writing any pipeline code; source classification (transactional, event stream, SaaS API, file-based) directly determines ingestion approach (full load, incremental, CDC); structured discovery workflows reduce onboarding time from months to weeks by front-loading profiling, quality assessment, and metadata documentation; data contracts (ODCS v3.1) formalize producer-consumer agreements around schema, quality, and SLAs; schema drift causes 7.8% of data quality incidents and production incidents increase 27% per percentage-point rise in drift rate; automated metadata catalogs decay without curation — manual-entry catalogs become untrusted within a year"
type: research
sources:
  - https://www.ovaledge.com/blog/data-discovery-steps
  - https://pathway.com/blog/data-discovery-to-data-pipeline-process/
  - https://dataflowmapper.com/blog/definitive-guide-data-onboarding
  - https://www.caitlinhudon.com/posts/2020/09/16/data-intake-form
  - https://www.brooklyndata.co/ideas/2024/12/18/how-to-design-an-effective-data-intake-process
  - https://www.splunk.com/en_us/blog/platform/clara-fication-data-onboarding-best-practices.html
  - https://lantern.splunk.com/Splunk_Success_Framework/Data_Management/Data_onboarding_workflow
  - https://dataengineeringdecoded.substack.com/p/full-load-vs-incremental-load-vs
  - https://dagster.io/learn/data-ingestion
  - https://pipeline2insights.substack.com/p/api-fundamentals-part2-pagination-and-rate-limit
  - https://datacontract-specification.com/
  - https://bitol-io.github.io/open-data-contract-standard/v3.1.0/
  - https://www.gambilldataengineering.com/data-engineering/how-to-survive-schema-drift-the-silent-killer-of-data-pipelines
  - https://www.integrate.io/blog/what-is-schema-drift-incident-count/
  - https://dlthub.com/docs/general-usage/schema-evolution
  - https://dlthub.com/docs/general-usage/schema-contracts
  - https://www.montecarlodata.com/blog-data-quality-statistics/
  - https://www.siffletdata.com/blog/metadata-catalog
  - https://www.techtarget.com/searchdatamanagement/definition/data-profiling
  - https://datacontract.com/
  - https://www.montecarlodata.com/blog-data-ingestion/
related:
  - docs/plans/2026-03-21-data-pipeline-research-context.plan.md
  - docs/research/2026-03-22-pipeline-orchestration.research.md
  - docs/research/2026-03-22-operations-reliability.research.md
  - docs/research/2026-03-22-quality-engineering.research.md
  - docs/research/2026-03-22-data-catalog-lineage.research.md
---

## Summary

**Research question:** What methodologies should data engineers use to evaluate and onboard new data sources?

**Mode:** Technical | **SIFT rigor:** High | **Sources:** 21 | **Searches:** 12 across Google

**Key findings:**
- Source system evaluation requires assessment across six dimensions — connectivity, volume, freshness, schema stability, data quality, and access complexity — before writing any pipeline code
- Source classification (transactional, event stream, SaaS API, file-based) directly determines ingestion approach: full load for small/stable dimensions, incremental for predictable change patterns, CDC for high-value transactional data requiring delete tracking and real-time fidelity
- Structured discovery workflows (8-step OvalEdge model) reduce onboarding from months to weeks by front-loading profiling, quality assessment, and metadata documentation before pipeline construction
- Data profiling has three distinct types — structure discovery, content discovery, and relationship discovery — each revealing different categories of issues that affect pipeline design
- Data contracts (ODCS v3.1, Data Contract Specification) formalize producer-consumer agreements around schema, quality rules, and SLAs, shifting accountability to the source system owner
- Schema drift causes 7.8% of all data quality incidents, and production incidents increase 27% per percentage-point rise in schema drift rate — making schema stability assessment a critical pre-onboarding gate
- Automated metadata catalogs that combine machine-harvested technical metadata with human-curated business metadata are essential for sustainable discovery; manual-only catalogs become untrusted within a year

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://www.ovaledge.com/blog/data-discovery-steps | Data Discovery Steps: 8-Step Workflow Guide | OvalEdge | 2024 | T4 | verified — vendor blog |
| 2 | https://pathway.com/blog/data-discovery-to-data-pipeline-process/ | Data Discovery to Data Pipeline Process | Pathway | 2024 | T4 | verified — vendor blog |
| 3 | https://dataflowmapper.com/blog/definitive-guide-data-onboarding | The Definitive Guide to Data Onboarding | DataFlowMapper | 2025 | T5 | verified — practitioner resource |
| 4 | https://www.caitlinhudon.com/posts/2020/09/16/data-intake-form | An Intake Form for Data Requests | Caitlin Hudon | 2020 | T5 | verified — practitioner blog |
| 5 | https://www.brooklyndata.co/ideas/2024/12/18/how-to-design-an-effective-data-intake-process | How to Design an Effective Data Intake Process | Brooklyn Data | 2024 | T5 | verified — consultancy blog |
| 6 | https://www.splunk.com/en_us/blog/platform/clara-fication-data-onboarding-best-practices.html | Data Onboarding Best Practices | Splunk | 2023 | T4 | verified — vendor blog |
| 7 | https://lantern.splunk.com/Splunk_Success_Framework/Data_Management/Data_onboarding_workflow | Data Onboarding Workflow | Splunk Lantern | current | T4 | verified — vendor framework |
| 8 | https://dataengineeringdecoded.substack.com/p/full-load-vs-incremental-load-vs | Full Load vs Incremental Load vs CDC | Data Engineering Decoded | 2025 | T5 | verified — practitioner blog |
| 9 | https://dagster.io/learn/data-ingestion | Data Ingestion | Dagster | current | T4 | verified — vendor educational |
| 10 | https://pipeline2insights.substack.com/p/api-fundamentals-part2-pagination-and-rate-limit | API Fundamentals: Pagination and Rate Limits | Pipeline2Insights | 2025 | T5 | verified — practitioner blog |
| 11 | https://datacontract-specification.com/ | Data Contract Specification | Data Contract community | current | T3 | verified — open standard |
| 12 | https://bitol-io.github.io/open-data-contract-standard/v3.1.0/ | Open Data Contract Standard v3.1.0 | Bitol / Linux Foundation | current | T2 | verified — Linux Foundation project |
| 13 | https://www.gambilldataengineering.com/data-engineering/how-to-survive-schema-drift-the-silent-killer-of-data-pipelines | How to Survive Schema Drift | Gambill Data Engineering | 2025 | T5 | verified — practitioner blog |
| 14 | https://www.integrate.io/blog/what-is-schema-drift-incident-count/ | Schema-Drift Incident Count for ETL Pipelines | Integrate.io | 2025 | T4 | verified — vendor blog |
| 15 | https://dlthub.com/docs/general-usage/schema-evolution | Schema Evolution | dlt | current docs | T1 | verified |
| 16 | https://dlthub.com/docs/general-usage/schema-contracts | Schema and Data Contracts | dlt | current docs | T1 | verified |
| 17 | https://www.montecarlodata.com/blog-data-quality-statistics/ | Data Quality Statistics from Monitoring 11M+ Tables | Monte Carlo | 2025 | T4 | verified — vendor blog (largest dataset) |
| 18 | https://www.siffletdata.com/blog/metadata-catalog | Metadata Catalog: The New Standard for Data Discovery | Sifflet | 2024 | T4 | verified — vendor blog |
| 19 | https://www.techtarget.com/searchdatamanagement/definition/data-profiling | What is Data Profiling? | TechTarget | current | T3 | verified — reference definition |
| 20 | https://datacontract.com/ | Data Contracts: Complete Guide | datacontract.com | current | T3 | verified — community resource |
| 21 | https://www.montecarlodata.com/blog-data-ingestion/ | Data Ingestion: Types, Challenges, Best Practices | Monte Carlo | 2024 | T4 | verified — vendor blog |

---

## Sub-question 1: Source System Evaluation Criteria

### The six evaluation dimensions

Before writing pipeline code, data engineers must evaluate each source system across six dimensions that determine whether a source is ready for integration and what ingestion approach is appropriate.

**1. Connectivity** — How does the source expose its data? Direct database access (JDBC/ODBC), REST API, event stream (Kafka/Kinesis), file drop (SFTP/S3), or webhook. Connectivity determines the fundamental ingestion pattern and the tooling required. Database connections support SQL-based extraction with full query flexibility. APIs impose pagination, rate limits, and authentication complexity. File-based sources require polling mechanisms and format parsing. Each access method has different failure modes, retry semantics, and throughput ceilings [9][10].

**2. Volume** — What is the data size at rest and the change rate over time? Volume determines whether full loads are feasible or incremental loading is required. Monte Carlo's analysis of 11M+ monitored tables shows that volume anomalies are one of the four primary categories of data quality incidents (alongside freshness, schema, and quality) [17]. Volume assessment must include peak vs. average metrics — Splunk recommends using the 95th percentile rather than averages for capacity planning because averages mask burst behavior [7].

**3. Freshness** — How frequently does the source update, and how stale can data be before it loses value? Freshness requirements drive the choice between batch (hours/daily), micro-batch (minutes), and streaming (seconds) ingestion. Sources with strict freshness SLAs require CDC or streaming ingestion; sources with daily tolerance can use simpler incremental batch patterns. Freshness also has a measurement component: the source must expose a reliable timestamp field (e.g., `updated_at`, `modified_date`) to support incremental extraction [8][17].

**4. Schema stability** — How frequently does the source schema change, and are changes announced in advance? Schema drift causes 7.8% of all data quality incidents [17], and production incidents increase by 27% for each percentage-point increase in schema drift rate [14]. Assessment includes: does the source owner notify consumers before schema changes? Is there a migration process that data teams can observe? Are schema changes versioned? Sources with high schema volatility — particularly third-party SaaS APIs — require schema validation at ingestion time and contract modes that quarantine or reject non-conforming data rather than silently propagating changes [13][15].

**5. Data quality** — What is the baseline quality of the source data? Pre-ingestion profiling across the DAMA-DMBOK dimensions (accuracy, completeness, consistency, timeliness, validity, uniqueness) establishes the quality baseline [19]. Critical questions include: what percentage of records have null values in key fields? Are there duplicate records? Do values conform to expected domains? A source with known quality issues requires defensive pipeline design — validation gates, quarantine tables, and reconciliation checks — that a clean source does not [3][17].

**6. Access complexity** — What authentication, authorization, and operational overhead is required to extract data? Access complexity ranges from simple (service account with read access to a database) to highly complex (OAuth2 token refresh flows, IP allowlisting, VPN tunnels, rate-limited API keys with per-endpoint quotas). Splunk's onboarding framework explicitly captures access details — host names, IP addresses, paths, credentials, and permissions — as part of the intake questionnaire because access problems are the most common onboarding blocker [6][7]. SaaS APIs compound access complexity with pagination schemes (offset, cursor, keyset) that vary per endpoint, sometimes within the same API [10].

---

## Sub-question 2: Source System Classification and Ingestion Approach Selection

### Four source system types

Source systems fall into four categories, each with distinct characteristics that constrain ingestion approach selection.

**Transactional databases** (PostgreSQL, MySQL, Oracle, SQL Server) store structured data modified through ACID transactions. They expose data via JDBC/ODBC and support SQL-based extraction. Key evaluation concerns: can the source tolerate extraction load during business hours? Does the schema include reliable timestamp columns for incremental extraction? Are hard deletes used, requiring CDC to capture? [8]

**Event streams** (Kafka, Kinesis, Pub/Sub, EventHub) emit append-only sequences of events in real time. They are self-describing (schema registry) or semi-structured (JSON payloads with variable fields). Key evaluation concerns: what is the retention period? Is there a schema registry enforcing compatibility? What is the partition strategy, and does it align with downstream consumption patterns? Event streams are the highest-fidelity source type but require streaming infrastructure to consume [9].

**Third-party SaaS APIs** (Salesforce, HubSpot, Stripe, Google Analytics) expose data through REST endpoints with vendor-controlled authentication, rate limits, and pagination. These are the most volatile source type — vendors change APIs without notice, deprecate endpoints, and impose breaking schema changes. Key evaluation concerns: what pagination scheme does the API use? What are the rate limits, and do they differ by endpoint? Is there a webhook alternative for push-based ingestion? Does a managed connector (Airbyte, Fivetran) exist and what is its quality tier? [10]

**File-based sources** (CSV, JSON, XML, Parquet files via SFTP, S3, email attachments) require polling or event-driven detection (S3 notifications). They have no query interface — you ingest the entire file. Key evaluation concerns: is the file format consistent across deliveries? Is there a manifest or checksum for integrity verification? What is the naming convention, and can arrival time be predicted? File-based sources are often the least reliable — schema changes appear as format changes without versioning, and delivery failures produce silent data gaps [8][9].

### Ingestion approach selection framework

The choice between full load, incremental load, and CDC is determined by five source characteristics [8]:

| Question | Full Load | Incremental | CDC |
|----------|-----------|-------------|-----|
| Source system stability? | Any | Predictable | Any |
| Change frequency? | Rare changes | Moderate, regular | High frequency |
| Retroactive corrections / backfills? | Acceptable | Problematic | Handled natively |
| Must track hard deletes? | No | No | Yes |
| Freshness requirement? | Hours/daily | Hours/daily | Minutes/real-time |

Full loads suit small reference tables (<1M records) where reload cost is lower than change-detection overhead. Incremental loads work when the source exposes reliable timestamp columns and changes follow predictable patterns. CDC is required when hard deletes must be captured, when the source receives backfills that modify historical records, or when near-real-time freshness is needed. Most production environments use a hybrid: full loads for small dimensions, incremental for regular fact tables, CDC for high-value transactional data [8].

CDC has a critical advantage over incremental loading for source system impact: since CDC reads the database transaction log rather than running queries against tables, it avoids full-table scans and reduces CPU/IO pressure on the source. Incremental queries still hit the source database, which can impact production workloads during extraction windows [8].

---

## Sub-question 3: Structured Discovery Workflows

### The 8-step discovery model

OvalEdge defines an 8-step data discovery workflow that structures the progression from fragmented data visibility to governed, pipeline-ready assets [1]:

1. **Define business objectives and scope** — Identify stakeholders, regulatory requirements, and measurable outcomes. Output: clarified discovery goals and success criteria.
2. **Identify and inventory data sources** — Document structured, semi-structured, and unstructured sources across databases, SaaS platforms, cloud storage, and data lakes. Output: comprehensive data inventory with ownership and location details.
3. **Validate access and permissions** — Confirm connectivity, define user permissions, ensure authorized retrieval capability. Output: documented access controls and secure connection validation.
4. **Assess data quality and structure** — Examine for missing values, duplicates, inconsistent formats, schema misalignment, and completeness. Output: quality assessment findings with fitness determination for intended use cases.
5. **Classify and contextualize data** — Identify sensitive/regulated data, apply business labels, assign ownership, align with use cases. Output: classification metadata and stewardship assignments.
6. **Prepare and refine data for analysis** — Clean records, standardize formats, resolve transformation gaps. Output: analysis-ready datasets with resolved inconsistencies.
7. **Explore and interpret insights** — Use visualizations to surface patterns, validate assumptions, identify gaps. Output: documented findings and collaborative insights.
8. **Document findings and establish governance** — Record metadata, confirm stewardship, maintain audit-ready documentation. Output: formalized governance framework and accessible data catalog entries.

The critical principle: steps 1-5 happen before any pipeline code is written. Discovery is assessment, not implementation. By validating quality and structure before building, teams avoid the expensive pattern of discovering issues during dashboard creation or executive reporting [1][2].

### Data profiling as the assessment foundation

Data profiling provides the measurement foundation for source evaluation. Three profiling types address different dimensions [19]:

**Structure discovery** examines how data is formatted and organized — field types, lengths, patterns, formatting consistency. This reveals whether a phone number field contains text or incorrect digit counts, whether date fields use consistent formats, and whether numeric fields contain non-numeric values.

**Content discovery** evaluates individual data values for accuracy and consistency — missing values, incorrect values, ambiguous data, and domain violations. Structure discovery is quantitative; content discovery is qualitative, asking whether the values are accurate and meaningful.

**Relationship discovery** analyzes connections between datasets — foreign key relationships, shared identifiers, join candidates, and cross-source linkages. This is essential for new sources that must integrate with existing data assets.

The Pathway framework maps profiling directly to pipeline design: profiling findings determine the ingestion layer (based on source format), transformation logic (based on quality issues), storage selection (based on data structure), and monitoring parameters (based on quality benchmarks established during discovery) [2].

### The intake form as structured friction

Effective intake processes introduce "just enough friction to filter out lazy asks" while remaining accessible [4]. Caitlin Hudon's intake form model asks two key questions that distinguish serious requests from casual ones: "What decision will you make or action will you take with this data?" and "What is the real problem you're trying to solve?" [4]. Brooklyn Data recommends centralizing requests through intake forms (Google Forms, Slack workflows) with conditional logic — simpler requests require fewer fields while complex analyses gather more context upfront [5].

The Splunk onboarding framework adds operational rigor by requiring concrete technical details before triaging: source application, generating hosts, data format, file paths, sample data, sensitive data classification, retention requirements, and impact/urgency assessment if the data feed experiences an outage [6][7]. The five-phase Splunk workflow (Request → Define → Implement → Validate → Communicate) ensures that source definition and validation happen before implementation begins [7].

---

## Sub-question 4: Metadata Documentation Standards for New Sources

### What metadata to capture

Metadata documentation for new sources must cover two categories [18]:

**Technical metadata:** Schema structure (tables, columns, data types, constraints), data volumes, refresh schedules, access patterns, query performance characteristics, and storage location. This metadata can be harvested automatically by catalog tools through scheduled connectors.

**Business metadata:** Ownership assignments, plain-language definitions, quality scores, certification status, intended use cases, compliance indicators (PII classification, retention requirements), and data lineage. This metadata requires human curation and cannot be fully automated.

The 80/20 principle applies: machines handle technical metadata at scale (schema scanning, usage analysis, quality profiling) while humans provide strategic context through ownership assignment, business definitions, and governance classification [18]. Catalogs that rely solely on automated harvesting produce technically complete but semantically empty entries. Catalogs that rely solely on manual entry do not scale and decay within months [18].

### Data contracts as formalized metadata

Data contracts formalize the agreement between a data producer and its consumers, specifying schema, quality rules, SLAs, and governance metadata in a machine-readable format [11][12][20].

The Open Data Contract Standard (ODCS) v3.1.0, governed by Bitol under the Linux Foundation, defines 11 sections: fundamentals, schema, references, data quality, support and communication, pricing, team, roles, SLA, infrastructure, and custom properties [12]. The Data Contract Specification (now deprecated in favor of ODCS) provides a complementary YAML-based format with explicit fields for service levels (availability, freshness, latency, retention, frequency), quality checks (SQL-based, metric-based, or natural language), and classification metadata (sensitivity levels, PII indicators, custom tags) [11].

Key contract components for new source onboarding:

- **Schema definition** — Field names, types, nullability, precision, and structure (including nested/complex types). This is the contract's core: it defines what the producer commits to deliver.
- **Quality rules** — Minimum row counts, null percentage thresholds, uniqueness constraints, value range checks. These translate the profiling baseline into enforceable expectations.
- **SLAs** — Freshness threshold (maximum age of latest data), availability percentage, latency (source-to-destination delay), retention period, and update frequency (batch schedule or streaming).
- **Ownership** — Producer team, consumer teams, escalation contacts, and status (proposed, active, deprecated, retired).

### Catalog integration patterns

OpenMetadata uses a pull-based ingestion approach with 100+ pre-built connectors, based on the principle that "no metadata system can be purely push-based" — data sources cannot be reasonably expected to push metadata into a cataloging system [18]. DataHub supports both push-based integrations (metadata emitted from systems like Airflow and Spark when changes occur) and pull-based integrations (scheduled crawling of source systems) [18].

For new source onboarding, the recommended pattern is: (1) register the source in the catalog during the discovery phase, (2) run automated profiling to harvest technical metadata, (3) assign ownership and add business definitions during the classification step, (4) link the source to downstream assets to establish lineage, and (5) attach the data contract to the catalog entry as the authoritative specification [1][2][18].

---

## Sub-question 5: Schema Stability Assessment and Drift Prevention

### Schema drift as quantified risk

Monte Carlo's analysis of 11M+ monitored tables provides the most comprehensive dataset on schema drift impact [17]:

- Schema drift accounts for **7.8% of all data quality incidents** — behind pipeline execution faults (26.2%), real-world variation (20%), ingestion disruptions (16.6%), platform instability (15.2%), and intentional changes like backfilling (14.2%)
- Production incidents increase by **27% for each percentage-point increase in schema drift rate** [14]
- Teams average **67 data incidents per month**, with 68% taking 4+ hours to detect and an average of 15 hours to resolve [17]
- 1 data quality issue occurs per 10 tables annually (up from 1 per 15 tables in 2020-2023) [17]

Schema drift is particularly dangerous because it can cause silent data corruption — a pipeline may not fail outright but instead produce truncated, misaligned, or incorrectly typed data. A column type change from integer to string, or a renamed column, can flow through transformation layers without raising errors while producing incorrect analytical results [13].

### Assessment criteria for schema stability

Before onboarding a source, evaluate:

1. **Schema change frequency** — Track the field addition/deletion rate over time. High-volatility sources (particularly SaaS APIs) may change monthly; stable transactional databases may change quarterly or less [14].
2. **Change notification process** — Does the source owner inform consumers before schema changes? Is there a pull request process for database migrations that data teams can observe? A simple Slack notification when a migration touches a pipeline-feeding table is often sufficient [13].
3. **Change documentation** — Are schema changes version-controlled and logged? Organizations should track schema modifications similar to software code using version control systems [13].
4. **Historical stability** — What is the schema-drift incident count over the past 6-12 months? This metric helps identify unstable data providers and prioritize stabilization efforts [14].

### dlt schema contracts for enforcement

dlt provides a pragmatic implementation of schema contracts with four modes applied to three entities (tables, columns, data_types) [16]:

- **evolve** — No constraints; new tables and columns are created automatically. Use during development and initial discovery.
- **freeze** — Raises an exception when data does not fit the existing schema. Use in production for stable, contract-governed sources.
- **discard_row** — Discards entire rows that violate the schema. Use for event streams where some events may have variant structures.
- **discard_value** — Strips non-conforming fields from rows but loads the rest. Use as a resilient production default that tolerates drift without losing records.

The recommended progression: use `evolve` during initial source discovery to infer the schema automatically, then switch to `freeze` or `discard_value` in production to enforce the contract. Schema changes in production should be explicit and deliberate, not automatic [15][16].

Five prevention strategies for schema drift [13]:

1. **Schema validation before loading** — Compare incoming data structure against the expected schema contract before writing to destination
2. **Schema tracking and versioning** — Maintain metadata snapshots and version-control schema definitions
3. **Quarantine unexpected fields** — Isolate unknown columns rather than silently ingesting them
4. **Change logging** — Document when and why structural changes occur
5. **Regular pipeline reviews** — Monitor shared data sources for cascading schema impacts

---

## Challenge

Challenger research targeted the completeness of the six-dimension evaluation framework, the practical applicability of formal discovery workflows, the maturity of data contract standards, and the reliability of schema drift statistics. Six findings were challenged.

### The six evaluation dimensions are necessary but not universally ordered

The six dimensions (connectivity, volume, freshness, schema stability, data quality, access complexity) emerge from synthesizing multiple practitioner frameworks — Splunk's onboarding checklist [6][7], Monte Carlo's data observability pillars [17], and the OvalEdge discovery workflow [1]. No single source defines all six as a unified framework. The synthesis is defensible because each dimension appears independently across multiple sources and addresses a distinct category of onboarding risk. However, the relative importance of each dimension is context-dependent: for a data science team pulling a one-time research dataset, access complexity dominates; for a production analytics pipeline, schema stability and freshness dominate.

### Formal 8-step discovery workflows are aspirational for most teams

The OvalEdge 8-step model [1] provides a thorough framework but assumes organizational maturity that many data teams lack. Steps 5-8 (classify, prepare, explore, govern) require catalog tooling, stewardship roles, and governance processes that are absent in early-stage data teams. The practical minimum viable workflow is steps 1-4: define scope, inventory sources, validate access, and assess quality. Teams that skip directly to pipeline construction without at least these four steps consistently encounter the same failure modes: access problems discovered during deployment, quality issues discovered during stakeholder review, and schema changes discovered during the first incident.

### Data contracts are promising but adoption is early

ODCS v3.1.0 [12] and the Data Contract Specification [11] provide machine-readable formats for formalizing source agreements. The Data Contract Specification was deprecated in favor of ODCS — this fragmentation itself signals that the ecosystem is not yet settled. ODCS originates from PayPal's internal data contract template and has Linux Foundation governance, which provides institutional credibility. But data contracts require organizational buy-in from source system owners who must commit to maintaining the contract — and source system teams (often application engineers) have historically been uninterested in data consumer needs. The technology is ready; the organizational adoption challenge remains.

### Schema drift at 7.8% understates its impact

Monte Carlo's 7.8% figure [17] measures schema drift as a category of data quality incidents. This understates the true impact for two reasons: (1) schema drift often triggers cascading failures that are categorized under "pipeline execution faults" (26.2%) or "ingestion disruptions" (16.6%) rather than drift itself, and (2) the 27% compounding effect [14] means even a small drift rate has outsized downstream consequences. A source with a 3% monthly schema change rate does not produce a 3% incident rate — it produces a systematically degrading reliability profile.

### The "months to weeks" onboarding reduction claim needs qualification

Multiple sources claim automation reduces onboarding from "months to minutes" or "weeks to hours" [3]. The elapsed-time reduction is real for the mechanical parts of onboarding — connector configuration, schema mapping, initial load execution. But the cognitive parts — understanding the source's business context, establishing quality expectations, defining ownership, negotiating SLAs — cannot be automated. Realistic expectations: automation reduces the mechanical onboarding work (connector setup, schema mapping, initial profiling) from weeks to days. The full onboarding cycle including business context, quality benchmarking, and governance integration remains a multi-week process for complex sources.

### Manual metadata catalogs decay faster than expected

Sifflet's characterization that manual-entry catalogs become untrusted within a year [18] aligns with broader industry experience but the timeline varies by organization. High-churn environments (frequent source changes, rapid team turnover) see catalog decay in months. Stable environments with strong stewardship culture can maintain manual catalogs for longer. The underlying principle is sound: any metadata asset that requires ongoing human effort without automation support will lag reality. The 80/20 automation-curation split (machines handle technical metadata, humans handle business context) is the sustainable model.

---

## Findings

### Finding 1: Source system evaluation requires structured assessment across six dimensions before pipeline construction
**Confidence: HIGH**

Every source system must be evaluated across connectivity (how data is exposed), volume (size and change rate), freshness (update frequency and staleness tolerance), schema stability (change frequency and notification process), data quality (baseline profiling results), and access complexity (authentication, authorization, and operational overhead). These dimensions are not a checklist to complete once — they define the constraints that determine ingestion approach, error handling strategy, monitoring configuration, and maintenance burden. Teams that skip pre-pipeline assessment consistently discover the same problems later at higher cost: access failures during deployment, quality issues during stakeholder review, and schema changes during the first production incident. The minimum viable assessment covers access validation, quality profiling, and schema stability review.

### Finding 2: Source classification determines ingestion approach — this is not a free choice
**Confidence: HIGH**

Transactional databases support full load, incremental, or CDC depending on volume and freshness needs. Event streams require streaming consumers. SaaS APIs are constrained by rate limits, pagination schemes, and vendor-controlled authentication. File-based sources require polling or event-driven detection with no query flexibility. The ingestion approach is constrained by the source type, not chosen independently. CDC is required when hard deletes must be captured or near-real-time freshness is needed, but CDC introduces operational overhead (connector management, log position tracking). Incremental loading works only when the source exposes reliable timestamp columns and does not receive backfills. Full loads are appropriate only for small reference tables. Most production environments use a hybrid approach — matching ingestion method to source characteristics rather than standardizing on a single pattern.

### Finding 3: Data profiling (structure, content, relationship) is the measurement foundation for source evaluation
**Confidence: HIGH**

Data profiling is not optional pre-work — it is the measurement system that produces the inputs for every other evaluation dimension. Structure discovery reveals format inconsistencies and type mismatches. Content discovery identifies null rates, duplicate percentages, and domain violations. Relationship discovery maps foreign keys and join candidates across sources. Without profiling, quality assessment is subjective ("the data looks fine"), schema stability is unknown ("we haven't had problems yet"), and volume baselines are absent ("it's about this big"). Profiling transforms source evaluation from opinion-based to evidence-based. The profiling baseline also becomes the foundation for ongoing monitoring — alerting on deviations from the measured baseline rather than guessing at thresholds.

### Finding 4: Data contracts formalize source agreements but require organizational adoption, not just tooling
**Confidence: MODERATE**

ODCS v3.1.0 provides a machine-readable standard for defining schema, quality rules, SLAs, and ownership metadata. The technology is mature enough for production use. The adoption challenge is organizational: data contracts require source system owners (typically application engineering teams) to accept accountability for the data they produce. This is a cultural shift — historically, data quality has been treated as the data team's problem, not the producer's problem. Teams that successfully adopt data contracts start with high-value sources where the business cost of quality failures is obvious, negotiate contracts with willing producer teams, and expand incrementally. Starting with a contract mandate across all sources without organizational buy-in produces shelf-ware.

### Finding 5: Schema stability assessment is a quantifiable pre-onboarding gate with measurable risk thresholds
**Confidence: HIGH**

Schema drift is not an abstract risk — it is measurable and its impact compounds. At 7.8% of data quality incidents and a 27% compounding effect per percentage-point increase in drift rate, schema stability directly predicts pipeline reliability. Pre-onboarding assessment should measure: schema change frequency over the past 6-12 months, existence of change notification processes, and availability of schema version control. Sources that fail these criteria require defensive pipeline design — schema validation at ingestion, quarantine tables for unexpected fields, and contract modes (dlt's `freeze` or `discard_value`) that halt or degrade gracefully rather than silently propagating changes. The cost of not assessing schema stability is discovering it through production incidents.

---

## Claims

| # | Claim | Source | Status | Notes |
|---|-------|--------|--------|-------|
| 1 | Schema drift causes 7.8% of all data quality incidents | [17] | verified | Monte Carlo analysis of 11M+ monitored tables |
| 2 | Production incidents increase 27% per percentage-point rise in schema drift rate | [14] | qualified | Integrate.io claim; compounding effect is plausible but methodology not detailed |
| 3 | Teams average 67 data incidents per month with 15-hour average resolution time | [17] | verified | Monte Carlo / Wakefield Research survey of 200 data professionals |
| 4 | 1 data quality issue per 10 tables annually (up from 1 per 15 in 2020-2023) | [17] | verified | Monte Carlo longitudinal data across 11M+ tables |
| 5 | Data profiling has three distinct types: structure, content, and relationship discovery | [19] | verified | Widely accepted taxonomy confirmed across multiple sources |
| 6 | CDC reduces CPU/IO pressure on source systems vs. incremental query-based extraction | [8] | verified | CDC reads transaction logs instead of querying tables |
| 7 | ODCS v3.1.0 is the recommended data contract standard (Data Contract Spec deprecated) | [11][12] | verified | Linux Foundation governance via Bitol project |
| 8 | dlt schema contracts support four modes: evolve, freeze, discard_row, discard_value | [16] | verified | Official dlt documentation; applied to tables, columns, data_types entities |
| 9 | Manual-entry metadata catalogs become untrusted within the first year | [18] | qualified | Sifflet claim; timeline varies by organizational churn rate and stewardship maturity |
| 10 | SaaS APIs are the most volatile source type — vendors change APIs without notice | [10][13] | verified | Consistent across practitioner reports; pagination and rate limit variability confirmed |
| 11 | Splunk onboarding workflow uses five phases: Request, Define, Implement, Validate, Communicate | [7] | verified | Splunk Lantern framework documentation |
| 12 | Alert engagement drops 15% when channels receive >50 alerts/week, additional 20% at >100/week | [17] | verified | Monte Carlo analysis of alert channel engagement data |
| 13 | Automated metadata catalogs should follow 80/20 split: machine-harvested technical, human-curated business | [18] | qualified | Sifflet recommendation; ratio is illustrative, not empirically derived |
| 14 | Pipeline execution faults (26.2%) are the largest single category of data quality incidents | [17] | verified | Monte Carlo analysis; followed by real-world variation (20%) and ingestion disruptions (16.6%) |
| 15 | Intake forms should ask "What decision will you make with this data?" as a filtering question | [4] | verified | Caitlin Hudon's practitioner-tested intake form design |
