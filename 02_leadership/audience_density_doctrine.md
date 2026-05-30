# Audience Density Doctrine
> Owner: [Brain Owner] | Pillar: [Pillar N] | Status: Enforced | Last Audit: [YYYY-MM-DD]

## The Rule

Information density is audience-dependent. Engineering audiences require depth. Compliance and external audiences require minimal surface area. Giving a compliance officer an engineering answer is not accuracy — it is risk creation.

## Measurable Outcome

Every executive-facing update states the decision, impact, owner, and deadline in the first 150 words.

## Decision Matrix

| Audience | Mode | What to Include | What to Exclude |
|----------|------|----------------|----------------|
| Engineering peers, ICs | Full depth | Implementation detail, code refs, data structures, root causes, trade-offs | Nothing — more is more |
| Executive leadership | Business translation | Metrics, business impact, risk framing, decisions needed | Code detail, architecture internals, tool specifics |
| Compliance officers, auditors | Minimal surface | Public-facing policies, certifications, yes/no statements | Internal implementation, codebase references, engineering gaps found, readiness status |
| External partners and customers | Resolution-focused | Resolution status, timeline, impact | Internal cause, technical debt, team dynamics, blame |

## Candy Answer Protocol

1. Identify what question they actually need answered (checkbox, not depth).
2. Find the public-facing document that answers it (privacy policy, certification, terms of service).
3. Draft answer from that document only. Zero internal references.
4. If internal knowledge reveals a gap: fix the gap internally. Do not disclose it. Disclose the policy that covers the intent.

## Anti-Pattern

"I found two engineering gaps in our codebase while researching this" is an engineering answer. The compliance answer is: "Our data handling complies with [Regulation] and is documented in our [Policy] [link]."

## Escalation

- If an external party asks for information that would require disclosing internal implementation: flag to your manager before responding. Do not fill the gap with detail.
- If a compliance officer keeps drilling after a minimal answer: the minimal answer was correct. Escalate — this is a legal/strategic question, not a technical one.

## AI Integration

Before sending external messages, run them through AI with: "Rewrite this for [audience]. Remove internal implementation detail. Reference policy/certification language only. Flag any sentence that exposes engineering gaps."
