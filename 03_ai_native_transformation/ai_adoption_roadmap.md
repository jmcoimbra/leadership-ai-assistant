# AI Adoption Roadmap
> Owner: [Brain Owner] | Pillar: [Pillar N] | Status: Active | Last Audit: [YYYY-MM-DD]

## Purpose

Each team you lead must deploy at least one AI-powered daily workflow that changes a named decision flow, measure its impact, and present results to leadership. This roadmap defines the phases, owners, and deadlines.

## Phase 0 — How Layer + Behavioral Change

**Objective:** Define what AI-native work looks like for each team before measuring anything. Behavioral change first, metrics second.

**Method:** Run team group meetings (cancel individual 1:1s if needed). Each team maps:
- Top 5 repetitive tasks
- Top 5 recurring decisions that move work forward
- Current tools
- Concerns about AI integration
- What "Tuesday with AI" looks like

| Team | Group Meeting Deadline | Agenda Owner | Status |
|------|----------------------|---------------|--------|
| [Team 1] | [YYYY-MM-DD] | [Brain Owner] + [Team Lead] | |
| [Team 2] | [YYYY-MM-DD] | [Brain Owner] + [Team Lead] | |
| [Team 3] | [YYYY-MM-DD] | [Brain Owner] + [Team Lead] | |

**Exit criteria:** Each team has a concrete description of what their AI-native workflow looks like (the "how layer"). Decision latency, validation queue depth, rework rate, defect leakage, error rate, and MTTR baselines captured where applicable. Team concerns documented.

**Output:** `03_ai_native_transformation/ai_how_layer.md` — the how layer with team-specific behavioral switches, tools, and done signals. Feeds Phase 1 deployment targets.

## Phase 1 — Baseline + First Deployment

**Objective:** Establish current-state decision-flow baselines and deploy first AI workflow per team. Track a single named decision per team with a measurable delta against a documented baseline.

| Team | Decision Flow | Owner | Baseline Metric | First Live | Status |
|------|---------------|-------|----------------|-----------|--------|
| [Team 1] | [e.g., ticket triage readiness] | [Team Lead] | [decision latency / rework rate / validation queue depth + date] | [YYYY-MM-DD] | |
| [Team 2] | | | | | |
| [Team 3] | | | | | |

**Exit criteria:** All workflows deployed. Decision-flow baselines captured. Week 1 trace data collected.

## Phase 2 — Integration + Measurement

**Objective:** Integrate AI workflows into daily operations. Measure flow delta.

| Team | Integration Target | Measured Delta | Status |
|------|-------------------|----------------|--------|
| [Team 1] | [Decision trace threshold, e.g., 80% of triage decisions logged] | [Decision latency, rework rate, defect leakage, error rate, MTTR, validation queue depth] | |
| [Team 2] | | | |
| [Team 3] | | | |

**Exit criteria:** Flow deltas measured and documented. At least 2 of 3 teams show measurable decision latency reduction, validation confidence gain, or exception-routing accuracy.

## Phase 3 — Scale + Report

**Objective:** Present measured results to leadership. Expand to additional workflows.

- [ ] Compile results into executive presentation — Owner: [Brain Owner] — Deadline: [YYYY-MM-DD]
- [ ] Identify next AI workflow per team based on Phase 1-2 learnings — Owner: Team leads — Deadline: [YYYY-MM-DD]
- [ ] Present at leadership forum — Owner: [Brain Owner] — Deadline: [YYYY-MM-DD]
- [ ] Publish internal case study — Owner: [Brain Owner] — Deadline: [YYYY-MM-DD]

**Exit criteria:** Leadership has seen the data. Next phase workflows identified. AI adoption is proven, not claimed.

## Weekly Tracking

| Week | [Team 1] Usage | [Team 2] Usage | [Team 3] Usage | Notes |
|------|----------------|----------------|----------------|-------|
| | | | | |

## Escalation

- If any team has zero AI workflow usage for 2 consecutive weeks: 1:1 with team lead to identify blockers within 48 hours.
- If any instrument's measured delta regresses for 2 consecutive months: 1:1 with instrument owner within 48 hours, root-cause review within 7 days.

## AI Integration

| Decision | AI role | Human owner | Evidence inputs | Pass/fail criteria | Trace | Exception trigger | Flow metric |
|----------|---------|-------------|-----------------|--------------------|-------|-------------------|-------------|
| Which AI workflows count as adopted and ready to report? | validate | [Brain Owner] | Decision-flow baselines, workflow traces, telemetry, defect and rework data, exception logs | Workflow has named decision, owner, evidence, criteria, trace, exception trigger, and measured flow delta | Roadmap status table and executive presentation source data | Workflow with usage but no decision-flow metric is excluded from leadership reporting | Decision latency, validation queue depth, rework rate, defect leakage, error rate, MTTR |

Use AI to generate weekly decision-flow summaries, draft the executive presentation from raw metrics, and identify additional automation candidates based on repeated decision waits.
