# AI How Layer
> Owner: [Brain Owner] | Pillar: [Pillar N] | Status: Draft | Last Audit: [YYYY-MM-DD]

## Purpose

Define what AI-native work looks like for each team. Answer the question: "Which decisions move faster or get safer on an engineer's Tuesday in the AI-native world?"

Relying on the team to discover the answer organically does not work fast enough. Pave the way explicitly.

## The Stack

**Agentic coding tool + personal GitHub repo per team member.**

Replace your chat-UI projects with a GitHub repository the agent operates on. This gives you:
- Version control (every change tracked)
- Auditability (`Co-Authored-By:` on every commit — automatic, no manual tagging)
- Portability (works on any machine with the same agent)

## Capability Artifact Lens

Use to classify what a person BUILDS, orthogonal to the AI tier framework (which measures WHERE they are).

| Layer | What gets built | Signal artifact |
|-------|-----------------|-----------------|
| Prompt Engineering | Better inputs to a chat UI | Prompt library, templated queries |
| Context Engineering | Shaping what the model sees | MCP connections, brain repo, retrieval patterns |
| Harness Engineering | How a single agent rides an LLM | Custom commands, skills, hooks, session templates |
| Orchestration | Multi-agent coordination | Parallel-agent workflows, cross-team automation pipelines |

Rule: promote the vocabulary in 1:1s and IDPs. "What layer is your next artifact?" beats "use AI more."

## Decision-Flow Lens

Every workflow candidate must identify the decision it changes before the team measures usage.

| Field | Required answer |
|-------|-----------------|
| Decision | What decision moves work forward? |
| Current owner | Who makes it today? |
| Evidence | What facts are required? |
| Criteria | What makes the decision pass or fail? |
| Waiting cost | Decision latency, validation queue depth, rework rate, defect leakage, error rate, or MTTR |
| AI role | draft, recommend, validate, decide, or monitor |
| Human role | approver, exception handler, or system owner |
| Trace | Where the decision record lives |

## The Rule

1. **Use AI on your NORMAL work.** Not experiments. Not curiosity projects. Your existing daily tasks.
2. **Before doing a task manually, ask: "Can AI draft this?"** If yes, use it. If no, log why.
3. **Feed your talent review goals into your repo.** Ask the agent to adjust your priorities and course of action. Your repo becomes your personal operating system.
4. **Avoid scope creep.** Don't expand your role or chase novelty. Focus on going faster at what you already do. The creativity comes after the habit forms.

## Migration Plan (per person)

1. Create a GitHub repo (private, personal) — structure it like a project workspace
2. Add your role context: what you do daily, your tools, your talent review goals
3. Start using the agent for your next task (not a special task — the next normal one)
4. Log what worked, what did not, and how long it took vs. manual
5. Bring findings to the next 1:1

## Team Template — One Section per Team

### [Team Name] — [Team Members]

#### Behavioral Switches

| # | Switch | Decision Changed | Trigger | AI Role | Human Owner | Tool | Done Signal |
|---|--------|------------------|---------|---------|-------------|------|-------------|
| 1 | [Specific behavior change] | [Decision moved or validated] | [When it fires] | [draft / recommend / validate / decide / monitor] | [Person] | [Which tool] | [Flow metric delta and trace] |
| 2 | | | | | | | |

#### Current Tools

- [Tool 1]
- [Tool 2]

#### First Week Action

[The next normal task to try with AI, not a special project.]

#### Concerns to Surface in Group Meeting

| # | Concern | Raised By | Resolution |
|---|---------|-----------|------------|
| 1 | [e.g., hallucination risk] | | [Mitigation] |

#### Setup Status

| Member | Brain Repo | Tooling Configured | Blocker |
|--------|-----------|--------------------|---------|
| [Name] | [Y/N] | [Y/N] | |

#### Commitments

| # | Commitment | Owner | Deadline | Verification |
|---|------------|-------|----------|--------------|
| 1 | | | | |

## Cross-Team Pattern — Internal Tickets

All teams use "the brain" to detect repeatable work. The natural order:

1. Team member uses brain daily on normal work
2. Brain accumulates context and patterns
3. AI surfaces what is repeatable ("you've done this 5 times — here's a template")
4. Team understands how to scale it

This is organic, not mandated as a separate initiative. The brain grows smarter as you use it.

## Guardrails

- AI handles first drafts. Humans own judgment, correctness, and production safety.
- Customers/partners never receive raw AI output without human review.
- No expanding role scope to chase AI novelty — stay in your lane, go faster.
- Data sensitivity: no customer PII in prompts. Use anonymized examples.

## Escalation

- If any team member has not used AI on a normal task by end of the rampup window: direct conversation in next 1:1
- If a team's group meeting does not happen by the deadline: schedule it unilaterally

## Cross-References

- AI adoption roadmap: `03_ai_native_transformation/ai_adoption_roadmap.md`
- AI baseline assessment: `03_ai_native_transformation/ai_baseline_assessment.md`

## AI Integration

| Decision | AI role | Human owner | Evidence inputs | Pass/fail criteria | Trace | Exception trigger | Flow metric |
|----------|---------|-------------|-----------------|--------------------|-------|-------------------|-------------|
| Which team behavior switch is ready for adoption? | validate | [Brain Owner] + [Team Lead] | Behavioral switch table, decision-flow lens, baseline assessment, concern log | Switch has named decision, AI role, human owner, evidence, trace, exception trigger, and flow metric | Team section in this file | Switch with only tool usage and no decision-flow metric stays in draft | Decision latency, validation queue depth, rework rate, defect leakage, error rate, MTTR |

This file defines the AI decision layer for each team. Use AI to turn repeated work into workflow candidates, then require a human owner, trigger, tool, proof metric, and decision trace before adoption.
