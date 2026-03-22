---
name: "Data Platform Engineering"
description: "Terraform is the de facto IaC tool for data platforms but each provider (Databricks, Snowflake, ClickHouse) has fundamentally different resource models and maturity levels; Databricks cluster policies are the primary cost governance lever with job clusters costing 50-75% less than all-purpose clusters; Snowflake's zero-copy cloning enables instant dev/staging/prod environment provisioning at zero additional storage cost; ClickHouse Keeper replaces ZooKeeper with lower resource consumption and no GC pauses; environment separation should use directory-per-environment with shared modules (not Terraform workspaces); the Snowflake Terraform provider underwent disruptive v0.x-to-v1.0-to-v2.0 migration with official support only from v2.0.0; provider version pinning with pessimistic constraints (~>) and committed lock files is mandatory for production stability"
type: research
sources:
  - https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/cluster_policy
  - https://docs.databricks.com/aws/en/admin/clusters/policy-definition
  - https://docs.databricks.com/aws/en/lakehouse-architecture/cost-optimization/best-practices
  - https://docs.databricks.com/aws/en/data-governance/unity-catalog/best-practices
  - https://docs.databricks.com/aws/en/dev-tools/terraform/automate-uc
  - https://www.databricks.com/blog/2022/03/10/functional-workspace-organization-on-databricks.html
  - https://www.databricks.com/blog/cluster-policy-onboarding-primer
  - https://docs.snowflake.com/en/user-guide/warehouses-considerations
  - https://docs.snowflake.com/en/user-guide/warehouses-multicluster
  - https://docs.snowflake.com/en/user-guide/resource-monitors
  - https://docs.snowflake.com/en/user-guide/terraform
  - https://select.dev/posts/snowflake-terraform
  - https://select.dev/posts/snowflake-rbac-best-practices
  - https://clickhouse.com/docs/architecture/cluster-deployment
  - https://clickhouse.com/docs/knowledgebase/why_recommend_clickhouse_keeper_over_zookeeper
  - https://clickhouse.com/blog/new-terraform-provider-manage-clickhouse-database-users-roles-and-privileges-with-code
  - https://clickhouse.com/blog/clickhouse-cloud-terraform-for-continuous-integration-and-continuous-delivery-deployment-ci-cd
  - https://developer.hashicorp.com/terraform/tutorials/configuration-language/provider-versioning
  - https://spacelift.io/blog/iac-architecture-patterns-terragrunt
  - https://docs.snowflake.com/en/sql-reference/sql/create-clone
  - https://www.unraveldata.com/resources/databricks-serverless-vs-classic-compute/
related:
  - docs/plans/2026-03-21-data-pipeline-research-context.plan.md
  - docs/research/2026-03-22-cost-optimization-finops.research.md
  - docs/research/2026-03-22-production-platform-landscape.research.md
  - docs/research/2026-03-22-governance-compliance.research.md
---

## Summary

**Research question:** How should data platform infrastructure be managed as code, and what are best practices for environment provisioning and compute management?

**Mode:** Technical | **SIFT rigor:** High | **Sources:** 21 | **Searches:** 18 across Google

