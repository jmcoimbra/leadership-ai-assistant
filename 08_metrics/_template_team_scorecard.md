# [Team] Scorecard
> Owner: [Brain Owner] | Pillar: [Pillar N] | Status: Active | Last Audit: [YYYY-MM-DD]

## Purpose

Tracks the measurable outputs this team owns. Updated [Weekly / Monthly] during the operating rhythm.

## Scorecard

| Metric | Baseline | Target | Current | Trend | Source | Last Updated |
|--------|----------|--------|---------|-------|--------|--------------|
| [e.g., defect leakage] | [Number + date] | [Number] | [Number] | ↑ / ↓ / → | [Dashboard URL] | [YYYY-MM-DD] |
| [e.g., cycle time avg] | | | | | | |
| [e.g., on-call escalations] | | | | | | |
| [e.g., decision latency] | | | | | | |
| [e.g., validation queue depth] | | | | | | |
| [e.g., rework rate] | | | | | | |

## Definitions

For each metric, define how it is measured.

- **[Metric 1]:** [SQL query, dashboard filter, or calculation]
- **[Metric 2]:**

## Trend Notes

Latest cycle observations. Surface anything that moves >10% week-over-week.

- [YYYY-MM-DD]: [Observation]

## Escalation Triggers

- [Metric crosses threshold] → [Action, who is notified, by when]

## AI Integration

| Decision | AI role | Human owner | Evidence inputs | Pass/fail criteria | Trace | Exception trigger | Flow metric |
|----------|---------|-------------|-----------------|--------------------|-------|-------------------|-------------|
| Which metric requires owner action this cycle? | recommend | [Metric Owner] | Scorecard values, thresholds, source freshness, trend notes | Metric has current source; movement beyond threshold has owner follow-up and deadline | Trend Notes and owner follow-up draft | Source stale 30+ days or metric crosses threshold | Decision latency, validation queue depth, rework rate, defect leakage, error rate, MTTR |

Use AI to compare current metric values against thresholds, detect stale sources, and draft owner-specific follow-ups. The metric owner verifies the source before any status is sent externally.
