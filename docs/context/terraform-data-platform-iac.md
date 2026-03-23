---
name: Terraform for Data Platform IaC
description: "Terraform provider maturity across Databricks, Snowflake, and ClickHouse — version pinning requirements, state management patterns, resource ownership boundaries between Terraform/dbt/pipeline tools, and the Snowflake provider forced migration timeline"
type: context
related:
  - docs/research/2026-03-22-data-platform-engineering.research.md
  - docs/context/environment-provisioning-patterns.md
  - docs/context/compute-governance-patterns.md
  - docs/context/production-platform-comparison.md
---

## Key Insight

Terraform is the de facto IaC tool for data platforms, but provider maturity varies dramatically. The Databricks provider is stable with incremental releases. The Snowflake provider underwent a multi-year breaking migration (v0.x to v1.0 to v2.0), with legacy versions being removed from the Terraform registry through April 2026. The ClickHouse provider is split across two providers and most likely to have breaking changes. Provider maintenance is ongoing operational work, not a one-time setup.

## Provider Maturity

**Databricks:** Most stable. Incremental releases aligned to platform features. Operates at two levels: account-level (metastores, workspace creation) and workspace-level (clusters, policies, jobs, catalog objects). Supports full Unity Catalog lifecycle through aliased providers with `depends_on` for resource ordering.

**Snowflake:** Most disruptive upgrade history. Official support starts at v2.0.0 only. Teams on v0.x face registry removal by April 2026. Migration is non-trivial: resource renames (e.g., `snowflake_role` became `snowflake_account_role`), attribute restructuring, state manipulation via `terraform state mv`, and some resources require complete reimport. Treat this as a planned migration project, not routine maintenance.

**ClickHouse:** Newest and least mature. Requires two providers for complete coverage: `ClickHouse/clickhouse` for Cloud service provisioning and `clickhousedbops` for database-level objects (users, roles, grants). The `cluster_name` parameter must be null for Cloud but set for self-hosted -- an abstraction leak revealing the split. Pin to exact versions (`=`) rather than pessimistic constraints until the providers stabilize.

## Version Pinning

Pessimistic constraints (`~>`) are the recommended default: `~> 5.31.0` allows patch updates (5.31.x) but blocks minor/major updates with potential breaking changes. The `.terraform.lock.hcl` file records exact versions and cryptographic checksums and must be committed to version control. Upgrade procedure: run `terraform init -upgrade` in non-production, execute `terraform plan` to verify, commit updated lock file only after validation. Never upgrade multiple providers simultaneously in a major version jump.

## State Management

Remote state backends (S3, GCS, Azure Blob) with versioning and locking are non-negotiable. State locking prevents concurrent modifications (DynamoDB for AWS, native locking for Terraform Cloud). Component-sliced state files reduce blast radius: separate state for networking, compute, catalog/schema objects, and permissions. A failed cluster policy change should not risk corrupting schema state.

## Resource Ownership Boundaries

This is the most common source of state drift in data platform Terraform:

- **Terraform owns:** workspace/service creation, cluster policies, warehouse definitions, role hierarchies, resource monitors, catalog/database/schema containers, grants
- **dbt owns:** table and view creation within schemas
- **Pipeline tools own:** data loading into tables (column additions by Airbyte, dlt, Fivetran)

Violating these boundaries causes Terraform to detect and attempt to revert changes made by dbt or pipeline tools on the next apply. The principle: Terraform manages containers and policies, application tools manage content within those containers.

## Takeaway

Budget for Terraform provider maintenance as ongoing work. The Snowflake migration is the most urgent action item (April 2026 deadline). Pin versions, commit lock files, slice state by component, and enforce clear ownership boundaries between Terraform and application tools.