**Key findings:**
- Terraform is the de facto IaC tool for data platforms, but each provider (Databricks, Snowflake, ClickHouse) has fundamentally different resource models, maturity levels, and operational patterns — there is no unified "data platform Terraform module"
- Databricks cluster policies are the primary cost governance lever — job clusters cost 50-75% less in DBUs than all-purpose clusters, and policies enforce autoscaling limits, spot instance usage, and auto-termination through JSON attribute definitions
- Snowflake zero-copy cloning enables instant dev/staging/prod environment provisioning at zero additional storage cost until data diverges — this is the single most powerful environment management feature across all three platforms
- ClickHouse Keeper is the recommended replacement for ZooKeeper, offering lower resource consumption, no Java GC pauses, faster recovery, and production-readiness since April 2022
- Environment separation should use directory-per-environment with shared Terraform modules, not Terraform workspaces — workspaces lack structural enforcement and create accidental cross-environment apply risk
- The Snowflake Terraform provider underwent a disruptive multi-year migration from v0.x through v1.0 to v2.0, with official Snowflake support starting only at v2.0.0 — teams on older versions must migrate by April 2026 before registry removal
- Provider version pinning with pessimistic constraints (`~>`) and committed `.terraform.lock.hcl` files is mandatory for production stability

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/cluster_policy | databricks_cluster_policy resource | Databricks | current docs | T1 | verified |
| 2 | https://docs.databricks.com/aws/en/admin/clusters/policy-definition | Compute policy reference | Databricks | current docs | T1 | verified |
| 3 | https://docs.databricks.com/aws/en/lakehouse-architecture/cost-optimization/best-practices | Best practices for cost optimization | Databricks | current docs | T1 | verified |
| 4 | https://docs.databricks.com/aws/en/data-governance/unity-catalog/best-practices | Unity Catalog best practices | Databricks | current docs | T1 | verified |
| 5 | https://docs.databricks.com/aws/en/dev-tools/terraform/automate-uc | Automate Unity Catalog setup using Terraform | Databricks | current docs | T1 | verified |
| 6 | https://www.databricks.com/blog/2022/03/10/functional-workspace-organization-on-databricks.html | 5 Best Practices for Databricks Workspaces | Databricks | 2022 | T4 | verified — vendor blog |
| 7 | https://www.databricks.com/blog/cluster-policy-onboarding-primer | Cluster Policy Onboarding Primer | Databricks | 2023 | T4 | verified — vendor blog |
| 8 | https://docs.snowflake.com/en/user-guide/warehouses-considerations | Warehouse considerations | Snowflake | current docs | T1 | verified |
| 9 | https://docs.snowflake.com/en/user-guide/warehouses-multicluster | Multi-cluster warehouses | Snowflake | current docs | T1 | verified |
| 10 | https://docs.snowflake.com/en/user-guide/resource-monitors | Working with resource monitors | Snowflake | current docs | T1 | verified |
| 11 | https://docs.snowflake.com/en/user-guide/terraform | Snowflake Terraform provider | Snowflake | current docs | T1 | verified |
| 12 | https://select.dev/posts/snowflake-terraform | Terraform for Streamlined Snowflake Management | Select.dev | 2024 | T4 | verified — vendor blog |
| 13 | https://select.dev/posts/snowflake-rbac-best-practices | Top 7 Snowflake RBAC Best Practices | Select.dev | 2024 | T4 | verified — vendor blog |
| 14 | https://clickhouse.com/docs/architecture/cluster-deployment | Replication + Scaling | ClickHouse | current docs | T1 | verified |
| 15 | https://clickhouse.com/docs/knowledgebase/why_recommend_clickhouse_keeper_over_zookeeper | Why ClickHouse Keeper over ZooKeeper | ClickHouse | current docs | T1 | verified |
| 16 | https://clickhouse.com/blog/new-terraform-provider-manage-clickhouse-database-users-roles-and-privileges-with-code | New Terraform provider for ClickHouse | ClickHouse | 2024 | T4 | verified — vendor blog |
| 17 | https://clickhouse.com/blog/clickhouse-cloud-terraform-for-continuous-integration-and-continuous-delivery-deployment-ci-cd | ClickHouse Cloud and Terraform for CI/CD | ClickHouse | 2024 | T4 | verified — vendor blog |
| 18 | https://developer.hashicorp.com/terraform/tutorials/configuration-language/provider-versioning | Lock and upgrade provider versions | HashiCorp | current docs | T1 | verified |
| 19 | https://spacelift.io/blog/iac-architecture-patterns-terragrunt | Patterns of IaC Architecture | Spacelift | 2024 | T4 | verified — vendor blog |
| 20 | https://docs.snowflake.com/en/sql-reference/sql/create-clone | CREATE CLONE | Snowflake | current docs | T1 | verified |
| 21 | https://www.unraveldata.com/resources/databricks-serverless-vs-classic-compute/ | Databricks Serverless vs Classic Compute | Unravel Data | 2025 | T4 | verified — vendor analysis |

---

## Sub-question 1: Terraform for Databricks (Workspace, Cluster Policies, Metastore, Permissions)

### Databricks Terraform provider architecture

The Databricks Terraform provider operates at two distinct levels: **account-level** and **workspace-level** [5]. Account-level resources include metastores, workspace creation, and account-wide groups. Workspace-level resources include clusters, cluster policies, jobs, notebooks, and catalog objects. A common pattern uses aliased providers — one pointing to the accounts API endpoint (`host = "https://accounts.cloud.databricks.com"`) and one pointing to the workspace URL — with `depends_on` clauses ensuring proper resource ordering [5].

The provider supports the full lifecycle of Unity Catalog resources: `databricks_metastore` (one per region), `databricks_metastore_assignment` (binding metastore to workspace), `databricks_catalog`, `databricks_schema`, `databricks_grants`, and `databricks_metastore_data_access` for storage credentials [5]. The modular approach recommended by Databricks separates infrastructure into modules: cluster pools, cluster policies, Unity Catalog objects, and external locations, each independently composable [5].

### Cluster policies as cost governance

Cluster policies are the primary mechanism for enforcing cost controls in Databricks [2][7]. Policies are expressed as JSON definitions where each attribute can be constrained using one of six types:

