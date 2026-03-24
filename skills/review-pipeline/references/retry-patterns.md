# Retry & Failure Handling Patterns

## Failure Mode Classification

Every known failure mode must be classified before production:

| Type | Definition | Examples | Action |
|------|-----------|----------|--------|
| **Transient** | Temporary, may resolve on retry | Network timeout, rate limit, connection pool exhaustion, API throttling | Retry with backoff |
| **Terminal** | Permanent, will never resolve on retry | Auth error, schema mismatch, invalid SQL, missing column, permissions denied | Halt immediately |

**Assessment question:** Has every known failure mode been classified? Unclassified failures default to terminal (fail-fast) — but undiscovered transient failures cause unnecessary crashes.

## Retry Strategy Assessment

| Criterion | Good | Anti-pattern |
|-----------|------|-------------|
| Backoff | Exponential with jitter: `min(base * 2^attempt, max_delay) + random()` | Fixed-interval retry (causes thundering herd) |
| Max retries | Bounded (3-5 attempts typical) | Unbounded retries (mask terminal failures) |
| Jitter | Present (prevents synchronized retry storms) | Absent (all retries hit at same interval) |
| Terminal handling | Immediate halt, alert, no retry | Retrying terminal failures (wastes resources, delays detection) |

## Dead Letter Queue

For records that exhaust retries:

| Check | Status |
|-------|--------|
| DLQ exists for failed records? | {{yes / no}} |
| DLQ records include: original payload, error, timestamp, retry count, source? | {{yes / partial / no}} |
| Parking-lot pattern for later investigation? | {{yes / no}} |
| DLQ monitoring and alerting? | {{yes / no}} |

## dlt-Specific Flag

**dlt has no default retry behavior.** Pipelines fail immediately on transient errors unless tenacity is explicitly configured:

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=60))
def load_data():
    pipeline.run(data)
```

This is not optional for production deployments despite being treated as optional in dlt documentation.

## Alert Fatigue Mitigation

| Technique | What It Does |
|-----------|-------------|
| **Deduplication** | Collapse repeated alerts for the same root cause |
| **Grouping** | Bundle related alerts (e.g., all downstream of a failed source) |
| **Suppression** | Silence during known maintenance windows |
| **Severity layering** | Critical → pages on-call; Warning → Slack; Info → dashboards only |
