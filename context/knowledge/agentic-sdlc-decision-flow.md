# Agentic SDLC Decision-Flow Doctrine
> Owner: [Brain Owner] | Pillar: Pillar 4 (AI Execution) + Pillar 5 (Operating Scale) | Last Updated: 2026-05-31

AI adoption is operationally meaningful only when it changes a decision flow.

Tool usage, token volume, prompt count, and generated artifacts are activity metrics. They do not prove the delivery system changed. A workflow counts as AI-native when it removes, shortens, validates, or continuously monitors a decision that previously waited on human memory or manual inspection.

## Decision Contract

Every AI workflow must define:

| Field | Required answer |
|-------|-----------------|
| Decision | What decision moves work forward? |
| Current owner | Who makes it today? |
| Evidence | What facts are required? |
| Criteria | What makes the decision pass or fail? |
| Waiting cost | How long does work wait there today? |
| AI role | draft, recommend, validate, decide, or monitor |
| Human role | approver, exception handler, or system owner |
| Metric | decision latency, rework rate, error rate, lead time delta, MTTR, validation queue depth |
| Trace | Where is the audit trail stored? |

## Operating Rules

- Measure flow before usage. Baseline decision latency, waiting time, validation queue depth, defect leakage, review rework, and MTTR.
- Separate build latency from trust latency. AI can compress artifact creation without removing the validation gate.
- Treat local productivity wins as signals, not system proof. System proof requires a traceable decision moved, shortened, or made safer.
- Refuse AI workflows with no exception path. Uncertainty must route to a named human owner.
- Do not import vendor maturity curves as fact. Treat them as external framing until verified against internal flow data.

## Manager Question

Replace "Are you using AI?" with:

> Which human decision did AI remove, shorten, or make safer this week?

## Cross-References

- `context/knowledge/sdlc-pipeline.md` - phase gates and decision inventory.
- `00_foundation/brain_governance.md` Rule 7 - AI Decision Contract requirement.
