# Looker LookML Patterns

**Added:** 2026-03-11
**Last Updated:** 2026-05-19 (Tools NOT in use at [Your Company] section, Spectacles entry from [your-org]-looker#379 closed-loop hallucination). Earlier 2026-04-10.
**Source:** PR #325 QA Dashboard fix ([your-org]-looker)

## Filter Logic: AND vs OR

### `type: count` with multiple filters = AND

```lookml
# This counts rows where BOTH conditions are true (AND)
measure: both_coverage_count {
  type: count
  filters: [has_manual: "yes", has_automated: "yes"]
}
```

### OR logic requires `type: number` + CASE WHEN

```lookml
# This counts rows where EITHER condition is true (OR)
measure: any_coverage_count {
  type: number
  sql: COUNT(CASE WHEN ${has_manual} OR ${has_automated} THEN 1 END) ;;
}
```

**Common bug:** Label says "Any Coverage" but implementation uses `type: count` with multiple filters (AND logic). Always verify filter semantics match the label.

## Dimension Groups for Timestamps

Looker `dimension_group` with `type: time` auto-generates `_raw`, `_time`, `_date`, `_week`, `_month`, `_quarter`, `_year` dimensions from a single timestamp column. Prefer this over pre-computing date parts in dbt when the mart is Looker-only.

## yesno Dimensions

Map boolean flags from dbt as `type: yesno`. Looker renders as Yes/No filter dropdowns. SQL references the boolean column directly:

```lookml
dimension: is_defect_leakage {
  type: yesno
  sql: ${TABLE}."IS_DEFECT_LEAKAGE" ;;
}
```

## Drill Fields

Always add `drill_fields` to measures for dashboard interactivity. Standard pattern:

```lookml
measure: count {
  type: count
  drill_fields: [issue_key, project_key, priority, status, created_date, assignee]
}
```

## Dashboard UI Patterns (Looker Web)

### Filters require at least one tile

Dashboard filter button is grayed out on empty dashboards. Looker needs at least one tile
referencing an explore before filters can be created.
**Workaround:** Add a dummy single-value tile (any measure from the target explore), then add filters.
Delete or repurpose the dummy tile after. Filters persist independently.

### "Colored by" = Pivot

When a chart spec says "colored by `field`", add that field as a **Pivot** in Looker:
1. Add the field to the query
2. Click the Pivot icon (two arrows) on the field
3. Run — each unique value becomes a separate color series

Works for: bar charts (stacked/grouped), line charts (multi-line), area charts.
Does NOT apply when the "color" field is already the x-axis dimension (e.g., coverage rates by project).

### Stacked bars

After pivoting, switch to stacked: Edit visualization → Series/Plot section → Stacking = "Stacked".

Added 2026-03-13. Source: QA Dashboard build session.

## Table Calculations (Ad-Hoc Rates)

For one-off rate tiles without adding a LookML measure:
1. Add both measures to the query
2. Click "Add calculation"
3. Expression: `${view.numerator} / ${view.denominator}`
4. Set format to Percent
5. Hide raw measures, switch viz to Single Value

Prefer a permanent LookML measure (`::FLOAT / NULLIF()` pattern) if the rate is reused across tiles.

Added 2026-03-16. Source: QA Dashboard build session.

## Dashboard Documentation

Three layers of context for dashboard users:
- **Dashboard description:** Click title area → description. Shows as (i) icon. One-liner scope.
- **Text tiles:** Section headers between tile groups. Keep short: "*Section Name* — what it measures"
- **Tile descriptions:** Edit tile → title → Description field. Shows as (i) hover. Define the metric formula.
- **Reference lines:** Edit viz → Plot → Reference Lines. Add target constants (e.g., 10% leakage target).

Added 2026-03-16. Source: QA Dashboard build session.

## Permissions

Looker access is folder-based, not per-dashboard. If a user cannot see a dashboard:
1. Check the folder's Manage Access settings (three-dot menu on folder)
2. If dashboard is in a personal folder, move it to a shared folder
3. If user has no Looker account, they need provisioning (check if Google SSO is enabled)

Added 2026-03-16.

## QA Metric Formulas (qa_stability view)

### QA Found Rate
`qa_found_count / defect_leakage_count` — ratio of QA catches to production defects.
- Numerator (`is_qa_found_issue`): PLAT/DATA Bug/Sub-bug/Issue + BUGS Issue/Outage with `qa-found` label
- Denominator (`is_defect_leakage`): BUGS Issue/Outage (not Canceled/No Action Taken)
- NOT a detection percentage. It's catches per production defect.

### BUGS Project Issue Types (verified 2026-03-19)
Issue, Outage, Sub-bug, Sub-task, Task, Sub Test Execution, Small Improvement.
No "Bug" type exists. The `is_defect_leakage` filter includes Bug type harmlessly.

Added 2026-03-19. Source: QA Found Rate fix session, PR #368.

## MTBF/MTTR Measures (qa_stability view)

### MTBF (Mean Time Between Failures)
`DATEDIFF(HOUR, MIN(created_at), MAX(created_at)) / NULLIF(count - 1, 0)`
- Auto-scopes per time group when used with `created_month` or `created_week` dimension. Looker's GROUP BY constrains MIN/MAX to each period.
- No separate "MTBF by period" measure needed. Single measure works for both single-value tiles and trend charts.

### MTTR (Mean Time To Resolve)
`type: average` on `lead_time_hours`, filtered to `is_stability_incident = yes` AND `is_resolved_not_wont_do = yes`.
- Avg + median on same chart: median shows typical experience, avg exposes outlier spikes.

### Stability Incident Flag Pattern
Boolean dimension `is_stability_incident` (computed in dbt) filters all stability measures. Dashboard users control severity via Priority filter, not hardcoded SQL.
- Population: BUGS project, issue_type IN ('Issue', 'Outage'). All priorities included; dashboard filter slices.
- Keeps measures reusable: same measures power single-value tiles, trend charts, and drilldowns.

Added 2026-03-20. Source: PRs [your-org]-dbt #833, [your-org]-looker #369.

## Async Dashboard Spec Workflow

When LookML changes are merged but not yet deployed to production:
1. Document chart specs in a Notion reference page (dimensions, measures, pivots, filters, chart type)
2. Include Looker setup instructions per tile (pivot field, stacked bar config, filter wiring)
3. Build tiles in Looker UI once deploy lands, following the spec

Avoids: blocking on deploy, losing chart design decisions, repeated Looker exploration.
Added 2026-03-20.

## [your-org]-looker Repository

- Views: `views/<name>.view.lkml`
- Models: `models/<name>.model.lkml`
- Dashboards: LookML dashboards or UI-built (most are UI-built at [Your Company])
- PRs require Looker validation (CI check)

### Tools NOT in use at [Your Company]

Do not gate PR reviews on these tools even if a PR test plan references them. Generator-LLMs sometimes inject plausible-sounding LookML CI gates from training data.

- **Spectacles** (spectacles.dev). Real LookML CI product; [Your Company] does not subscribe, has no API credentials, no team owner, no historical run. If a PR test plan lists "Stage 2 Spectacles SQL validation" or asks for a Spectacles run URL, retract the gate. Acceptable validation paths: Looker UI project validator on the dev branch + reconciliation queries against the affected explore (e.g., `claimed + unclaimed == count` per merchant). Source: 2026-05-19 [your-org]-looker#379 closed-loop hallucination, enforced 3 rounds across 11 days before Bailey DM surfaced it.

## Looker MCP Tile Creation Limitations

`mcp__looker__add_dashboard_element` can create tiles but has significant gaps:

1. **No pivot support.** Cannot set a field as pivot. Stacked bars render as horizontal bars with concatenated dimension labels. Must fix manually in Looker UI: move field to Pivot, switch to Column chart, set Stacking = "Stacked".
2. **No text-only tiles.** Cannot create section header or explanatory text tiles via API.
3. **No tile notes.** Cannot set the (i) tooltip icon text ("Note on Tile" in Looker UI). Manual step: Edit dashboard → tile three-dot menu → Edit → "Note on Tile".
4. **No global filter wiring.** New tiles are not automatically connected to dashboard filters. Must manually wire each filter in the tile's Filters tab.
5. **No update API.** `update_dashboard_element` does not exist in the MCP. Cannot modify existing tiles programmatically.
6. **Tiles land at bottom.** New tiles are appended to the end of the dashboard layout. Must drag into correct section manually.

**Implication:** Use API for bulk tile creation (measures, dimensions, filters, sorts), then do a manual pass for pivots, layout, text tiles, notes, and filter wiring.

Added 2026-04-10.

## QA Dashboard #508: Canonical Query

**Dashboard:** [Looker #508 QA Dashboard](https://[your-company].cloud.looker.com/dashboards/508)

**Default filter set for AI adoption / weekly review pulls:**
- Project: `BUGS,DATA,PLAT`
- Priority: `Blocker,Critical or Major`
- Created Date: `this year to second`

**Direct URL with params (fastest path for screenshot or share):**
```
https://[your-company].cloud.looker.com/dashboards/508?Project=BUGS%2CDATA%2CPLAT&Priority=Blocker%2CCritical+or+Major&Created+Date=this+year+to+second
```

**Tiles (May 2026 snapshot, YTD with default filters):** 337 Prod Issues, 21.36% QA Found, 74.23% Defect Leakage (trending down), 67.40% Resolution, 732 Defects, 78 Currently Open, 8.5d Cycle Time, 276.2d Lead Time. Charts: QA Found Issues by month/project, Incident Count by priority, AVG Cycle vs Lead Time, Defect Leakage by project, MTTR Over Time, MTBF Over Time, MTTR by Priority, Median Cycle/Lead Time by Project.

**Programmatic pull via `mcp__looker__query`:** explore name + dimension names not yet captured. Capture next time the QA Dashboard is touched in Looker UI (Edit Tile → "Show SQL") so weekly review can pull defect leakage rate without screenshot.

**Why this dashboard matters:** Pillar 1 outcome artifact for QA team. Defect leakage trend is the load-bearing measurement for Phase 1 AI adoption (QA team). MoM / QoQ / YoY comparisons built in.

Added 2026-05-01. Source: 2026-05-01 weekly review session.

## Pre-Build Data Verification Pattern

Before building a dashboard manually, run a verification query via Looker MCP to confirm data flows:

```
mcp__looker__query(model, explore, fields=[all key measures], filters={date range}, limit=1)
```

Confirms: Snowflake table populated, dbt models ran, Looker explore resolves, measures return non-null values. Catches: missing dbt runs, broken Snowflake permissions, stale cache.

Added 2026-04-10.
