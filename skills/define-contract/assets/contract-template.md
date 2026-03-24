---
name: {{name}}
artifact_type: contract
version: 1.0.0
owner: {{owner}}
status: draft
last_modified: {{date}}
---

# Data Contract: {{name}}

## 1. Fundamentals

| Field | Value |
|-------|-------|
| **Contract ID** | {{unique identifier, e.g., contract-<product-name>-v1}} |
| **Name** | {{data product name}} |
| **Version** | {{MAJOR.MINOR.PATCH}} |
| **Status** | {{proposed / active / deprecated / retired}} |
| **Owner** | {{team or individual responsible for this contract}} |
| **Description** | {{what this data product provides and its business purpose}} |

## 2. Schema

ODCS uses "objects" (tables) and "properties" (columns) to stay database-agnostic.

### Object: {{object_name}}

**Description:** {{what this object represents}}

| Property | Logical Type | Nullable | Constraints | Description |
|----------|-------------|:--------:|-------------|-------------|
| {{property_name}} | {{string / integer / long / float / double / boolean / date / timestamp / decimal(p,s)}} | {{yes / no}} | {{PK / FK(target) / UNIQUE / CHECK(expr) / none}} | {{what this property represents}} |

{{Repeat the object block for each object in the data product.}}

### Relationships

| Source | Target | Type | Description |
|--------|--------|------|-------------|
| {{object.property}} | {{object.property}} | {{FK / reference}} | {{relationship description}} |

## 3. References

| Reference | Link | Description |
|-----------|------|-------------|
| {{Data dictionary}} | {{URL or path}} | {{description}} |
| {{Lineage diagram}} | {{URL or path}} | {{description}} |
| {{Design document}} | {{URL or path}} | {{description}} |

## 4. Data Quality

### Object-Level Rules

Rules that apply across multiple properties or require cross-field checks.

| Rule ID | Object | Rule | Severity | Description |
|---------|--------|------|----------|-------------|
| {{Q-001}} | {{object_name}} | {{SQL expression or plain text}} | {{critical / warning / informational}} | {{what this rule validates}} |

### Property-Level Rules

Rules scoped to individual properties.

| Rule ID | Object | Property | Dimension | Rule | Severity |
|---------|--------|----------|-----------|------|----------|
| {{Q-101}} | {{object_name}} | {{property_name}} | {{completeness / uniqueness / validity / accuracy / consistency / timeliness}} | {{SQL expression, threshold, or plain text}} | {{critical / warning / informational}} |

**Guidance:**
- Start with completeness (null rates) and validity (range/pattern checks) -- highest signal-to-investment ratio.
- Use thresholds, not absolutes: `null_rate < 0.02` is more sustainable than `null_rate = 0`.
- Quality rules translate profiling baselines into enforceable expectations.

## 5. Support & Communication

