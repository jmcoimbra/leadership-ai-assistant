---
name: why-lens
description: WHY-first framing check for any communication that opens a discussion, proposes a new direction, or changes an existing approach. Auto-activates on stakeholder messages, team-level proposals, new ideas, change-of-approach pitches, RFC/PRD intros, meeting talking points, and Slack threads that seed a decision. Based on "Comece pelo porquê" (Start With Why) by Simon Sinek. Source mapping: Notion Books DB `327a84ed-4024-817c-be0b-cdbf75899927`.
---

# WHY Lens

Auto-triggered framing check that runs on any draft that opens a discussion, proposes a new direction, or changes an existing approach. Output is a short check appended before the draft is presented to [Brain Owner]. Internal application is deep. External language stays jargon-free and free of em dashes.

**This is not a standalone command.** It activates automatically during drafting.

## When to Trigger

Activate when the draft does any of:

1. **Opens a discussion** with anyone (not just [Your CTO], [Your CEO], [Your CDO]). Includes direct reports, peers ([Peer Manager 2], [Peer Manager]), cross-functional, R&D Leadership, vendors.
2. **Pitches a new idea** (e.g., AI-driven IDP, QA-as-platform, mobile-first triage queue, vendor swap).
3. **Changes an approach** in any team [Brain Owner] leads (QA, [Mobile Team], Dev Support) or any program he influences.
4. **Frames a strategic shift** in a 1:1 talking point, weekly meeting topic, RFC/PRD intro, retro recommendation, hiring pitch.
5. **Sets a narrative** for AI adoption, automation rollout, capability investment, headcount, budget, or platform migration.

## When to Skip

- Pure brain-internal edits (file refactors, knowledge consolidation, command authoring) with no outbound surface.
- Operational status pings with no decision attached ("CI is green", "PR merged", "tomorrow's meeting moved").
- 1:1 logging, meeting ingestion, transcript cleanup, voice-profile linting.
- Replies inside an active thread where WHY was already established upstream.

If unsure, run the lens. False positives cost 5 lines. False negatives cost a stakeholder reset.

## How to Apply (internal reasoning)

The agent must run all five filters before producing the WHY Check. The framework names below are internal scaffolding. They never appear in user-facing output.

### Filter 1: WHY → HOW → WHAT order (Golden Circle)

Read the opening sentence. Classify what it leads with.

- **WHY**: the purpose, impact, or stake. Example: "Merchants lose 6% of guests when checkout latency exceeds 2s."
- **HOW**: the approach, principle, or method. Example: "We are moving QA to platform ownership so the team scales without headcount."
- **WHAT**: the artifact, tool, feature, metric, or process. Example: "We are upgrading to RuboCop 1.65."

If the draft leads with WHAT, mark as features-first. Propose a rewrite of the opening line that leads with merchant impact, guest engagement, or platform reliability. The rewritten draft keeps HOW and WHAT in that order behind the new opener.

### Filter 2: Decision filter against [Your Company] WHY (Celery Test)

[Your Company] WHY: every restaurant deserves the loyalty tools that drive profitable frequency.

Apply the filter. Does this initiative reinforce one of three pulls?

1. **Merchant retention** (acquisition, churn defense, partner objection cover).
2. **Guest engagement** (frequency, basket, loyalty mechanics).
3. **Platform reliability** (uptime, security, compliance, scale, AI-execution capability).

If the answer is "no" or "indirect", flag it. The draft either needs an explicit connection to one of the three pulls, or the initiative itself fails the filter and should be redirected.

### Filter 3: Stake-first opening (limbic entry point)

People decide on meaning first and rationalize with data second. The opening must land in the reader's stake before any technical detail.

- **Pass**: opening names a person, partner, consequence, or commitment. Numbers may appear, but only as proof of the stake. Example: "Merchants lose 6% of guests when checkout latency exceeds 2s."
- **Fail**: opening is a bare metric, dashboard label, sprint marker, or tool name with no stake attached. Examples: "p95 latency is 2.3s.", "Sprint 47 burndown is at 60%.", "RuboCop is on 1.42."

If failing, propose a rewrite where the stake leads and the metric supports.

### Filter 4: Audience segmentation (Law of Diffusion)

Identify the audience and adjust the proof requirement.

