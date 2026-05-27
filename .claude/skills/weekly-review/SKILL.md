---
description: Monday weekly review. Scans all brain state, generates ranked topics, audits execution/metrics/people/career/compliance, and produces next-week plan with action items. Takes 30-45 min. Non-negotiable operating rhythm.
---

# Weekly Review

Scan full brain state, generate ranked topics, audit all operating domains, and produce next week's plan. This is your Monday operating rhythm. Without it, initiatives drift, metrics stale, and the brain decays.

Read `.claude/commands/_preamble.md` for shared constants (Notion DB IDs, Slack channel IDs, team roster path, GH CLI workaround).

**Runtime:** 30-45 minutes. Non-negotiable.

## Mode Routing (FIRST ACTION)

Pick the mode before loading any brain files. Most invocations are full Monday review. Other modes exist; do not collapse them into the default.

| Mode | Trigger | Scope | Time |
|------|---------|-------|------|
| **Full Monday review** | No argument, or `/weekly-review` on a Monday | All steps 0-10, all 9 core files, all 8 person files | 30-45 min |
| **Mid-week check-in** | `/weekly-review check-in` or invoked Tue-Fri | Steps 0, 1, 2 only (topics + execution + metrics). Skip people/career/compliance | 10-15 min |
| **Targeted topic** | `/weekly-review <topic>` (e.g., `metrics`, `people`, `career`) | Only the named step. Other steps skipped | 5-10 min |
| **Continuation** | `/weekly-review --continue` after prior run truncated | Resume from last completed step. Steps 7-9 if those were deferred | Varies |

Mode pick gates Phase A. Different modes load different sets of brain files. Picking the wrong mode wastes context window.

Pattern source: nilbuild/diffity tour skill, "pick a mode first" as the first instruction.

## Autonomy Model

| Action | Mode |
|--------|------|
| Read all brain files, query all MCP tools (Notion, Slack, Calendar, GitHub) | Autonomous |
| Scan metrics, score topics, generate scripts, flag gaps | Autonomous |
| Update brain files | Gated (show diff, wait for approval) |
| Draft external communications | Autonomous (never send) |
| Create calendar events, update Jira, post to Slack | Gated |

| Save weekly review to Notion | Autonomous (create automatically, report URL). Personal DB, only [Brain Owner] reads. Source: 2026-05-17 user correction "this type doesn't need to be gated, only myself is reading this notion page". |

**Context window note:** This command reads 15-20 brain files. If output quality degrades in later steps, defer Steps 7-9 to a follow-up invocation.

## Citation Discipline (MANDATORY for every step)

Apply the Citation Verification Protocol from `context/knowledge/citation-verification.md` before any number, status, ownership claim, or quote lands in the weekly review output. Every metric in Step 2, every 1:1 date in Step 3, every PR / Jira / Notion ID, every project status, every "X was decided" assertion gets the matching mechanical check. Three outcomes: VERIFIED (cite), WRONG (fix), UNVERIFIABLE (omit or label `"unverified, confirm at [moment]"`).

The "brain dashboards drift" problem (`contextual-rules.md` Evidence & Data Rules) is the highest-frequency failure mode here. The dashboard summary is read-only; the source is authoritative. Query the source.

## Phase A: Brain State Load

Read these 9 core files. They feed topic generation and multiple subsequent steps. Do not summarize - hold raw content for extraction across all steps.

1. `08_metrics/stability_metrics.md`
2. `08_metrics/ai_adoption_metrics.md`
3. `08_metrics/leadership_influence_metrics.md`
4. `12_projects/projects_tracker.md`
5. `09_people/team_roster.md`
6. `10_career/cto_trajectory.md`
7. `11_compliance_security/compliance_operational_model.md`
8. `02_leadership/assertiveness_playbook.md`
9. `10_career/executive_mentorship_tracker.md`

After reading, proceed to Phase A.5.

## Phase A.5: Recent Decisions Scan (2 min)

Run AFTER Phase A loads, BEFORE Step 0 generates topics. Catches reframes that invalidate scorecard rows downstream.

**Why:** Scorecard rows are dashboards; recent decision_log entries and Monthly Tracking entries are the truth. Brain files frequently carry a stale top-of-file row alongside a fresh tracking entry that reframes the metric. Topics built on the stale row are already wrong. Source: 2026-05-09 user correction after I proposed a "Phase 1 9 days overdue" R&D Leadership topic when Phase 1 was reframed 8 days earlier (2026-05-01).

**Method:**
1. Read `99_archive/decision_log.md`. Extract entries dated within the last 14 days.
2. For each Phase A metric file (`stability_metrics.md`, `ai_adoption_metrics.md`, `leadership_influence_metrics.md`), read the bottom 3 rows of every Monthly / Quarterly / Weekly Tracking table.
3. Cross-reference: any entry that changes a target, baseline, escalation trigger, or status becomes a "recent reframe."
4. List the corresponding stale lines (top-of-file scorecard rows that have not been updated to match the reframe).

**Output:**

```
## Phase A.5: Recent Decisions

### Reframes (last 14 days)
| Date | File | What Changed |
|------|------|-------------|
| YYYY-MM-DD | file.md | One-line summary |

### Stale Lines (do not cite as current truth in topic generation)
- file.md L_n scorecard row: superseded by [reframe date]
```

If 0 reframes detected: output "No reframes in last 14 days. Scorecard rows authoritative." and continue.

**Downstream impact:**
- **Step 0 Topic Generation:** topics MUST NOT cite a reframed metric as a problem unless the reframe itself is the topic. Topics built on stale baselines are auto-rejected.
- **Step 5 AI Check:** AI adoption tables read from the reframed instruments, not the original framing.
- **Step 8 Compliance Check:** compliance reframes (RoC date shifts, evidence deadline changes) override the original certification timeline row.
- **Final Health Dashboard:** status calls read reframed values, not stale rows.

## Step 0: Topic Generation (5 min)

Read these additional source files:
- `04_qa_brain/qa_coverage_framework.md`
- `04_qa_brain/qa_authority_model.md`
- `05_aps_brain/aps_metrics_model.md`
- `06_dev_support_brain/dev_support_operational_model.md`
- `02_leadership/visibility_plan.md`
- `02_leadership/performance_gap_enforcer.md`
- `10_career/development_goals_2026.md`
- `03_ai_native_transformation/ai_adoption_roadmap.md`
- `01_strategy/strategic_pillars.md`

