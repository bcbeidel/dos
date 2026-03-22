---
name: "Agentic Skill Design"
description: "Phased skill structure (plan-execute-resume-verify) with inspectable artifacts at each phase is the emerging production pattern; deterministic phase gates using Python/CLI checks outperform LLM-based validation for artifact correctness; Claude Code hooks (PreToolUse, PostToolUse, Stop, SubagentStop) provide the most comprehensive lifecycle event system across coding agents; the Agent Skills open standard enables cross-provider skill portability across 16+ tools; error output design for self-correction requires structured JSON with specific field-level diagnostics; atomic skills with <150 lines are the gold standard for composability; Praetorian's 39-agent platform demonstrates eight-layer deterministic defense with three-level feedback loops; resumability requires idempotent tool calls with checkpoint state serialized to durable storage"
type: research
sources:
  - https://www.praetorian.com/blog/deterministic-ai-orchestration-a-platform-architecture-for-autonomous-development/
  - https://code.claude.com/docs/en/hooks
  - https://code.claude.com/docs/en/skills
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
  - https://agentskills.io/specification
  - https://hatchworks.com/blog/ai-agents/orchestrating-ai-agents/
  - https://medium.com/quantumblack/agentic-workflows-for-software-development-dc8e64f4a79d
  - https://zylos.ai/research/2026-03-04-ai-agent-workflow-checkpointing-resumability
  - https://www.kubiya.ai/blog/deterministic-ai-architecture
  - https://agents.md/
  - https://github.com/agentsmd/agents.md
  - https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks/
  - https://temporal.io/blog/durable-execution-meets-ai-why-temporal-is-the-perfect-foundation-for-ai
  - https://activewizards.com/blog/a-deep-dive-into-langgraph-for-self-correcting-ai-agents
  - https://smartscope.blog/en/generative-ai/github-copilot/github-copilot-agents-md-guide/
  - https://dev.to/burakboduroglu/agentic-coding-rules-skills-subagents-and-reflection-how-we-steer-models-so-multi-step-work-2l59
  - https://github.com/anthropics/skills
  - https://serenitiesai.com/articles/agent-skills-guide-2026
  - https://www.pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns
  - https://github.com/disler/claude-code-hooks-multi-agent-observability
related:
  - docs/plans/2026-03-21-data-pipeline-research-context.plan.md
---

## Summary

**Research question:** What are best practices for designing AI agentic skills with deterministic feedback loops and phased execution?

**Mode:** Technical | **SIFT rigor:** High | **Sources:** 20 | **Searches:** 18 across Google