- **fixed** — attribute locked to a specific value (hidden from users)
- **range** — numeric bounds via `minValue`/`maxValue`
- **allowlist** — enumerated permitted values
- **blocklist** — enumerated prohibited values
- **forbidden** — attribute cannot be set at all
- **unlimited** — no restriction, optionally with a default value

A practical cost-control policy fixes auto-termination, limits autoscaling range, and caps maximum DBU consumption:

```json
{
  "autotermination_minutes": {"type": "fixed", "value": 30, "hidden": true},
  "autoscale.min_workers": {"type": "fixed", "value": 1},
  "autoscale.max_workers": {"type": "range", "maxValue": 25},
  "dbus_per_hour": {"type": "range", "maxValue": 100}
}
```

The `dbus_per_hour` virtual attribute is the most direct cost lever — it represents the maximum DBUs a cluster can consume hourly including the driver node, providing a hard ceiling on per-cluster spend [2]. Policies are managed via Terraform using `databricks_cluster_policy` resources and should be maintained through CI/CD pipelines for consistent cross-workspace enforcement [7].

### Unity Catalog metastore and permissions

Unity Catalog follows a one-metastore-per-region architecture [4]. All workspaces within a region share a single metastore, providing consistent access control, auditing, and lineage regardless of workspace. Catalogs within the metastore map to organizational divisions — typically environments (dev, staging, prod), business units, or a combination [4].

Workspace-catalog binding restricts which catalogs are visible in which workspaces. For example, `prod_catalog` can be bound exclusively to `prod_workspace`, ensuring development users cannot access production data even if they hold individual grants [4]. Permissions follow a hierarchy: metastore > catalog > schema > table/view, with grants inheriting downward. Best practice: assign privileges to groups, not individual users [4].

---

## Sub-question 2: Terraform for Snowflake (Warehouses, Databases, Roles, Resource Monitors)

### Snowflake Terraform provider maturity and migration

The Snowflake Terraform provider has undergone a disruptive multi-year evolution [11]. The original community-maintained provider (Snowflake-Labs) went through extensive reworks between v0.85.0 and v1.0.0, making those versions unstable. Version 1.0 released in December 2024 stabilized the API surface, but official Snowflake support only begins with v2.0.0 [11]. Teams on older versions face a forced migration timeline: v0.28.6 removed from registry in January 2026, remaining 0.x.x versions removed by April 2026. The recommended path is to jump directly to v2.x.x following the reimport path rather than stepping through intermediate versions.

Key breaking changes include resource renames (e.g., `snowflake_role` became `snowflake_account_role`) and attribute restructuring. This migration history is a cautionary tale: data platform Terraform providers are less stable than cloud provider Terraform providers (AWS, Azure, GCP), and teams must budget for periodic migration effort.

### Warehouse management via Terraform

Snowflake warehouses are fully manageable through Terraform with parameters including `warehouse_size`, `auto_suspend`, `auto_resume`, `min_cluster_count`, `max_cluster_count`, `scaling_policy`, and `resource_monitor` assignment [12]. The critical configuration pattern:

```terraform
resource "snowflake_warehouse" "etl_wh" {
  name                = "ETL_WH"
  warehouse_size      = "medium"
  auto_suspend        = 60
  auto_resume         = true
  min_cluster_count   = 1
  max_cluster_count   = 3
  scaling_policy      = "STANDARD"
  resource_monitor    = snowflake_resource_monitor.etl_monitor.name
}
```

### Role hierarchy via Terraform

Snowflake RBAC follows a three-tier model [13]: **Access Roles** (data-centric: `READ`, `READWRITE` per database), **Functional Roles** (business-centric: `ANALYST`, `ENGINEER`, `ADMIN`), and **Service Roles** (system-centric: for dbt, Airflow, etc.). Access Roles grant object-level privileges. Functional Roles aggregate Access Roles. Users receive Functional Roles only — never Access Roles directly [13].

Terraform enforces this hierarchy through `snowflake_account_role`, `snowflake_grant_privileges_to_account_role`, and `snowflake_grant_account_role`. The critical anti-pattern: granting Access Roles directly to users. When a new user with similar responsibilities joins, you must manually replicate the same grants. With Functional Roles, adjustments apply to all users automatically [13].

### Resource monitors for cost control

Resource monitors track credit consumption and trigger actions at configurable thresholds [10]. Each monitor supports one suspend action, one suspend-immediate action, and up to five notify-only actions. Thresholds are percentage-based (e.g., notify at 75%, suspend at 90%, suspend-immediate at 100%). Monitors operate at account level (one per account) or warehouse level (one per warehouse) [10].

Critical caveat: suspension is not instantaneous. Running queries may consume credits beyond the threshold before suspension takes effect. Setting thresholds below 100% (e.g., 90%) provides a buffer [10]. Resource monitors only cover warehouse compute — they do not track serverless feature consumption, Snowpark compute, or AI services. For those, Snowflake budgets are required [10].