Then:
1. Scan all loaded files for signals: wins, risks, stalls, approaching deadlines, escalation triggers hit
2. Generate 5 candidate topics
3. Score each on 4 dimensions per `07_operating_rhythms/topic_generation_protocol.md`:
   - Urgency (1-5): 5 = deadline within 7 days or escalation triggered / 3 = within 30 days / 1 = no pressure
   - Visibility (1-5): 5 = relevant to [Your CEO]/[Your CDO]/[Your CTO] / 3 = peers or broader engineering / 1 = internal only
   - Career Impact (1-5): 5 = directly closes a gap or demonstrates CTO competency / 3 = indirect / 1 = none
   - Pillar Alignment (1-5): 5 = Pillar 1 or 5 / 3 = Pillar 2, 3, or 4 / 1 = none
4. Select top 3. At least 1 must involve healthy friction. If there's a tie, prefer the friction topic.
5. For each selected topic, generate the full output:

```
TOPIC: [One sentence]
SCORE: [X/20]. Urgency [X] / Visibility [X] / Career [X] / Pillar [X]
FORUM: [Where to raise: R&D Leadership / [Your CTO] 1:1 / Slack / QA Sync / [Mobile Team] Replenishment]
FRAME:
  WHY: [Business impact in stakeholder language]
  WHAT: [Specific data or event]
  SO WHAT: [Implication]
  ASK: [Decision / alignment / awareness]
SCRIPT: [2-3 sentences in [Brain Owner]'s voice. Direct, data-backed, no hedging]
PUSHBACK PREP: [Anticipated objection + response]
```

**Meeting prep triggers:** Check Google Calendar (`gcal_list_events`) for this week:
- R&D Leadership meeting this week? Note 72-hour prep per `07_operating_rhythms/rnd_leadership_meeting_playbook.md`
- [Your CTO] 1:1 tomorrow? Generate the 1-1-1 (one metric, one risk, one recommendation) per `07_operating_rhythms/one_on_one_protocol.md`

**Eureka surfacing:** Read `context/knowledge/eureka-log.md` if it exists. Take the most recent 10 entries within the last 7 days. Each eureka is a candidate topic for R&D Leadership or [Your CTO] 1:1. If a eureka contradicts a current commitment or assumption tracked in `12_projects/projects_tracker.md`, set the topic's Visibility dimension to 5 (the dimension max per `07_operating_rhythms/topic_generation_protocol.md`) and add a `[EUREKA-CONTRADICT]` flag in the topic's frame. Use the flag as a tiebreaker when two topics score the same, not as a score modifier. Do not invent topics; eurekas augment, they do not replace, the topic generation logic.

Output:

```
## Step 0: Topics for This Week

### Selected Topics (3)

| # | Topic | Score | Forum | Friction? |
|---|-------|-------|-------|-----------|
| 1 | ... | X/20 | ... | Yes/No |
| 2 | ... | X/20 | ... | Yes/No |
| 3 | ... | X/20 | ... | Yes/No |

[Full TOPIC/SCORE/FORUM/FRAME/SCRIPT/PUSHBACK PREP for each]

### Meeting Prep Triggers
- R&D Leadership this week? [Yes/No, date]
- [Your CTO] 1:1 tomorrow? [Yes/No, date]
```

## Step 0a: Engineering Activity Quant (5 min)

Pulls hard numbers on team shipping behavior. Surfaces patterns that the qualitative person-check (Step 3) misses.

**Scope:** the 3 teams [Brain Owner] leads (QA, [Mobile Team], Dev Support).

**Configuration prerequisite:** requires a `repos:` block in `config/team.yaml` mapping each team to its primary application repo(s) (e.g., `qa: [your-company]-web-ordering-tests`, `mobile_team: [[your-company]-[mobile-app], [your-company]-branded-apps]`, `dev_support: [your-company]-[engineering-toolkit]`). If `repos:` is absent or empty, emit ONE warning row in the output ("CONFIG MISSING: add `repos:` to config/team.yaml; Step 0a skipped this run") and skip the rest of this step. Do NOT silently skip.

**Repo path resolution:** the brain operates against local clones at `~/Development/<repo>` per CLAUDE.md. For each repo name `<repo>` from team.yaml, resolve to `~/Development/<repo>`. If the directory does not exist, emit a warning row and skip that repo.

**Source:** gstack `/retro` quantitative metrics, ported and reduced for an EM (not solo-builder) context 2026-05-08.

**Stale-origin detection (mandatory):** for each repo, before running the window queries, check the age of the local origin-tracking branch via `git -C "$REPO" log -1 --format=%ar origin/$DEFAULT`. If the most recent origin commit is older than 2 days AND the window returns 0 commits, origin tracking is stale, not the repo. Two paths:

- **Surface-and-skip (fallback):** emit a warning row `STALE ORIGIN: <repo> last fetch >N days ago, window returned 0 commits. Skipping. Run \`git fetch\` in \`~/Development/<repo>\` before next session.`

Never silently report 0s. Source: 2026-05-09 weekly review run silently returned 0s for QA/[Mobile Team]/Dev Support after a stale-origin condition; team activity data went missing without anyone noticing until the user asked.

For each resolved repo path, run:

```bash
REPO="$HOME/Development/<repo>"
DEFAULT=$(GH_TOKEN="" gh -R [your-company]/<repo> repo view --json defaultBranchRef --jq .defaultBranchRef.name)

# 1. Total commits this window
TOTAL=$(git -C "$REPO" log "origin/$DEFAULT" --since="7 days ago" --oneline | wc -l | tr -d ' ')

# 2. AI-assisted commit count (Co-Authored-By: Claude trailer)
AI=$(git -C "$REPO" log "origin/$DEFAULT" --since="7 days ago" --grep="Co-Authored-By: Claude" --oneline | wc -l | tr -d ' ')

# 3. AI ratio = AI / TOTAL (guard against div-by-zero)
[ "$TOTAL" -gt 0 ] && AI_PCT=$(( AI * 100 / TOTAL )) || AI_PCT=0

# 4. Fix-prefix commits
FIX=$(git -C "$REPO" log "origin/$DEFAULT" --since="7 days ago" --format="%s" | grep -cE '^fix(\(|:)')
[ "$TOTAL" -gt 0 ] && FIX_PCT=$(( FIX * 100 / TOTAL )) || FIX_PCT=0

# 5. Per-author commit counts
git -C "$REPO" log "origin/$DEFAULT" --since="7 days ago" --format="%aN" | sort | uniq -c | sort -rn

# 6. Per-author insertions/deletions (aggregate --shortstat output)
git -C "$REPO" log "origin/$DEFAULT" --since="7 days ago" --format="AUTHOR:%aN" --shortstat | \
  awk '/^AUTHOR:/ {a=substr($0,8); next} /files? changed/ {for(i=1;i<=NF;i++){if($i~/insertion/)ins[a]+=$(i-1); if($i~/deletion/)del[a]+=$(i-1)}} END {for(a in ins) print a"|"ins[a]"|"del[a]}'

# 7. Top-level directory focus (% commits touching the single most-changed top-level dir)
git -C "$REPO" log "origin/$DEFAULT" --since="7 days ago" --format="" --name-only | \
  awk -F/ 'NF>0 {print $1}' | sort | uniq -c | sort -rn | head -1

# 8. Hotspot files (5+ touches)
git -C "$REPO" log "origin/$DEFAULT" --since="7 days ago" --format="" --name-only | \
  grep -v '^$' | sort | uniq -c | sort -rn | awk '$1 >= 5'

# 9. Shipping streak (consecutive days with >= 1 commit going back from today)
git -C "$REPO" log "origin/$DEFAULT" --format="%ad" --date=format:"%Y-%m-%d" | sort -u

# 10. Ship of the week (highest-LOC merged PR; requires gh)
GH_TOKEN="" gh -R [your-company]/<repo> pr list --state merged --search "merged:>=$(date -v-7d +%Y-%m-%d)" \
  --json number,title,additions,deletions,author --jq 'sort_by(.additions + .deletions) | reverse | .[0]'
```

**Compute these metrics per team (sum across repos if multiple):**

| Metric | Definition | Signal |
|--------|------------|--------|
| Commits | total to default branch | volume |
| Logical contributors | unique authors with >= 1 commit | participation |
| Fix ratio | `fix(`-prefix or `fix:` commits / total | >50% = review-gap signal |
| AI-assisted ratio | commits with `Co-Authored-By: Claude` trailer / total | feeds AI Adoption Step 5 |
| Focus score | % commits touching the single most-changed top-level dir | <30% = scattered context-switching |
| Ship of the week | highest-(additions+deletions) PR merged this window | named win to surface |
| Hotspot count | files touched 5+ times | churn risk |
| Shipping streak | consecutive days with >= 1 commit | momentum |

**Per-author leaderboard (current user always first if present):**

```
Contributor       Commits  +/-          Top area              AI%
You ([your-github-handle])          N   +X/-Y        path/                 Z%
<teammate-1>           N   +X/-Y        path/                 Z%
```

**Week-over-week deltas:** if a prior week's snapshot exists at `08_metrics/engineering_activity_history.jsonl`, load it and show:

```
                  Last week   This week    Delta
Commits:               N    →    N         ↑/↓
Fix ratio:             X%   →    Y%        ↑/↓
AI-assisted ratio:     X%   →    Y%        ↑/↓
Logical contributors:  N    →    N         ↑/↓
```

**Save snapshot:** append a JSON line to `08_metrics/engineering_activity_history.jsonl`. Schema:

```json
{"date":"YYYY-MM-DD","window":"7d","team":"<team-name>","repo":"<repo>","commits":N,"contributors":N,"fix_ratio":0.NN,"ai_ratio":0.NN,"focus_dir":"path/","focus_pct":0.NN,"hotspots":N,"streak":N,"ship_of_week":{"pr":"<repo>#<num>","title":"...","loc":N}}
```

If `08_metrics/engineering_activity_history.jsonl` does not exist, create it without a header (raw JSONL) AND create a sibling `08_metrics/engineering_activity_history.md` governance descriptor with Owner / Pillar / Measurable Outcome / Escalation Trigger pointing at the JSONL as the data file.

Output:

```
## Step 0a: Engineering Activity Quant

| Team | Commits | Contributors | Fix ratio | AI% | Focus | Streak |
|------|---------|--------------|-----------|-----|-------|--------|
| QA | N | M | X% | Y% | path/ Z% | N days |
| [Mobile Team] | N | M | X% | Y% | path/ Z% | N days |
| Dev Support | N | M | X% | Y% | path/ Z% | N days |

### Ship of the Week
- **<repo>#<PR>**: <title> by <author>. <one phrase on why it matters>

### Quant Signals

(Emit each line ONLY if its condition is true. Do not emit literal "[If ...]" text.)

- For any team with `fix_ratio > 0.5`: emit "<team> fix ratio <X%>. Review-gap signal. Either reviews missed bugs or the team is firefighting. Investigate with the team lead in 1:1."
- For any team with `focus_pct < 0.3`: emit "<team> focus score <X%>. Context-switching above tolerance. Check WIP limits."
- For any team where AI ratio dropped >=5pp WoW: emit "<team> AI-assisted ratio dropped <X pp> WoW. Counter to AI execution pillar. Surface as topic candidate."
- For any file with `>= 5` touches in window: emit "<file> touched <N> times. Churn risk. Consider refactor scope."

### Action Items from Step 0a
- [ ] ...
```

**Feeds Step 5 (AI Check):** AI-assisted ratio per team feeds the Team AI Usage table. Step 5 references Step 0a numbers; do not double-count.

**Feeds Step 2 (Metric Check):** if `08_metrics/engineering_delivery_metrics.md` is stale (>30 days), use Step 0a data to propose a refresh.

## Step 1: Execution Check (10 min)

Data sources:
- `12_projects/projects_tracker.md` (already loaded)
- GitHub PRs via shell: `GH_TOKEN="" gh search prs --author=[your-github-handle] --state=open --json number,title,url,repository,createdAt,updatedAt` (GH CLI workaround per `_preamble.md`)
- Notion Initiatives DB via `mcp__claude_ai_Notion__notion-fetch` (ID per `_preamble.md`)
- `12_projects/initiatives_database.md` for sync rules

Checks:
1. Scan `projects_tracker.md` for any project with no activity in 21+ days
2. List all open GitHub PRs with days-open. Flag any >14 days.
3. Compare brain initiatives (from `01_strategy/strategic_pillars.md`) vs Notion DB entries. Flag discrepancies in both directions: brain-only (invisible to team) and Notion-only (unaccountable).
4. Any initiative stuck in "conceptual" for >14 days? Either add an execution plan or recommend killing it.

