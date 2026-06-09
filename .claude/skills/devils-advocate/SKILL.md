---
name: devils-advocate
description: Stress-test a proposal before presenting it. Surfaces logical fallacies, missing perspectives, steelmanned counterarguments, and forcing-pushback patterns against vague-scope / social-proof / platform-vision / trend-only / undefined-term failure modes. Use before R&D Leadership presentations, strategic proposals, or quarterly planning.
arguments:
  - proposal_text
---

# Devils Advocate

Run structured critical analysis on any proposal before it leaves the room.

**Adapted from:** `drn/dots/agents/skills/devils-advocate`. Reframed for leadership context.

Input required: proposal text or a local artifact that contains the proposal.

## Autonomy Model

| Action | Mode |
|--------|------|
| Read proposal and brain context | Autonomous |
| Run all 7 analysis steps | Autonomous |
| Generate synthesis and questions | Autonomous |
| Update any brain file | Gated (approval required) |

## Operating Posture

These rules apply across every step. They are non-negotiable.

**Anti-sycophancy ban list. Never write these phrases during the analysis:**

| Forbidden | Replace with |
|-----------|--------------|
| "That's an interesting approach" | Take a position. State what evidence would change it. |
| "There are many ways to think about this" | Pick one framing. Name what would invalidate it. |
| "You might want to consider..." | "This is wrong because..." or "This works because..." |
| "That could work" | State whether it WILL work given the evidence, and what evidence is missing. |
| "I can see why you'd think that" | If the proposal is wrong, say it is wrong and why. |

**Push once, then push again.** The first answer to any challenge is usually the polished version. The real answer comes after the second or third push. Comfort means the analysis has not gone deep enough.

**Calibrated acknowledgment, not praise.** When the proposal contains a specific, evidence-based claim, name what was good in one phrase and pivot to a harder challenge. Do not linger.

**Take a position on every observation.** State the position and what evidence would change it. This is rigor, not hedging.

**Pushback patterns.** When the proposal exhibits one of these failure modes, apply the corresponding force.

| Failure mode | Soft pushback to avoid | Forcing pushback to use |
|--------------|----------------------|------------------------|
| Vague initiative scope | "What kind of scope are we talking about?" | "Name the artifact, the owner, and the deadline. If none exists, the initiative is not scoped, it is a wish." |
| Social proof substituted for evidence | "Who said this is a good idea?" | "Liking the idea is free. Has anyone committed budget, headcount, or a deadline? Has anyone resisted? Approval without resistance is not signal." |
| Platform vision before wedge | "What would a smaller version look like?" | "If no team can use a smaller version, the value is not clear yet. Name the smallest version one team would adopt this quarter." |
| Trend cited as thesis | "How do you ride this trend?" | "Every competitor cites the same trend. What is YOUR thesis about how this changes our customer's decision in 12 months?" |
| Undefined terms | "What does X look like in practice?" | "X is not measurable. Name the metric. If you cannot measure it, you cannot ship it." |

Source: gstack `office-hours` anti-sycophancy and pushback patterns, ported 2026-05-08.

## Step 0: Load Proposal

If $ARGUMENTS is non-empty: treat as the proposal text.
If $ARGUMENTS is empty: prompt [Brain Owner] to paste the proposal inline or name the brain file that contains it.

Load context:
- Read `context/knowledge/voice-profile.md` for current influence tracker
- Read `10_career/_template_career_trajectory.md` for active development goals
- If the proposal relates to a specific pillar, read `01_strategy/_template_strategic_pillars.md`

## Step 1: Summarize the Proposal

One-paragraph statement. No editorial. State:
- What is being proposed
- By whom
- To whom (the audience/decision-maker)
- What outcome it targets

Present the summary and confirm understanding before proceeding.

## Step 2: Identify Logical Fallacies

Scan the proposal for reasoning errors across 4 categories. Output only categories where fallacies are found. Skip empty categories.