---

## Sub-question 3: Terraform for ClickHouse

### Two Terraform providers for different deployment models

ClickHouse has two distinct Terraform providers [16][17]:

1. **`ClickHouse/clickhouse`** (official) — manages ClickHouse Cloud services: service provisioning, cloud provider/region selection, tier configuration, idle scaling, and IP access rules. Cannot manage database-level objects.
2. **`clickhousedbops`** — manages database-level objects in both Cloud and self-hosted: databases, users, roles, and privilege grants. For self-hosted clusters with multiple replicas, a `cluster_name` parameter creates resources across all replicas. This parameter must be null for Cloud deployments [16].

This split means ClickHouse Cloud users need both providers for complete IaC coverage. Self-hosted users need `clickhousedbops` plus their cloud provider's Terraform resources (AWS EC2, GCP Compute, etc.) for infrastructure provisioning.

### ClickHouse Cloud service configuration

The Cloud provider manages services with key parameters [17]:

```terraform
resource "clickhouse_service" "analytics" {
  name           = "analytics-prod"
  cloud_provider = "aws"
  region         = "us-east-1"
  tier           = "production"
  idle_scaling   = true
  idle_timeout_minutes = 15
  min_total_memory_gb  = 24
  max_total_memory_gb  = 96
}
```

The `idle_scaling` parameter enables scale-to-zero for cost optimization. Development tier services require `idle_scaling = true` and cannot disable it. Production tier services can optionally enable it. The `min_total_memory_gb` and `max_total_memory_gb` parameters define the scaling boundaries [17].

### Self-hosted cluster configuration

Self-hosted ClickHouse clusters require manual coordination layer setup [14]. The recommended production topology is 2 shards with 2 replicas each, plus a 3-node ClickHouse Keeper cluster. Each node needs macros defined in `config.d/` for shard and replica identification. ReplicatedMergeTree tables use Keeper paths for coordination: `ENGINE = ReplicatedMergeTree('/clickhouse/tables/{database}/{table}/{shard}', '{replica}')` [14].

Keeper nodes need 4GB RAM minimum, with dedicated hosts strongly recommended in production (not co-located with database servers). The `internal_replication = true` cluster config setting ensures writes go to one replica and are replicated automatically, rather than writing to all replicas simultaneously [14].

---

## Sub-question 4: Environment Provisioning Patterns (Dev/Staging/Prod)

### Databricks: workspace separation with Unity Catalog binding

Databricks supports three environment isolation strategies [4][6]:

1. **Separate workspaces per environment** (traditional) — dev, staging, and prod workspaces with code promoted via CI/CD. Provides strongest isolation but highest management overhead.
2. **Shared workspaces with catalog-workspace binding** (recommended) — a single Unity Catalog metastore per region with separate catalogs (dev_catalog, staging_catalog, prod_catalog) bound to their respective workspaces. Users in the dev workspace cannot see prod_catalog regardless of individual grants [4].
3. **Multi-account isolation** (enterprise) — separate Databricks accounts per environment, each with its own Unity Catalog metastore. Maximum isolation but eliminates cross-environment data sharing without Delta Sharing.

Databricks recommends minimizing workspace count while using Unity Catalog governance for logical isolation [4]. For most organizations, three workspaces (dev, staging, prod) linked to a single metastore with catalog-workspace binding provides the right balance of isolation and manageability.

### Snowflake: zero-copy cloning for environment provisioning

Snowflake's zero-copy cloning is the most powerful environment provisioning feature across all three platforms [20]. A clone creates a new metadata pointer to existing micro-partitions — the clone is instant regardless of data volume and consumes zero additional storage until data diverges. Clones are fully independent from the source: modifications to either the clone or the source do not affect the other [20].

Environment provisioning pattern:

```sql
CREATE DATABASE staging_db CLONE production_db;
CREATE DATABASE dev_db CLONE staging_db;
```

This provides dev and staging environments with production-identical data for realistic testing. Storage costs accrue only for modified micro-partitions. Combined with Terraform-managed role separation (dev roles cannot access prod databases), this provides both data fidelity and access isolation [20].

Snowflake environment separation further leverages the account structure: databases, warehouses, and roles are provisioned per environment via Terraform, with resource monitors providing per-environment cost boundaries [12].

### ClickHouse: limited native environment separation

ClickHouse Cloud provides environment separation through separate services — dev and prod services run independently with their own scaling configurations and endpoints [17]. The Terraform provider creates ephemeral services for CI/CD testing, enabling per-branch environments that are destroyed after test completion [17].

