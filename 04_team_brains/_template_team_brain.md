# [Team Name] Brain
> Owner: [Brain Owner] | Pillar: [Pillar N] | Status: Draft | Last Audit: [YYYY-MM-DD]

## Purpose

Why this team exists, what it owns, what it does not own. One paragraph. Specific enough that a new EM could pick this up and operate.

## Charter

- **Mission:** [One sentence — what this team is accountable for]
- **Scope (owns):** [Bulleted, specific responsibilities]
- **Scope (does not own):** [Adjacent areas that get confused with this team]
- **Authority model:** [Where this team can block, where it advises, where it executes]

## Team

| Member | Role | Cadence | Notes |
|--------|------|---------|-------|
| [Name] | [Lead / Senior IC / IC] | [Weekly / Bi-weekly 1:1] | |

## Operating Cadences

- **Standup:** [Daily / Weekly] [time, channel]
- **Sync:** [Cadence, focus]
- **Retro:** [Cadence]

## KPIs

| Metric | Baseline | Target | Source | Owner |
|--------|----------|--------|--------|-------|
| [e.g., on-call SLO] | | | [Dashboard URL or query] | [Team Lead] |
| [e.g., cycle time] | | | | |

## Active Initiatives

Link to entries in `12_projects/`:
- `12_projects/[initiative_name].md`

## Runbooks / SOPs

Index of operational procedures owned by this team. One-line description + link.

- [Runbook 1]: [Link]
- [Runbook 2]: [Link]

## AI Integration

| Decision | AI role | Human owner | Evidence inputs | Pass/fail criteria | Trace | Exception trigger | Flow metric |
|----------|---------|-------------|-----------------|--------------------|-------|-------------------|-------------|
| [Decision this team's AI workflow changes] | [draft / recommend / validate / decide / monitor] | [Team Lead] | [Dashboards, tickets, PRs, incidents, customer signals] | [Pass/fail criteria for the decision] | [Where the decision record lives] | [Condition that routes to human review] | [Decision latency / rework rate / error rate / MTTR] |

Reference the relevant entries in `03_ai_native_transformation/ai_how_layer.md`. A team AI workflow is not active until this table has a named decision, human owner, evidence inputs, trace, exception trigger, and flow metric.

## Escalation Triggers

- [Condition 1] → [Action, who is notified]
- [Condition 2] → [Action]

## Cross-References

- `03_ai_native_transformation/ai_how_layer.md` — behavioral switches for this team
- `08_metrics/_template_team_scorecard.md` — metric tracking template
