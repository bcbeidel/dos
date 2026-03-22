---
name: Environment Provisioning Patterns
description: "Dev/staging/prod separation across Databricks, Snowflake, and ClickHouse — Snowflake zero-copy cloning as standout capability, Unity Catalog workspace-catalog binding, directory-per-environment Terraform pattern vs workspaces"
type: context
related:
  - docs/research/2026-03-22-data-platform-engineering.research.md
  - docs/context/terraform-data-platform-iac.md
  - docs/context/local-duckdb-development.md
  - docs/context/ci-cd-pipeline-design.md
---

## Key Insight

Environment provisioning patterns differ fundamentally across platforms. Snowflake zero-copy cloning is the standout capability -- instant, storage-free environment copies with production-identical data. Databricks uses Unity Catalog workspace-catalog binding for logical isolation. ClickHouse has no data-sharing mechanism between environments. The Terraform organizational pattern (directory-per-environment with shared modules) matters as much as the platform-specific features.

## Snowflake: Zero-Copy Cloning

Cloning creates a new metadata pointer to existing micro-partitions. The clone is instant regardless of data volume and consumes zero additional storage until data diverges. Clones are fully independent -- modifications to either clone or source do not affect the other.

```sql
CREATE DATABASE staging_db CLONE production_db;
CREATE DATABASE dev_db CLONE staging_db;
```

This provides dev and staging environments with production-identical data for realistic testing. Combined with Terraform-managed role separation, this delivers both data fidelity and access isolation.

**The "zero cost" caveat:** Dev and staging environments diverge quickly. Test data modifications, schema experiments, and failed loads all create new micro-partitions billed to the clone. Implement clone refresh schedules (weekly or per-sprint) and drop stale clones to control costs.

## Databricks: Unity Catalog Binding

Three environment isolation strategies, from least to most separation:

1. **Shared workspaces with catalog-workspace binding** (recommended): Single Unity Catalog metastore per region with separate catalogs (dev_catalog, staging_catalog, prod_catalog) bound to their respective workspaces. Users in dev cannot see prod_catalog regardless of individual grants.
2. **Separate workspaces per environment**: Strongest isolation but highest management overhead. Code promoted via CI/CD.
3. **Multi-account isolation** (enterprise): Separate Databricks accounts per environment with their own metastores. Maximum isolation but eliminates cross-environment data sharing without Delta Sharing.

Databricks recommends minimizing workspace count while using Unity Catalog governance for logical isolation. Three workspaces linked to a single metastore with catalog-workspace binding is the typical right balance.

## ClickHouse: Service Separation

ClickHouse Cloud provides environment separation through separate services with independent scaling and endpoints. The Terraform provider enables ephemeral per-branch services for CI/CD testing, destroyed after test completion.

Self-hosted ClickHouse has no native environment separation features and no zero-copy cloning equivalent. Teams run separate clusters per environment with environment-specific Terraform variable files. Environment data must be physically copied or generated synthetically.

## Terraform: Directory-per-Environment

Directory separation is superior to Terraform workspaces for permanent environments:

```
infrastructure/
  modules/
    databricks-workspace/
    snowflake-warehouse/
    clickhouse-service/
  environments/
    dev/
      main.tf
      terraform.tfvars
    staging/
      main.tf
      terraform.tfvars
    prod/
      main.tf
      terraform.tfvars
```

Workspaces share `.tf` files with conditional logic to differentiate environments. One wrong `terraform workspace select` applies dev changes to production with no structural guardrail. Workspaces remain appropriate for ephemeral environments (feature branches, testing) where configuration is truly identical.

**Recommended hybrid:** Directories for permanent environments, workspaces for ephemeral ones. Terragrunt adds DRY configuration inheritance -- root `terragrunt.hcl` defines backend and shared variables, environment-level files add overrides.

**Nuance:** For environments that are purely parameter-only variations (same modules, same structure, different variable values), workspaces with CI/CD guardrails can eliminate code duplication without the maintenance burden of keeping directory trees in sync.

## Takeaway

Snowflake's zero-copy cloning is the strongest environment provisioning feature across these platforms. Databricks compensates with Unity Catalog binding. ClickHouse requires the most manual effort. Regardless of platform, use directory-per-environment Terraform layout for permanent environments and enforce environment targeting through CI/CD pipelines.