Output:

```
## Step 1: Execution Check

### Project Staleness
| Project | Last Activity | Days Since | Status |
|---------|--------------|------------|--------|
| ... | ... | ... | OK / STALE / ACTION NEEDED |

### Open PRs ([N] total)
| PR | Repo | Days Open | Status |
|----|------|-----------|--------|
| ... | ... | ... | OK / STALE (>14d) |

### Brain-Notion Sync
| Initiative | In Brain? | In Notion? | Discrepancy |
|-----------|-----------|-----------|-------------|
| ... | Yes/No | Yes/No | ... |

### Action Items from Step 1
- [ ] ...
```

## Step 2: Metric Check (10 min)

Read additionally: `08_metrics/engineering_delivery_metrics.md`

Checks:
1. Status each metric domain as GREEN / YELLOW / RED based on current values vs targets
2. Stability: any incidents, MTTR spikes, release failures?
3. AI Adoption: any team with zero usage?
4. QA Coverage: defect leakage trending up?
5. Compliance: any certification deadline within 30 days without evidence of readiness?
6. Staleness audit: any metric file not updated in 30+ days?

Output:

```
## Step 2: Metric Check

### Metric Health
| Domain | Status | Key Finding | Last Updated | Stale? |
|--------|--------|------------|--------------|--------|
| Stability | GREEN/YELLOW/RED | ... | YYYY-MM-DD | Yes/No |
| AI Adoption | GREEN/YELLOW/RED | ... | YYYY-MM-DD | Yes/No |
| QA Coverage | GREEN/YELLOW/RED | ... | YYYY-MM-DD | Yes/No |
| Eng Delivery | GREEN/YELLOW/RED | ... | YYYY-MM-DD | Yes/No |
| Leadership Influence | GREEN/YELLOW/RED | ... | YYYY-MM-DD | Yes/No |
| Compliance | GREEN/YELLOW/RED | ... | YYYY-MM-DD | Yes/No |

### Action Items from Step 2
- [ ] ...
```

## Step 3: People Check (10 min)

Read additionally:
- All 8 person files: `09_people/{report1,report2,...}.md`
- `09_people/talent_review_tracker.md`
- `02_leadership/stakeholder_map.md`

Checks:
1. 1:1 staleness: anyone without a 1:1 in 21 days? (Respect active pause overrides if documented.)
2. Growth goals: any stale goals (no progress in 30 days)?
3. Delegation maturity: any stalled delegation? Apply [Coaching Framework] Principle 4: "If I disappeared for 2 weeks, would my teams operate?"
4. Talent reviews: all complete? Cross-check each person's `## Talent Review Status` section in their person file. Do NOT flag a talent review as missing unless the person file confirms it is incomplete. The person file is the source of truth, not Notion alone.
5. Stakeholder engagement: anyone in stakeholder map not engaged in 30+ days?
6. Blocked reports: anyone waiting on [Brain Owner] to clear a path?
7. Cross-functional friction: any being avoided?

Output:

```
## Step 3: People Check

### 1:1 Status (8 reports)
| Name | Team | Last 1:1 | Days Since | Status |
|------|------|----------|------------|--------|
| ... | ... | ... | ... | OK / OVERDUE / OVERRIDE |

### Growth Goal Status
| Name | Goal | Status | Days Since Progress |
|------|------|--------|-------------------|
| ... | ... | ... | ... |

### Delegation Maturity
| Name | Current Level | Movement This Week? |
|------|--------------|-------------------|
| ... | ... | Yes/No/Stalled |

### Stakeholder Engagement
| Stakeholder | Last Engaged | Days Since | Status |
|-------------|-------------|------------|--------|
| ... | ... | ... | OK / GAP (>30d) |

### Action Items from Step 3
- [ ] ...
```

## Step 3b: Delegation Readiness Test (3 min)

Uses the same person files already loaded in Step 3. Apply [Coaching Framework] Principle 4: "If I disappeared for 2 weeks, would my teams operate?"

### 3b-1. Per-team assessment

For each team (QA, [Mobile Team], Dev Support), assess 4 criteria by scanning person files and team brain files:

| Criterion | How to Check | Dependent Signal |
|-----------|-------------|-----------------|
| **Standup autonomy** | Does the team run their sync without [Brain Owner]? Check calendar: is [Brain Owner] an optional attendee? Do action items flow without his presence? | Team cannot run standup → Dependent |
| **Decision bottleneck** | Scan person files for action items where Owner = [Brain Owner] or blocked on [Brain Owner]. Count items. | 3+ items blocked on [Brain Owner] → Dependent |
| **Growth goal coverage** | Does every team member have at least 1 active growth goal in their person file? | Any member with 0 goals → Developing (not investing in autonomy) |
| **Escalation pattern** | Has the same type of issue been escalated to [Brain Owner] 3+ times by the same team? Check 1:1 logs for repeated escalation topics. | Same escalation 3x → Dependent ([Brain Owner] is the crutch, not the coach) |

### 3b-2. Score each team

| Score | Definition |
|-------|-----------|
| **Autonomous** | All 4 criteria pass. Team operates independently. [Brain Owner] adds strategic value, not operational. |
| **Developing** | 1-2 criteria fail. Team mostly operates but has gaps. Specific coaching actions needed. |
| **Dependent** | 3-4 criteria fail. Team relies on [Brain Owner] for daily operations. Structural change needed. |

### 3b-3. Output

```
## Step 3b: Delegation Readiness Test

### Team Delegation Scores
| Team | Standup | Decisions | Goals | Escalation | Score | Trend |
|------|---------|-----------|-------|-----------|-------|-------|
| QA | Pass/Fail | [N] blocked | [N]/2 with goals | [pattern or none] | Autonomous/Developing/Dependent | ↑/→/↓ vs last week |
| [Mobile Team] | Pass/Fail | [N] blocked | [N]/4 with goals | [pattern or none] | Autonomous/Developing/Dependent | ↑/→/↓ vs last week |
| Dev Support | Pass/Fail | [N] blocked | [N]/2 with goals | [pattern or none] | Autonomous/Developing/Dependent | ↑/→/↓ vs last week |

### Bottleneck Items (blocked on [Brain Owner])
| Person | Item | Days Waiting |
|--------|------|-------------|
| ... | ... | ... |

### Escalation Patterns (3+ repeats)
| Team | Escalation Type | Count | Fix |
|------|----------------|-------|-----|
| ... | ... | ... | [coaching action or structural fix] |
```

