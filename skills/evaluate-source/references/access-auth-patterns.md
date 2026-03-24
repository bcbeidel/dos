# Access & Authentication Patterns

## Authentication Mechanisms

| Mechanism | Token Lifetime | Rotation | Best For |
|-----------|:-------------:|----------|----------|
| **OAuth M2M** | 1 hour (auto-expire) | Automatic | Production standard — Databricks, cloud services |
| **Service Account + Key-Pair** | Key-based (no expiry) | 90 days, dual-key zero-downtime | Snowflake `TYPE=SERVICE` users |
| **API Key** | Indefinite | 30-90 day manual schedule | SaaS APIs with simple auth |
| **JDBC Credentials** | Indefinite | 30-90 day manual schedule | Direct database access |
| **Vault Dynamic Secrets** | Per-session (minutes to hours) | Automatic (per-request) | Gold standard — per-execution DB credentials |
| **PAT (Personal Access Token)** | Configurable (often months) | Manual | **Anti-pattern in production** — legacy only |

**Production standard:** Service principals with OAuth M2M (1h tokens). Any token lasting months is a liability.

## Credential Management Checklist

| Criterion | Expected |
|-----------|----------|
| Secrets stored in a secrets manager (not code/config) | Required |
| Rotation automated or on defined schedule | Required |
| No shared credentials across environments | Required |
| No static PATs in production | Required |
| One service principal per workload | Required |
| Minimum required permissions (least privilege) | Required |
| Environment isolation (separate dev/staging/prod) | Required |
| Pre-commit hooks scan for accidental secret exposure | Recommended |

## Anti-Patterns

| Anti-Pattern | Risk | Remediation |
|-------------|------|-------------|
| Static PATs in production | Indefinite exposure window | Replace with OAuth M2M or Vault dynamic secrets |
| Shared credentials across apps | Blast radius of compromise is all apps | One service principal per workload |
| Secrets in code or config files | Exposed in version control | Centralized secrets manager |
| Personal user accounts for pipelines | Pipeline breaks on employee departure | Service principal identity |
| No rotation cadence | Credentials accumulate risk over time | Automated rotation or defined schedule |
| Same credentials for dev and prod | Dev compromise → prod exposure | Environment-isolated credentials |

## Secrets Manager Options

| Option | Rotation Support | Operational Cost | Best For |
|--------|:---------------:|:----------------:|----------|
| **HashiCorp Vault** | Dynamic per-session | High (HA, seal/unseal, DR) | Full control, dynamic DB credentials |
| **AWS Secrets Manager** | Auto via Lambda | Low | AWS-native stacks |
| **Azure Key Vault** | Via Azure Functions | Low | Azure-native stacks |
| **GCP Secret Manager** | Via Cloud Scheduler + Pub/Sub | Low | GCP-native stacks |

Cloud-native managers provide 80% of Vault's security benefit at 20% of the operational cost.

## dlt Configuration Pitfalls

- **Bug #2782:** `dlt.config.get()` reads from `secrets.toml` instead of `config.toml` — test config/secrets separation explicitly
- **Silent env var failures:** Double-underscore nesting errors produce no warning; dlt silently falls back to TOML
- **Silent destination fallback:** Misnamed destinations silently fall back to shorthand type string
