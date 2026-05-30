---
description: Synthesize CTO trajectory evidence from 14+ brain files into a 5-min pre-[Your CTO]-1:1 brief. Covers evidence inventory, QA authority scorecard, development goals, and mentorship ROI.
---

# Career Brief

Synthesize scattered career evidence into a structured brief for [Your CTO] 1:1 preparation.

Read `.claude/commands/_preamble.md` for shared constants and adapter rules. External systems are optional in the public template.

## Usage

```
/career-brief              → Full brief (all 4 sections)
/career-brief --quick      → Evidence inventory only (Section 1)
```

Arguments: $ARGUMENTS

## Autonomy Model

| Action | Mode |
|--------|------|
| Read all brain files listed below | Autonomous |
| Query Goals Tracker DB | Autonomous |
| Generate brief | Autonomous |
| Output | Inline (not saved to file) |

This command produces read-only output. No brain files are modified. No gating needed.

## Phase A: Load Evidence Sources

Read these files (all required):

**Career tier:**
1. `10_career/_template_career_trajectory.md` — gap analysis, quarterly milestones, evidence sections
2. `10_career/_template_career_trajectory.md` — 3 development goals with progress
3. `10_career/_template_career_trajectory.md` — insights, action plans, habits
4. `10_career/_template_career_trajectory.md` — accumulated evidence log

**Leadership tier:**
5. `context/knowledge/voice-profile.md` — influence tracker entries
6. `02_leadership/pr_hygiene_mandate.md` — gap closure status
7. `02_leadership/async_communication_standard.md` — visibility actions log

**Domain tier:**
8. `04_team_brains/_template_team_brain.md` — QA block events, authority assertions
9. `08_metrics/_template_team_scorecard.md` — team AI usage data
10. `08_metrics/_template_team_scorecard.md` — initiative completions
11. `03_ai_native_transformation/ai_adoption_roadmap.md` — team heat map and adoption evidence

**Compliance/execution tier:**
12. `11_compliance_security/_template_compliance_program.md` — compliance contributions
13. `12_projects/projects_tracker.md` — initiative completion status

**External:**
14. Optional goals tracker or calendar source when configured — habit repetition counts

## Phase B: Determine Time Window

Find the date of the last [Your CTO] 1:1 by:
1. Check Google Calendar for past [Your CTO] meetings (`gcal_list_events` or `gcal_search_events` for "[Brain Owner] / [Your CTO]")
2. Or parse `10_career/_template_career_trajectory.md` for the most recent entry date

Set `WINDOW_START` = date of last [Your CTO] 1:1.
Set `WINDOW_END` = today.

All evidence in the brief must fall within this window unless it is a cumulative metric.

## Section 1: Evidence Inventory by CTO Competency

From `cto_trajectory.md`, extract the CTO competency gap analysis table. For each competency:

1. Scan ALL loaded brain files for evidence logged between `WINDOW_START` and `WINDOW_END`
2. Match evidence to the competency's "Evidence Required" column
3. Rate: **Strong** (2+ concrete instances), **Partial** (1 instance), **None** (0 instances)

```
## Section 1: Evidence Inventory (since [WINDOW_START])

| CTO Competency | Evidence | Source File | Date | Rating |
|---------------|----------|------------|------|--------|
| Strategic Vision & Business Acumen | Presented AI monetization timeline to R&D Leadership | assertiveness_playbook.md | 2026-03-12 | Strong |
| Technical Breadth | [none this period] | — | — | None |
| Team Leadership & Culture | Coached an IC through first AI command build | 09_people/_template_individual_development_profile.md | 2026-03-10 | Partial |
| ... | ... | ... | ... | ... |

### Evidence Gaps (competencies with "None")
- Technical Breadth: No evidence this period. Suggestion: [specific action to demonstrate this competency before next 1:1]
- ...
```

## Section 2: QA Authority Scorecard

From `qa_authority_model.md` and `assertiveness_playbook.md`:

```
## Section 2: QA Authority Scorecard (since [WINDOW_START])

| Metric | This Period | Previous Period | Trend |
|--------|------------|----------------|-------|
| Release blocks exercised | [N] | [N] | ↑/→/↓ |
| Public authority assertions | [N] | [N] | ↑/→/↓ |
| QA pushbacks in cross-functional forums | [N] | [N] | ↑/→/↓ |

### Notable QA Authority Moments
- [Date]: [Specific moment from assertiveness_playbook.md or qa_authority_model.md]

### QA Authority Gap
- [If no events: "Zero QA authority events this period. Dev Goal 2 is not advancing. Suggestion: [specific action]"]
```

## Section 3: Development Goal Progress

From `development_goals_2026.md`:

```
## Section 3: Development Goal Progress

### Goal 1: AI-native adoption across all 3 teams by mid-cycle
- **Metric:** Team heat map movement (from [your-company]_ai_tier_framework.md)
- **This period:** [Who moved? Who stalled?]
- **Evidence:** [Specific instances: commands built, AI usage observed, team members coached]
- **Status:** On track / At risk / Behind

### Goal 2: QA as influential voice in engineering
- **Metric:** QA Authority Scorecard (Section 2 above)
- **This period:** [Summary from Section 2]
- **Status:** On track / At risk / Behind

### Goal 3: Communicate with directness and impact
- **Metric:** Assertiveness instances + feedback received
- **This period:** [Count of assertions from assertiveness_playbook.md] + [Any [Your CTO] feedback from review_cycle_evidence.md]
- **Evidence:** [Specific instances of direct communication logged]
- **Status:** On track / At risk / Behind
```

## Section 4: Mentorship ROI

From `executive_mentorship_tracker.md` and Goals Tracker DB:

```
## Section 4: Mentorship ROI

### Insight Application
- Total insights: [N]
- Applied: [N] ([%])
- Unapplied >30 days: [N] — [list the specific insights]

### Action Plan Completion
- Total action plans: [N]
- Done: [N] ([%])
- Overdue: [N]

### Habit Repetition Progress
| Habit | Reps | Target | On Track? |
|-------|------|--------|-----------|
| Reframe limiting beliefs | [X]/21 | 7x by week 2, 21x by week 4 | Yes/No |
| Future-value framing | [X]/21 | ... | Yes/No |
| Circle of Influence filter | [X]/21 | ... | Yes/No |
| Proactive response choice | [X]/21 | ... | Yes/No |

### Net Mentorship Assessment
[One line: "Mentorship is producing behavioral change" or "Mentorship is consumption without practice — [N] insights unapplied, [N] habits behind schedule"]
```

## Final Output: Brief Summary

After the 4 sections, produce a 3-line summary designed for the opening of a [Your CTO] 1:1:

```
## Brief Summary (Opening Lines for [Your CTO] 1:1)

**Strongest evidence this period:** [1 sentence — the best CTO competency demonstration]
**Biggest gap this period:** [1 sentence — what competency has zero evidence]
**One ask for [Your CTO]:** [1 sentence — specific feedback request or alignment check]
```

## Error Handling

| Failure | Behavior |
|---------|----------|
| Any brain file missing | Skip that file's data. Note gap. Never block the brief. |
| Goals Tracker DB unavailable | Skip Section 4 habit data. Note gap. |
| Calendar unavailable | Use most recent evidence date as WINDOW_START approximation. Note gap. |
| No evidence found in any section | State it. "Zero evidence this period" is itself critical information for the 1:1. |

## Important Notes

- This command is designed for **speed**. Output is inline, not saved. Consume in 5 minutes before the meeting.
- The brief does NOT replace `/meeting-prep` for [Your CTO] 1:1s. It complements it: `/meeting-prep` generates the meeting script with topics and agenda. `/career-brief` generates the career evidence layer.
- `/meeting-prep` can auto-suggest running `/career-brief` when it detects a [Your CTO] meeting.
- Evidence must be **concrete and dated**. Never say "[Brain Owner] demonstrated leadership" without a specific instance, date, and source file.
- Use future-value framing per Insight 5: frame evidence as "what this enables" not "what was delivered."
