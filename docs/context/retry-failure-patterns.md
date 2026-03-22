---
name: Retry and Failure Patterns
description: "Terminal vs transient failure classification is the foundation of retry strategy; exponential backoff with jitter prevents thundering herd; dlt has no default retry (must use tenacity); dead letter queues capture records that exhaust retries; alert fatigue is addressable through dedup, grouping, and suppression"
type: context
related:
  - docs/research/2026-03-22-operations-reliability.research.md
  - docs/context/schema-evolution.md
  - docs/context/incremental-loading-patterns.md
---

## Key Takeaway

Every retry strategy starts with one question: is this failure transient or terminal? Retrying terminal failures wastes resources and delays incident detection. Failing to retry transient failures causes unnecessary pipeline crashes. Get this classification right and the rest follows. Get it wrong and retries become a source of problems rather than a solution.

## Failure Classification

**Transient failures** are temporary conditions that may resolve on retry: network timeouts, rate limits, database connection pool exhaustion, cloud API throttling. These should be retried.

**Terminal failures** are permanent conditions that will never resolve on retry: authentication errors, schema mismatches, invalid SQL, missing required columns, permissions denied. These must not be retried.

dlt makes this distinction explicit -- exceptions inherit from either `TerminalException` or `TransientException`. Terminal exceptions immediately halt the pipeline. Airflow and Prefect rely on developer judgment to configure appropriate retry conditions.

## Exponential Backoff with Jitter

The standard formula: `min(base * 2^attempt, max_delay) + jitter`

- **Exponential component** prevents overwhelming a recovering service.
- **Jitter component** (random addition) prevents thundering herd -- multiple retries all hitting the service at the same backoff interval. Without jitter, synchronized retries can cause the exact load spike that caused the original failure.

Prefect supports custom backoff via `retry_delay_seconds` accepting a list (e.g., `[1, 10, 100]` for three retries with increasing delays). More explicit than a formula but less flexible for long retry chains.

## Tool-Specific Retry Behavior

**dlt:** No default retry behavior. This is surprising and under-documented. Pipelines fail immediately on transient errors unless tenacity is explicitly configured. The recommended pattern uses `retry_if_exception(lambda e: not isinstance(e, TerminalException))` with exponential backoff. Add this to the production deployment checklist -- it is not optional despite being treated as optional in documentation.

**dlt `replace` disposition risk:** Truncates the destination table before loading. If loading fails mid-stream, the table is left empty or partially loaded. Use staging with atomic swap where the destination supports it.

**Airflow:** Task-level configuration with `retries`, `retry_delay`, `retry_exponential_backoff`, and `max_retry_delay`. Callbacks (`on_retry_callback`, `on_failure_callback`) enable custom alerting. Trigger rules control downstream task behavior after upstream failures. Airflow SLAs were removed in 3.0 and replaced by Deadline Alerts in 3.1 -- teams upgrading lose SLA functionality in the transition window.

**Prefect:** Flow-level and task-level retries. `on_failure` hooks fire on each retry attempt, not just the final failure. Hooks run in-process and are not guaranteed if the process crashes. For guaranteed alerting, use Cloud automations over in-process hooks.

**Dagster:** Asset materialization is atomic -- succeeds or fails as a unit. Re-materialization targets specific assets without re-running the entire pipeline. Asset checks provide pre- and post-materialization validation.

## Dead Letter Queues

For streaming or event-driven components, DLQs capture failed records after retry exhaustion. DLQ records must include: original payload, error message, timestamp, retry count, source topic/table. The parking-lot pattern moves records from DLQ to a secondary topic after a configurable time for later investigation.

## Alert Fatigue

Alert fatigue is the primary operational burden for data teams. Three techniques reduce noise:

1. **Deduplication** -- collapse repeated alerts for the same root cause into one notification.
2. **Grouping** -- bundle related alerts (e.g., all assets downstream of a failed source) into one incident.
3. **Suppression** -- silence alerts during known maintenance windows.

Dagster addresses dedup natively by alerting only on state changes. Layer alerts by severity: critical pages on-call, warnings go to Slack, informational goes to dashboards only.

## Decision Rules

1. Classify every known failure mode as terminal or transient before going to production.
2. Always use jitter with exponential backoff. Never use fixed-interval retries in distributed systems.
3. Add tenacity retry configuration to dlt pipelines explicitly -- there is no default.
4. Use staging with atomic swap for dlt `replace` disposition to avoid empty-table failures.
5. Layer alerting by severity. Do not send everything to the same channel.