Self-hosted ClickHouse lacks native environment separation features. Teams typically run separate clusters for each environment, managed through infrastructure-as-code with environment-specific Terraform variable files. There is no zero-copy cloning equivalent — environment data must be physically copied or generated synthetically.

### Terraform patterns for multi-environment management

The directory-per-environment pattern is superior to Terraform workspaces for permanent environments (dev, staging, prod) [19]:

```
infrastructure/
  modules/
    databricks-workspace/
    snowflake-warehouse/
    clickhouse-service/
  environments/
    dev/
      main.tf        # references modules with dev-specific vars
      terraform.tfvars
    staging/
      main.tf
      terraform.tfvars
    prod/
      main.tf
      terraform.tfvars
```

Terraform workspaces share the same `.tf` files with conditional logic to differentiate environments. This is error-prone: one wrong `terraform workspace select` applies dev changes to production. There is no structural enforcement of differences between environments [19]. Workspaces remain useful for ephemeral environments (feature branches, testing) where the configuration truly is identical.

The recommended hybrid: directories for permanent environments, workspaces for ephemeral ones. Terragrunt adds DRY configuration inheritance — a root `terragrunt.hcl` defines backend and shared variables, environment-level files add overrides [19].

---

## Sub-question 5: Compute Management Patterns

### Databricks: job clusters vs all-purpose clusters

The cost difference between cluster types is the single largest optimization lever in Databricks [3]:

- **Job clusters** cost $0.15/DBU (automated jobs) — they start for a specific job, execute it, and terminate immediately. Optimized for production ETL, batch processing, and scheduled workloads.
- **All-purpose clusters** cost $0.40-$0.55/DBU (interactive compute) — they stay running for collaborative development, ad-hoc analysis, and notebook exploration. Prone to idle time if users forget to terminate.

This 2.5-3.7x cost multiplier means switching scheduled workloads from all-purpose to job clusters is the highest-impact cost optimization most teams can make [3]. The trade-off is startup time: job clusters take 5-12 minutes to provision, which is unacceptable for interactive work but irrelevant for scheduled batch jobs.

**Cluster pools** mitigate startup latency by maintaining idle, ready-to-use instances [3]. Databricks does not charge DBUs for idle pool instances (cloud provider VM charges still apply). Pools reduce cluster startup from 5-12 minutes to under 2 minutes. Best practice: configure pools with a small number of minimum idle instances for frequently-used instance types.

**Serverless compute** represents a third option with fundamentally different economics [21]: $0.70-$0.95/DBU but with 15-30 second startup (vs 5-12 minutes for classic). The break-even point is approximately 30 minutes of execution time — shorter jobs favor serverless despite higher per-DBU cost because eliminated startup overhead reduces total cost. Serverless is optimal for interactive SQL, short notebooks, and bursty workloads. Classic clusters remain superior for jobs exceeding 45 minutes, streaming workloads, and workloads requiring custom libraries or Spark tuning [21].

### Snowflake: warehouse sizing and auto-suspend

Snowflake warehouse sizing should match workload complexity, not default to large [8]:

- **X-Small to Medium** — testing environments, simple queries, low concurrency
- **Large to X-Large** — production analytics, complex joins, moderate concurrency
- **2X-Large+** — heavy ETL, large-scale data processing

Larger warehouses are not necessarily faster for simple queries — they add nodes that sit idle if the query cannot be parallelized [8]. The cost-optimization pattern: start with the smallest size that meets latency requirements and scale up based on measured query performance.

**Auto-suspend** is the primary cost control for warehouses [8]. Snowflake bills per second with a 60-second minimum. Recommended auto-suspend settings:
- **ETL/batch warehouses**: 60 seconds (queries complete and warehouse idles)
- **Interactive/BI warehouses**: 300-600 seconds (balances cache retention with cost)
- **Never disable auto-suspend** unless the warehouse runs continuous workloads

The 60-second minimum billing creates a cost trap for short, frequent queries: if queries arrive every 90 seconds and auto-suspend is 60 seconds, each query triggers a full 60-second minimum charge for the resume cycle [8].

**Multi-cluster warehouses** handle concurrency through auto-scaling rather than warehouse upsizing [9]. Start with max_cluster_count = 2-3 and min_cluster_count = 1. The Standard scaling policy prioritizes performance (starts clusters eagerly); the Economy policy prioritizes cost (waits until queries queue for 6+ minutes). Multi-cluster is for concurrency, not query speed — a single complex query runs at the same speed regardless of cluster count [9].

### ClickHouse: cluster configuration and scaling

Self-hosted ClickHouse scaling follows a shard-and-replicate model [14]:
- **Sharding** distributes data across nodes for horizontal scalability. Each shard handles a subset of the data.
- **Replication** copies data across nodes within a shard for fault tolerance. The standard topology is 2 replicas per shard.

