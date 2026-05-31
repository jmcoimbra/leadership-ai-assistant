# Strategic Pillars
> Owner: [Brain Owner] | Pillar: All | Status: Draft | Last Audit: [YYYY-MM-DD]

## Purpose

Define the 3-5 pillars your engineering org bets on this year. Every initiative, file, and metric maps to one. Pillars are the load-bearing concepts that anchor governance.

## Pillars

| # | Name | One-Sentence Thesis | Measurable Outcome (cycle) | Owner |
|---|------|---------------------|---------------------------|-------|
| 1 | [Pillar 1 Name] | [What it means in one sentence] | [Baseline → target → date] | [Brain Owner] |
| 2 | [Pillar 2 Name] | | | |
| 3 | [Pillar 3 Name] | | | |
| 4 | [Pillar 4 Name] | | | |
| 5 | [Pillar 5 Name] | | | |

## Escalation

If any active initiative cannot map to one of these pillars, decide within 7 days: add a pillar, rewrite the initiative, or archive it.

## AI Integration

| Decision | AI role | Human owner | Evidence inputs | Pass/fail criteria | Trace | Exception trigger | Flow metric |
|----------|---------|-------------|-----------------|--------------------|-------|-------------------|-------------|
| Does each active initiative map to a current strategic pillar? | validate | [Brain Owner] | Project list, pillar definitions, measurable outcomes, weekly review notes | Every active initiative maps to one pillar with baseline, target, owner, and deadline | Weekly review notes and pillar history | Unclassified initiative triggers owner review within 7 days | Unclassified initiative count |

Use AI to classify projects, people development goals, and operating metrics against these pillars during weekly review. Any unclassified item is flagged for owner review.

## How to Use

- **Every brain file maps to one pillar** (header: `> Pillar: N`).
- **Every initiative cites the pillar it serves** in `12_projects/<initiative>.md`.
- **Quarterly:** Re-rank. If a pillar has not moved its measurable outcome in a quarter, either the pillar is wrong or the work is wrong.

## In Outbound Content

Do NOT use the bare label "Pillar N" in messages, decks, or docs your team or stakeholders see. Name the substantive concept directly. The pillar number is internal scaffolding for the brain; it is not communication-ready.

The `.claude/hooks/check-pillar.sh` hook enforces this at write-time.

## Pillar History

Track when a pillar changes meaning or gets retired. Pillars should not silently mutate.

- [YYYY-MM-DD]: [Change made — e.g., "Pillar 3 narrowed from 'product growth' to 'loyalty reinvention'"]
