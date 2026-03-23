---
name: Data Contract Structure and Standards
description: "ODCS v3.1 is the emerging open standard for data contracts (11 sections, YAML, platform-agnostic); dbt contracts are narrower (schema-only, build-time enforcement); schema registries enforce compatibility at the streaming layer; ODCS defines the full agreement, dbt enforces the schema portion, registries guard serialization -- they are complementary"
type: context
related:
  - docs/research/2026-03-22-data-contracts.research.md
  - docs/context/data-contract-enforcement-versioning.md
  - docs/context/schema-evolution.md
  - docs/context/data-freshness-slas.md
  - docs/context/data-governance-foundations.md
---

## Key Takeaway

Data contracts are formal, code-enforced agreements between data producers and consumers covering schema, quality, freshness/SLAs, and governance. No single tool covers all contract aspects. ODCS defines the full contract, dbt contracts enforce schema at build time, and schema registries enforce compatibility at serialization time. Use all three together.

## ODCS v3.1 -- The Open Standard

The Open Data Contract Standard (ODCS) v3.1.0, governed by Bitol under the Linux Foundation, defines data contracts in platform-agnostic YAML across 11 sections:

1. **Fundamentals** -- ID, name, version, status, owner
2. **Schema** -- objects (tables) and properties (columns) with types, constraints, relationships
3. **References** -- links to related documentation
4. **Data Quality** -- rules at object and property levels (accuracy, completeness, validity)
5. **Support & Communication** -- contact and escalation paths
6. **Pricing** -- cost models and billing terms
7. **Team** -- organizational ownership
8. **Roles** -- consumer and producer responsibilities
9. **SLA** -- latency, availability, retention, freshness, frequency, backup
10. **Infrastructure** -- deployment and connection details
11. **Custom Properties** -- organization-specific extensions

ODCS uses "objects" instead of "tables" and "properties" instead of "columns" to stay database-agnostic. Quality rules support plain text, SQL with placeholders, or a predefined metrics library. SLAs are executable with cron/interval scheduling.

The Data Contract Specification (v1.2.1) is deprecated in favor of ODCS. The Data Contract CLI supports both formats during migration.

## dbt Model Contracts -- Narrow but Practical

dbt contracts solve a specific problem: preventing accidental schema changes at the transformation boundary. When `contract: { enforced: true }` is set, dbt performs a preflight check (verifies column names and types) and includes constraints in DDL.

Enforced elements: column names, data types, and constraints (`not_null`, `primary_key`, `foreign_key`, `unique`, `check`). Constraint enforcement varies by platform -- Postgres enforces all types; Snowflake/Redshift enforce a subset; most cloud warehouses define but do not enforce primary/foreign keys.

Limitations: every column must be explicitly defined, Python models are not supported, and contracts validate structure only -- data quality tests remain necessary for values.

## Schema Registries -- Streaming-Layer Enforcement

Schema registries validate message schema at serialization time, preventing non-conforming data from entering the stream:

- **Confluent** -- dominant, richest features, 7 compatibility modes, BACKWARD default. Schema Linking and Contexts require paid subscription.
- **AWS Glue** -- serverless, IAM integration, no deployment overhead. AWS-locked.
- **Apicurio** -- open-source (CNCF), broadest format support (Avro, Protobuf, JSON Schema, OpenAPI, AsyncAPI, GraphQL). Self-hosted.
- **Redpanda** -- built into every broker, Confluent API-compatible. Tied to Redpanda adoption.

Selection: AWS-native teams use Glue. Multi-cloud or on-premise teams choose Confluent (governance) or Apicurio (cost and format breadth). Redpanda users get it built in.

## ODCS vs dbt Contracts -- Complementary

ODCS is a declarative specification defining the full producer-consumer agreement. dbt contracts are an enforcement mechanism at the transformation layer. ODCS covers schema, quality, SLAs, pricing, governance, and ownership; dbt contracts cover schema structure only. In practice: define contracts in ODCS for cross-team agreements, enforce schema via dbt contracts within transformation pipelines, and use schema registries for streaming. The Data Contract CLI bridges ODCS to dbt-compatible formats.

## Adoption Reality

ODCS is well-designed but still early-stage. Gartner placed data contracts on the 2025 Hype Cycle as an emerging mechanism. Most teams today use ad-hoc YAML, dbt contracts, or schema registries rather than ODCS. The ecosystem tooling beyond Data Contract CLI has not caught up. dbt contracts have the widest practical adoption because they are embedded in the most widely used transformation tool.