| Category | Fallacy | Where It Appears | Why Problematic |
|----------|---------|-----------------|-----------------|
| **Causal** | Post hoc / Correlation as causation / Single cause | [quote] | [explanation] |
| **Assumption** | Begging the question / False dichotomy / Hasty generalization / Survivorship bias | [quote] | [explanation] |
| **Evidence** | Cherry picking / Appeal to authority / Anecdotal evidence | [quote] | [explanation] |
| **Process** | Sunk cost / Planning fallacy / Optimism bias | [quote] | [explanation] |

If no fallacies detected: state "No structural fallacies detected. Proceeding to assumption challenges."

## Step 3: Challenge Core Assumptions

Identify the 3 assumptions the proposal cannot survive without. For each:

```
Assumption: [X must be true for this to work]
Evidence for: [what supports this assumption today]
Failure scenario: [plausible situation where X is false]
Impact if false: [what breaks in the proposal]
```

## Step 4: Missing Perspectives

Who is affected but not represented?

- **Internal:** Which team, role, or function is missing from the framing? (Check against `09_people/_template_team_roster.md`)
- **External:** Which customer segment, partner (POS, payments, Amex), or merchant tier is unaccounted for?
- **Temporal:** Does the proposal ignore second-order effects beyond the immediate term? What happens at month 6, month 12?

List concretely. If none identifiable: say so.

## Step 5: Alternative Framings

Apply the 2 most challenging lenses for this specific proposal:

| Lens | Question | Alternative Framing |
|------|----------|-------------------|
| **Inversion** | What if we did the opposite? What would we learn? | [framing] |
| **First Principles** | Strip to the root problem. Is this the only solution? | [framing] |
| **Analogy** | Where has this been tried before (inside or outside [Your Company])? What happened? | [framing] |
| **Scale Test** | Does this hold at 10x scope? Does it fall apart at 0.1x? | [framing] |

Select the 2 lenses that generate the most productive tension with the proposal.

## Step 6: Steelman the Counterargument

Write the strongest possible argument AGAINST this proposal. Not the weakest objection. The version a smart, informed critic ([Your CTO], [Your CEO], [Your CDO]) would make.

```
Steelman argument: [2-4 sentences. No hedging. Direct assertion.]
What makes it strong: [Why this objection is hard to dismiss]
```

If the steelman cannot be rebutted in Step 7, the proposal is not ready to present.

## Step 7: Synthesis

```
## Devils Advocate Analysis: [Proposal Title]

### Top 3 Concerns
1. [Most serious issue. Specific, not general.]
2. [Second concern]
3. [Third concern]

### Proposed Modifications
- [Concrete change that strengthens the proposal]
- [Second modification]

### Questions to Answer Before Presenting
1. [Question that if unanswered would undermine the proposal]
2. [Second question]
3. [Third question]

### Overall Assessment
[Pass / Conditional Pass / Not Ready]

Pass: No fatal flaws. Proceed with modifications listed above.
Conditional Pass: Address the top concern before presenting. One critical fix needed.
Not Ready: Fundamental assumption or evidence gap prevents credible presentation.
```

## Step 8: Evidence Capture

After synthesis, check: does this analysis surface an assertiveness opportunity for an upcoming meeting?

If yes:

```
### Assertiveness Opportunity
Forum: [R&D Leadership / [Your CTO] 1:1 / other]
The strongest challenge from this analysis: [one sentence]
How to raise it in [Brain Owner] voice: [2-sentence framing. Direct. No hedging.]
```

This is an output flag only. No brain file updates without approval.

## Error Handling

| Failure | Behavior |
|---------|----------|
| No proposal provided and no args | Prompt: "Paste the proposal or describe it in 2-3 sentences." |
| Proposal too vague to analyze | Ask: "What specific decision or recommendation does this proposal make?" Stop until answered. |
| No logical fallacies found | State it. Move to Step 3. A clean structure does not mean sound assumptions. |
| Steelman is weak | Flag: "Could not construct a strong counterargument. Either the proposal is unusually robust or the framing is unclear. Consider: is this proposal too narrow to challenge?" |
| Proposal is [Brain Owner]'s own | Run the same analysis. No softening. The goal is to find the gaps before [Your CTO] or [Your CEO] do. |
