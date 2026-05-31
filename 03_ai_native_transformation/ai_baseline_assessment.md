# AI Baseline Assessment
> Owner: [Brain Owner] | Pillar: [Pillar N] | Status: Draft | Last Audit: [YYYY-MM-DD]

## Purpose

You cannot measure adoption without a starting point. This file captures the current decision-flow state of each team before AI workflows are deployed.

## Template — One Section per Team

### [Team Name] — Current State

Data collection owner: [Team Lead]. Deadline: [YYYY-MM-DD].

| Process | Decision It Moves | Current Owner | Evidence Used | Current Method | Waiting Cost | AI Candidate? | Notes |
|---------|-------------------|---------------|---------------|----------------|--------------|---------------|-------|
| [Process 1] | [Decision required to move work forward] | [Person / role] | [Facts required] | [Manual / Tool-assisted / etc.] | [Decision latency / queue depth] | Yes/No | [Notes] |
| [Process 2] | | | | | | | |
| [Process 3] | | | | | | | |

### Productivity Baselines

| Metric | Value | Source |
|--------|-------|--------|
| [e.g., decision latency avg] | [value] | [data source / dashboard] |
| [e.g., validation queue depth] | [value] | [data source / dashboard] |
| [e.g., rework rate] | [value] | [data source / dashboard] |
| [e.g., defect leakage] | [value] | [data source / dashboard] |
| [e.g., error rate] | [value] | [data source / dashboard] |
| [e.g., MTTR] | [value] | [data source / dashboard] |

## Current AI Tools in Use

| Tool | Team | Usage Level | Measured? |
|------|------|-------------|-----------|
| [Tool name] | [Team] | [Daily / Ad-hoc / Pilot] | Yes/No |

## Collection Protocol

1. **By [date]:** Run group meeting with each team. Walk through each process row, capture current decision owner, evidence inputs, waiting cost, and concerns about AI integration.
2. **By [date]:** Compile data from group meeting notes into this file.
3. **By [date]:** File transitions from `Draft` to `Active` with real data in every row.

## Completion Criteria

- [ ] All process rows have real data (decision, owner, evidence, method, waiting cost)
- [ ] At least one decision-flow baseline is captured per team
- [ ] Current AI tools inventory is complete

## Escalation

If productivity deltas are not measured against these baselines by the Phase 2 deadline in `ai_adoption_roadmap.md`: Phase 1 investment is unproven. Escalate to leadership with data request.

## AI Integration

| Decision | AI role | Human owner | Evidence inputs | Pass/fail criteria | Trace | Exception trigger | Flow metric |
|----------|---------|-------------|-----------------|--------------------|-------|-------------------|-------------|
| Which manual workflows qualify as AI decision-flow candidates? | recommend | [Brain Owner] + [Team Lead] | Process rows, current owner, evidence inputs, waiting cost, defect and rework data | Candidate has recurring decision, measurable waiting cost, available evidence, human owner, and trace location | Baseline assessment table | Candidate with no owner, evidence, or metric stays out of Phase 1 | Decision latency, validation queue depth, rework rate, defect leakage, error rate, MTTR |

Use AI to cluster repeated manual work, identify candidate decision flows, and draft measurement plans. The team lead confirms actual baselines before the assessment is marked active.