**Escalation rule:** If any team scores "Dependent" for 2 consecutive weeks, generate an explicit intervention plan:
1. Which criteria failed and why
2. What specific delegation move (per [Coaching Framework] Principle 2: Guided → Task → Result → Autonomous) to make this week
3. Who owns the move ([Brain Owner] or team lead)
4. By when the team should reach "Developing"

## Step 4: Assertiveness & Communication (5 min)

Checks:
1. Review `02_leadership/assertiveness_playbook.md` influence tracker: any entries logged this week?
2. Did QA exercise authority this week? Check `04_qa_brain/qa_authority_model.md` for block events.
3. Check person files for recent Performance Observations entries: did I give specific feedback to at least one person this week?
4. Did I use Context - Ask - Owner - Deadline format in async messages? (Dev Goal 3)
5. Am I avoiding a conversation? Present as a self-assessment question.

Output:

```
## Step 4: Assertiveness & Communication

### This Week's Assertions
| Date | Forum | What Asserted | Outcome |
|------|-------|---------------|---------|
| ... | ... | ... | ... |
(If empty: "No assertions logged this week. Gap 3 is not closing.")

### QA Authority Events
- Blocks exercised: [count]
- Latest: [description or "None"]

### Feedback Given
- Specific feedback delivered this week: [Yes/No]. To whom: [name]

### Self-Assessment
- Am I avoiding a conversation right now? [Present this as a prompt for [Brain Owner] to answer]

### Action Items from Step 4
- [ ] ...
```

## Step 5: AI Check (5 min)

Optionally read Slack #ai-show-and-tell (channel ID per `_preamble.md`) via `slack_read_channel` for recent team activity.

**AI-assisted ratio comes from Step 0a.** Pull the per-team `ai_ratio` numbers computed in Engineering Activity Quant; do NOT recompute. Reference Step 0a explicitly in the output table.

Checks:
1. Are teams using their AI workflows this week? Cross-reference Step 0a AI ratio + `ai_adoption_metrics.md` + Slack signals.
2. Any new AI opportunity identified this week?
3. Did [Brain Owner] use AI in his own work this week? (This weekly review counts.)

Output:

```
## Step 5: AI Check

### Team AI Usage
| Team | Activity This Week | Status |
|------|-------------------|--------|
| QA | ... | Active/Inactive |
| [Mobile Team] | ... | Active/Inactive |
| Dev Support | ... | Active/Inactive |

### New Opportunities
- [any new AI opportunities identified]

### Self-Usage
- [Brain Owner]'s AI usage this week: [description]

### Action Items from Step 5
- [ ] ...
```

## Step 6: Career Check (5 min)

Checks:
1. Did I demonstrate any CTO competency this week? Map evidence to gaps from `cto_trajectory.md`.
2. Am I making progress on the current quarter's milestone?
3. Review `10_career/development_goals_2026.md`: any goal still "Not started" that should have moved?
4. Review mentorship commitments in `executive_mentorship_tracker.md`: any overdue action plans? Any insights with "Applied? No" for >30 days?
5. **Query Goals Tracker DB live (mandatory).** Do NOT cite the static habit-rep snapshot in `executive_mentorship_tracker.md` (e.g., "Future-value 13/21" from 2026-05-01 triage); that snapshot decays daily as new reps log. Instead, run `mcp__claude_ai_Notion__notion-query-database-view` against the canonical view URL `https://www.notion.so/31aa84ed402480a597acced6ccf8c8da?v=31aa84ed402480df9b96000c48f9e2b9` (All Goals view, data source `31aa84ed-4024-80dd-b9a9-000bb3868086`), filter for `Goal name` containing `Habit:`, read live `Start value` per row. `notion-query-database-view` requires a view URL (with `?v=`), not a bare data source ID; if the canonical URL ever returns 400, recover by running `notion-fetch` on the DB ID first and reading the live view URL from the schema. Threshold check: flag if <7x after 2 weeks from creation, <21x after 4 weeks. If the MCP call fails or rate-limits, fall back to the static snapshot but label it explicitly in the output: `"DB unavailable, citing YYYY-MM-DD snapshot (may be N days stale)"`. Source: 2026-05-09 weekly review cited 8-day-old static numbers as if current. 2026-05-24 run guessed a view URL and got 400. Step 6b enforcement scoring depends on accurate reps; stale numbers produce wrong YELLOW/RED calls.
6. **Retrospective habit scan:** Review this week's meeting scripts and Slack activity (from `.context/slack-triage-latest.md` if available) for habit evidence missed by real-time detection. The 4 habits: Reframe limiting beliefs, Future-value framing, Circle of Influence filter, Proactive response choice. For each newly detected instance, log to the matching `Habit:` page in Goals Tracker DB (fetch page → append repetition log row → bump Start value). Report newly logged instances in output.
7. Purpose alignment: was this week's effort aligned with CTO trajectory purpose, or reactive drift?
8. Obstinacao vs. Teimosia: any stalled initiative trying the same failed approach twice? If yes, force alternative path within 7 days.

Output:

```
## Step 6: Career Check

### CTO Competency Evidence This Week
| Competency | Evidence | Gap Status |
|-----------|----------|------------|
| ... | ... | Advancing/Stalled/No evidence |

### Quarterly Milestone
- Current quarter: [Q]
- Milestone: [from cto_trajectory.md]
- Status: On track / At risk / Behind

### Development Goals
| Goal | Status | Last Progress |
|------|--------|--------------|
| AI-native adoption | ... | ... |
| QA as influential voice | ... | ... |
| Communicate with directness | ... | ... |

### Mentorship Commitment Status
| # | Action/Insight | Status | Days Overdue |
|---|---------------|--------|-------------|
| ... | ... | On track / OVERDUE | ... |

### Habit Repetition Progress (Goals Tracker DB)
| Habit | Reps | Target | Weeks Active | Status |
|-------|------|--------|-------------|--------|
| Reframe limiting beliefs | [Start value]/21 | 7x by week 2, 21x by week 4 | [weeks since 2026-03-07] | On track / BEHIND |
| Future-value framing | ... | ... | ... | ... |
| Circle of Influence filter | ... | ... | ... | ... |
| Proactive response choice | ... | ... | ... | ... |

### Purpose Alignment
- This week's effort alignment with CTO trajectory: [Aligned / Partially / Drifted]
- If drifted: [What consumed effort that wasn't purpose-aligned?]
- Obstinacao check: [Any stalled initiative trying same approach twice?]

### Action Items from Step 6
- [ ] ...
```