**Key findings:**
- Phased skill execution (plan, execute, resume, verify) with inspectable artifacts at each phase boundary is the production-grade pattern for multi-step agent work — requirements must be complete before tasks generate, architecture reviewed before implementation starts, and every phase produces machine-readable output that the next phase consumes
- Deterministic phase gates using Python/CLI checks (linters, test suites, schema validation, AST parsing) must run before LLM-based evaluation — the rule is "everything that can be validated without an LLM is handled by deterministic scripts; the LLM is reserved only for tasks requiring reasoning, creativity, or natural language understanding"
- Claude Code provides the most comprehensive hook ecosystem among coding agents with 20+ lifecycle events (PreToolUse, PostToolUse, Stop, SubagentStop, SessionStart, and others), three handler types (command, prompt, agent), and hierarchical scoping from enterprise to per-skill
- The Agent Skills open standard (agentskills.io), stewarded by the Agentic AI Foundation under the Linux Foundation, enables cross-provider skill portability across 16+ tools including Claude Code, GitHub Copilot, Cursor, OpenAI Codex, and Gemini CLI
- Praetorian's 39-agent development platform demonstrates that atomic agents (<150 lines) composed through a deterministic orchestrator with eight layers of defense achieve production reliability — agents cannot spawn agents, the orchestrator is stripped of Edit/Write, and workers are stripped of Task
- Resumability requires durable checkpoint storage (PostgreSQL, not in-memory), idempotent tool calls bound to deterministic keys, and the continue-as-new pattern for unbounded workflows

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://www.praetorian.com/blog/deterministic-ai-orchestration-a-platform-architecture-for-autonomous-development/ | Deterministic AI Orchestration | Praetorian / Nathan Sportsman | Feb 2026 | T4 | verified — vendor blog with production evidence |
| 2 | https://code.claude.com/docs/en/hooks | Hooks reference | Anthropic | current docs | T1 | verified |
| 3 | https://code.claude.com/docs/en/skills | Extend Claude with skills | Anthropic | current docs | T1 | verified |
| 4 | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | Skill authoring best practices | Anthropic | current docs | T1 | verified |
| 5 | https://agentskills.io/specification | Agent Skills specification | Anthropic / AAIF | current | T1 | verified |
| 6 | https://hatchworks.com/blog/ai-agents/orchestrating-ai-agents/ | Orchestrating AI Agents in Production | HatchWorks | 2025 | T4 | verified — practitioner guide |
| 7 | https://medium.com/quantumblack/agentic-workflows-for-software-development-dc8e64f4a79d | Agentic workflows for software development | QuantumBlack / McKinsey | Feb 2026 | T3 | verified — consulting firm with production evidence |
| 8 | https://zylos.ai/research/2026-03-04-ai-agent-workflow-checkpointing-resumability | AI Agent Workflow Checkpointing & Resumability | Zylos Research | Mar 2026 | T5 | verified — research blog |
| 9 | https://www.kubiya.ai/blog/deterministic-ai-architecture | Deterministic AI Architecture | Kubiya | 2025 | T4 | verified — vendor blog |
| 10 | https://agents.md/ | AGENTS.md | AAIF / Linux Foundation | current | T2 | verified — open standard |
| 11 | https://github.com/agentsmd/agents.md | AGENTS.md repository | AAIF | current | T2 | verified |
| 12 | https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks/ | Automate Your AI Workflows with Claude Code Hooks | GitButler | 2026 | T5 | verified — practitioner blog |
| 13 | https://temporal.io/blog/durable-execution-meets-ai-why-temporal-is-the-perfect-foundation-for-ai | Durable Execution meets AI | Temporal | 2025 | T4 | verified — vendor blog |
| 14 | https://activewizards.com/blog/a-deep-dive-into-langgraph-for-self-correcting-ai-agents | LangGraph for Self-Correcting AI Agents | ActiveWizards | 2025 | T5 | verified — practitioner blog |
| 15 | https://smartscope.blog/en/generative-ai/github-copilot/github-copilot-agents-md-guide/ | AGENTS.md Cross-Tool Unified Management Guide | SmartScope | Feb 2026 | T5 | verified — community guide |
| 16 | https://dev.to/burakboduroglu/agentic-coding-rules-skills-subagents-and-reflection-how-we-steer-models-so-multi-step-work-2l59 | Agentic Coding: Rules, skills, subagents, and reflection | Burak Boduroglu | 2026 | T5 | verified — practitioner blog |
| 17 | https://github.com/anthropics/skills | Agent Skills repository | Anthropic | current | T1 | verified |
| 18 | https://serenitiesai.com/articles/agent-skills-guide-2026 | AI Agent Skills Guide 2026 | Serenities AI | 2026 | T5 | verified — community guide |
| 19 | https://www.pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns | Claude Code Hooks: Production Quality CI/CD Patterns | Pixelmojo | 2026 | T5 | verified — practitioner blog |
| 20 | https://github.com/disler/claude-code-hooks-multi-agent-observability | Claude Code Hooks Multi-Agent Observability | disler | 2026 | T5 | verified — open source implementation |

---

## Sub-question 1: Phased Skill Structure (Plan, Execute, Resume, Verify)

### The four-phase lifecycle

Production-grade agentic skills follow a plan-execute-resume-verify lifecycle where each phase produces inspectable artifacts that the next phase consumes [1][7]. This is not optional architectural elegance — it is the mechanism that prevents agents from skipping steps, creating circular dependencies, or getting stuck in analysis loops on larger codebases with cross-cutting concerns [7].

The phases:

1. **Plan** — Agent produces a structured plan artifact (not freeform text). Requirements, designs, and tasks carry machine-readable metadata so the workflow engine can move work forward deterministically [7]. Praetorian's platform writes plans to `MANIFEST.yaml` with current phase, active agents, and validation status [1].
2. **Execute** — Agent performs bounded creative work within the plan's constraints. The orchestrator strips planning tools from workers (no Task/TodoWrite) and strips execution tools from the orchestrator (no Edit/Write), enforcing separation [1].
3. **Resume** — On interruption or failure, the system resumes from the last checkpoint rather than restarting. State flows through persistent artifacts (MANIFEST.yaml, scratchpad files), enabling any session to pick up from where it left off [1][8].
4. **Verify** — Every agent output goes through evaluation before the workflow proceeds. Deterministic checks run first (linters, test suites, structural validation), followed by optional critic-agent review for judgment calls [7].

### Inspectable artifacts at phase boundaries

Each phase boundary produces artifacts that are both machine-readable and human-inspectable [1][6]. This serves three purposes: downstream phases consume them as explicit inputs (not implicit context), humans can audit intermediate state without replaying the entire workflow, and the system can resume from any artifact boundary after interruption.