MergeTree engine storage requires attention: data is stored in immutable "parts" that are constantly merged by background processes. Nodes should maintain 2-3x free space relative to the largest unmerged part to accommodate merge operations. The `index_granularity` setting (default 8192 rows) controls the trade-off between index size and scan precision [14].

ClickHouse Cloud's SharedMergeTree eliminates manual shard/replica management by using shared object storage with a Keeper-based metadata layer. It supports hundreds of replicas per table and dynamic scaling without sharding. However, SharedMergeTree is exclusive to ClickHouse Cloud — it is not available for self-hosted deployments.

### ClickHouse Keeper vs ZooKeeper

ClickHouse Keeper is the recommended replacement for ZooKeeper in all ClickHouse deployments [15]. Key advantages:

- **C++ implementation** vs Java — eliminates GC pauses that cause coordination timeouts
- **Lower resource consumption** — 4GB RAM sufficient per Keeper node vs 8GB+ typical for ZooKeeper
- **Better compression** — snapshots and logs consume less disk space
- **Faster recovery** — recovers faster after network partitions
- **No zxid overflow** — ZooKeeper requires restart every ~2 billion transactions; Keeper has no such limit
- **Drop-in compatible** — implements the same protocol as ZooKeeper, making migration straightforward

Keeper has been production-ready since April 2022 and powers ClickHouse Cloud at scale [15]. The minimum deployment is 3 nodes for quorum consensus using the Raft algorithm, with dedicated hosts recommended in production.

---

## Sub-question 6: Platform Versioning and Upgrade Management

### Terraform provider version pinning

Provider version management is critical for data platform stability [18]. The pessimistic constraint operator (`~>`) is the recommended default: `~> 5.31.0` allows patch updates (5.31.x) but blocks minor/major updates that may contain breaking changes. The `.terraform.lock.hcl` file records exact versions and cryptographic checksums — it must be committed to version control [18].

Upgrade procedure: run `terraform init -upgrade` in a non-production environment, execute `terraform plan` to verify no unexpected changes, and only commit the updated lock file after validation. Never upgrade multiple providers simultaneously in a major version jump [18].

### Provider-specific versioning risks

**Databricks provider**: Relatively stable with incremental releases. The primary risk is Unity Catalog feature additions that require provider upgrades to manage new resource types. The provider follows the Databricks platform release cycle.

**Snowflake provider**: The most disruptive upgrade history of the three. The v0.x to v1.0 migration (December 2024) involved resource renames and attribute restructuring. The v1.0 to v2.0 migration introduced further changes with official support only from v2.0.0 [11]. Legacy versions are being removed from the Terraform registry on a rolling schedule through April 2026. Teams must treat Snowflake provider upgrades as project-level work, not routine maintenance.

**ClickHouse provider**: The newest and least mature of the three. Two separate providers (`ClickHouse/clickhouse` for Cloud services, `clickhousedbops` for database objects) add complexity. Breaking changes are more likely in early-stage providers. Pin to exact versions (`=`) rather than pessimistic constraints until the provider stabilizes [16].

### Terraform state management for data platforms

Remote state backends (S3, GCS, Azure Blob) with versioning and locking are non-negotiable for production data platform management [18]. State locking prevents concurrent modifications — DynamoDB for AWS, native locking for Terraform Cloud. State versioning provides rollback capability when applies produce unexpected results.

Component-sliced state files reduce blast radius: separate state for networking, compute (clusters/warehouses), catalog/schema objects, and permissions [19]. A failed cluster policy change should not risk corrupting the state for database schemas. The rollback strategy is VCS-based: revert Terraform configuration to the last known good commit and re-apply [19].

### Resource ownership boundaries

A critical operational pattern is clear ownership boundaries between Terraform and other tools [12]:

- **Terraform owns**: workspace/service creation, cluster policies, warehouse definitions, role hierarchies, resource monitors, catalog/database/schema containers, grants
- **dbt owns**: table and view creation within schemas (do not manage with Terraform)
- **Pipeline tools own**: data loading into tables (Airbyte, dlt, Fivetran column additions)

Violating these boundaries causes state drift: Terraform detects changes made by dbt or Airbyte and attempts to revert them on the next apply. The principle: Terraform manages containers and policies, application tools manage content within those containers [12].

---

## Challenge

Challenger research targeted provider maturity claims, cost optimization magnitudes, environment separation recommendations, and the universality of patterns across platforms. Six findings were challenged.

### Job cluster vs all-purpose cluster cost differential

