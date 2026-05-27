---
description: Coaching and management practice lens for all direct report 1:1s. Auto-activates during meeting-prep. Not a standalone tool.
---

# Management Lens

Auto-triggered skill that enriches 1:1 prep for ALL direct reports with coaching nudges and management practice checks. Based on "The Manager's Path" (the framework), grounded in [Your Company] role expectations.

**This is not a standalone command.** It activates during `/meeting-prep` when the meeting is a 1:1 with any direct report.

## When Triggered

During meeting-prep Step 4 (Generate Prep Script), when the meeting matches a 1:1 with any of [Brain Owner]'s 8 direct reports: [Senior IC], [Senior IC], [Direct Report], [Direct Report], [Direct Report], [Direct Report], [Direct Report], [Team Lead].

## What It Does

After loading the person's brain file (already done by meeting-prep Step 3a), load `context/knowledge/managers-path.md` and generate a `### Management Lens` section (3-5 lines total) appended to the 1:1 template.

## Two Sub-Sections

### A. Coaching Nudge (report's growth)

Look up the person's level in the Per-Report Level Mapping table. Use the corresponding chapter lens (IC → Ch 1-2 signals, Senior → Ch 3 signals) to surface ONE observation or question:

- Check the person's brain file for recent observations (last 30 days)
- Match observations against the growth signals for their level
- Generate one coaching question derived from the gap between observation and growth edge

**IC-level reports ([Direct Report], [Direct Report], [Direct Report], [Direct Report], [Direct Report], [Team Lead]):**
- Focus on: ownership, proactive communication, feedback seeking, self-advocacy, cross-team relationships
- Example: "Is [Direct Report] bringing topics to 1:1s or waiting for direction? Ownership signal to watch."

**Senior-level reports ([Senior IC], [Senior IC]):**
- Focus on: proposing vs executing, delegation, public influence, building durable processes
- Example: "Has [Senior IC] proposed an [Mobile Team] initiative this quarter that was not assigned to him?"

### B. Management Practice Check ([Brain Owner]'s execution)

Based on the person's current situation, surface ONE check from the management frameworks:

| Situation | Framework | Check |
|-----------|-----------|-------|
| New hire (<90 days) | Ch 4 onboarding | "Is the 30/60/90 plan being used as conversation anchor?" |
| Performance concern | Ch 4 trust-building | "Have I given timely feedback? Does this person know where they stand?" |
| Team dysfunction signal | Ch 5 debugging | "Which symptom? Not Shipping / People Drama / Overwork / Collaboration failure?" |
| Delegation decision | Ch 6 matrix | "Simple or complex? Frequent or infrequent? Match delegation approach" |
| Cross-functional pushback needed | Ch 6 Saying No | "Which strategy fits? Yes-and / Policy / Help-me-say-yes / Budget appeal?" |
| Default (no special situation) | Ch 4 trust questions | "Am I this person's ally for growth, or just their task assigner?" |

## Output Format

```
### Management Lens

**Coaching nudge:** [one observation or question about the report's growth, grounded in their level]
**Practice check:** [one management framework check relevant to the current situation]
**Nudge:** [optional: if observations show growth opportunity, suggest a stretch — e.g., "ask them to break down the next project for the team" or "have them present their work in the next team demo"]
```

## Interaction with Staff Development Skill

For [Senior IC] and [Senior IC], BOTH `staff-development` and `management-lens` activate. They complement:
- `staff-development` → Staff Engineer's Path lens (technical leadership, system thinking)
- `management-lens` → Manager's Path lens (coaching signals, delegation, organizational influence)

If both produce a nudge, combine into one. Do not duplicate.

## Rules

- Never use framework jargon ("Debugging Dysfunctional Teams", "Stone of Triumph", "Alpha Geek", "Delegation Matrix") in the output. The book informs the thinking, not the language.
- Never score or rate. No "Strong/Partial/None" tables.
- Always tie back to [Your Company] business context (merchant reliability, AI product quality, platform scale, QA authority).
- If no relevant observations exist in the last 30 days, say so: "No recent observations to assess. Log more frequently."
- Keep it to 3-5 lines total. This is a lens, not a report.
- Update the Growth Edge column in `context/knowledge/managers-path.md` Per-Report Level Mapping table when 1:1 observations surface new growth edges.

## Operating Rules (migrated from memory tier 2026-04-27)

- **1:1 language per IC:** EN for [Direct Report], [Senior IC], [Direct Report], [Team Lead]. PT-BR for [Senior IC], [Direct Report], [Direct Report], [Direct Report]. Apply to script content AND draft messages. PR titles stay in English regardless.
- **Team framing ([Brain Owner]'s canonical):** QA = enablers; [Mobile Team] = self-service to platform team destination; DS = SA path improving TAM [Your Company]'s way. Do not substitute taxonomies. When summarizing the teams to leadership or peers, use this exact framing. Source: 2026-04-24 Q1 one-pager review with [Your CTO].
- **Tiger Team standup role:** [Your CTO] leads, [Brain Owner] coordinates. Assess coordination quality, not facilitation quality. [Brain Owner]'s score is on whether owners hit their commitments and rotating handoffs land cleanly, not on whether he ran the meeting.
- **People docs private by default.** IDPs, talent reviews, comp docs are created as private/detached Notion pages. Never under a teamspace parent (private-parent inheritance is automatic). Sharing a private page = explicit, scoped grant per person, not via permissions cascade.
- **IC team attribution: home team always wins.** When an IC ships work in another team's repo or dashboard, frame the action under the IC's home team and call out the cross-team beneficiary explicitly. Example: "DS: [Direct Report] will ship the reactive-vs-automation dashboard, used by [Mobile Team] for whirlwind tracking" — NOT "[Mobile Team]: [Direct Report] will ship..." Cross-reference `09_people/team_roster.md` before any team-attribution call. QA = [Senior IC], [Direct Report]. [Mobile Team] = [Team Lead], [Senior IC], [Direct Report], [Direct Report]. DS = [Direct Report], [Direct Report]. Repo / dashboard domain ([your-company]-appops, etc.) never overrides home team in scripts, briefs, or commitment blocks.
- **Spec ownership = stakeholder alignment ownership.** When a direct report owns a spec or proposal, they drive alignment with stakeholders ([Your CTO], peer EMs, partners). EM does not insert themselves as the messenger. Manager surfaces the alignment dependency as the report's action ("alinha com X antes de abrir spec do Y"); report executes the ping. Generalizes the cross-team meeting ownership test in `managers-path.md`: if EM facilitates the upstream alignment, future asks route through EM by default and the report never grows the relationship. Source: 2026-05-04 PR #168 review draft where I wrote "Vou pingar o [Your CTO]" for [Senior IC]'s Layer 0/1 dependency; user correction redirected to [Senior IC] pinging [Your CTO] herself.
