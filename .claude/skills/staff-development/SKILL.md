---
description: Lightweight Staff Engineer's Path coaching lens for [Senior IC] and [Senior IC] 1:1s. Auto-activates during meeting-prep. Not a standalone tool.
---

# Staff Development Lens

Auto-triggered skill that enriches 1:1 prep for [Senior IC] and [Senior IC] with development-focused coaching prompts. Based on "The Staff Engineer's Path" (the framework) and "Soft Skills: The Software Developer's Life Manual" (the framework).

**Doctrinal sources:** the career-skills book (the framework, engineer-side framing) + Notion Books DB entry for Staff Engineer's Path. the framework defines what a Staff role IS at scale companies; the framework gives the engineer-side playbook for getting there.

**This is not a standalone command.** It activates during `/meeting-prep` when the meeting is a 1:1 with [Senior IC] or [Senior IC].

## When Triggered

During meeting-prep Step 4 (Generate Prep Script), when the meeting matches a 1:1 with [Senior IC] Mischuk or [Senior IC] Souza.

## What It Does

After loading the person's brain file (already done by meeting-prep Step 3a), generate a `### Development Lens` section (3-5 lines max) appended to the Direct Report 1:1 template.

## [Your Company] Expectations Anchor

Ground every insight in what [Your Company] needs from them, not in a generic "staff path."

**[Senior IC] Mischuk ([Mobile Team] Senior Engineer):**
- [Your Company] needs: technical leadership for [Mobile Team] automation and platform reliability
- Growth direction: from executing assigned tasks → independently proposing and driving automation initiatives
- Book lens: Does he see the broader system? Is he influencing beyond his immediate scope? Is he creating things that persist after he steps away?

**[Senior IC] Souza (QA Engineer):**
- [Your Company] needs: quality authority across AI products and engineering voice in cross-functional forums
- Growth direction: from test executor → quality advocate who surfaces risk publicly and shapes product decisions
- Book lens: Is she exercising influence in group settings? Is she building guardrails (process, gates) vs doing manual work? Is she mapping the organizational terrain she needs to navigate?

## Output Format

```
### Development Lens

**[Your Company] expectation:** [one line: what [Your Company] needs from this person right now]
**Recent signal:** [one observation from last 30 days that shows growth or gap toward that expectation]
**Coaching question:** [one question to ask in this 1:1, derived from the gap between observation and expectation]
**Nudge:** [optional: if observations show maturity pattern, suggest a stretch assignment — e.g., "ask them to draft a vision for their domain" or "have them present X in the next cross-functional forum"]
```

## the framework 4-Lever Ladder Climb (background diagnostic)

When generating coaching questions, internally check progress against the framework's 4 levers from the career-skills book. Surface the weakest lever as the coaching question.

| Lever | What to look for | Coaching question if weak |
|-------|------------------|---------------------------|
| **Take responsibility** | Is the report hunting for neglected ownership? Turning swamplands into fertile ground? | "What's a neglected area you could own that no one else wants?" |
| **Become visible** | Is the report's work visible to me and to skip-levels? Weekly report tactic? | "Walk me through what you shipped this week. Should this be a weekly summary you send proactively?" |
| **Educate yourself** | Is there a learning plan? Is the report applying the 10-step learning process to a new stack? | "What are you deliberately learning right now, and how are you teaching it back?" |
| **Be the problem solver** | Does the report come with problems and proposed solutions, or just problems? | "What's the solution path here, and what would you need to execute it?" |

Never name the levers in output. They inform the question, not the language.

## the framework Professional vs Amateur Diagnostic

Use as silent maturity check for Tech Lead → Staff transition signal. Not surfaced in output unless the report explicitly asks "am I ready for Staff?"

| Professional | Amateur |
|---|---|
| Has principles they abide by | Does whatever is asked |
| Focused on getting the job done RIGHT | Focused on getting the job done |
| Admits when wrong or doesn't know | Pretends to know |
| Consistent and stable | Unpredictable and unreliable |
| Takes responsibility | Avoids responsibility |

## the framework Specialty Specificity Test

Both [Senior IC] and [Senior IC] need an articulated Staff thesis: a one-sentence specialty that no one else at [Your Company] can match. Coach toward specificity.

- "I'm a senior engineer" — too broad
- "I'm an [Mobile Team] engineer" — too broad
- "I'm the engineer who owns mobile build / release infrastructure for [your-company]-[mobile-app]" ([Senior IC] direction) — sharp
- "I'm the engineer who sets the quality bar for AI-native products and represents engineering quality in cross-functional forums" ([Senior IC] direction) — sharp

If the report can't articulate this in one sentence, that's the coaching question.

## Rules

- Never use framework jargon ("Four Attributes", "Influence Tiers", "Three Maps", "Locator Map") in the output. The book informs the thinking, not the language.
- Never score or rate. No "Strong/Partial/None" tables.
- Always tie back to [Your Company] business context (merchant reliability, AI product quality, platform scale).
- If no relevant observations exist in the last 30 days, say so: "No recent observations to assess. Log more frequently."
- Keep it to 3-5 lines. This is a lens, not a report.