Multiple sources cite 50-75% cost savings from switching to job clusters [3]. The DBU rate differential is real ($0.15 vs $0.40-$0.55), but the total cost comparison is more nuanced. Job clusters incur startup costs (5-12 minutes of provisioned-but-idle compute), and short-running jobs may spend a significant fraction of their total runtime on startup. Cluster pools mitigate this but add their own VM costs for idle instances. The 50-75% savings figure applies to workloads that run long enough for the startup overhead to be negligible (>15-20 minutes). Short, frequent jobs may see smaller savings or break even.

### Snowflake zero-copy cloning is not truly "zero cost"

Zero-copy cloning creates instant environments at zero additional storage cost — but only until data diverges [20]. In practice, dev and staging environments diverge quickly: test data modifications, schema experiments, and failed loads all create new micro-partitions that are billed to the clone. The initial clone is free, but a dev environment that has been active for weeks may accumulate significant storage. Teams should implement clone refresh schedules (weekly or per-sprint) and drop stale clones to control costs.

### Directory-per-environment is not universally superior to workspaces

The directory-per-environment recommendation [19] assumes environments have meaningful configuration differences. For truly identical environments (same modules, same structure, different variable values), Terraform workspaces eliminate code duplication without the maintenance burden of keeping three directory trees in sync. The risk of accidental cross-environment applies is real but mitigable through CI/CD guardrails (workspace selection in pipeline configuration, not manual commands). The recommendation should be: directories for environments with structural differences, workspaces for environments that are parameter-only variations, with CI/CD enforcement in both cases.

### ClickHouse Terraform provider maturity is overstated

The ClickHouse Terraform providers are positioned as production-ready [16][17], but the split into two providers (Cloud services vs database objects) is a maturity indicator. No other major data platform requires two providers for complete IaC coverage. The `clickhousedbops` provider's restriction that `cluster_name` must be null for Cloud deployments reveals an abstraction leak between deployment models. Teams should expect more breaking changes and fewer community examples compared to the Databricks and Snowflake providers.

### Snowflake provider migration timeline creates real operational risk

The removal of legacy Snowflake provider versions from the Terraform registry [11] means teams that have not migrated will be unable to run `terraform init` once their version is removed. This is not a theoretical risk — it affects any team running versions below v1.0.0, which based on provider download statistics includes a significant portion of the user base. The migration is not trivial: resource renames require state manipulation (`terraform state mv`), and some resources require complete reimport. Teams should treat this as a planned migration project, not a routine upgrade.

### Serverless compute break-even point is workload-dependent

The ~30-minute break-even between serverless and classic compute [21] is a useful heuristic but varies significantly by workload type. The comparison assumes classic clusters run for the full job duration plus startup time. In practice, clusters shared across multiple jobs, clusters with pool-backed fast startup, or clusters with warm caches change the calculation. The break-even is not a single number — it is a function of job frequency, cluster sharing, cache hit rates, and startup configuration.

---

## Findings

### Finding 1: Terraform is the de facto IaC tool for data platforms but provider maturity varies dramatically
**Confidence: HIGH**

Terraform is the standard for managing data platform infrastructure as code — all three platforms (Databricks, Snowflake, ClickHouse) have official providers. However, provider maturity differs fundamentally. The Databricks provider is the most stable, with incremental releases aligned to platform features. The Snowflake provider underwent a multi-year breaking migration from v0.x through v1.0 to v2.0, with official support only from v2.0.0 and legacy versions being removed from the registry through April 2026. The ClickHouse provider is the newest, split across two providers (Cloud services and database objects), and most likely to have breaking changes. Teams must budget for provider maintenance as ongoing operational work, not a one-time setup. Provider version pinning with pessimistic constraints and committed lock files is mandatory.

### Finding 2: Cluster policies and resource monitors are the primary cost governance levers, not manual cluster/warehouse management
**Confidence: HIGH**

In Databricks, cluster policies enforce cost boundaries through JSON attribute definitions — fixing auto-termination, capping autoscaling ranges, limiting DBU-per-hour maximums, and requiring spot instances [2][7]. In Snowflake, resource monitors track credit consumption and trigger suspend/notify actions at configurable thresholds [10]. Both approaches shift cost governance from manual oversight to code-enforced policy. The critical insight: cost controls must be defined at the platform level (policies and monitors), not at the individual workload level. Users who can create unrestricted clusters or warehouses will create unrestricted clusters or warehouses. Policy-as-code via Terraform makes cost governance auditable, version-controlled, and consistently enforced across environments.

### Finding 3: Environment provisioning patterns differ fundamentally across platforms — Snowflake's zero-copy cloning is the standout capability
**Confidence: HIGH**

Snowflake zero-copy cloning creates instant, storage-free environment copies that are fully independent from the source [20]. Databricks uses Unity Catalog workspace-catalog binding for logical isolation within a shared metastore, requiring separate data loading for non-production environments [4]. ClickHouse Cloud uses separate services with no data-sharing mechanism between them [17]. For teams evaluating platforms, Snowflake's cloning capability provides a significant operational advantage: dev and staging environments can have production-identical data without storage duplication or ETL. The caveat is that diverged data accumulates storage costs, requiring periodic clone refresh.