## Step 6a: Insight Application Check (3 min)

Read `10_career/ai_engineering_book.md` and `10_career/executive_mentorship_tracker.md` (already loaded in Phase A for mentorship tracker).

1. **Flag overdue action plans** (>14 days past deadline): hard fail, surface as urgency 5 topic for Step 0
2. **Cross-reference unapplied insights against next week's calendar.** For each unapplied insight, check if next week has a meeting that touches its domain:
   - AI Engineering insights (evaluation, monitoring, context engineering) → R&D Leadership, [Your CTO] 1:1, AI-related meetings
   - [Coaching Framework] insights (assertiveness, delegation, purpose) → any 1:1, R&D Leadership
3. **Present practice targets:**

```
### This Week's Practice Targets (from book trackers)

| # | Insight | Source | Practice Opportunity (Meeting) | Date |
|---|---------|--------|-------------------------------|------|
| 1 | [insight summary] | AI Engineering Ch.3 | R&D Leadership | 2026-03-24 |
| 2 | [insight summary] | [Coaching Framework] Module 1 | [Your CTO] 1:1 | 2026-03-25 |
```

If no matching meetings: "No practice opportunities this week. Pick 1 insight to apply in async communication instead."

## Step 6b: Mentorship Enforcement (2 min)

Data source: `10_career/executive_mentorship_tracker.md` (already loaded in Phase A).

### 6b-1. Count overdue items

From the Insights table (Section 1):
- Count insights with "Applied? No" column
- For each, compute days since module completion date

From the Action Plans table (Section 2):
- Count action plans where Deadline < today AND Status != Done

### 6b-2. Apply escalation thresholds

| Threshold | Condition | Flag |
|-----------|-----------|------|
| Action plan overload | 3+ action plans overdue >14 days | RED. Urgency 5 topic for Step 0 |
| Consumption trap | 50%+ insights with "Applied? No" after 60 days from module completion | RED. Force behavior audit session |
| Ingestion stall | 0 new modules ingested in 30+ days (check Module Log table dates) | YELLOW. "Mentorship commitment is stalling" |
| Habit stall | Any habit in Goals Tracker DB with <7 reps after 2 weeks from creation | YELLOW. Habit not practicing |

### 6b-3. Generate health score

```
## Step 6b: Mentorship Enforcement

### Mentorship Health: [GREEN / YELLOW / RED]

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Insights unapplied | [X]/[total] ([%]) | <50% after 60d | GREEN/YELLOW/RED |
| Action plans overdue >14d | [X] | <3 | GREEN/RED |
| Days since last module ingestion | [X] | <30 | GREEN/YELLOW |
| Habit reps on track | [X]/4 habits | All on schedule | GREEN/YELLOW |

### Overdue Action Plans
| # | Action | Deadline | Days Overdue |
|---|--------|----------|-------------|
| 1 | ... | ... | ... |

### Unapplied Insights (oldest first)
| # | Insight | Module | Days Since Module | Behavior Change Required |
|---|---------|--------|------------------|------------------------|
| 1 | ... | 0 | ... | ... |

### Enforcement Actions
- [If RED: "ESCALATION: Add mentorship enforcement as urgency 5 topic in Step 0. Schedule 30-min behavior audit this week."]
- [If YELLOW: "WARNING: Mentorship momentum declining. Pick 1 insight to apply this week."]
- [If GREEN: "On track."]
```

**Rule from tracker:** "Conhecimento que não é colocado em prática não serve para nada." If 3+ action plans are overdue, this step MUST produce an explicit remediation plan, not just a flag.

## Step 7: Plan Next Week (5 min)

Check Google Calendar (`gcal_list_events`) for next week's meetings.

Process:
1. Synthesize the top 3 priorities from all findings in Steps 0-6
2. Identify meetings requiring preparation (load relevant playbook references)
3. Identify what to say "no" to (based on overcommitment signals from execution check)

Output:

```
## Step 7: Plan Next Week

### Top 3 Priorities
| # | Priority | Source | Deadline |
|---|----------|--------|----------|
| 1 | ... | Step X finding | ... |
| 2 | ... | Step X finding | ... |
| 3 | ... | Step X finding | ... |

### Meeting Prep Needed
| Meeting | Date | Prep Required | Playbook |
|---------|------|--------------|----------|
| ... | ... | ... | ... |

### Say No To
- [Things to decline or defer this week]
```

## Step 8: Compliance Check (5 min)

Checks:
1. Any active workstream past its deadline in `compliance_operational_model.md`?
2. Is the next compliance team meeting scheduled? Check Google Calendar. If not scheduled: flag.
3. Any Bridge Letter or audit action items due this week?
4. Any compliance-related decision made but not logged in `99_archive/decision_log.md`?

Output:

```
## Step 8: Compliance Check

### Active Workstreams
| Workstream | Owner | Deadline | Status |
|-----------|-------|----------|--------|
| ... | ... | ... | On track / OVERDUE / At risk |

### Compliance Meeting Cadence
- Last meeting: [date]
- Next scheduled: [date or "NOT SCHEDULED"]
- Status: OK / OVERDUE (>21 days since last)

### Action Items from Step 8
- [ ] ...
```

## Step 9: Meeting Ingestion Check (2 min)

Data sources:
- Google Calendar (`gcal_list_events`) for past week's meetings
- Notion Meeting Transcripts DB (ID per `_preamble.md`) via `mcp__claude_ai_Notion__notion-search` or `notion-fetch`
- `07_operating_rhythms/meeting_ingestion_protocol.md` for cadence rules (24h for 1:1s and leadership, 48h for all others)

Checks:
1. List past week's meetings from calendar
2. Check which have transcripts in Notion
3. Flag any meeting >48 hours old without extraction

Output:

```
## Step 9: Meeting Ingestion Check

### Past Week's Meetings
| Meeting | Date | Type | Ingested? | Hours Since |
|---------|------|------|----------|-------------|
| ... | ... | ... | Yes/No | ... |

### Overdue (>48h without ingestion)
| Meeting | Date | Hours Overdue |
|---------|------|--------------|
| ... | ... | ... |

### Action Items from Step 9
- [ ] Force extraction for overdue meetings
```