- **Innovator-side** ([Your CTO], AI-curious engineers, partners already buying the vision): inspire with the destination. Low proof bar. They will pull others.
- **Majority-side** (skeptical peers, legacy-process holders, risk-averse stakeholders): lead with social proof. High proof bar. Show who already adopted, what broke, what got fixed, before asking them to follow.
- **Laggards**: do not target. Do not spend airtime convincing them. They follow the majority once the tipping point passes.

Flag the segment in the check. If the draft tone is matched to the wrong segment (vision-language at majority-side, or proof-piling at innovator-side), propose the corrected framing.

### Filter 5: Operator pairing and durability (WHY-HOW partnership + School Bus Test)

Two checks in one filter:

- **Operator named.** Every new direction needs a named operator who will execute it. If the draft proposes a vision without naming who runs it, flag as `No`. Vision without an operator is a sermon.
- **Team-durable.** For team-level direction changes, would the team still execute this if [Brain Owner] disappeared tomorrow? If only [Brain Owner] can articulate the WHY, flag as `team-fragile` and recommend a transfer step (write-up, team forum, recorded principle) before scaling the initiative.

Both checks land on the same output line. Pass when an operator is named and the WHY is transferable.

## Output Format

Append before presenting the draft. Use this exact template. No em dashes. No padding.

```
### WHY Check

**Opens with:** <WHY | HOW | WHAT>. "<one phrase quoting the opening>"
**[Your Company] WHY pull:** <Merchant retention | Guest engagement | Platform reliability | Indirect, flag>.
**Audience read:** <Innovator-side | Majority-side>. Proof bar: <low | high>.
**Operator named:** <Yes (name) | Yes (name), team-fragile | No, flag>.
**Suggested opening:** "<concrete one-line rewrite in [Brain Owner]'s voice>"
```

Rules for the template:
- **Suggested opening** is omitted entirely when filters 1, 3, and 4 all pass.
- Total length: 4 lines on a clean pass, 5 lines when a rewrite is needed.
- Quote the actual opening of the draft in the **Opens with** line. No paraphrase.
- Operator name comes from the draft when present, or from the team roster (`09_people/_template_team_roster.md`) when implied. If neither, flag `No`.

### Worked example: passing draft

Input draft opening: "Merchants lose 6% of guests when checkout latency exceeds 2s. [Senior IC] is leading a Sentry-driven triage queue that targets the top three offenders by January."

```
### WHY Check

**Opens with:** WHY. "Merchants lose 6% of guests when checkout latency exceeds 2s."
**[Your Company] WHY pull:** Platform reliability.
**Audience read:** Majority-side. Proof bar: high.
**Operator named:** Yes ([Senior IC]).
```

### Worked example: failing draft

Input draft opening: "We are upgrading RuboCop to 1.65 across all repos."

```
### WHY Check

**Opens with:** WHAT. "We are upgrading RuboCop to 1.65 across all repos."
**[Your Company] WHY pull:** Indirect, flag.
**Audience read:** Majority-side. Proof bar: high.
**Operator named:** No, flag.
**Suggested opening:** "Engineers spend 4 hours a week resolving stale lint rules that no longer match our style. RuboCop 1.65 retires those rules. Lucas owns the cross-repo bump."
```

## Rules

- **No jargon in output.** Never write "Golden Circle", "Celery Test", "limbic system", "Law of Diffusion", "Rupture", "School Bus Test", "WHY-HOW partnership". Translate every concept to plain operating language ("Opens with", "[Your Company] WHY pull", "Audience read", "Operator named", "team-fragile").
- **No em dashes.** Use periods, colons, or restructure. This rule applies to the WHY Check itself and to any rewrite suggestion.
- **No padding.** If a filter passes, state it in one phrase. Do not explain.
- **Concrete rewrites only.** When suggesting a new opening, write the actual sentence in [Brain Owner]'s voice: short, declarative, deterministic, no hedging, no em dashes, no forbidden phrases ("perhaps", "leveraging", "ensuring", "streamlining", "fostering").
- **Stack with other skills.** Run `why-lens` first (framing), then `writing-docs` (structure) or `slack-communication` (channel, voice) on top. The WHY Check is reusable input for those skills.
- **Internal-only application.** The frameworks inform the reasoning. Never expose them in user-facing output. The output sounds like [Brain Owner]'s operating brain, not a book report.
- **Source of depth.** When in doubt about a concept's application, re-derive from the Notion Books DB entry `327a84ed-4024-817c-be0b-cdbf75899927`. Do not invent.
