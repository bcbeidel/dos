---
name: Secrets Management and Credential Rotation
description: "Centralized secrets management with automated rotation is essential -- Vault dynamic secrets generate per-session database credentials eliminating static credential risk; service principals with OAuth M2M (1h tokens) are the production auth standard; PATs and passwords are anti-patterns; cloud-native secrets managers provide 80% of Vault's benefit at 20% of the operational cost"
type: context
related:
  - docs/research/2026-03-22-platform-security-access-control.research.md
  - docs/context/secrets-environment-management.md
  - docs/context/access-control-models.md
  - docs/context/ci-cd-pipeline-design.md
---

## Key Insight

Static credentials are the root cause of most data platform breaches. The fix is two-fold: service principals with short-lived tokens for authentication, and centralized vaults with automated rotation for all other secrets. Vault dynamic secrets are the gold standard (per-session credentials that auto-expire), but cloud-native secrets managers (AWS Secrets Manager, Azure Key Vault) provide most of the benefit with far less operational overhead.

## Service Principal Authentication

Service principals are the exclusive identity type for automated workloads. Never use personal user accounts for pipelines, CI/CD, or scheduled jobs -- employee departures break pipelines and credentials outlive employment.

**Databricks**: OAuth M2M tokens expire after 1 hour and support scope-based least privilege. Scopes restrict what an application can do -- request only what is needed. PATs are legacy; any token lasting months is a liability.

**Snowflake**: `TYPE=SERVICE` users enforce key-pair or OAuth only -- password authentication is blocked at the platform level. Dual-key rotation (via `RSA_PUBLIC_KEY` and `RSA_PUBLIC_KEY_2`) enables zero-downtime credential cycling: assign the new key to the unused slot, migrate clients, then remove the old key.

**Least-privilege patterns** (non-negotiable in production):
1. One service principal per workload -- never share credentials across applications
2. Minimum required permissions -- `SELECT` only for analytics, `INSERT`/`UPDATE` only for ETL write targets
3. Environment isolation -- separate workspaces/accounts for dev, staging, production
4. Short-lived credentials -- OAuth tokens (1h) or Vault dynamic secrets over static PATs

## Vault Dynamic Secrets

Vault's database secrets engine generates credentials on demand:

1. Admin configures a database connection and defines roles with SQL templates
2. Application requests credentials through a role-based endpoint
3. Vault creates a database user with a random password and the defined permissions
4. Vault returns credentials with a unique `lease_id` for audit trail correlation
5. Credentials auto-expire after the configured TTL (default 1h, max 24h)

If an application is compromised, only that application's credentials require revocation -- not a global rotation. For ETL jobs, this means per-execution database credentials that expire when the job completes. No static passwords exist to leak.

The operational cost is real: Vault requires HA deployment, storage backend management, seal/unseal procedures, and DR planning. HCP Vault Secrets (SaaS) reduces this but may not satisfy data residency requirements.

## Cloud-Native Alternatives

For teams without dedicated platform engineering capacity:

- **AWS Secrets Manager**: automatic rotation for RDS, Redshift, DocumentDB via Lambda functions; custom Lambda for other credential types
- **Azure Key Vault**: secret versioning (same name creates new version), event-driven rotation via Azure Functions
- **GCP Secret Manager**: notification-driven rotation via Cloud Scheduler and Pub/Sub

These provide 80% of Vault's security benefit at 20% of the operational cost.

## Rotation Frequency

| Secret Type | Rotation Cadence |
|---|---|
| Dynamic database credentials | Per-session (minutes to hours) |
| OAuth M2M tokens | Auto-expire after 1 hour |
| API keys / static credentials | 30-90 day schedule |
| RSA key pairs (Snowflake) | 90 days, dual-key zero-downtime |
| TLS certificates | Before expiration, automated via ACME/cert-manager |

## OWASP Requirements

Minimum viable secrets strategy from OWASP guidance:
- Never store secrets in plaintext -- encrypt at rest (AES-256-GCM or ChaCha20-Poly1305)
- Centralize in a dedicated secrets manager, not scattered config files
- Enforce TLS for all secret transmission
- Implement pre-commit hooks and CI/CD scanning for accidental exposure
- Use separate vaults/instances for production and development

## Takeaway

Service principal lifecycle management is the actual hard problem. Creating a service principal is trivial; preventing privilege creep over months requires automated access reviews (quarterly minimum) and just-in-time provisioning -- neither is built into Databricks or Snowflake natively. Invest in lifecycle automation, not just credential creation.