Praetorian's implementation writes persistent scratchpad files at `.claude/.output/scratchpad-{task}.md` recording iterations, failures, and next steps [1]. QuantumBlack's approach treats requirements, designs, and tasks as typed artifacts with consistent structure, traceability, and sequencing metadata [7].

The HatchWorks two-phase action pattern separates work into Plan (agent proposes structured actions with evidence) and Validate (deterministic policy checks, not another LLM call), where plans become signed artifacts creating an audit trail separate from execution [6].

### Phase transition enforcement

A deterministic workflow engine — not the agent — controls phase transitions [7]. Agents do not decide what phase they are in or what comes next; they execute tasks given to them by the workflow engine. QuantumBlack reports that without this constraint, agents on larger codebases "routinely skipped steps, created circular dependencies, or got stuck in analysis loops" [7].

Praetorian's 16-phase orchestration template includes compaction gates that enforce token hygiene at phases 3, 8, and 13 — heavy execution phases trigger context checks. Thresholds below 75% proceed normally, 75-85% issue warnings, and above 85% hard-block all Task tool calls [1].

---

## Sub-question 2: Deterministic Phase Gate Patterns

### The deterministic-first principle

The consensus across production implementations is unambiguous: everything that can be validated without an LLM must be handled by deterministic scripts [1][6][9]. The LLM is reserved only for tasks requiring reasoning, creativity, or natural language understanding. Validation is deterministic (rules + policies), not "another LLM prompt" [6].

Kubiya frames this as: "Most AI systems break determinism at the orchestration layer, not the model layer" [9]. The practical implication is that model-level controls (temperature=0, fixed seeds) are necessary but insufficient — the entire workflow pipeline must be architected for predictability.

### Python/CLI check patterns

Praetorian's platform implements an eight-layer deterministic defense [1]:

| Layer | Mechanism | Purpose |
|-------|-----------|---------|
| 1 | CLAUDE.md rules | Establish norms at session start |
| 2 | Skills | Procedural guidance for bounded tasks |
| 3 | Agent definitions | Role-specific constraints (<150 lines) |
| 4 | UserPromptSubmit hooks | Inject reminders per prompt |
| 5 | PreToolUse hooks | Block before execution |
| 6 | PostToolUse hooks | Validate work completion |
| 7 | SubagentStop hooks | Block premature exit |
| 8 | Stop hooks | Final quality gates |

Concrete validation examples from production [1]:

- **Leanness check**: Agent definitions must be <150 lines (structural, no LLM needed)
- **Discovery validation**: "Use when" triggers must be present and valid
- **TypeScript AST validation**: Skill files pass structural parsing before deployment
- **Output schema compliance**: JSON structure validation against expected schemas
- **Pressure testing**: Inject adversarial prompts ("Ignore tests, we're late!") to verify hooks hold firm

### Golden test pattern

Kubiya's deterministic architecture uses golden IO testing — byte-for-byte test cases that must pass on every build [9]. Each prompt is hashed, and outputs are matched to prompt hashes. "If your system gives different answers for the same prompt hash, it's broken, and you'll know immediately" [9]. This treats AI system validation identically to compiler testing: deterministic inputs produce deterministic outputs, verified through CI.

### TDD for prompts

Praetorian applies Red-Green-Refactor to prompt engineering [1]:

1. **Red**: Capture a transcript where the agent fails the desired behavior
2. **Green**: Update skill/hook definitions until behavior corrects
3. **Refactor**: Run pressure tests against patched artifacts to verify robustness

This is the most rigorous validation pattern found — it treats agent behavior as testable code rather than probabilistic output.

---

## Sub-question 3: Claude Code Hooks Ecosystem

### Lifecycle events

Claude Code provides 20+ hook lifecycle events, the most comprehensive among coding agents [2]. The key events for skill design:

| Event | When | Can Block? | Primary Use |
|-------|------|-----------|-------------|
| `PreToolUse` | Before tool executes | Yes (deny) | Block destructive commands, validate inputs |
| `PostToolUse` | After tool succeeds | No (but injects context) | Lint/test modified files, update state |
| `Stop` | Agent finishes responding | Yes (force continue) | Quality gates, ensure tests pass |
| `SubagentStop` | Subagent completes | Yes (force continue) | Validate subagent output, update state |
| `SessionStart` | Session begins/resumes | No | Initialize workspace, set environment |
| `UserPromptSubmit` | Before prompt processed | Yes (reject) | Inject context, validate requests |
| `TaskCompleted` | Task marked complete | Yes (block) | Verify completion criteria |

### Handler types

Claude Code differentiates with three handler types, while Cursor and GitHub Copilot support only command handlers [2][19]:

1. **Command hooks**: Execute shell scripts. Input arrives on stdin as JSON. Exit code 0 = success, exit code 2 = blocking error. This is the workhorse for deterministic validation.
2. **Prompt hooks**: Send evaluation prompts to Claude model. Use for semantic checks that require LLM judgment (e.g., "Does this code follow our architecture patterns?").
3. **Agent hooks**: Spawn subagents for deep verification tasks. Use when validation requires codebase exploration or multi-step reasoning.

### Hook scoping and composition

Hooks are configured at six scope levels with clear precedence [2]:

| Scope | Location | Shareable |
|-------|----------|-----------|
| Enterprise (managed) | Managed policy | Yes |
| Personal | `~/.claude/settings.json` | No |
| Project | `.claude/settings.json` | Yes |
| Local | `.claude/settings.local.json` | No |
| Plugin | `hooks/hooks.json` in plugin | Yes |
| Skill/Agent | YAML frontmatter | Yes |

This enables a layered composition model: enterprise-level security gates, project-level lint checks, and per-skill lifecycle hooks all coexist. Hooks at all matching levels run in parallel, with identical handlers deduplicated [2].

### Practical hook patterns

**PostToolUse linting** — After any Edit or Write, run the linter on the modified file. If linting fails, inject the error output as context so Claude self-corrects [2][12]:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/lint-check.sh"
      }]
    }]
  }
}
```

**Stop quality gate** — Prevent the agent from stopping until tests pass. Check the `stop_hook_active` field to prevent infinite loops [2]:

```json
{
  "decision": "block",
  "reason": "More work needed: tests still failing"
}
```

**SubagentStop state management** — Archive subagent results and update orchestrator state. The critical design insight: SubagentStop handles state changes but does not inject prompts into the main conversation. Stop handles prompt injection based on whatever state SubagentStop left behind. This separation is the core of the Claude Code orchestrator pattern [1][19].

---

## Sub-question 4: Shared vs. Per-Skill Check Library Composition

### The composition problem

As skill libraries grow, validation logic duplicates. The same lint check, test runner, or schema validator gets reimplemented across skills. Two composition strategies emerge: shared check libraries consumed by multiple skills, and per-skill validation embedded in each skill's lifecycle [1][4].

### Shared check libraries

Praetorian centralizes tuning parameters in `.claude/config/orchestration-limits.yaml` — retry limits per model cost, phase skip thresholds by work type, compaction gate percentages, and parallel dispatch limits [1]. This is configuration-driven composition: skills read shared config rather than embedding their own limits.

For validation scripts, the pattern is a shared hooks directory at `.claude/hooks/` containing reusable scripts that multiple skills reference. The hook configuration's `$CLAUDE_PROJECT_DIR` variable enables portable references [2]:

```bash
"$CLAUDE_PROJECT_DIR"/.claude/hooks/lint-check.sh
"$CLAUDE_PROJECT_DIR"/.claude/hooks/test-runner.sh
"$CLAUDE_PROJECT_DIR"/.claude/hooks/schema-validate.sh
```

Anthropic's skill authoring guidance explicitly recommends utility scripts over generated code: "Even if Claude could write a script, pre-made scripts offer advantages — more reliable than generated code, save tokens, save time, ensure consistency across uses" [4].

### Per-skill validation

Skills can define hooks in their YAML frontmatter that activate only during the skill's lifecycle [2][3]:

```yaml
---
name: secure-ops
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

This enables domain-specific validation that only fires when the relevant skill is active. A database migration skill checks SQL syntax; a deployment skill verifies environment variables; a code generation skill runs type checking. Each skill carries its own validation contract.

### The recommended approach

The practical pattern combines both: shared infrastructure checks (linting, formatting, security scanning) live in project-level hooks that fire for all skills, while domain-specific validation (schema compliance, business rule enforcement, output format verification) lives in per-skill hooks or utility scripts [1][4]. Uber's internal "Lang Effect" framework demonstrates this at scale — shared primitives wrapped in an opinionated framework, with product-specific validation layered on top.

---

## Sub-question 5: Error Output Design for Agent Self-Correction

### Structured error output is the mechanism for self-correction

When a deterministic check fails, the error output is injected back into the agent's context as the primary mechanism for self-correction [2][6][14]. The quality of this error output directly determines whether the agent can fix the problem or enters a retry loop producing the same broken output.

Claude Code's PostToolUse hooks inject error messages via the `additionalContext` field in the JSON response [2]:

```json
{
  "decision": "block",
  "reason": "Test suite must pass",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "ESLint error in src/auth.ts:42 - 'userId' is defined but never used"
  }
}
```

### Design principles for actionable error output

Anthropic's skill authoring best practices state: "Make validation scripts verbose with specific error messages like 'Field signature_date not found. Available fields: customer_name, order_total, signature_date_signed' to help Claude fix issues" [4]. This follows three principles:

1. **Specific location**: File path, line number, field name — not "validation failed"
2. **What was expected vs. what was found**: "Expected type 'string', got 'number' for field 'user_id'"
3. **Available alternatives**: List valid options so the agent can select the correct one without guessing

The LangGraph actor-critic pattern formalizes this: the Validator node checks outputs against criteria and returns structured feedback that routes back to the actor for another attempt. The state serves as shared memory holding the problem description, the generated answer, and any feedback for correction [14].

### Iteration caps prevent infinite loops

Self-correction must be bounded. Praetorian caps iterations at three levels [1]:

- **Level 1 (Intra-Task)**: Max 10 iterations per agent via `iteration-limit-stop.sh`
- **Level 2 (Inter-Phase)**: `feedback-loop-state.json` tracks implementation-review-test cycles, blocking exit until all phases pass
- **Level 3 (Orchestrator)**: Re-invokes entire phases if macro-goals are missed

QuantumBlack caps iteration attempts at 3-5 to prevent infinite loops; if the agent cannot pass evals within the limit, the workflow fails and rolls back for human intervention [7].

### Loop detection

Praetorian implements loop detection that blocks exit when three consecutive iterations show >90% string similarity [1]. This catches the failure mode where an agent produces nearly identical (broken) output on each retry — a sign that the error output is insufficient for self-correction or the problem exceeds the agent's capability.

---

## Sub-question 6: Atomic vs. Composite Skill Decomposition

### Atomic skills: the <150-line gold standard

Praetorian's production platform enforces a strict <150-line limit for agent definitions — the "thin agent pattern" [1]. Each atomic agent has:

- **Execution cost**: ~2,700 tokens per spawn (down from ~24,000 in early versions)
- **Discovery cost**: ~500-1,000 characters visible to orchestrator
- **Isolation**: Fresh context window per spawn, zero shared history
- **Constraint**: Agents cannot spawn agents (architectural invariant)

This last constraint is critical — it prevents delegation loops and forces a flat "leaf node" execution model managed by the orchestrator kernel. The orchestrator has Task/TodoWrite/Read but is stripped of Edit/Write. Workers have Edit/Write/Bash but are stripped of Task [1].

### Composite skills through orchestration

Composite workflows emerge from orchestrator composition of atomic skills, not from building monolithic skills. Praetorian's three orchestration patterns [1]:

1. **Persisting-agent-outputs**: Invoked at startup to establish the workspace
2. **Iterating-to-completion**: Used within phases when agents need retries, with completion promises (e.g., `ALL_TESTS_PASSING`) that trigger only when success criteria are genuinely met
3. **Dispatching-parallel-agents**: Identifies independent failures and spawns concurrent workers

The dispatching pattern is the most sophisticated — the orchestrator identifies failures with no shared state dependencies and spawns parallel workers. After parallel execution, it verifies no conflicts and integrates fixes sequentially [1].

### Skill decomposition heuristics

The Agent Skills specification recommends keeping `SKILL.md` under 500 lines and using progressive disclosure to split content into referenced files [4][5]. Anthropic's guidance provides a practical decomposition framework:

- **High freedom** (text instructions): Multiple approaches are valid, decisions depend on context — code reviews, research tasks
- **Medium freedom** (pseudocode with parameters): A preferred pattern exists but variation is acceptable — report generation, data analysis
- **Low freedom** (specific scripts, few parameters): Operations are fragile and error-prone, consistency is critical — database migrations, deployments

The analogy: "Think of Claude as a robot exploring a path. Narrow bridge with cliffs = provide specific guardrails (low freedom). Open field = give general direction (high freedom)" [4].

---

## Sub-question 7: Cross-Provider Compatibility

### AGENTS.md: the universal standard

AGENTS.md is an open format standard stewarded by the Agentic AI Foundation under the Linux Foundation, used by 60,000+ open-source projects [10][11]. OpenAI originated the spec in August 2025 for their Codex CLI; in December 2025, the Linux Foundation announced AAIF with AGENTS.md as one of three founding projects alongside Anthropic's MCP and Block's goose [10].

As of March 2026, these tools natively parse AGENTS.md: GitHub Copilot, Cursor, Windsurf, Zed, JetBrains Junie, OpenAI Codex CLI, Google Jules, Gemini CLI, Devin, Aider, goose, and others [10][15]. One AGENTS.md file works across essentially every major AI coding tool.

AGENTS.md is standard Markdown with no mandatory fields or rigid structure — "Think of AGENTS.md as a README for agents" [10]. Best practice is to keep it under 150 lines covering build commands, code style, testing instructions, and project conventions [10].

