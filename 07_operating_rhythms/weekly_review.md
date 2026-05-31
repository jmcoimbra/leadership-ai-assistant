# Weekly Review Protocol
> Owner: [Brain Owner] | Pillar: All | Status: Enforced | Last Audit: [YYYY-MM-DD]

## Purpose

This is your Monday operating rhythm. Without a weekly review, initiatives drift, metrics stale, and the brain decays. Target time: 30-45 minutes. Non-negotiable.

## Weekly Review Checklist

### 0. Topic Generation (5 min)
- [ ] Scan brain state, output ranked topics with talking points
- [ ] Select top 3 topics. At least 1 must involve healthy friction.
- [ ] If a leadership meeting is this week: begin 72-hour prep.
- [ ] If a 1:1 with your manager is tomorrow: generate the 1-1-1 (one metric, one risk, one recommendation).

### 1. Execution Check (10 min)
- [ ] What did I commit to last week? Did I deliver?
- [ ] What initiatives moved forward? Which stalled?
- [ ] Are any initiatives stuck in "conceptual" for > 14 days? If yes, either add an execution plan or kill them.
- [ ] Review `12_projects/projects_tracker.md` — any project with no commit in 21+ days? If yes: ship, archive, or log decision.
- [ ] Review open GitHub PRs — any PR open >14 days? Address within 7 days.
- [ ] PR hygiene compliance: Are team PRs being socialized per `02_leadership/pr_hygiene_mandate.md`? Any reviewer non-responses >48 hours?
- [ ] Stuck vs. stubborn check: For any stalled initiative, has the same approach been tried twice? If yes, force a different path within 7 days.

### 2. Metric Check (10 min)
- [ ] Review your scorecard files in `08_metrics/` — any red flags?
- [ ] Any team with zero AI usage this week?
- [ ] Any compliance certification deadline within 30 days without evidence of readiness?
- [ ] Any metric not updated in 30+ days? Flag it.

### 3. People Check (10 min)
- [ ] Review `09_people/` — anyone without a 1:1 in the past 21 days? If yes: schedule within 48 hours.
- [ ] Review delegation maturity — am I holding decisions that should be delegated? ("If I disappeared for 2 weeks, would my teams operate?")
- [ ] Review growth goals — any person with stale goals (no progress in 30 days)?
- [ ] Any team member blocked and I have not cleared the path?
- [ ] Any cross-functional friction I am avoiding instead of addressing?

### 4. Assertiveness & Communication Check (5 min)
- [ ] Did I push back or assert in any forum this week? Log it.
- [ ] Am I avoiding a conversation? If yes, schedule it today.
- [ ] Did I use Context → Ask → Owner → Deadline format in async messages this week?
- [ ] Did I give specific, constructive feedback to at least one person this week?

### 5. AI Check (5 min)
- [ ] Which team decision flows used AI this week?
- [ ] Which AI workflow lacks a decision owner, trace, exception trigger, or flow metric?
- [ ] Did AI reduce decision latency, validation queue depth, rework rate, defect leakage, error rate, or MTTR this week?

### 6. Career Check (5 min)
- [ ] Review `10_career/` — did I demonstrate any growth-target competency this week?
- [ ] Am I making progress on the current quarter's milestone?
- [ ] Any development goal still "Not started" that should have moved?
- [ ] Purpose alignment check: Is my effort this week aligned with my career trajectory, or just busy?

### 7. Plan Next Week (5 min)
- [ ] What are the 3 most important things to accomplish next week?
- [ ] What meeting this week requires preparation?
- [ ] What am I going to say "no" to this week?

### 8. Compliance Check (5 min)
- [ ] Any active compliance workstream past its deadline?
- [ ] Is the next compliance touchpoint scheduled? If not, schedule within 7 days.

### 9. Meeting Ingestion Check (2 min)
- [ ] Are all meetings from the past week ingested into their respective project/people files?
- [ ] Any meetings >48 hours old without extraction? Force extraction now.

## Output

After each weekly review, update:
- Any stale metrics
- This file's "Last Audit" date

## Escalation

If you skip the weekly review 2 weeks in a row: the brain is dying. Force a 1-hour deep review and reset.

## AI Integration

| Decision | AI role | Human owner | Evidence inputs | Pass/fail criteria | Trace | Exception trigger | Flow metric |
|----------|---------|-------------|-----------------|--------------------|-------|-------------------|-------------|
| What needs owner action in this weekly review? | recommend | [Brain Owner] | Project tracker, scorecards, people files, PRs, tickets, chat threads, CI/CD data, calendar, AI decision contracts | Review output names top actions with owner, deadline, escalation trigger, and source evidence | Weekly review notes | Missing owner, stale metric, or AI workflow without decision contract blocks closeout | Open action age and stale metric count |

Use AI to pre-generate the weekly review from source data. The brain owner reviews, annotates, and records decisions.

## Cross-References

- `07_operating_rhythms/mid_cycle_checkpoint_protocol.md` - mid-cycle review protocol.
- `07_operating_rhythms/quarterly_refactor_checklist.md` - quarterly governance audit.
- `07_operating_rhythms/one_on_one_protocol.md` - 1:1 cadence and prep.
