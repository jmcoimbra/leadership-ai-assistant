# Agentic Systems — Implementation Patterns

Operational frameworks extracted per chapter. Two lenses: (A) brain diagnostics via the 7-component agent taxonomy, (B) team AI adoption playbook organized by team.

---

## Part A: Brain Diagnostics (Ch 1, 7-8, 10-11)

The brain project IS an agentic system. The 7-component framework diagnoses it.

### Ch 1 — Introduction to Agents (Taxonomy)

**5 core components of any agent:**
1. Profile/Persona — identity, instructions, constraints
2. Actions/Tools — what the agent can do in the world
3. Memory/Knowledge — what the agent knows and remembers
4. Reasoning/Evaluation — how the agent thinks and checks its work
5. Planning/Feedback — how the agent sequences tasks and learns from outcomes

**Agent type spectrum:**
- Direct interaction (user drives) → Proxy (agent mediates) → Assistant (gated autonomy) → Autonomous (full autonomy)
- Brain operates as "Assistant" type: researches autonomously, gates all external actions on [Brain Owner]'s approval

**Brain diagnostic:**
| Component | Brain Implementation | Status |
|-----------|---------------------|--------|
| Persona | CLAUDE.md system prompt + voice profile | Strong |
| Actions | 250+ MCP tools ([Your IDP Tool], Notion, Slack, GitHub, Calendar, Jira) | Strong |
| Knowledge | `context/knowledge/` (18 topic files), `09_people/` person files | Strong |
| Memory | `memory/MEMORY.md` + feedback files | Adequate |
| Evaluators | None. No skill self-checks its output before presenting | **Missing** |
| Planners | Plan mode + `/next-task` + task tracker | Adequate |
| Feedback | `/improve` + Error Correction Log + knowledge base | Strong |

**Gap:** Evaluators. The brain generates meeting scripts, Slack drafts, PR reviews, and stakeholder comms without any critic pass. High-stakes outputs go straight from generation to presentation.

### Ch 8 — Agent Memory and Knowledge (Memory Architecture)

**Memory taxonomy:**
- Sensory memory (immediate RAG context) → Short-term (conversation buffer) → Long-term (semantic + episodic + procedural)
- Long-term subdivides: semantic (facts), episodic (experiences), procedural (how-to)

**Brain mapping:**
| Memory Type | Brain Equivalent | Notes |
|-------------|-----------------|-------|
| Sensory | Tool results in current context | Ephemeral, per-session |
| Short-term | Conversation history | Compressed automatically |
| Long-term semantic | `context/knowledge/` files | Facts, patterns, tool behaviors |
| Long-term episodic | `99_archive/decision_log.md`, meeting notes, 1:1 logs | Dated experiences |
| Long-term procedural | `.claude/commands/` skills, CLAUDE.md contextual rules | How-to encoded as triggers |

**Memory compression pattern:**
- Cluster similar memories via k-means, then summarize each cluster into a single representative memory
- Application: brain files that exceed 25K tokens (decision_log.md) could benefit from periodic compression: cluster related entries, summarize clusters, archive originals
- Current approach (quarterly split) is simpler but loses cross-entry patterns

