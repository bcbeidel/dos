# ODCS v3.1 Structure

The Open Data Contract Standard (ODCS) v3.1.0, governed by Bitol under the Linux Foundation, defines data contracts in platform-agnostic YAML across 11 sections. ODCS uses "objects" instead of "tables" and "properties" instead of "columns" to stay database-agnostic.

## Section Inventory

### Core Sections (detailed requirements)

**1. Fundamentals** -- ID, name, version, status, owner. Every contract starts here. Status lifecycle: `proposed` -> `active` -> `deprecated` -> `retired`.

**2. Schema** -- Objects (tables) and properties (columns) with types, constraints, and relationships. This is the contract's core: what the producer commits to deliver. Field-level requirements: name, logical type, nullability, precision for numerics, constraints (not_null, primary_key, foreign_key, unique, check).

**3. Data Quality** -- Rules at object and property levels covering accuracy, completeness, and validity. Quality rules support plain text descriptions, SQL with placeholders, or a predefined metrics library. Rules can be defined per-property or per-object (cross-field checks).

**4. SLA** -- Latency (source-to-destination delay), availability percentage, retention period, freshness threshold (maximum age of latest data), update frequency, and backup policy. SLAs are executable with cron/interval scheduling.

**5. Team** -- Organizational ownership: producer team, consumer teams, escalation contacts. Maps to the ownership component of the four core contract elements.

### Peripheral Sections (lighter requirements)

**6. References** -- Links to related documentation: data dictionaries, lineage diagrams, design documents, external standards. No required fields beyond at least one link.

**7. Support & Communication** -- Contact channels (Slack, email, PagerDuty), escalation paths, support hours. Defines how consumers reach producers when issues arise.

**8. Pricing** -- Cost models and billing terms. Placeholder for most teams. Relevant for data marketplace or chargeback scenarios. Fields: model (free, per-query, subscription), unit, currency.

**9. Roles** -- Consumer and producer responsibilities. Who can read, who can write, who approves schema changes. Maps to access control and change governance.

**10. Infrastructure** -- Deployment and connection details: server, database, schema, format (Parquet, Avro, JSON), platform (Snowflake, Databricks, S3). How consumers physically access the data.

**11. Custom Properties** -- Organization-specific extensions. Key-value pairs for metadata that does not fit standard sections (cost center, compliance tags, data classification).

## Four Core Components

For source onboarding and initial contracts, four components matter most:

| Component | ODCS Section | What It Defines |
|-----------|-------------|-----------------|
| Schema | Schema | Field names, types, nullability, constraints |
| Quality | Data Quality | Min row counts, null thresholds, uniqueness, value ranges |
| SLAs | SLA | Freshness, availability, latency, retention, frequency |
| Ownership | Team + Fundamentals | Producer team, consumer teams, escalation, lifecycle status |

## ODCS vs dbt Contracts

ODCS is a declarative specification defining the full producer-consumer agreement. dbt contracts are an enforcement mechanism at the transformation layer.

| Aspect | ODCS | dbt Contracts |
|--------|------|---------------|
| Scope | Schema + quality + SLAs + pricing + governance + ownership | Schema structure only |
| Enforcement | Declarative (needs tooling to enforce) | Build-time preflight check |
| Format | Platform-agnostic YAML | dbt model YAML |
| Columns | "Properties" | "Columns" |
| Tables | "Objects" | "Models" |
| Quality rules | Supported (SQL, plain text, metrics) | Not included (use dbt tests) |

The Data Contract CLI bridges ODCS to dbt-compatible formats.

## Consumer-Defined vs Producer-Defined

**Consumer-defined** (theoretically stronger): Requirements originate at the consumption point. Consumers define what they need; providers see which consumers depend on which elements. Generates problem visibility that catalyzes culture change.

**Producer-defined** (practical default): The producer defines the contract, consumers accept or negotiate. Simpler to implement. Sufficient for most organizations starting out.

**Pragmatic path:** Start producer-driven, instrument consumer usage patterns, evolve toward consumer-driven as the organization matures.

Three-phase maturity: Awareness (producers understand impact) -> Collaboration (producers communicate changes) -> Contract ownership (formal versioning and evolution).
