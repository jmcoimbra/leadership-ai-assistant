# Async Communication Standard
> Owner: [Brain Owner] | Pillar: [Pillar N] | Status: Enforced | Last Audit: [YYYY-MM-DD]

## Purpose

Every strategic message you send must be actionable within 60 seconds of reading. No long-form ambiguity. No hedging. No burying the ask.

## Required Format

Every strategic async message (Slack, email, written updates) follows this structure:

```
CONTEXT: [1-2 sentences. What is the situation.]
ASK: [Specific action needed. Not "thoughts?" — a decision or action.]
OWNER: [Who needs to act.]
DEADLINE: [By when.]
IMPACT IF NO ACTION: [What happens if this is ignored.]
```

## Examples

**Bad:**
> "Hey, wanted to circle back on the QA discussion from last week. I think there are some concerns we should probably address around the release process. Let me know your thoughts when you get a chance."

**Good:**
> "CONTEXT: QA identified 3 unresolved critical issues in the v4.2 release candidate. Release is scheduled for Thursday.
> ASK: Approve a 48-hour release delay to resolve critical issues, or accept production risk.
> OWNER: [Decision Maker]
> DEADLINE: Decision needed by EOD Tuesday.
> IMPACT IF NO ACTION: Release ships Thursday with known critical bugs affecting [X] customers processing [Y] transactions/day. QA is on record opposing."

## Rules

1. **No "thoughts?"** — Replace with a specific ask.
2. **No "when you get a chance"** — Replace with a deadline.
3. **No passive voice** — "A decision is needed" → "[Name] needs to decide."
4. **Always state impact of inaction** — Make the cost of ignoring your message explicit.
5. **Keep it under 150 words** — If it's longer, it needs a document, not a message.

## Escalation

If a strategic async message goes unanswered for 48 hours after its deadline, escalate to the owner named in the message with the original ask and impact.

## AI Integration

Before sending any strategic message, run it through AI with this prompt: "Remove all hedging language. Make the ask explicit. Add a deadline and impact statement. Keep it under 150 words."
