# Compliance Program
> Owner: [Brain Owner] | Pillar: [Pillar N] | Status: Draft | Last Audit: [YYYY-MM-DD]

## Scope

This file is the index of compliance commitments your engineering org owns. **Do not store raw evidence here.** Reference it. Raw evidence (pentest reports, control owners, auditor PII, partner negotiation state) belongs in a private system.

## Active Frameworks

| Framework | Status | Renewal | Internal Owner | Evidence Location |
|-----------|--------|---------|----------------|-------------------|
| [e.g., SOC 2 Type II] | [In progress / Maintained] | [YYYY-MM-DD] | [Person] | [Private system reference] |
| [e.g., PCI DSS] | | | | |
| [e.g., HIPAA] | | | | |
| [e.g., GDPR] | | | | |

## Workstreams

For each active control gap or audit response, track:

| Workstream | Driver (audit / partner / regulator) | Status | Owner | Deadline | Escalation Trigger |
|------------|--------------------------------------|--------|-------|----------|--------------------|
| [Name] | [What forced this] | [Not started / In progress / Done] | [Person] | [YYYY-MM-DD] | [Condition + who is notified] |

## External Dependencies

People outside your org you rely on (security team, legal, external auditors). Store contact details in your private system, reference by role only.

- **Internal security team:** [Reference]
- **External auditor:** [Reference]
- **Legal:** [Reference]

## Cadences

- **Compliance team sync:** [Frequency, day, owner]
- **Audit response window:** [SLA for responding to auditor questions]
- **Evidence refresh:** [Frequency for re-collecting evidence files]

## Measurable Outcome

Each compliance workstream has a status, deadline, owner, private evidence reference, and response SLA.

## AI Integration

| Decision | AI role | Human owner | Evidence inputs | Pass/fail criteria | Trace | Exception trigger | Flow metric |
|----------|---------|-------------|-----------------|--------------------|-------|-------------------|-------------|
| Which compliance workstream needs evidence or response action? | recommend | [Brain Owner] | Workstream table, renewal dates, evidence references, response SLA, control narratives | Workstream has owner, deadline, private evidence reference, and current response status | Compliance program file and private evidence system reference | Missing evidence reference, missed SLA, or renewal within 30 days without readiness action triggers escalation | Audit-response latency and evidence-gap count |

Use AI for drafting control narratives, summarizing non-sensitive evidence indexes, and checking new code against control requirements. Do not feed AI any sensitive partner-negotiation context or named PII.

## Cross-References

- `02_leadership/audience_density_doctrine.md` — Candy Answer Protocol for compliance officer interactions
- `00_foundation/brain_governance.md` Rule 12 — sensitive data stays out of this repo
