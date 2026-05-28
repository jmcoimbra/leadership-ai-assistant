# Voice Profile

> Owner: [Brain Owner] | Pillar: All | Status: Active | Last Audit: [YYYY-MM-DD]

## Purpose

Behavioral rules for written and spoken communication produced by the brain owner or by AI drafting on their behalf. Every draft must pass these checks before sending.

This is the canonical reference for the deterministic-language rule in `00_foundation/brain_governance.md`. Hooks in `.claude/hooks/` enforce a subset of these at write-time.

## Adopters: Replace This Profile With Yours

The patterns below are a **starting voice**, not yours. Before relying on this file, run the `voice-capture` skill (`.claude/skills/voice-capture/SKILL.md`) with 10-20 samples of your own writing. The skill will extract YOUR patterns and rewrite this file in place. Until you do, AI drafts will inherit a voice that probably is not yours.

## Greetings & Closings

- **"Hi" not "Hey".** Hey is too casual for written work artifacts.
- **"I am" not "I'm".** Contraction removal projects assertion.
- **No greeting in artifact-anchored comments** (in-doc comments, PR inline comments, ticket comments). The context is the artifact; a greeting reads as noise.
- **Close on a commitment, not a hope.** "I will send by Thursday" beats "let me know if you have questions."

## Sentence Structure

- **Short, declarative sentences.** Assertion first. Subordinate clauses last, if at all.
- **No em dashes.** Use period, comma, parenthesis, or colon. Em dashes signal AI-drafted prose.
- **No semicolons in chat / short messages.** Break into two sentences instead.
- **One idea per sentence.** If you need a conjunction other than "and", you have two sentences.

## Deterministic Language

- **Required pattern for any commitment, initiative, or measurable claim:** `[verb] [thing] from [baseline] to [target] by [date]`.
- **Banned words without specifics:** *improve, enhance, support, explore, consider, leverage, ensure, streamline, foster*.
- **Banned hedges:** *I think maybe*, *perhaps*, *just wanted to flag*, *it's important to note*, *we should probably consider*.
- **Quantifiers must be exact.** Not "many", not "often" — give the count or the date.
- **Trait labels banned in performance contexts.** Not "aggressive", "sloppy", "lazy". Replace with observed behavior: "in the last 3 sprints, 2 stories shipped 1 sprint after committed date."

## Emotional Register

- **Direct without being curt.** State the thing. Move on.
- **Praise specific behavior, not the person.** "The way you sequenced that rollout reduced our risk window" beats "great job."
- **Critique behavior in private. Praise behavior in public.** Default rule.

## Formatting

- **For long-form messages, use bold sentinels** for skim-readability: `**Context:** ...`, `**Ask:** ...`, `**Deadline:** ...`. See `02_leadership/async_communication_standard.md`.
- **No headers in chat messages** unless the message is over 200 words. Most are under.
- **Code blocks for commands, paths, and quoted output.** Inline code for identifiers.

## Anti-Patterns

| Pattern | Why it fails | Fix |
|---------|--------------|-----|
| Trailing summary that restates the opener | Reads as filler; the reader already saw the opener | Cut it |
| Defensive padding in chat ("all green CI", date qualifiers the audience lived) | Signals insecurity | State the ask; drop the qualifier |
| Implicit / subtext asks ("you are working too hard" expecting "I'll take time off") | Receiver does not interpret subtext the way the sender intends | State the ask explicitly |
| Buried ask | Reader has to hunt for the action | Lead with the ask, supply context after |
| Conclusions that restate the opener | Filler | Cut the closing line |
| Vague quantifiers in feedback ("rarely", "often", "always", "never") | Reads as judgment; triggers defensive posture | Replace with specific counts and dates |

## Evidence-to-Assert Discipline

- **Never write hedge words in status updates, scripts, or briefs.** Either verify the claim and assert, or label it "unverified, confirm at [moment]".
- **Never write "likely shipped" / "should be done" / "appears to be ready".** Check the actual state.
- **For external claims (market data, statistics, third-party quotes, public figures' positions):** never assert without a verifiable source. Use "I am not certain" / "Based on the information available to me" / "This is my best estimate, not a confirmed fact". Never invent citations, papers, URLs, or quotes.

## AI-Drafted Content Boundary

Every AI-drafted message goes through this check before sending:

1. **Em dash scan.** Replace any `—` with `.`, `,`, `:`, or parenthesis.
2. **Hedge scan.** Search for banned hedge words; replace with assertion or "unverified".
3. **Trait scan.** Search for trait labels; replace with observed behavior.
4. **Length scan.** If over 200 words for chat, condense to under 150.
5. **Voice scan.** Read aloud. Would a colleague who knows you think "that's me" or "that's AI"? If uncertain, cut 30%.

## Honest Qualifiers in Proposals

- When proposing a plan, name what you do not know. Honest qualifiers ("I have not validated X" / "I am uncertain whether Y") signal trust, not weakness.
- Never overstate confidence to win the room. Calibrated certainty is the long-term position.

## Stakeholder Credits in Outbound Content

When work involved others, credit them by name in the artifact: "[Person] led the X investigation", "with [Person] on the Y rollout". Skipping credit reads as appropriation.

## Source Material Verification

When citing a person, a published source, or an internal document: verify it exists and says what you claim. Do not paraphrase from memory if the source is reachable in-session. Pull it.

## Self-Check Before Sending

Read the draft once. Cut anything that does not advance the ask, the context, or the relationship. If you cannot defend a sentence with "this changes the reader's behavior", delete it.

## Code-Switching

If you write in multiple languages, codify per-language rules in a separate section. Examples: pronoun choice (formal vs. informal), accentuation, idiomatic constructions. Apply the same deterministic-language rule across languages.

## PR Review Voice

- **Lead with the change request, not the framing.** "Move this lookup into the helper" beats "I noticed this lookup could be moved..."
- **Cite the line, not the file.** `file.rb:123` is enforceable; "in the controller" is not.
- **No "could", "maybe", "what do you think about".** Use "change to X" or "ask: why X over Y?".
- **Differentiate blockers from suggestions explicitly.** `Blocker:`, `Suggestion:`, `Question:`. Reviewers should not have to guess severity.

## Cross-References

- `02_leadership/async_communication_standard.md` — Context/Ask/Owner/Deadline format
- `02_leadership/audience_density_doctrine.md` — Information density per audience
- `00_foundation/brain_governance.md` Rule 5 — Deterministic language requirement
- `.claude/hooks/check-em-dash.sh` — em dash hook enforcement
