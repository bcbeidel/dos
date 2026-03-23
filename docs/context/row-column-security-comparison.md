---
name: Row and Column Security Comparison
description: "Snowflake has the most mature RLS/column-masking (row access policies, tag-based masking); Databricks Unity Catalog ABAC is approaching parity but requires Runtime 16.4+ and is Public Preview; ClickHouse has row policies and column GRANTs but no dynamic masking -- users get errors instead of redacted values"
type: context
related:
  - docs/research/2026-03-22-governance-compliance.research.md
  - docs/context/data-governance-foundations.md
  - docs/context/access-control-models.md
  - docs/context/production-platform-comparison.md
  - docs/context/data-masking-tokenization.md
---

## Key Insight

Snowflake provides the most complete row-level and column-level security among Snowflake, Databricks, and ClickHouse. Its tag-based masking is the standout feature: classify sensitive columns, apply tags, bind masking policies to tags, and new tables automatically receive protection without manual intervention. ClickHouse is fundamentally different -- it restricts column access entirely (users see errors) rather than masking values (users see redacted data).

## Row-Level Security

### Snowflake Row Access Policies

Row access policies (RAPs) are schema-level objects that evaluate at query runtime. Key architectural details:

- **Owner-context evaluation**: Policies evaluate using the policy owner's role, not the querying user's. This allows policies to reference mapping/entitlement tables the user cannot directly access.
- **Statement coverage**: Policies apply to SELECT, UPDATE, DELETE, and MERGE -- but do not prevent insertions.
- **Performance trade-off**: RAPs eliminate metadata-only query optimizations. Simple CASE-based policies have negligible cost; policies with mapping table lookups can significantly degrade performance.
- **Limitations**: Cannot attach to materialized views if the base table has a policy. CURRENT_ROLE() and CURRENT_USER() return NULL in data-sharing consumer accounts.

### Databricks Row Filters

Two approaches via Unity Catalog:

1. **Manual assignment**: SQL UDFs applied as row filters per table. Does not scale.
2. **ABAC policies** (Public Preview): Filter UDFs associated with governed tags. Policies at catalog/schema level inherit to child objects. Cannot be overridden by table owners.

Critical limitations: row filters cannot be applied to views (tables only), time travel is unsupported on filtered tables, deep/shallow clones cannot be performed on protected tables. ABAC requires Runtime 16.4+.

### ClickHouse Row Policies

Native `CREATE ROW POLICY` syntax. Policies are primarily designed for read-only users. No ABAC or tag-based inheritance -- each policy is bound to a specific table and role. Known security advisory: RBAC is bypassed when query caching is enabled (GHSA-45h5-f7g3-gr8r) -- verify patched version.

## Column-Level Security

### Snowflake: Dynamic Masking + Tag-Based Masking

Dynamic data masking applies at query runtime -- users see plain-text, partially masked, or fully masked values depending on role and policy conditions. Enterprise Edition required.

Tag-based masking is the scalability feature: create a tag (e.g., `sensitivity = 'pii'`), create masking policies per data type, assign policies to the tag, apply the tag to databases/schemas/tables/columns. New columns matching the data type automatically receive protection. Column-level policies take precedence over tag-based policies when both apply.

### Databricks: Column Masks

Column masks in Unity Catalog return actual values or redacted versions based on governed tags. Same ABAC inheritance model as row filters. Same limitations: no view support, no time travel, requires Runtime 16.4+ for ABAC.

### ClickHouse: Column GRANT Restrictions

Column-level security through GRANT statements -- users can only query columns where they have explicit access. `SELECT *` fails with an insufficient permissions error if any column lacks access. No dynamic masking: users see errors, not redacted values. Implementing partial masking requires custom views with conditional logic, which is fragile and does not scale.

## Platform Comparison

| Capability | Snowflake | Databricks | ClickHouse |
|---|---|---|---|
| Row-level security | GA (RAPs) | GA manual, Preview ABAC | GA (row policies) |
| Dynamic column masking | GA (tag-based) | Preview (ABAC masks) | None |
| Tag-based auto-application | Yes | Preview | No |
| View support | Yes | No | N/A |
| Audit logging | Native (365d) | Native (regional) | Custom build |

## Takeaway

If governance requirements include dynamic masking, tag-based auto-application, or view-level security, Snowflake is the clear choice today. Databricks ABAC will reach parity when it goes GA -- monitor Runtime 16.4+ adoption and Public Preview graduation. ClickHouse requires custom engineering for any governance feature beyond basic row policies and column GRANTs.
