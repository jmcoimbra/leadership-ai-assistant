# PR Hygiene Mandate
> Owner: [Brain Owner] | Pillar: [Pillar N] | Status: Enforced | Last Audit: [YYYY-MM-DD]

## Purpose

PRs that are created but not socialized do not get reviewed. PRs that are not reviewed do not ship. This mandate encodes the minimum standard for PR lifecycle management across the teams you lead.

## Rules

### 1. Author Responsibilities (upon opening a PR)

| # | Action | When |
|---|--------|------|
| 1 | Assign yourself (and pair partner if paired) as assignee | Before requesting review |
| 2 | Request review from the relevant team subgroup | Immediately |
| 3 | Post a link in the team's chat channel with 1-2 sentence context | Within 1 hour of opening |
| 4 | Monitor your open PRs daily | Every working day |

### 2. Reviewer Responsibilities (upon receiving a review request)

| # | Action | When |
|---|--------|------|
| 1 | Acknowledge in chat or PR comment | Within 24 hours |
| 2 | Complete review | Within 48 hours (72h max for large PRs) |
| 3 | If blocked or unable to review, say so explicitly | Within 24 hours |

### 3. Review Request Targets

Define your teams' GitHub team mentions and chat channels in `config/team.yaml.example` (copy to `team.yaml` for local use). Example schema:

```yaml
teams:
  - name: <team_name>
    github_handle: <org>/<team>
    chat_channel: <#channel-name>
```

### 4. Socialization Format

When posting a PR in chat, use this minimum format:

```
PR: [title] - [repo]
[link]
What it does: [1 sentence]
Review needed by: [date]
```

### 5. Dashboard URLs

Every team member must bookmark these two URLs (replace `{username}` with your GitHub handle):

| Dashboard | URL |
|-----------|-----|
| PRs awaiting my review | `https://github.com/pulls?q=is%3Apr+is%3Aopen+review%3Anone+draft%3Afalse+review-requested%3A{username}` |
| My open PRs | `https://github.com/pulls?q=is%3Apr+is%3Aopen+draft%3Afalse+author%3A{username}` |

### 6. Staleness Enforcement

| Condition | Action |
|-----------|--------|
| No reviewer response in 48 hours | Author re-pings in chat with @ mention |
| PR open >7 days without review | Author escalates to manager |
| PR open >14 days without activity | Stale. Address within 7 days: merge, close, or log decision |
| PR open >30 days | Vision > Execution violation. Address same week |

## Measurable Outcome

- **Baseline:** No standard. PRs assigned but not socialized. No review SLA.
- **Target:** 100% of PRs socialized in chat within 1 hour of opening. 90% of reviews completed within 48 hours. Zero PRs >14 days without activity.
- **Measurement:** Weekly PR audit during `07_operating_rhythms/weekly_review.md`.

## Escalation

- Reviewer non-response after author re-ping (48h): manager intervenes directly.
- Same person accumulates 3+ late reviews in a month: 1:1 conversation about PR hygiene as a professional standard.
- Team-wide compliance drops below 80% in any week: addressed in team meeting.

## Cross-References

| Brain File | Connection |
|-----------|-----------|
| `12_projects/projects_tracker.md` | Staleness rules (>14 days, >30 days) |
| `02_leadership/async_communication_standard.md` | CONTEXT/ASK/OWNER/DEADLINE format for escalations |
| `07_operating_rhythms/weekly_review.md` | PR staleness check |

## AI Integration

Use AI to scan open PRs for age, reviewer non-response, missing context, and unclear ownership. Draft follow-up comments for the brain owner to send.