## Step 10: Brain Maintenance Cadence (1 min)

Check when `/brain-audit` and `/dream` were last run. These are the brain's garbage collector and integrity scanner. Without periodic runs, contradictions accumulate and memory bloats.

**Method:**
1. `git log --all --oneline --grep="Brain Audit Report" --since="90 days ago"` — find last brain-audit commit
2. `git log --all --oneline --grep="/dream" --since="90 days ago"` — find last dream commit
3. Parse `memory/MEMORY.md` line count (budget: 150)
4. Count memory files: `ls memory/*.md | wc -l`

**Cadence thresholds:**

| Command | GREEN | YELLOW | RED |
|---------|-------|--------|-----|
| `/brain-audit` | Run within 30 days | 31-60 days ago | >60 days or never |
| `/dream` | Run within 30 days | 31-60 days ago | >60 days or never |
| MEMORY.md lines | <120 | 120-149 | 150+ (hard limit) |

```
## Step 10: Brain Maintenance Cadence

| Command | Last Run | Days Since | Status |
|---------|----------|------------|--------|
| /brain-audit | YYYY-MM-DD | [N] | GREEN/YELLOW/RED |
| /dream | YYYY-MM-DD | [N] | GREEN/YELLOW/RED |

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| MEMORY.md lines | [N] | 150 max | GREEN/YELLOW/RED |
| Memory files | [N] | — | Info |

### Maintenance Actions
- [If `/brain-audit` is RED: **HALT THE REVIEW**. Output: `"BLOCKING: /brain-audit overdue (>60 days). Run /brain-audit before continuing the weekly review. Re-invoke /weekly-review after the audit lands. Reason: governance contradictions accumulate silently when audit cadence slips. Same enforcement pattern as the pre-merge self-review rule in CLAUDE.md."` Stop the review. Do NOT proceed to Self-Check or Final Output.]
- [If `/dream` is RED: "RUN NOW: `/dream` overdue. Schedule in this session or next."]
- [If YELLOW: "Due soon. Schedule `/brain-audit` or `/dream` within the next 2 weeks."]
- [If all GREEN: "Brain maintenance on track."]
```

**Why blocking on `/brain-audit` RED:** 2026-05-09 weekly review flagged /brain-audit as RED (>120 days since last run) and proceeded anyway. The audit eventually ran but only because the user prompted explicitly. Blocking gate matches the pre-merge self-review enforcement pattern: governance moves from suggestion to mandatory.

## Self-Check (before presenting Final Output)

Verify each assertion. If any fails, fix or flag explicitly in the report.

- [ ] All 9 core files from Phase A were loaded (not skipped due to read failure without noting gap)
- [ ] 3 topics generated with scores; at least 1 involves healthy friction
- [ ] Each health domain rated GREEN/YELLOW/RED with specific evidence (not guessed)
- [ ] All 8 direct reports checked for 1:1 staleness
- [ ] Metric staleness audit completed (flagged any file not updated in 30+ days)
- [ ] Calendar checked for next week's meetings requiring prep
- [ ] Total action items > 0 (0 items = review too shallow or brain stale)
- [ ] Brain maintenance cadence checked (Step 10) — /brain-audit and /dream staleness surfaced
- [ ] No brain file was updated without showing the diff and getting approval first

## Final Output: Weekly Review Report

After all steps, produce a consolidated summary:

```
## Weekly Review Report. [Date]

### Health Dashboard Thresholds

| Domain | GREEN | YELLOW | RED |
|--------|-------|--------|-----|
| Execution | No project stale >21d, no PR >14d | 1 stale project or 1 stale PR | 2+ stale projects or conceptual >14d |
| Metrics | All metric files updated <30d | 1 metric file >30d stale | 2+ metric files stale or key metric trending wrong |
| People | All 1:1s <21d, all goals progressing | 1 overdue 1:1 or 1 stalled goal | 2+ overdue 1:1s or blocked report |
| Assertiveness | 1+ assertion logged this week | 0 assertions but QA blocked something | 0 assertions and no QA authority events |
| AI Adoption | All teams active this week | 1 team inactive | 2+ teams inactive or 0 [Brain Owner] AI usage |
| Career | Evidence mapped to gap this week | Milestone on track but no evidence | Milestone at risk or dev goal stalled |
| Compliance | All workstreams on track | 1 workstream approaching deadline | Overdue workstream or missed meeting cadence |

| Meeting Ingestion | All meetings ingested within threshold | 1 meeting overdue | 2+ meetings >48h without ingestion |
| Brain Maintenance | /brain-audit + /dream run <30d ago | 31-60 days ago | >60 days or never |

### Health Dashboard
| Domain | Status | Key Finding |
|--------|--------|------------|
| Execution | GREEN/YELLOW/RED | ... |
| Metrics | GREEN/YELLOW/RED | ... |
| People | GREEN/YELLOW/RED | ... |
| Assertiveness | GREEN/YELLOW/RED | ... |
| AI Adoption | GREEN/YELLOW/RED | ... |
| Career | GREEN/YELLOW/RED | ... |
| Compliance | GREEN/YELLOW/RED | ... |
| Meeting Ingestion | GREEN/YELLOW/RED | ... |
| Brain Maintenance | GREEN/YELLOW/RED | ... |

### Topics for This Week
1. [topic]. [forum]. [score]/20
2. [topic]. [forum]. [score]/20
3. [topic]. [forum]. [score]/20

### Next Week's Priorities
1. ...
2. ...
3. ...

### All Action Items ([N] total)
| # | Action | Source | Owner | Deadline |
|---|--------|--------|-------|----------|
| 1 | ... | Step X | ... | ... |
| ... | ... | ... | ... | ... |

### Say No To
- ...

### Things to Surface to [Your CTO] (next 1:1)

Outward-pointing block. Items the weekly review surfaced that [Your CTO] should know about but that did NOT make it into Step 0's top-3 topics. Examples: a non-obvious tradeoff in a technical decision, a defensive choice worth flagging, a stakeholder dynamic [Your CTO] may not have visibility into, a stale assumption in a prior commitment, a metric trend that is too early to be a topic but worth watching together.

If nothing surfaces, write `None this week.` Do not omit the block. The weekly review is the operating rhythm; pointing outward is part of its job.

Pattern source: nilbuild/diffity tour skill, "things to flag in PR conversation" as the highest-value artifact step.
```

