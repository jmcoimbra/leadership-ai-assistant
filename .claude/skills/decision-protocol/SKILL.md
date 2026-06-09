---
name: decision-protocol
description: >-
  Decision-quality lens. Auto-activates on high-stakes ambiguity
  (architecture, destructive scope, data model, missing context) and when
  presenting options to the user. Two patterns: Confusion Protocol
  (STOP + name + 2-3 options + ask) and Completeness Scoring
  (annotate options with X/10 coverage so user sees the tradeoff explicitly).
  Composes with intelligence-layers, sdlc-gate, and devils-advocate.
---

# Decision Protocol

Two behavioral patterns that apply across any session that produces decisions or option sets. Auto-fires and works as a lens, not a standalone workflow.

**Owner:** [Brain Owner]
**Pillar:** Pillar 4 (AI Execution)
**Measurable Outcome:** Zero silent decisions on architecture, destructive scope, data model, or option presentation. Every option set the agent surfaces to [Brain Owner] includes either a Completeness score per option, or an explicit "differ in kind" note.
**Escalation Trigger:** If a session produces an architecture or destructive-scope action without a Confusion Protocol output (no STOP, no named ambiguity, no option block), flag it in the next session learning capture run as a missed gate.

**Source:** gstack `office-hours` Confusion Protocol + Boil-the-Lake completeness scoring, ported and adapted 2026-05-08.

**Doctrinal source:** `context/knowledge/decision-frameworks.md` (Algorithms to Live By, Christian & Griffiths). The Confusion Protocol pattern is Computational Kindness for AI-to-human option presentation. The "My read" line implements "state preferences first." The 2-3 cap implements "reduce options, don't maximize." Completeness X/10 implements cognitive subsidy: pre-compute the coverage tradeoff so the user verifies instead of searches. When the user picks among options that differ on more than coverage, also load the Pick-Metric-Before-Strategy doctrine from that file.

## When Triggered

Confusion Protocol fires when the agent encounters:
- Architecture ambiguity (skill placement, file routing, hook design, multi-tier system)
- Destructive scope (rm -rf, force-push, schema migration, file restructure across many files)
- Data model decision (skill vs harness vs primitive; composes with `intelligence-layers`)
- Missing context (a key file/source/transcript is absent and the answer would change with it)

Completeness Scoring fires when the agent presents 2+ options to the user.

**Skip when:** routine coding, obvious changes, trivial yes/no replies, or the user has already given explicit direction. The protocol is for genuine ambiguity, not for hedging on every turn.

## Confusion Protocol

When ambiguity is genuinely high-stakes:

1. **STOP.** Do not guess. Do not ship the most likely choice and announce it.
2. **Name the ambiguity in one sentence.** Not a paragraph. One sentence the user can read in 5 seconds.
3. **Present 2-3 options with tradeoffs.** Each option gets a Completeness score (see below) when options differ in coverage.
4. **Ask.**

Format:

```
### Confusion Protocol

**The ambiguity:** <one sentence>

**Options:**
- A) <option>. <tradeoff>. Completeness: N/10.
- B) <option>. <tradeoff>. Completeness: N/10.
- C) <option>. <tradeoff>. Completeness: N/10.

**My read:** <which one and why, in one sentence>. State what would change my read.
```

The "My read" line is non-negotiable. The user wants a position with the option set, not a neutral menu. State the position; let the user override.

## Completeness Scoring

When presenting options that differ in coverage (edge cases, error paths, tests, surface area), annotate each option with `Completeness: X/10`:

Calibrate to one of five anchor scores. Do not invent intermediate values; the resolution is intentional.

| Score | Meaning |
|-------|---------|
| 10 | All edge cases handled. Tests cover happy path + failures. No known gaps. |
| 7 | Happy path covered. Common errors handled. Some edge cases deferred. |
| 5 | Happy path only. Errors fall through. Edge cases unexamined. |
| 3 | Shortcut. Demonstrates the idea. Production unsafe. |
| 1 | Hack. Single-use only. |

**Do not fabricate scores.** If you cannot calibrate, write: `Note: options differ in kind, not coverage. No completeness score.`

When options differ in kind (e.g., "build vs buy", "in-house vs vendor", "Slack vs email") rather than in coverage, the score does not apply. Surface that explicitly.

## Output Examples

### Genuine ambiguity, options differ in coverage

```
### Confusion Protocol

**The ambiguity:** Whether to add the Confusion Protocol as a new skill, an addition to intelligence-layers, or rules in CLAUDE.md.

**Options:**
- A) New `decision-protocol` skill. Composes with existing lenses, auto-fires on ambiguity. Completeness: 9/10.
- B) Append to intelligence-layers. Co-located with related judgment patterns. Completeness: 6/10. Loses Completeness Scoring scope (broader than intelligence layering).
- C) CLAUDE.md hard constraint. Fires every turn. Completeness: 4/10. Bloats CLAUDE.md and weakens the lens model.

**My read:** A. Skill model matches the brain's existing lens architecture. State what would change my read: if intelligence-layers were near a refactor, B becomes preferable.
```

### Options differ in kind (no score)

```
### Confusion Protocol

**The ambiguity:** Whether to draft the email to the external authority today, wait for their reply on format, or ask one clarifying question.

**Options:**
- A) Draft today against a guessed format. Send when the authority confirms.
- B) Wait for the authority's reply. Draft after format is known.
- C) Send a single clarification question now. Defer the draft.

Note: options differ in kind, not coverage. No completeness score.

**My read:** C. Per voice-profile rule on external authority emails, the authority owns the spec; ASK do not propose. State what would change my read: if the authority has been silent >5 days, A becomes a forcing function.
```

## Composition

| Skill | When to compose | Order |
|-------|-----------------|-------|
| `intelligence-layers` | When the ambiguity is about which layer (skill / harness / primitive) | Decision Protocol surfaces the question, intelligence-layers picks the layer |
| `sdlc-gate` | When the ambiguity is about which SDLC phase artifacts are required | Decision Protocol surfaces options, sdlc-gate confirms gate fit |
| `devils-advocate` | When the option set is itself the proposal | Decision Protocol surfaces the options, devils-advocate stress-tests them |
| `product-diagnostic` | When the ambiguity is "should we build this?" | product-diagnostic runs first; Decision Protocol applies if the diagnostic surfaces 2+ paths |

Do not duplicate. The protocol surfaces the decision; composed skills handle the domain reasoning.

## Anti-Patterns

- **Hedging instead of stopping.** "Maybe A, maybe B, you decide" is not a Confusion Protocol invocation. State your read.
- **Faking Completeness scores.** Do not invent a score to make options look symmetric. If they differ in kind, say so.
- **Triggering on trivia.** "Should I use 4-space or tab indent?" is not high-stakes ambiguity. Pick one and ship.
- **Presenting >3 options.** Forces the user to compare too many states. Cut to 2-3, even if the discarded options were valid.

## Operating Rules

- The protocol output is internal-decision-shaped. Do not include it in outbound content (Slack, email, Notion, Jira). For outbound content, the user's WHY-Lens output and slack-communication structure apply.
- **H3 paste rule:** the `### Confusion Protocol` header is a literal H3 heading. If pasted into a brain file or workspace artifact, strip the `### ` prefix or downshift to H4 to avoid clobbering the host file's heading hierarchy. If surfaced inline to the user, render the labels (`The ambiguity:`, `Options:`, `My read:`) without the H3 wrapper.
- Em-dash hook applies to any user-facing output. Use periods or rewrite.
- The protocol does NOT fire when the user has already given explicit direction. Direction overrides ambiguity.
