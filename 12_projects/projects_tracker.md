# Projects Tracker
> Owner: [Brain Owner] | Pillar: All | Status: Active | Last Audit: [YYYY-MM-DD]

## Purpose

Single index of every active initiative the brain owner is accountable for. One row per project. One detail file in `12_projects/<project_name>.md` per row.

## Active

| Project | Owner | Pillar | Stage | Last Update | Detail File |
|---------|-------|--------|-------|-------------|-------------|
| [Name] | [Person] | [Pillar N] | [Draft / Active / Launched / Maintained] | [YYYY-MM-DD] | `12_projects/[name].md` |

## On Hold

| Project | Owner | Reason on Hold | Resume Trigger |
|---------|-------|----------------|----------------|
| [Name] | | [Why] | [Condition to resume] |

## Recently Shipped

Keep last 4 weeks. Archive older entries to `99_archive/` quarterly.

| Project | Shipped Date | Outcome | Lessons |
|---------|--------------|---------|---------|
| [Name] | [YYYY-MM-DD] | [Result vs target] | [One sentence] |

## Staleness Rules

- **>14 days no commit on detail file:** Address within 7 days (merge / pause / archive)
- **>21 days no commit:** Surface in weekly review
- **>30 days no commit:** Vision > Execution violation. Resolve in same week.

## Escalation

If an active project has no logged movement for 21 days, decide within 7 days: ship, re-scope, archive, or escalate to the sponsor.

## AI Integration

| Decision | AI role | Human owner | Evidence inputs | Pass/fail criteria | Trace | Exception trigger | Flow metric |
|----------|---------|-------------|-----------------|--------------------|-------|-------------------|-------------|
| Which active project needs status action this week? | recommend | [Brain Owner] | Detail files, commit dates, project stage, owner, deadline, chat or ticket evidence | Project has movement within 21 days or an explicit ship, pause, archive, or escalation decision | Projects tracker and weekly review notes | No logged movement for 21 days triggers weekly review action | Stale project count and status-decision latency |

Use AI to scan detail files weekly, surface stale projects in weekly review, and draft status updates from recent commits and source evidence.
