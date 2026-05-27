# Stepwise Resolution Protocol

**Added:** 2026-03-06
**Last Updated:** 2026-03-06
**Sources:** Clark's meeting insight (one-shot failure mode), Boris Way guide (verification-first development)

## Trigger Conditions

Apply when ALL are true:
- Task is ad-hoc (no predefined `/command` covers it)
- Problem has 3+ unknowns, interdependent parts, or spans multiple systems
- A wrong intermediate assumption would invalidate downstream work

Do NOT apply when:
- Running a predefined command (commands have their own step structure)
- Task is a single lookup, draft, or factual question
- Plan mode is active (plan mode has its own decomposition)

## Protocol

### 1. Decompose

Break the problem into 2-6 sequential steps. Each step must produce a verifiable intermediate result. Present the steps before executing any.

```
Step plan: [problem statement]
1. [Action] → Expected output: [what this produces] → Verify by: [how to check]
2. [Action] → Expected output: [what this produces] → Verify by: [how to check]
3. [Action] → Expected output: [what this produces] → Verify by: [how to check]
```

### 2. Intention Declaration (before each step)

One sentence: "I will [action] to determine [what]. This matters because [dependency on later steps]."

### 3. Execute

Run the step. Produce the intermediate result.

### 4. Fitness Check (after each step)

Three questions:

| Question | If No |
|----------|-------|
| Did this step produce the expected output? | Stop. Diagnose. Restate the step or add a prerequisite step. |
| Does the result confirm or change assumptions for the next step? | Adjust remaining step plan. State what changed and why. |
| Is the next step still the right move? | Reorder or replace steps. Present updated plan. |

If the check reveals the problem is simpler than expected, collapse remaining steps. If harder, add steps.

### 5. Repeat 2-4 until complete

### 6. Synthesize

Present the combined result. Reference which step produced each key finding.

## Verification-First Rule

Define how to verify the result BEFORE executing each step. Tests, queries, type checks, or specific output conditions.

Bad: "Fix the health score discrepancy."
Good: "Fix the health score discrepancy. Verify by querying Catalyst for NbC parent account and confirming score components match transaction data."

## 2-Failure Restart Rule

After 2 failed attempts at the same step, do not iterate further. Instead:
1. State what was tried and why it failed
2. Reassess: is the step correctly scoped? Are prerequisites missing?
3. Either reframe the step, add a prerequisite, or restart from a different angle

Correction loops beyond 2 attempts waste context and compound errors.

## Complexity Heuristics

| Signal | Complexity | Action |
|--------|-----------|--------|
| Single data source, known schema | Low | Direct execution. No protocol needed. |
| 2 data sources OR 1 unknown | Medium | Optional. Use judgment. |
| 3+ unknowns, cross-system, or causal chain | High | Protocol mandatory. |
| Debugging production issue | Always High | Protocol mandatory. Wrong assumptions waste time and create noise. |
| Drafting strategy/proposal with multiple stakeholders | High | Protocol mandatory. Validate framing before content. |

## Anti-Patterns

| Anti-Pattern | Correct Behavior |
|-------------|-----------------|
| "Let me analyze everything at once" | Decompose first. Execute one step at a time. |
| Skipping fitness check because result "looks right" | Always run the 3 questions. Fast when correct. Critical when not. |
| Declaring intent but executing multiple steps before checking | Each step completes and passes fitness check before the next begins. |
| Plan has 10+ steps | Too granular. Consolidate into 2-6 meaningful steps. |
| Fitness check is "looks good, moving on" | Must answer the 3 specific questions. |
| Retrying same failing approach 3+ times | 2-failure restart rule. Reassess after 2 attempts. |
| No verification criteria defined upfront | Define "verify by" for each step during decomposition. |
