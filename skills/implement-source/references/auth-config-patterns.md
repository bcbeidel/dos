# Authentication & Configuration Patterns

## Auth Mechanisms by Source Type

| Source Type | Recommended Auth | Notes |
|-------------|-----------------|-------|
| Transactional DB (PostgreSQL, MySQL) | Service principal + key-pair or Vault dynamic secrets | Per-session credentials via Vault are ideal; key-pair rotation for Snowflake |
| SaaS API (Stripe, HubSpot) | OAuth M2M (1h tokens) | Scope-based least privilege; PATs are legacy anti-pattern |
| Cloud Storage (S3, GCS) | IAM role / service account | No static keys; use workload identity federation |
| File-based (SFTP, FTP) | Key-pair authentication | Avoid password auth; rotate keys on 90-day schedule |
| Event Stream (Kafka) | mTLS or SASL/SCRAM | Certificates preferred over passwords |

## Credential Management Assessment

Evaluate during source implementation:

| Criterion | Green | Yellow | Red |
|-----------|-------|--------|-----|
| Secret storage | Centralized vault | Cloud-native secrets manager | Config files, env vars in code |
| Rotation cadence | Automated, <90 days | Manual, quarterly | Never rotated / unknown |
| Token lifetime | Short-lived (<1h) | Medium (hours-days) | Static / no expiry |
| Access scope | Least privilege, per-workload | Shared across related services | Shared admin credentials |
| Audit trail | All access logged | Partial logging | No audit trail |

**Anti-patterns to flag:**
- Static PATs with no expiration
- Shared credentials across multiple pipelines
- Secrets in `.env` files committed to version control
- Personal user accounts for automated workloads

## dlt Config/Secrets Separation

dlt separates configuration (non-sensitive, safe to commit) from secrets (sensitive, never commit):

| File | Purpose | Commit? |
|------|---------|---------|
| `.dlt/config.toml` | Destination type, dataset name, batch size | Yes |
| `.dlt/secrets.toml` | Database credentials, API keys, tokens | **Never** |
| Environment variables | Override both config and secrets (highest priority) | N/A |

**Environment variable naming:** Uppercase with double underscores for nesting:
```
DESTINATION__POSTGRES__CREDENTIALS__HOST=db.example.com
DESTINATION__POSTGRES__CREDENTIALS__PASSWORD=secret
SOURCES__MY_API__API_KEY=sk-xxx
```

**Known pitfalls:**
- Bug #2782: `dlt.config.get()` reads from `secrets.toml` — test separation explicitly
- Silent env var failures: wrong nesting structure produces no warning, falls back to TOML
- Progressive section elimination: dlt searches progressively shorter paths, which can match unintended values
