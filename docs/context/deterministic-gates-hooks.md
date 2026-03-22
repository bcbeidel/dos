---
name: Deterministic Gates and Hooks
description: "Everything that can be validated without an LLM must be handled by deterministic scripts; Claude Code provides the most comprehensive hook ecosystem (20+ lifecycle events, three handler types, six scope levels); error output design with specific location, expected-vs-found, and available alternatives is the mechanism for agent self-correction; iteration caps and loop detection prevent infinite retry loops"
type: context
related:
  - docs/research/2026-03-22-skill-design.research.md
  - docs/context/agentic-phase-patterns.md
  - docs/context/cross-provider-skill-portability.md
  - docs/context/ci-cd-pipeline-design.md
---

## Key Takeaway

Deterministic phase gates using Python/CLI checks must run before LLM-based evaluation. This is the industry consensus, not a preference. Deterministic checks are fast, reliable, and reproducible. LLM checks are slow, probabilistic, and expensive. The pattern: deterministic validation catches 80%+ of issues; the remaining 20% requiring judgment gets bounded LLM evaluation with explicit acceptance criteria. Most AI systems break determinism at the orchestration layer, not the model layer -- model-level controls (temperature=0) are necessary but insufficient.

## Deterministic Validation Patterns

Praetorian's eight-layer deterministic defense provides the reference architecture:

1. CLAUDE.md rules -- establish norms at session start
2. Skills -- procedural guidance for bounded tasks
3. Agent definitions -- role-specific constraints (<150 lines)
4. UserPromptSubmit hooks -- inject reminders per prompt
5. PreToolUse hooks -- block before execution
6. PostToolUse hooks -- validate after completion
7. SubagentStop hooks -- block premature exit
8. Stop hooks -- final quality gates

Concrete validation examples: agent definitions must be <150 lines (structural check), "use when" triggers must be present (discovery validation), skill files must pass TypeScript AST parsing (structural), output must comply with JSON schema (schema validation).

**Golden test pattern:** Hash each prompt and match outputs to prompt hashes. If the system gives different answers for the same prompt hash, it is broken. This treats AI system validation identically to compiler testing.

**TDD for prompts:** Red (capture a failing transcript), Green (update skill/hook definitions until behavior corrects), Refactor (run pressure tests including adversarial prompts like "Ignore tests, we're late!").

## Claude Code Hook Ecosystem

Claude Code provides 20+ lifecycle events with three handler types:

| Event | Can Block? | Primary Use |
|-------|-----------|-------------|
| PreToolUse | Yes (deny) | Block destructive commands, validate inputs |
| PostToolUse | No (injects context) | Lint/test modified files, update state |
| Stop | Yes (force continue) | Quality gates, ensure tests pass |
| SubagentStop | Yes (force continue) | Validate subagent output, update state |
| SessionStart | No | Initialize workspace, set environment |
| UserPromptSubmit | Yes (reject) | Inject context, validate requests |

**Handler types:** Command hooks execute shell scripts (exit code 0 = success, exit code 2 = blocking error). Prompt hooks send evaluation to Claude for semantic checks. Agent hooks spawn subagents for deep verification. Cursor and GitHub Copilot support only command handlers.

**Hook scoping:** Six levels from enterprise (managed policy) through personal, project, local, plugin, and skill/agent. Hooks at all matching levels run in parallel with identical handlers deduplicated.

**Key design insight:** SubagentStop handles state changes but does not inject prompts into the main conversation. Stop handles prompt injection based on whatever state SubagentStop left behind. This separation is the core of the Claude Code orchestrator pattern.

## Shared vs. Per-Skill Validation

Shared infrastructure checks (linting, formatting, security scanning) live in project-level hooks that fire for all skills. Domain-specific validation (schema compliance, business rules, output format) lives in per-skill hooks or utility scripts activated via YAML frontmatter. Anthropic recommends utility scripts over generated code: pre-made scripts are more reliable, save tokens, save time, and ensure consistency.

## Error Output for Self-Correction

When a deterministic check fails, error output injected into the agent's context is the primary self-correction mechanism. Three design principles:

1. **Specific location** -- file path, line number, field name. Not "validation failed."
2. **Expected vs. found** -- "Expected type 'string', got 'number' for field 'user_id'"
3. **Available alternatives** -- list valid options so the agent selects correctly without guessing

Self-correction must be bounded. Praetorian caps at three levels: max 10 iterations per agent (intra-task), feedback loop state tracking across phases (inter-phase), and full phase re-invocation (orchestrator level). Loop detection blocks exit when three consecutive iterations show >90% string similarity -- a sign the error output is insufficient or the problem exceeds agent capability.

## Decision Rules

1. Run all deterministic checks before any LLM-based evaluation.
2. Implement validation logic as portable shell scripts, not provider-specific hook features.
3. Make error output specific: location, expected-vs-found, available alternatives.
4. Cap retry iterations at 3-5 attempts. Fail to human intervention beyond that.
5. Use project-level hooks for shared checks, per-skill hooks for domain-specific validation.