**RAG architecture (book's pattern):**
- Load → Transform/Split → Embed → Store → Retrieve → Augment prompt
- Brain does NOT use embedding-based retrieval. Uses keyword search (Grep/Glob) which is deterministic but misses semantic similarity
- Trade-off: keyword search is transparent and debuggable. Embedding search catches more but is opaque

### Ch 10 — Agent Reasoning and Evaluation (Evaluator Patterns)

**Reasoning techniques applicable to skills:**
- Zero-shot CoT ("Let's think step by step") — free accuracy boost for complex skills
- Self-consistency: run the same prompt N times, take majority vote. Reduces variance on high-stakes outputs
- Prompt chaining: break complex tasks into sequential sub-prompts. Each step is simpler and more reliable

**LLM-as-evaluator pattern:**
- Second LLM call scores the output of the first against a rubric
- Rubric = criteria + 1-5 scale + grounding statement (what each score means)
- Application: high-stakes skills (`meeting-ingest`, `pr-review`, `slack-triage`) get a critic pass before output

**Embedding similarity scoring:**
- Compare generated output to reference examples via cosine similarity
- Application: voice profile compliance. Compare draft to known [Brain Owner] messages. Flag if similarity drops below threshold

**Brain action:** Add evaluator pass to 3 skills. Define rubrics: what does a 5/5 meeting script look like? What disqualifies a PR review?

### Ch 11 — Agent Planning and Feedback (Feedback Loops)

**Planning patterns:**
- Sequential planner: fixed sequence of steps. Predictable but rigid
- Iterative planner: execute → evaluate → replan. Flexible but expensive
- Brain uses sequential planning (plan mode with explicit steps). Missing: iterative replanning when a step fails

**Feedback types:**
- Corrective: "that was wrong, fix it" (Error Correction Log)
- Suggestive: "try this approach instead" (`/improve` loop)
- Epistemic: "here is new knowledge that changes the landscape" (knowledge base updates)
- Brain has all three. Strong point: the `/improve` command explicitly routes learnings

**Missing feedback loop:** No automated detection of skill output quality degradation. A skill could produce worse results after a CLAUDE.md change and nobody would know until a human notices.

---

## Part B: Team AI Adoption Playbook (Ch 2-7, 9)

Organized by team, not by chapter. Each pattern references its source chapter.

### QA Team

**Behavior trees for test automation (Ch 6):**
- Selector (fallback) node: try automated test → if fails, try alternative path → if fails, flag for human
- Sequence node: all conditions must pass (precondition check → test execution → result validation)
- Application: QA test orchestration. Replace linear test scripts with tree-structured control flow that handles failures gracefully
- Immediate use: flaky test handling. Selector node retries with different conditions before failing the suite

**LLM-as-evaluator for test quality (Ch 10):**
- Second LLM call scores test case quality: coverage, clarity, edge case inclusion
- Application: when AI generates test cases (CWR Walk phase), a critic agent validates them before they enter the suite
- Rubric: Does the test case cover the happy path AND at least one edge case? Is the assertion specific (not just "no error")?

**Self-consistency for test plan review (Ch 10):**
- Generate test plan 3 times, compare. Items appearing in all 3 are high-confidence. Items in only 1 are speculative
- Application: AI-generated test plans get a consistency check before QA engineer review

### Mobile Team

**Multi-agent patterns for service orchestration (Ch 4):**
- Controller/worker: one agent coordinates, specialists execute. Controller evaluates results before returning
- Critic/reviewer pattern: writer agent generates, reviewer agent validates. Only validated output surfaces
- Application: [Engineering Toolkit] plugin development. Writer skill generates code, reviewer skill validates against patterns before PR creation
- CrewAI's `allow_delegation=True/False`: specialists that should NOT delegate (classifier agents, routing decisions) vs ones that can (research agents spawning sub-queries)

**Parallel tool dispatch (Ch 5):**
- Single LLM response triggers multiple independent tool calls simultaneously
- Application: sprint health checks fire Jira + CircleCI + Sentry in parallel, not sequentially. 3-5x latency reduction
- Already a pattern in Claude Code. Make it explicit in skill design: list independent queries, fire them in one block

**Selector fallback for MCP tools (Ch 6):**
- Primary tool → alternative tool → flag for human. Three-tier fallback
- Application: any skill calling [Your IDP Tool]/Notion/Slack. If MCP tool returns empty, try alternative query. If still empty, surface the gap instead of producing output from no data
- Current gap: skills that get empty MCP results silently produce thin output. No fallback, no flag

**Agent platform architecture (Ch 7):**
- 7-component diagnostic as design checklist: Persona, Actions, Knowledge, Memory, Evaluators, Planners, Feedback
- Application: when reviewing any AI feature proposal ([Engineering Toolkit] skills, new MCP tools), check which components are addressed. Missing component = missing capability

### Developer Support Team

**Ticket classification agents (Ch 1, 4):**
- Profile: "You are a Dev Support triage agent. Classify tickets as: bug, config error, feature request, knowledge gap"
- Actions: read ticket, query Jira history, check [Your IDP Tool] for similar issues
- Application: automated first-pass triage. Agent classifies, human confirms. Reduces classification time from minutes to seconds

**Selector fallback for triage routing (Ch 6):**
- Check known solutions DB → check similar tickets → check documentation → escalate to human
- Application: Dev Support resolution flow. Agent searches knowledge base first. Only surfaces tickets that genuinely need human judgment
- Reduces "easy" ticket volume for the team. Frees time for complex investigation

**RAG for internal documentation (Ch 8):**
- Load internal docs → chunk → embed → retrieve relevant context for each ticket
- Application: Dev Support agents retrieve relevant Zendesk articles, Runbook entries, and Confluence pages when triaging
- Current state: manual search. Agent-assisted retrieval would surface relevant docs automatically

### Cross-Team Patterns

**Prompt engineering discipline (Ch 9):**
- Build → Write → Evaluate → Batch evaluate → Ground → Deploy
- Application: ANY team creating AI-powered workflows. Do not ship prompts without evaluation
- Current gap: brain skills ship without batch evaluation. No test set, no rubric, no validation

**Tool description quality (Ch 5):**
- Function/tool descriptions are what the LLM uses to decide which tool to call. Bad descriptions = wrong tool selection
- Application: MCP tool descriptions in [Your IDP Tool]. If agents select wrong tools, fix descriptions first, prompts second
- Audit: review 3 most-used MCP tool descriptions for precision

**Cache/resumability (Ch 4):**
- Cache identical calls (SQLite + cache_seed). Enables resumable long operations
- Application: batch PR reviews, sprint analysis. If interrupted, resume from last cached result instead of restarting
- Claude Code does not natively cache. But skills can implement checkpoint files for multi-step operations
