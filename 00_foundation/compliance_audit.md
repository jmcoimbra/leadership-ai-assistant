# Compliance Audit Protocol
> Owner: [Brain Owner] | Pillar: All | Status: Enforced | Last Audit: 2026-05-31

## Purpose

This is the immune system of the brain. It verifies compliance with `brain_governance.md` using tiered checks - continuous enforcement at write-time, quarterly deep audits, and semi-annual language reviews.

## File Discovery

Do NOT maintain a static file list. At audit time, discover files dynamically:

**Include:** All `*.md` files in directories `00_foundation/` through `12_projects/`
**Exclude:** `99_archive/`, `CLAUDE.md`, `AGENTS.md`, `README.md`, `.context/`, this file

This ensures new files are automatically covered without manual list maintenance.

## Tier 1 - Write-Time Enforcement (Continuous)

Enforced by the agent every time a file is created or modified (see CLAUDE.md "File Compliance Check").

| # | Criterion | When |
|---|-----------|------|
| 1 | Has named owner in header | Every file write |
| 2 | Maps to a strategic pillar | Every file write |
| 3 | Updated within the last 90 days | Every file write (check existing files during weekly review) |
| 4 | AI Integration section contains an AI Decision Contract table | Every operational domain file write |

Files failing Tier 1 at write-time must be fixed before committing.

## Tier 2 - Quarterly Audit (Initiative/Operational Files)

Run quarterly against files in: `01_strategy/`, `03_ai_native_transformation/`, `04_team_brains/`, `08_metrics/`, `11_compliance_security/`, `12_projects/`.

| # | Criterion | Pass/Fail |
|---|-----------|-----------|
| 1 | Contains at least one measurable outcome (baseline -> target -> date) | |
| 2 | Defines escalation trigger | |
| 3 | AI Decision Contract names decision, AI role, human owner, evidence, pass/fail criteria, trace, exception trigger, and flow metric | |

Files scoring 0/3 are flagged RED - remediate within 14 days or archive.

## Tier 3 - Semi-Annual Language Audit (Strategic/Leadership Files)

Run every other quarter against files in: `01_strategy/`, `02_leadership/`, `10_career/`.

The deterministic-language rule and banned-word list live in `context/knowledge/voice-profile.md`. Audit checks alignment with that profile.

| # | Criterion | Pass/Fail |
|---|-----------|-----------|
| 1 | Uses deterministic language (no banned vague words without specifics) | |

Banned words without specifics: improve, enhance, support, explore, consider, leverage. Required pattern: `[verb] [thing] from [baseline] to [target] by [date]`.

## People File Compliance (Quarterly)

Run against every file in `09_people/`:

| # | Criterion | Pass/Fail |
|---|-----------|-----------|
| 1 | 1:1 logged within last 21 days | |
| 2 | At least one growth goal defined (not stale >30 days) | |
| 3 | Delegation maturity assessed (Task / Result / Autonomous) | |
| 4 | Talent review status documented | |

People files scoring below 3/4 are flagged RED - schedule a focused 1:1 within 7 days.

## Career File Compliance (Quarterly)

Run against `10_career/` files:

| # | Criterion | Pass/Fail |
|---|-----------|-----------|
| 1 | Career trajectory milestones have evidence updates | |
| 2 | Development goals have checkpoint status updates | |
| 3 | External coaching/mentorship goals have logged evidence of progress | |

## Audit Schedule

| Audit Type | Next Run | Frequency |
|-----------|----------|-----------|
| Tier 1 | Continuous | Every file write + weekly review freshness check |
| Tier 2 | [Set during onboarding] | Quarterly (aligned with quarterly refactor) |
| Tier 3 | [Set during onboarding] | Semi-annual |
| People files | [Set during onboarding] | Quarterly |
| Career files | [Set during onboarding] | Quarterly |

## Escalation

- Tier 2 file scoring 0/2: remediate or archive within 14 days
- Files not updated in 90+ days (Tier 1 check): flagged for owner review in weekly review
- If >30% of files fail Tier 2 in a quarterly audit: brain structure refactor triggered immediately
- People files with no 1:1 in 21 days: schedule 1:1 within 48 hours
- Career files with no quarterly update: force career review with the brain owner's manager within 14 days

## AI Integration

| Decision | AI role | Human owner | Evidence inputs | Pass/fail criteria | Trace | Exception trigger | Flow metric |
|----------|---------|-------------|-----------------|--------------------|-------|-------------------|-------------|
| Is a brain file compliant enough to commit or keep active? | validate | [Brain Owner] | File headers, AI Decision Contract tables, measurable outcomes, escalation triggers, audit schedule | Tier 1 errors equal 0 and Tier 2 RED files have remediation or archive decision | Audit output and quarterly refactor notes | Any Tier 1 error blocks commit; any Tier 2 RED file older than 14 days escalates to owner review | Non-compliant file count and remediation age |

Use AI to discover files, run Tier 1 and Tier 2 checks, populate audit reports, and flag stale decision contracts. The brain owner verifies remediation decisions before commit.