### Agent Skills: the capability standard

While AGENTS.md provides project-level context, Agent Skills (agentskills.io) provides the standard for packaging reusable capabilities [5][17]. The spec requires only two frontmatter fields (`name` and `description`) and imposes minimal structure. As of March 2026, 16+ tools support Agent Skills including Claude Code, GitHub Copilot, Cursor, OpenAI Codex, and Gemini CLI [18].

The relationship between AGENTS.md and Agent Skills: AGENTS.md tells agents how your project works (conventions, build commands, testing). Agent Skills give agents new capabilities (PDF processing, database analysis, deployment workflows). A project typically has one AGENTS.md and multiple skills [3][10].

### Provider-specific extensions

Each provider extends the base standards with proprietary features [2][3]:

- **Claude Code**: `context: fork` for subagent isolation, `disable-model-invocation` for manual-only skills, hooks in YAML frontmatter, three handler types (command, prompt, agent)
- **GitHub Copilot**: `.github/copilot-instructions.md` for workspace instructions, agent plugins in preview, hooks in `.github/hooks/*.json`
- **OpenAI Codex**: AGENTS.md as primary configuration, skills following the Agent Skills spec

Cross-provider skills should use only the base Agent Skills specification fields (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`) and avoid provider-specific extensions in the core SKILL.md [5].

### GitHub Agent HQ

GitHub launched Agent HQ in February 2026, allowing Copilot Pro+ and Enterprise users to run coding agents from multiple providers (Copilot, Claude, OpenAI Codex) directly inside GitHub, GitHub Mobile, and VS Code [15]. GitHub is expanding to include agents from Google, Cognition, and xAI. This makes cross-provider skill compatibility not just theoretically useful but operationally necessary — the same repository will be worked on by different agents from different providers.

---

## Sub-question 8: Resumability Patterns After Interruption

### Checkpoint boundaries

Three checkpoint granularity models exist in production [8]:

1. **Node-level (LangGraph)**: Every graph node writes state before and after execution. A 50-step workflow generates 50 persisted states, trading storage volume for minimal replay work.
2. **Activity-level (Temporal)**: Each Activity records in Event History. Deterministic workflow code replays against history, skipping completed Activities by reading cached results.
3. **Explicit commit points**: Manual save calls at safe boundaries (reads before writes). Coarser granularity means potential re-work but easier reasoning.

Praetorian's approach uses explicit commit points via MANIFEST.yaml: the process control block persists current phase, active agents, and validation status. Any session can resume from the last checkpoint [1].

### Durable execution for agent workflows

Temporal's durable execution model has become the reference architecture for resumable agent workflows [13]. The core requirement: workflow code must be deterministic — given the same event history, it always produces the same commands. Non-deterministic operations (timestamps, randomness, network calls) must wrap as Activities whose results are recorded in history [8][13].

Recovery flow: a new worker picks up the workflow from the Temporal service, replays event history from the beginning, skips already-completed Activities (reading cached results), and resumes normal execution at the failure point [13]. The 2025 integration between OpenAI's Agents SDK and Temporal brought this pattern to agents built on OpenAI tooling [8].

### Idempotency is non-negotiable

"If a workflow is replayed and tool calls are re-executed without idempotency, the result is duplicate side effects: two tickets created, two emails sent, two charges processed" [8]. The solution: bind external writes to deterministic idempotency keys derived from workflow + step identity. Temporal caches completed Activity results automatically; custom pipelines must implement idempotency at the tool level [8].

For coding agents specifically, this means file edits must be idempotent (editing the same content twice produces the same result), git operations must check current state before acting, and API calls must use idempotency keys [1][8].

### Human-in-the-loop resumability

Workflows persist state, emit interrupts, and halt for human review [8]. Humans review the checkpoint state through a UI or API, provide input, and resume. The agent continues exactly where it paused, with human input injected into its state. This enables a spectrum from fully autonomous (no interrupts) to fully supervised (interrupt before each tool call) [8].

### Continue-as-new for long workflows

Temporal addresses unbounded event-history growth with the continue-as-new pattern: atomically complete the current run and start fresh with the same workflow ID, preserving only essential state [8][13]. LangGraph uses explicit Python type controls to prune stale context and summarize historical information. Without this pattern, long-running agent workflows accumulate unbounded state that degrades performance and eventually exhausts storage [8].

---

## Challenge

Challenger research targeted the novelty of phased execution patterns, the comprehensiveness of Claude Code's hook system, the maturity of cross-provider standards, and the practicality of deterministic validation. Six findings were challenged.

### Phased execution is not new — but agent-specific patterns are

Plan-execute-verify is a well-established software engineering pattern (waterfall, stage-gate). What is genuinely new is applying it to non-deterministic LLM agents where the "execute" phase produces probabilistic output that must be validated deterministically [1][7]. QuantumBlack's contribution is proving this works at enterprise scale across multiple client engagements. Praetorian's contribution is proving it works with 39 agents and 350+ prompts in a 530k-line codebase. The pattern itself is borrowed; the application to agent orchestration is novel and production-validated.

### Claude Code's hook ecosystem is comprehensive but young

Claude Code's 20+ lifecycle events are the most extensive among coding agents [2]. However, the ecosystem is months old (early 2026). GitHub Copilot's hooks (in preview) support a similar event set (`preToolUse`, `postToolUse`, `agentStop`), and the patterns are converging. The architectural insight — deterministic shell commands wrapping non-deterministic agent behavior — is provider-independent. Teams should implement hooks as portable shell scripts that can be adapted to any provider's hook system rather than relying on Claude Code-specific features like prompt or agent handler types.

### AGENTS.md adoption is broad but the spec is minimal

60,000+ projects use AGENTS.md [10], but the specification is deliberately minimal — standard Markdown with no mandatory structure. This is both its strength (universal compatibility) and weakness (no enforcement of quality). Two AGENTS.md files from different projects may bear no structural resemblance. The Agent Skills spec adds more structure (required name/description, validation tooling) but is also intentionally lightweight. Cross-provider skill portability works for simple skills; complex skills with provider-specific hooks, subagent configurations, or tool restrictions will not port cleanly.

### Deterministic validation has limits

The "everything deterministic first" principle is sound [6][9], but some validation inherently requires judgment: "Does this code follow our architecture patterns?" "Is this error message user-friendly?" "Does this implementation match the requirements?" Praetorian addresses this with a hybrid "cyborg" approach — structural checks (AST validation, file sizes, syntax) run deterministically, then an LLM judges clarity, tone, and utility [1]. The deterministic layer catches 80%+ of issues; the remaining 20% requires bounded LLM evaluation with explicit acceptance criteria.

### Resumability patterns assume durable infrastructure

Temporal, LangGraph with PostgresSaver, and Dagster all provide checkpoint persistence [8][13]. But most Claude Code and GitHub Copilot users run agents locally without durable state infrastructure. Praetorian's MANIFEST.yaml approach works for local file-based persistence but does not survive machine failures. True resumability for coding agents requires either cloud-hosted agent execution (GitHub Agent HQ, Anthropic's hosted Claude Code) or explicit local checkpoint management that teams must build themselves.

### Atomic agent sizing is context-dependent

The <150-line rule is Praetorian's gold standard [1], but it applies to their specific architecture where agents are spawned by a deterministic orchestrator. For Claude Code skills used interactively (not orchestrated), Anthropic recommends keeping SKILL.md under 500 lines with progressive disclosure to referenced files [4]. The optimal size depends on whether the skill is human-invoked (more context needed) or orchestrator-invoked (less context, more constraint). The principle — smaller is better for composability — is universal; the specific line count is architecture-dependent.

---

## Findings

### Finding 1: Phased skill execution with inspectable artifacts is the production pattern for multi-step agent work
**Confidence: HIGH**

The plan-execute-resume-verify lifecycle with machine-readable artifacts at each phase boundary is independently validated by Praetorian (39-agent platform), QuantumBlack/McKinsey (enterprise client engagements), and HatchWorks (production orchestration guide). The key mechanism is that a deterministic workflow engine — not the agent — controls phase transitions. Agents execute bounded work within a phase and produce typed artifacts; the engine validates artifacts and advances to the next phase. Without this constraint, agents on complex codebases routinely skip steps, create circular dependencies, or get stuck in analysis loops. Inspectable artifacts serve three purposes: downstream phase inputs, human audit capability, and resumption points after interruption.

### Finding 2: Deterministic phase gates must precede LLM-based evaluation
**Confidence: HIGH**

The industry consensus is unambiguous: Python/CLI checks (linters, test suites, AST parsing, schema validation, file size limits) must run before any LLM-based evaluation. Deterministic checks are fast, reliable, and reproducible. LLM checks are slow, probabilistic, and expensive. Praetorian's eight-layer defense demonstrates the pattern at scale — CLAUDE.md rules, skill constraints, PreToolUse blocking, PostToolUse validation, SubagentStop checks, and Stop quality gates all fire deterministically before optional LLM critic evaluation. The golden test pattern (byte-for-byte expected output matching) and TDD-for-prompts (red-green-refactor on agent behavior) represent the most rigorous validation approaches found.

### Finding 3: Claude Code provides the most comprehensive hook ecosystem, but patterns are converging across providers
**Confidence: HIGH**

Claude Code's 20+ lifecycle events, three handler types (command, prompt, agent), and six-level scoping hierarchy make it the most feature-rich hook system among coding agents. However, GitHub Copilot's hooks (in preview) support a similar event set, and the core pattern — deterministic shell commands wrapping non-deterministic agent behavior — is provider-independent. Teams should implement validation logic as portable shell scripts callable by any provider's hook system. The hook ecosystem's real value is in composition: enterprise security gates, project lint checks, and per-skill validation all coexist through hierarchical scoping with parallel execution and deduplication.

### Finding 4: Cross-provider skill portability is practical for simple skills but limited for complex ones
**Confidence: MODERATE**

Two complementary standards enable cross-provider compatibility: AGENTS.md for project context (60,000+ projects, 20+ tools) and Agent Skills for packaged capabilities (16+ tools). Simple skills that consist of instructions and utility scripts port cleanly across Claude Code, GitHub Copilot, Cursor, and OpenAI Codex. Complex skills that use provider-specific features (Claude Code's `context: fork`, prompt/agent handler types, SubagentStop hooks) do not port without modification. The practical strategy is to write core skill logic in the portable Agent Skills format and layer provider-specific orchestration on top. GitHub Agent HQ — where multiple providers work on the same repository — makes this not theoretical but operationally necessary.

### Finding 5: Resumability requires durable state infrastructure that most local agent setups lack
**Confidence: MODERATE**

Production resumability requires three components: durable checkpoint storage (PostgreSQL, not in-memory), idempotent tool calls bound to deterministic keys, and the continue-as-new pattern for unbounded workflows. Temporal's durable execution model is the reference architecture; LangGraph provides PostgresSaver for production checkpointing. However, most Claude Code and GitHub Copilot users run agents locally without this infrastructure. File-based persistence (MANIFEST.yaml, scratchpad files) provides basic resumability within a machine but does not survive hardware failures. Cloud-hosted agent execution (GitHub Agent HQ, hosted Claude Code) provides implicit durability but removes local control. The gap between local convenience and production durability is the primary unsolved problem for resumable coding agents.

---

## Claims

| # | Claim | Source | Status | Notes |
|---|-------|--------|--------|-------|
| 1 | Praetorian's platform uses 39 agents, 350+ prompts, and a 530k-line codebase with deterministic orchestration | [1] | verified | Medium post corroborates blog post with additional detail |
| 2 | Agent definitions must be <150 lines in Praetorian's thin agent pattern | [1] | verified | Execution cost ~2,700 tokens per spawn |
| 3 | Claude Code provides 20+ hook lifecycle events with three handler types | [2] | verified | Official documentation lists PreToolUse, PostToolUse, Stop, SubagentStop, SessionStart, and 15+ others |
| 4 | Agent Skills open standard is supported by 16+ tools as of March 2026 | [5][17][18] | verified | Anthropic-published specification, adopted by Claude Code, Copilot, Cursor, Codex, Gemini CLI, and others |
| 5 | AGENTS.md is used by 60,000+ open-source projects | [10] | qualified | Self-reported by AAIF; adoption count methodology not detailed |
| 6 | QuantumBlack reports agents routinely skipped steps on larger codebases without deterministic workflow engines | [7] | verified | Based on production engagements across multiple clients |
| 7 | Temporal's durable execution model replays event history and skips completed Activities | [8][13] | verified | Core architectural pattern documented in official Temporal docs |
| 8 | Praetorian's loop detection blocks exit when three consecutive iterations show >90% string similarity | [1] | verified | Specific implementation detail from blog post |
| 9 | GitHub Agent HQ launched February 2026 with Claude and Codex alongside Copilot | [15] | verified | GitHub Changelog and multiple news sources confirm |
| 10 | Claude Code hooks exit code 2 = blocking error; exit code 0 = success with optional JSON | [2] | verified | Official Anthropic documentation |
| 11 | SKILL.md name field must be max 64 characters, lowercase letters/numbers/hyphens only | [5] | verified | Agent Skills specification on agentskills.io |
| 12 | Praetorian enforces tool restriction boundary: orchestrator has Task/Read but no Edit/Write; workers have Edit/Write but no Task | [1] | verified | Prevents delegation loops and forces flat execution model |
| 13 | Kubiya reports byte-for-byte identical outputs running same workflow twice with deterministic architecture | [9] | qualified | Vendor claim; requires fixed model version, temperature=0, and no dynamic context |
| 14 | LangGraph recommends PostgresSaver for production, MemorySaver for development only | [8] | verified | Consistent across LangGraph documentation and Zylos research |
| 15 | Anthropic recommends SKILL.md under 500 lines with progressive disclosure to referenced files | [4] | verified | Official skill authoring best practices |
