---
name: Agentic Phase Patterns
description: "Plan-execute-resume-verify lifecycle with inspectable artifacts at each phase boundary is the production pattern for multi-step agent work; a deterministic workflow engine -- not the agent -- controls phase transitions; atomic skills (<150 lines) composed through orchestration outperform monolithic skills; resumability requires durable checkpoint storage and idempotent tool calls"
type: context
related:
  - docs/research/2026-03-22-skill-design.research.md
  - docs/context/deterministic-gates-hooks.md
  - docs/context/cross-provider-skill-portability.md
---

## Key Takeaway

Production-grade agentic skills follow a plan-execute-resume-verify lifecycle where each phase produces machine-readable artifacts that the next phase consumes. The critical architectural constraint: a deterministic workflow engine controls phase transitions, not the agent. Without this, agents on complex codebases routinely skip steps, create circular dependencies, or get stuck in analysis loops. This is independently validated by Praetorian (39-agent, 530k-line codebase), QuantumBlack/McKinsey (enterprise engagements), and HatchWorks (production orchestration).

## The Four Phases

1. **Plan** -- Agent produces a structured plan artifact (not freeform text). Praetorian writes plans to `MANIFEST.yaml` with current phase, active agents, and validation status.
2. **Execute** -- Agent performs bounded creative work within the plan's constraints. The orchestrator is stripped of Edit/Write; workers are stripped of Task. This enforces separation between planning and execution.
3. **Resume** -- On interruption or failure, the system resumes from the last checkpoint rather than restarting. State flows through persistent artifacts (MANIFEST.yaml, scratchpad files).
4. **Verify** -- Every agent output goes through evaluation before the workflow proceeds. Deterministic checks run first, followed by optional LLM critic review.

## Inspectable Artifacts at Phase Boundaries

Each phase boundary produces artifacts that are both machine-readable and human-inspectable. This serves three purposes: downstream phases consume them as explicit inputs (not implicit context), humans can audit intermediate state without replaying the entire workflow, and the system can resume from any artifact boundary after interruption. Praetorian writes scratchpad files at `.claude/.output/scratchpad-{task}.md` recording iterations, failures, and next steps.

## Atomic Skill Decomposition

Praetorian enforces a strict <150-line limit for agent definitions. Each atomic agent costs approximately 2,700 tokens per spawn (down from 24,000 in early versions). The critical constraint: agents cannot spawn agents. This prevents delegation loops and forces a flat execution model managed by the orchestrator.

Composite workflows emerge from orchestrator composition of atomic skills, not from monolithic skills. Three orchestration patterns: persisting-agent-outputs (workspace setup), iterating-to-completion (retry within phases with completion promises), and dispatching-parallel-agents (concurrent workers for independent failures).

Anthropic recommends keeping SKILL.md under 500 lines with progressive disclosure to referenced files. The optimal size depends on invocation context: orchestrator-invoked skills need less context and more constraint; human-invoked skills need more context.

## Resumability Requirements

Production resumability requires three components: durable checkpoint storage (PostgreSQL, not in-memory), idempotent tool calls bound to deterministic keys, and the continue-as-new pattern for unbounded workflows. Temporal's durable execution model is the reference architecture. Recovery replays event history from the beginning, skips completed Activities by reading cached results, and resumes at the failure point.

File-based persistence (MANIFEST.yaml, scratchpad files) provides basic resumability within a machine but does not survive hardware failures. Cloud-hosted agent execution provides implicit durability but removes local control. The gap between local convenience and production durability is the primary unsolved problem for resumable coding agents.

Idempotency is non-negotiable: if tool calls re-execute without idempotency, the result is duplicate side effects. File edits must be idempotent, git operations must check current state before acting, and API calls must use idempotency keys.

## Decision Rules

1. Use a deterministic workflow engine to control phase transitions. Never let agents decide what phase they are in.
2. Every phase must produce machine-readable artifacts that the next phase consumes.
3. Keep atomic skills under 150 lines for orchestrator-invoked agents, under 500 lines for human-invoked skills.
4. Agents must not spawn agents. The orchestrator dispatches; workers execute.
5. Implement idempotent tool calls before claiming resumability support.
