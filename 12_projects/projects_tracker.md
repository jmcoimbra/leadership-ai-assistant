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

- Use AI to scan detail files weekly and surface stale projects in your weekly review.
- Use AI to draft status updates per project from recent commits + chat threads.