| Field | Value |
|-------|-------|
| **Primary Contact** | {{team or individual, e.g., #data-products-team on Slack}} |
| **Escalation Path** | {{who to contact if primary is unresponsive, e.g., engineering-manager@company.com}} |
| **Support Hours** | {{e.g., business hours M-F 9am-5pm ET / 24x7 for critical}} |
| **Notification Channel** | {{where contract changes are announced, e.g., #data-contracts-changelog}} |
| **Incident Process** | {{link to runbook or description of incident response process}} |

## 6. Pricing

Most teams leave this section as a placeholder. Relevant for data marketplace or chargeback scenarios.

| Field | Value |
|-------|-------|
| **Model** | {{free / per-query / subscription / chargeback / N/A}} |
| **Unit** | {{per query / per GB / per month / N/A}} |
| **Currency** | {{USD / EUR / N/A}} |
| **Notes** | {{billing cadence, cost center, budget owner, or "No pricing model applied"}} |

## 7. Team

| Role | Name / Team | Contact |
|------|-------------|---------|
| **Data Product Owner** | {{name}} | {{email or Slack}} |
| **Producer Team** | {{team name}} | {{channel or email}} |
| **Consumer Team(s)** | {{team name(s)}} | {{channel or email}} |
| **Steward / Governance** | {{name or team}} | {{contact}} |

## 8. Roles

Define who can do what with this data product.

| Role | Responsibility | Assigned To |
|------|---------------|-------------|
| **Producer** | Maintain schema, meet SLAs, publish changes with versioning | {{team}} |
| **Consumer** | Read data, report quality issues, migrate on breaking changes | {{team(s)}} |
| **Approver** | Approve schema changes and version bumps | {{individual or team}} |
| **Observer** | Read-only access to contract metadata and quality dashboards | {{team(s) or "any authenticated user"}} |

## 9. SLA

| Dimension | Target | Measurement |
|-----------|--------|-------------|
| **Freshness** | {{e.g., data no more than 4 hours stale}} | {{how measured: loaded_at timestamp, freshness check}} |
| **Availability** | {{e.g., 99.5% uptime}} | {{measurement window and method}} |
| **Latency** | {{e.g., source-to-destination < 30 minutes}} | {{end-to-end measurement}} |
| **Retention** | {{e.g., 13 months rolling}} | {{retention policy and purge schedule}} |
| **Update Frequency** | {{e.g., hourly / daily at 6am UTC / event-driven}} | {{schedule or trigger mechanism}} |
| **Backup** | {{e.g., daily snapshots, 7-day retention}} | {{backup mechanism and recovery SLA}} |

**Error Budget:** {{e.g., 99.5% compliance allows ~3.6 hours of cumulative violation per month}}

**SLA vs SLO:** The targets above are SLAs (contractual commitments). Internal SLOs should be stricter (e.g., SLO: 99.9%, SLA: 99.5%) to provide buffer before customer-facing breaches.

## 10. Infrastructure

| Field | Value |
|-------|-------|
| **Platform** | {{Snowflake / Databricks / BigQuery / Postgres / S3 / Kafka}} |
| **Server / Account** | {{connection identifier}} |
| **Database** | {{database name}} |
| **Schema** | {{schema name}} |
| **Format** | {{Parquet / Avro / JSON / Delta / Iceberg / database tables}} |
| **Access Method** | {{JDBC / REST API / S3 path / Kafka topic}} |
| **Environment** | {{production / staging / development}} |

## 11. Custom Properties

Organization-specific metadata that does not fit standard sections.

| Key | Value | Description |
|-----|-------|-------------|
| {{data_classification}} | {{public / internal / confidential / restricted}} | {{Data sensitivity level}} |
| {{cost_center}} | {{CC-1234}} | {{Billing allocation}} |
| {{compliance_tags}} | {{GDPR, SOC2}} | {{Applicable regulatory frameworks}} |

---

## Versioning

This contract follows semantic versioning (MAJOR.MINOR.PATCH):

| Bump | When | Action Required |
|------|------|-----------------|
| **MAJOR** | Breaking change (remove column, change type, tighten constraint) | Expand-contract migration; announce with timeline |
| **MINOR** | Additive change (new optional column, new quality rule) | No consumer action needed |
| **PATCH** | Documentation or metadata only | No consumer action needed |

### Expand-Contract Migration (for MAJOR changes)

1. **Expand:** Introduce new elements alongside existing ones. Dual-write both old and new. No consumers break.
2. **Migrate:** Consumers update to new elements at their own pace. Set deprecation date on old version.
3. **Contract:** Remove old elements after all consumers have migrated and deprecation date has passed.

Default to **BACKWARD** compatibility: consumers using the new schema can read old data. Consumers upgrade first.

## Enforcement Strategy

| Layer | When | What It Catches | Tooling |
|-------|------|-----------------|---------|
| **CI-Time** | Pull request / merge | Breaking schema changes before deploy | dbt Cloud CI, schema registry compatibility checks, Data Contract CLI |
| **Build-Time** | Transformation execution | Structural mismatches (wrong columns, types) | dbt contract preflight, schema registry serialization, dlt freeze mode |
| **Runtime** | Pipeline execution | Quality violations, freshness breaches, volume anomalies | Soda, Great Expectations, dbt tests, circuit breakers |

**Enforcement severity:**
- **Critical** (schema mismatch, required field null) -- block writes, quarantine records
- **Warning** (volume anomaly, distribution shift) -- allow writes, alert
- **Informational** (minor metric deviation) -- log to dashboard

## dbt Contract Snippet (Optional)

If using dbt for transformation enforcement, add contract configuration to the model YAML:

```yaml
models:
  - name: {{model_name}}
    config:
      contract:
        enforced: true
    columns:
      - name: {{column_name}}
        data_type: {{type}}
        constraints:
          - type: not_null
          - type: primary_key
        # Repeat for each column in the schema section above
```

**Note:** dbt contracts enforce schema structure only. Quality rules, SLAs, and ownership are defined in this ODCS contract and enforced through separate tooling. Every column must be explicitly defined when `contract.enforced: true`.

## Next Steps

1. **`/dos:assess-quality`** -- Translate the quality rules above into a full quality configuration with scoring, thresholds, and validation tooling. The contract's quality section seeds the assessment.
2. **`/dos:implement-models`** -- Build the dbt models that implement this contract. The schema section directly maps to model definitions; the enforcement strategy guides contract configuration.

## Changelog

| Date | Version | Change | Author |
|------|---------|--------|--------|
| {{date}} | 1.0.0 | Initial contract | {{author}} |
