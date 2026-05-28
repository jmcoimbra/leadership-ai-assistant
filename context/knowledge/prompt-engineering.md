# Prompt Engineering — Operational Knowledge

> Archive: `99_archive/prompt_engineering_techniques.md`
> Owner: [Brain Owner] | Pillar: Pillar 4 (AI Execution) | Last Updated: 2026-03-21
> Measurable Outcome: 5+ skills patched with PE patterns by 2026-05-15
> Escalation Trigger: If evaluator rubrics remain prose-based after 30 days

---

## 1. Five Principles Mapped to Skill Authoring

| Principle | Brain Application | Current Gap |
|-----------|------------------|-------------|
| Direction | YAML frontmatter `description:` sets role. First paragraph sets task + context | Some skills lack explicit role definition in description |
| Format | Evaluator rubric tables, Output Summary templates | Rubrics are prose-based, not structured. No schema enforcement on outputs |
| Examples | Few-shot in skill instructions (1-3 representative outputs per format) | No skill includes output examples. Minimum: 1 example per output format |
| Evaluate | Evaluator Pass section with structured criteria | On 3 skills (meeting-ingest, pr-review, slack-triage). Expand to all output-producing skills |
| Divide Labor | Step-by-step execution with per-step success criteria (stage gates) | meeting-ingest has steps but lacked explicit gates. weekly-review (11 steps) needs gates |

**Anti-pattern: Blind Prompting.** Adding instructions without testing whether they change the output. Every skill change must be tested against representative inputs. If you cannot name the test case, the change is blind.

## 2. Structured Output Validation Pattern

When a skill parses MCP tool output or LLM-generated data:

1. **Define expected schema** — fields, types, required vs optional
2. **Validate response against schema** — check structure before using values
3. **If validation fails → try alternative query** (Selector Fallback from ai-agents-in-action.md)
4. **If still fails → surface gap explicitly** — do not silently skip

Application targets: GitHub API responses (PR data, review comments), Notion search results (page properties), Slack search results (message structure).

Pattern source: Ch3 YAML schema validation + Ch4 Pydantic output parsers.

## 3. Evaluator Rubric Upgrade Pattern

Prose rubrics produce inconsistent scoring. Structured rubrics with binary or countable indicators are deterministic.

**Upgrade template:**

| Current (prose) | Upgraded (structured) |
|----------------|----------------------|
| "Every finding references specific code" | "Finding has: file_path (present/absent) + line_number (present/absent) + code_snippet (present/absent). Score = count of 3" |
| "Most items captured" | ">=90% of transcript action items captured (count: X/Y)" |
| "Correct urgency ranking" | "Zero urgency misclassifications in batch (actual escalations = flagged escalations)" |
| "Tone matches [Brain Owner]'s voice" | "Zero forbidden phrases detected. No compliment openers. Assertion-first structure" |

When evaluator pass produces ambiguous score (3/5), use **labeled pairwise comparison**: compare current output vs known-good output for same input type. Pick the better one.

For efficiency criteria beyond correctness (bias rate, tool call ratio, ideal trajectory definitions), see `deep-agent-evals.md`.

## 4. Prompt Chaining Formalization

Every multi-step skill should declare per-step success criteria:

| Step | Input | Output | Gate (proceed if) |
|------|-------|--------|--------------------|
| N | What this step receives | What it produces | Boolean condition to pass |

If gate fails: stop execution, surface the failure, do not continue with degraded input.

Pattern source: Ch10 Research → Interview → Outline → Generate → Style pipeline.

Target skills:
- `meeting-ingest` — 8 steps, gates added for extraction and routing steps
- `weekly-review` — 11 steps, needs gates for scan completeness and metric freshness
- `pr-review` — multi-agent pipeline, needs gates for finding count and severity distribution

## 5. Self-Consistency Pattern

For high-variance outputs (urgency classification, stakeholder drafts, test plan generation):

1. Generate N=3 variants independently
2. Score each against evaluator rubric
3. Present highest-scoring variant (or majority vote for classification)

**When to use:** Only for outputs where variation matters. NOT for deterministic operations (data lookups, file edits, git commands).

**Fail-safe rule:** For safety-critical classifications (urgency=HIGH), if two independent classifications disagree, default to the higher severity.

Target: slack-triage urgency classification, meeting-ingest performance review generation.

## 6. Prewarm/Internal Retrieval Pattern

Before generating output, ask the LLM to recall best practices for the specific task. Then use that recalled context alongside the actual data.

**How it works:**
1. Prompt: "What are the 3 most common mistakes when [doing this specific task]?"
2. LLM generates best practices from its training data
3. Include those best practices as grounding context for the actual task

**Combines with:** Few-shot (Principle 3). Prewarm generates examples on demand rather than hardcoding them. Useful when the task varies too much for static examples.

Target: pr-review (recall review pitfalls for the PR's language/framework before generating findings).

## 7. Explore-Agent-in-Plan-Mode Anti-Pattern

When delegating to the `Explore` subagent during plan mode (Phase 1: Initial Understanding), the agent sometimes returns clarifying questions instead of a research summary, even when the prompt explicitly asked for read-only investigation with file paths and findings.

**Repro (2026-04-29):** Plan-mode Explore agent prompt asked to find every reference to "top nav menu" / "placement" in the app-preview codebase, with explicit "Do not edit anything. Read-only" + "Report back with file paths, line numbers, and short snippets, under 400 words."

The agent returned: "Before I proceed with the modifications, I need to clarify a few things to ensure the changes are implemented correctly: 1. Placement field in NavigationTabStyle... 2. Default behavior... 3. toggleNavTabs function... 4. Testing scope..."

The agent inverted the contract: treated the read-only research request as an implementation request and asked questions back. Manual file reads recovered the findings in ~5 minutes.

**Mitigation in the prompt:**
1. Open with the verb explicitly: "INVESTIGATE only. Do not propose changes. Do not ask clarifying questions."
2. Specify the EXACT output shape: "Output: file paths + line numbers + 1-line summary per match. No other content."
3. Anchor the boundary: "If you finish the search and want to ask a clarifying question, instead append it as a 'Questions for the user' section at the end of the report. Never as the entire response."
4. For plan mode specifically, the orchestrator should treat any Explore output that opens with "Before I proceed..." or contains a clarifying-questions list as a partial result and re-read the relevant files directly rather than re-prompting the agent.

Source: 2026-04-29 [your-org]-app-preview top-nav-removal plan. Cost: agent round-trip wasted; orchestrator re-read 3 files manually to confirm the findings the agent had clearly already gathered.