## Post-Review: Update Brain Files

Present all proposed brain file updates for approval:

1. Update `07_operating_rhythms/weekly_review.md` header: set "Last Audit" to today's date
2. Route action items to relevant brain files (list each target file and change)
3. Update stale metric files if data was gathered
4. Add assertiveness entries if surfaced
5. Log evidence to `10_career/review_cycle_evidence.md` if career-relevant findings emerged

**Format:** Show each proposed update as a numbered list with target file and change description. Wait for explicit approval before applying. ("Apply all? Or specify numbers.")

## Post-Review: Save to Notion

After generating the final report and proposing brain file updates, save the review to Notion:

1. Create a page in "[Brain Owner]'s Weekly Reviews" database (ID per `_preamble.md`) using `mcp__claude_ai_Notion__notion-create-pages`
2. **Page name:** "Weekly Review - [Date]"
   - **Icon:** Derive from the Health Dashboard. Count RED/YELLOW/GREEN domains:
     - Majority GREEN (0-1 RED) → `"icon": "🟢"`
     - Mixed (2-3 RED or majority YELLOW) → `"icon": "🟡"`
     - Majority RED (4+ RED) → `"icon": "🔴"`
     - Default if unsure → `"icon": "🟠"`
   - This is mandatory — do not omit the icon.
3. **Content:** The full Weekly Review Report (Health Dashboard, Topics, Priorities, All Action Items, Say No To) plus the proposed brain file updates list
4. Do NOT include the detailed step-by-step outputs (Steps 0-9) in Notion - only the consolidated Final Output section and proposed updates. The full detail lives in the brain commit.
5. **Strip brain-internal paths from the Notion content before creating the page.** No `00_foundation/...`, `01_strategy/...`, `02_leadership/...`, `08_metrics/...`, `09_people/...`, `10_career/...`, `11_compliance_security/...`, `12_projects/...`, `13_infrastructure/...`, `99_archive/...`, `context/...`, `.claude/...`, `CLAUDE.md`, `AGENTS.md` paths. Replace with the substance directly (e.g., write "PCI evidence" not "compliance_operational_model.md", write "the assertiveness tracker" not "02_leadership/assertiveness_playbook.md"). Brain file commit SHAs and external IDs (Notion page IDs, Jira keys, PR URLs) are fine. Source: 2026-05-09 Notion create call to `35ca84ed-4024-81e4-a1ab-d8b51d0be432` was blocked by `check-brain-paths.sh` hook on first attempt because the "Brain Updates Applied This Session" + "Key Patterns Captured" sections embedded paths. Hook caught it (working as designed); skill should catch it first.
6. This is an AUTONOMOUS action - create the page and report the URL. Do not ask for approval. Personal DB, only [Brain Owner] reads. Source: 2026-05-17 user correction. Brain-file edits remain gated separately.

## Error Handling

Standard error patterns per `_preamble.md`. Additional:

| Failure | Behavior |
|---------|----------|
| Brain file read failure (any of 9 core files) | Skip that domain's audit. Log gap. Continue with available files. Never block the full review |
| GitHub API unavailable | Skip PR staleness check (Step 1). Note: "PR data unavailable — manual check needed" |
| Notion DB unavailable | Skip Notion archive (post-review). Save review output to `.context/drafts/{date}-weekly-review.md` |
| No topics score above 10/20 | Flag: "Zero topics above threshold. Either brain is stale or nothing meaningful happened." Proceed with top 3 regardless |
| Context window pressure (output quality degrades) | Defer Steps 7-9 to follow-up invocation. Output: "Review truncated at Step [N]. Run `/weekly-review --continue` or re-invoke" |


## Important Notes

- This command reads 15-20 brain files across all steps. Phase A pre-loads the 9 most-referenced.
- **"Think Freely, Speak Through Me" applies throughout.** AI reads everything, scores everything, drafts everything. But: no Slack messages sent, no Jira updates, no calendar events created, no Notion pages published, no PR comments posted. All external actions are presented as drafts.
- **GH CLI workaround:** Per `_preamble.md`.
- If any MCP tool is unavailable, skip that data source and note the gap. Do not block the review.
- The weekly review is a forcing function. If it surfaces uncomfortable truths (stale metrics, avoided conversations, missed deadlines), that is the point. Do not soften findings.
- Topic scoring minimum for selection: 10/20. If 0 topics score above 10, investigate: either the brain is stale or nothing meaningful happened.
- If this review produces 0 action items, something is wrong. Either the brain is perfectly maintained (unlikely) or the review is too shallow.
- **Notion DB IDs:** Per `_preamble.md`. Weekly Reviews DB for archive, Initiatives DB for sync check, Meeting Transcripts DB for ingestion audit.

## Operating Rules (migrated from memory tier 2026-04-27)

- **Verify pending items against live state.** Before claiming "X is still pending" in any review section, cross-check GitHub (PRs, branch state), Calendar (meetings happened), Slack (last replies), and Notion (page status). Stale carry-overs from prior reviews are the #1 erosion of weekly-review trust.
- **Re-read current state before reporting.** Do not carry stale findings across turns or reviews. If the previous /weekly-review said "needs X", verify X again — do not auto-claim it still needs X.
- **Drop resolved questions.** Once user confirms a check is done, drop it from all subsequent outputs. Do not re-surface "for completeness." A confirmed check is finished work, not a recurring agenda item.
- **Disambiguate similar-named projects.** When a keyword matches 2+ memories or initiative files (e.g. "RBAC" matches [your-idp-tool]_rbac AND mx_dashboard_rbac), read ALL matching files + verify from source before drafting. Then disambiguate back to the user explicitly: "I found X and Y matching that name. Which?"
- **No unconfirmed estimates.** Never include time estimates ("2 weeks", "by mid-May") in reviews unless the initiative owner has confirmed them in writing. Estimates without owner sign-off become [Brain Owner]'s commitments by default.
- **GCal Tasks (manual), not Events**, for weekly review action items. Tasks live in Google Tasks UI, not Calendar; agent does NOT auto-create. Tasks roll forward and check off; calendar events are immutable. Surface action items as a checklist for [Brain Owner] to manually add to his Tasks list.
- **Adapt frameworks as-is.** Do not add scoring layers or rubrics beyond what the source framework specifies. If [Coaching Framework]'s Tension Doctrine has 3 questions, use 3; do not invent a 5-question variant. Source fidelity over invention.
