---
name: manager-influence-strategy
description: Manager influence strategy lens for detecting influence or manipulation aimed at the manager, and for rewriting stakeholder messages, meeting strategy, alignment asks, feedback, deadline requests, and persuasion plans. Use when the user asks about influence, persuasion, manipulation, convincing someone, rewriting a message, aligning a stakeholder, preparing a meeting, responding to pressure, or asking someone to do something.
---

# Manager Influence Strategy

Use this skill when a manager needs to understand influence in either direction:

1. **Influence Defense:** assess whether an incoming message, meeting move, or stakeholder request is influencing, pressuring, or manipulating the manager.
2. **Influence Action:** rewrite the manager's message, meeting strategy, stakeholder ask, feedback, deadline request, or decision pitch using ethical influence.

Never use influence to hide trade-offs, fabricate urgency, exploit personal trust, or push someone toward an action that harms their interest.

## Mode Selection

Pick one mode from the user's intent.

| User intent | Mode |
|-------------|------|
| "Is this manipulating me?", "why do I feel pressured?", "how should I respond?", "what tactic is this?" | Influence Defense |
| "Improve this message", "convince X", "align this stakeholder", "prepare this meeting", "make this ask land" | Influence Action |

If the request contains both, run Defense first, then Action.

## Influence Patterns

Use these labels internally and in output when useful:

| Pattern | Ethical form | Risk form | Defense question |
|---------|--------------|-----------|------------------|
| Contrast | Compare against a real baseline or real option | Inflated anchor or fake bad option | Is the anchor real and relevant? |
| Reason | Explain why the action matters to the audience, team, or business | Reason only serves the sender's urgency | Does the reason explain my stake? |
| Reciprocity | Give useful value before asking | Create artificial debt | Am I deciding or clearing debt? |
| Affinity | Build trust through reliability, shared goals, and respectful tone | Use flattery, borrowed trust, or forced similarity | Would I say yes if I did not like them? |
| Commitment | Ask for a small, active, freely chosen commitment | Trap someone in a stale prior statement | Did the facts change since the commitment? |
| Coercion | State a real consequence transparently | Threat, guilt, rank pressure, or fear | Can the person say no without punishment? |

## Influence Defense

When evaluating incoming influence:

1. Identify the sender's objective.
2. Name the influence pattern.
3. Separate legitimate persuasion from manipulation or coercion.
4. State the risk to the manager.
5. Give one verification question.
6. Draft a response that slows the decision without escalating unnecessarily.

Default response stance: calm, specific, written, and decision-focused.

## Influence Action

When rewriting the manager's strategy:

1. Define the exact action wanted.
2. Name the audience state: aligned, skeptical, overloaded, defensive, undecided, or blocked.
3. Pick one primary influence pattern and one backup pattern.
4. Make the reason audience-centered.
5. Use only defensible contrast: real baseline, real risk, real alternative.
6. Add value before the ask when possible.
7. End with explicit owner, deadline, and decision.

Default channel rule:
- Use async for documentation, status, and clear asks.
- Use live conversation for conflict, trust repair, high-stakes persuasion, or ambiguous trade-offs.
- Use written follow-up after live decisions.

## Output Format

Use this format unless the user asks for a different one:

```
Goal: [action or decision]
Audience state: [read]
Influence pattern: [primary pattern]
Risk: [manipulation, coercion, weak reason, weak contrast, hidden trade-off, or none]
Recommended move: [one concrete strategy]
Draft: [message or talking points]
```

For Defense mode, the draft is a response to the incoming influence.

For Action mode, the draft is the revised ask or meeting script.

## Guardrails

- Do not optimize for getting a yes at any cost.
- Do not invent facts, metrics, deadlines, consequences, or stakeholder motives.
- Do not create false scarcity, false urgency, or fake alternatives.
- Do not bury the ask.
- If the ethical path requires a harder truth, state the harder truth.
- If the request would disadvantage the other party if they knew the full context, refuse and offer a transparent alternative.

## Examples

### Defense

Input: "A stakeholder says everyone else is already aligned and I need to approve today."

Output:

```
Goal: Decide whether to approve today.
Audience state: Sender is applying time pressure and social proof.
Influence pattern: Coercion risk plus weak reason.
Risk: Approval may happen before the trade-off is visible.
Recommended move: Ask for the decision record and the consequence of waiting 24 hours.
Draft: "I need the decision record before I approve. Send the options, trade-off, owner, and consequence of waiting 24 hours. I will respond after reviewing that."
```

### Action

Input: "Rewrite this ask: can you send me the doc by Wednesday?"

Output:

```
Goal: Get the document by Wednesday.
Audience state: Unknown workload.
Influence pattern: Reason plus commitment.
Risk: Current ask gives no reason and no consequence.
Recommended move: Explain why Wednesday matters and ask for a written commitment or counter-date.
Draft: "I need the doc by Wednesday 15:00 because Thursday's review decides whether the project keeps its slot this month. Can you commit to that date, or send the earliest date you can own?"
```
