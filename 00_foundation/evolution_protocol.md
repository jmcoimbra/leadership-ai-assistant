# Evolution Protocol
> Owner: [Brain Owner] | Pillar: All | Status: Enforced | Last Audit: [YYYY-MM-DD]

## Purpose

Defines how this brain grows without decaying. Expansion without governance produces entropy.

## When Adding a New Domain

Before creating any new directory or file:

1. **Define the boundary.** What does this domain cover? What does it NOT cover?
2. **Define measurable outputs.** What metrics does this domain own? What are the baselines?
3. **Define the AI integration layer.** How does AI participate in this domain?
4. **Define escalation triggers.** What conditions trigger escalation? To whom?
5. **Map to a strategic pillar.** If it does not map to one of your defined pillars, it does not belong.
6. **Assign an owner and a review date.** No orphan files.

## When Modifying Existing Files

- Update `Last Audit` date in the header
- Verify the file still passes compliance (`00_foundation/compliance_audit.md`)
- If a concept is being moved, delete it from the old location — no duplicates

## Entropy Check Schedule

Set quarterly refactor dates during onboarding. Suggested cadence: every 13 weeks.

### Entropy check actions
- Remove dead initiatives (no activity in 60 days, no metric movement)
- Merge overlapping doctrines
- Update all metrics with current data
- Archive anything that has been superseded
- Verify every file passes governance rules

## Domain Scope Registry

| Directory | Boundary | Owner |
|-----------|----------|-------|
| `00_foundation/` | Governance, compliance, evolution rules | [Brain Owner] |
| `01_strategy/` | Strategic pillars and company-level doctrines | [Brain Owner] |
| `02_leadership/` | Communication standards, audience-awareness, PR hygiene | [Brain Owner] |
| `03_ai_native_transformation/` | AI adoption roadmap, baselines, leverage layers | [Brain Owner] |
| `04_team_brains/` | Per-team charters, authority models, KPIs (one folder per team you lead) | [Brain Owner] |
| `07_operating_rhythms/` | Weekly review, mid-cycle checkpoint, 1:1 protocol, quarterly refactor | [Brain Owner] |
| `08_metrics/` | Scorecards for AI adoption, delivery, leadership influence | [Brain Owner] |
| `09_people/` | Individual development profiles, 1:1 logs, talent review tracking | [Brain Owner] |
| `10_career/` | Career trajectory, development goals, mentorship commitments | [Brain Owner] |
| `11_compliance_security/` | Compliance program tracking, audit evidence (references to private system, no raw data) | [Brain Owner] |
| `12_projects/` | Active initiatives, project tracker, status sync | [Brain Owner] |
| `99_archive/` | Distilled book concepts, decision log template, historical records | [Brain Owner] |

## Anti-Entropy Rules

- No file is added "to think about later." If it is not ready for governance, it stays in `99_archive/` as a draft.
- If 3+ files reference the same concept, consolidate into one source of truth.
- If a metric has not been updated in 30 days, the file is flagged for review.
- When a new team member joins, create their `09_people/` file within 7 days following the individual development profile template.
- When a team member departs, move their `09_people/` file to `99_archive/` with a departure note.