### Finding 4: Directory-per-environment with shared modules is the recommended Terraform pattern for permanent data platform environments
**Confidence: MODERATE**

Directory separation provides explicit, visible environment differences, eliminates accidental cross-environment applies, and enables environment-specific resource additions (monitoring in prod, debug tools in dev) [19]. Terraform workspaces are appropriate for ephemeral environments only. The trade-off is code duplication in per-environment glue code, which shared modules and Terragrunt mitigate. CI/CD pipelines must enforce environment targeting regardless of pattern choice. Resource ownership boundaries are equally important: Terraform owns infrastructure containers and policies, while dbt owns tables/views and pipeline tools own data content [12].

### Finding 5: Databricks compute strategy is a three-way decision between classic job clusters, classic all-purpose clusters, and serverless — each with distinct economics
**Confidence: HIGH**

Job clusters ($0.15/DBU) are 50-75% cheaper than all-purpose clusters ($0.40-$0.55/DBU) for automated workloads but incur 5-12 minute startup latency [3]. Serverless compute ($0.70-$0.95/DBU) eliminates startup latency (15-30 seconds) but carries a higher per-DBU rate [21]. The break-even between serverless and classic is approximately 30 minutes of job execution time. Cluster pools reduce classic startup to under 2 minutes without DBU charges for idle instances. The optimal strategy layers all three: serverless for interactive SQL and short notebooks, job clusters for scheduled production workloads, and all-purpose clusters only for collaborative development with aggressive auto-termination (30-60 minutes) [3].

---

## Claims

| # | Claim | Source | Status | Notes |
|---|-------|--------|--------|-------|
| 1 | Databricks job clusters cost $0.15/DBU vs $0.40-$0.55/DBU for all-purpose clusters | [3] | verified | 50-75% savings; the single largest cost optimization lever |
| 2 | Databricks cluster policies support six attribute constraint types (fixed, range, allowlist, blocklist, forbidden, unlimited) | [2] | verified | JSON-defined, managed via Terraform `databricks_cluster_policy` resource |
| 3 | Unity Catalog requires one metastore per region, shared across all workspaces in that region | [4] | verified | Workspace-catalog binding provides logical isolation within shared metastore |
| 4 | Snowflake zero-copy cloning creates instant environment copies at zero additional storage until data diverges | [20] | verified | Most powerful environment provisioning feature across all three platforms |
| 5 | Snowflake resource monitors support one suspend, one suspend-immediate, and up to five notify actions per monitor | [10] | verified | Suspension is not instantaneous — set thresholds below 100% for buffer |
| 6 | Snowflake RBAC best practice uses three-tier hierarchy: Access Roles, Functional Roles, Service Roles | [13] | verified | Never grant Access Roles directly to users; always through Functional Roles |
| 7 | Snowflake Terraform provider official support starts at v2.0.0; all prior versions unsupported | [11] | verified | Legacy versions being removed from registry through April 2026 |
| 8 | ClickHouse Keeper is production-ready since April 2022 and eliminates ZooKeeper GC pauses | [15] | verified | Uses Raft consensus; 4GB RAM sufficient per node; drop-in compatible |
| 9 | ClickHouse requires two Terraform providers for complete IaC coverage (Cloud services + database objects) | [16][17] | verified | `cluster_name` must be null for Cloud, set for self-hosted multi-replica |
| 10 | Terraform pessimistic constraint (~>) allows only rightmost version increment, preventing breaking changes | [18] | verified | `.terraform.lock.hcl` must be committed to version control |
| 11 | Databricks serverless compute starts in 15-30 seconds vs 5-12 minutes for classic clusters | [21] | verified | Break-even at ~30 minutes job execution time; higher per-DBU rate |
| 12 | Snowflake multi-cluster warehouses handle concurrency, not query speed — single queries run at same speed regardless of cluster count | [9] | verified | Start with max_cluster_count = 2-3, monitor before increasing |
| 13 | Snowflake auto-suspend has a 60-second minimum billing floor that creates cost traps for short frequent queries | [8] | verified | Align auto-suspend with actual query gap intervals |
| 14 | Self-hosted ClickHouse production topology: 2 shards, 2 replicas each, 3-node Keeper cluster | [14] | verified | 2x storage overhead; nodes need 2-3x free space for merge operations |
| 15 | Terraform directory-per-environment is safer than workspaces for permanent environments due to structural enforcement | [19] | qualified | Workspaces viable for identical environments with CI/CD guardrails; directories better when environments differ structurally |
