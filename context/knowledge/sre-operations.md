# SRE Operations — [Your Company] Applied Doctrines

**Added:** 2026-03-22
**Last Updated:** 2026-03-22
**Source:** Google SRE Book (Beyer et al.), mapped to [Your Company] 17-service AWS/ECS architecture
**Owners:** [Brain Owner], [Your CTO], [Direct Report 2]
**Pillar:** Pillar 2 (Partner Objections) + Pillar 5 (Play Big)
**Measurable Outcome:** SLIs defined for 3 revenue-critical services by 2026-05-01; toil tracked quarterly starting Q2 2026
**Escalation:** If no SLI for revenue-critical services by 2026-05-01, escalate to [Your CTO]

## Risk Tolerance by Service Tier

| Tier | Services | Target Availability | Error Budget (30d) | Rationale |
|------|----------|--------------------|--------------------|-----------|
| Revenue-critical | [your-org]-api, [your-org]-ordering, [your-org]-transaction | 99.9% | 43.2 min/month | Direct revenue path: ordering, payments, loyalty |
| Partner-facing | [your-org]-pos, [your-org]-card-vault | 99.9% | 43.2 min/month | POS failures = merchant churn |
| Internal-critical | [your-org]-core (sidekiq_segmentation), [your-org]-offer | 99.5% | 3.6 hr/month | Batch/async. OOM on segmentation already consuming budget |
| Internal-support | [your-org]-admin, [your-org]-[your-idp-tool] | 99.0% | 7.2 hr/month | Internal tools. Lower cost of brief outages |

**Error budget rule (SRE Ch3):** If error budget is spent, freeze non-critical changes on that service until budget recovers. This replaces vibes-based prioritization. Example: sidekiq_segmentation OOM (24% of hourly windows peak >1900 MB per BUGS-4025). If that exceeds 99.5% budget, it is a P1. If within budget, it is backlog.

## PagerDuty Auto-Resolve Paging Behavior

Auto-resolved incidents still page on-call before resolving. The sequence: alert fires → on-call gets paged (phone/push) → auto-resolve triggers → incident closes. This means auto-resolved incidents reduce MTTR but do NOT reduce on-call burden or sleep-hour interruptions. Feb 2026: 282/306 auto-resolved, yet 113 sleep-hour interruptions from high-urgency alone. The "bang for buck" optimization target is reducing alert volume at the source (tuning thresholds, suppression rules), not faster auto-resolution. Added 2026-04-08.

## SLI Templates ([Your Company] Standard)

### Availability SLI
- **Metric:** Proportion of successful HTTP responses (non-5xx) to total requests
- **Source:** ALB TargetResponseTime + HTTPCode_Target_5XX_Count (CloudWatch)
- **Exclude:** Health checks, internal /status endpoints
- **Aggregation:** 1-minute windows, report as daily/weekly percentile

### Latency SLI
- **Metric:** p99 response time for user-facing endpoints
- **Source:** Datadog APM traces (env:production)
- **Thresholds:** <200ms (API reads), <500ms (API writes), <2s (ordering checkout)
- **Rule (SRE Ch4):** Use distributions, not averages. p99 of one backend = median of frontend.

### SLI Review Process
- **Reviewer:** [Your CTO] validates SLIs reflect merchant-visible impact
- **Visibility:** [Peer Manager 2] and [Peer Manager] receive SLI proposals for input (may contribute implementation)
- **Cadence:** Review before SLI goes live. Quarterly check on relevance.

### Correctness SLI (ordering-specific)
- **Metric:** Orders placed successfully / orders attempted
- **Source:** Datadog logs (env:production, service:[your-org]-ordering)

### Throughput SLI (segmentation-specific)
- **Metric:** Hourly segmentation jobs completed without OOM / total scheduled
- **Source:** ECS task status + Datadog sidekiq.job traces
- **Baseline:** ~76% (24% OOM windows per BUGS-4025)

## Toil Inventory

Track quarterly. Cap at 50% of any individual's time (SRE Ch5). If exceeded, escalate.

| Category | Current Examples | Est. Hours/Week | Automation Target |
|----------|-----------------|----------------|-------------------|
| SOC 2 evidence generation | Manual .txt creation, Drata uploads | 4h ([Brain Owner]) | Terraform → Drata API pipeline |
| Stale PR triage ([your-org]-devops) | Rebase/review of ancient PRs | 2h | GitHub Action: auto-label >30d, auto-close >90d |
| Terraform apply | Manual local apply after merge | 2h | CI-driven apply with approval gate |
| Monitoring noise triage | PagerDuty 289 incidents/90d | 3h | Severity filter + error budget burn-rate alerts |

## Alerting Doctrine

Established by [Your CTO] (Mar 9, 2026). See `compliance-evidence.md` for full context.

Three outputs only (SRE AppB):
- **Page:** A human must act NOW. PagerDuty. Revenue-critical services only.
- **Ticket:** A human must act within days. Jira. Partner-facing and internal-critical.
- **Log:** No immediate action. Datadog logs. Available for forensics.

**Rule:** New monitors start at Slack/email. Promote to PagerDuty only after: (a) low noise confirmed over 2+ weeks, (b) actionable with clear runbook, (c) sleep-worthy (would you wake someone for this?).

## PagerDuty Hygiene

PagerDuty owns on-call routing. The gap is noise, not routing.

- **Current state:** 289 incidents in 90 days (~3.2/day) = alert fatigue guaranteed
- **Target:** <1 page/day (30/month). Every page must be actionable.
- **Action:** Audit all PD-routed monitors. Reclassify per alerting doctrine. Align monitor severity with service tiers above.
- **Schedule audit:** Verify PD schedules match current team structure quarterly.

## Postmortem Process

**Triggers (any one = mandatory postmortem, SRE Ch15):**
- Revenue-critical service outage >5 min
- Error budget exhausted for any tier
- Data loss or corruption (any amount)
- Security incident (any severity)
- Customer-visible degradation reported by 3+ merchants

**Rules:**
- Blameless. Focus on systems, not people. "What broke?" not "who broke it?"
- Written record within 5 business days
- Must include: timeline, root cause(s), impact assessment, action items with owners and deadlines
- Review: shared in #engineering Slack + R&D Leadership if Tier 1 service
- Quarterly: Wheel of Misfortune exercise. Pick a past incident, 2 people, 30-min drill + 15-min debrief. Builds runbook library. Addresses "untested runbooks" gap from IR tabletop (Feb 2026).

## Automation Maturity Ladder

| Domain | Current State | Next Step (SRE Ch7) |
|--------|--------------|---------------------|
| Terraform apply | Manual local apply | CI: plan-on-PR (diff as comment), apply-on-merge with approval gate |
| Monitoring setup | Manual .tf files per monitor | Templated Terraform module per service tier |
| Incident response | Ad-hoc Slack coordination | Runbook per service tier, tested via Wheel of Misfortune |
| Capacity planning | Reactive (OOM = resize) | Monthly 30-min resource utilization review. Flag >70% sustained. |

**Hierarchy (SRE Ch7):** No automation → personal script → shared script → CI automation → autonomous system. Always move right.

## Additional Practices

### Progressive Rollouts (SRE AppB)
ECS supports weighted target groups. For [your-org]-api and [your-org]-ordering: route 5% traffic to new task definition, monitor error rate for 10 min, then full rollout. Near-zero cost. [Your IDP Tool] deploys direct-to-production (no staging) and is the highest-risk gap.

### Monthly Resource Utilization Review
30-min monthly review of ECS memory/CPU via Datadog or CloudWatch ContainerInsights. Flag any service >70% sustained utilization. Resize proactively, not reactively. Prevents OOM firefighting.

### Toil Tracking
Weekly question in standup or async: "Hours of unplanned operational work this week?" Aggregate monthly. If any individual >50%, escalate to their manager.

## [your-org]-devops Top 3 Priorities

### Priority 1: Automated Terraform Apply Pipeline
- **SRE mapping:** Ch7 (automation hierarchy) + Ch5 (toil elimination)
- **Problem:** Merged PR ≠ applied infrastructure. Drata check DCF-87 failed silently for 6 months because no one ran `terraform apply` after merge.
- **Deliverable:** CI pipeline: `terraform plan` on PR (post diff as comment), `terraform apply` on merge to master with approval gate (Slack notification + 10-min hold)
- **Owner:** [Brain Owner]
- **Measurable outcome:** 0 infrastructure drift incidents from unapplied Terraform

### Priority 2: Stale PR and Issue Triage
- **SRE mapping:** Ch5 (toil has no enduring value)
- **Problem:** 5 PRs are 7-15 months stale. Issue #42 is 6 years old. This is organizational debt.
- **Deliverable:** Close or rebase all PRs >90d with documented rationale. GitHub Action: auto-label >30d as `stale`, auto-close >90d. Triage 5 open issues: close-with-rationale or assign owner + deadline.
- **Owner:** [Brain Owner]
- **Measurable outcome:** 0 PRs older than 90 days. Open issue count reduced to actionable backlog only.

### Priority 3: Monitoring Noise Reduction + SLO Foundation
- **SRE mapping:** Ch4 (SLIs/SLOs as decision framework) + Ch6 (Four Golden Signals)
- **Problem:** 289 PagerDuty incidents in 90 days = alert fatigue. No SLOs = no framework for signal vs noise.
- **Deliverable:** Audit all PD-routed monitors, reclassify per Alerting Doctrine. Define SLIs for [your-org]-api, [your-org]-ordering, [your-org]-transaction using templates above. Create error budget burn-rate alerts.
- **Owner:** [Brain Owner] + [Direct Report 2]
- **Measurable outcome:** PagerDuty incidents drop from ~3.2/day to <1/day. SLIs defined for 3 services.

## [Direct Report 2] Cybersecurity Backlog (4h/week)

[Direct Report 2]: Sr Software Engineer ([Peer Manager 2]'s team). Drata admin, Eden Data sync attendee. Career pivot to cybersecurity driven by AI impact on software engineering roles. Prefers compliance/architecture over SOC ops. 4h/week = ~16h/month.

| # | Title | SRE Ch | Effort | Measurable Outcome |
|---|-------|--------|--------|--------------------|
| 1 | Drata Automated Check Audit | Ch6 | 8h | 100% of Drata checks in known state (passing, risk-accepted, or remediation-planned) |
| 2 | Quarterly Access Review Automation | Ch5,7 | 12h | Reviews completed in <2h (vs ad-hoc). 0 stale accesses >30d |
| 3 | Rate Limiting (/users endpoint) | AppB | 8h | 0 open pentest findings (closes Cobalt Low #PT33140_3) |
| 4 | AI Risk Assessment Document | Ch3 | 8h | Risk register (LLM data leakage, prompt injection, model poisoning) mapped to DCF controls |
| 5 | GuardDuty Finding Triage Runbook | Ch15,6 | 6h | Written runbook in Notion. Response SLA: HIGH/CRITICAL <4h, MEDIUM <24h |
| 6 | Backup Restoration Test | AppB | 8h | RPO/RTO validated via RDS PITR test. SOC 2 evidence produced |
| 7 | Identity Revocation Centralization Plan | Ch7 | 12h | Revocation checklist covering all platforms. Time-to-revoke baselined |
| 8 | SNS Topic Subscription Audit | Ch6 | 4h | 0 pending-confirmation subscriptions |

**Sequencing:** Items 1-2 first (establish visibility). Items 3-5 parallel. Items 6-8 flex with compliance calendar.

**AI risk leverage (item 4):** Channels [Direct Report 2]'s firsthand AI impact perspective into a concrete, audit-ready deliverable. Development assignment per [Coaching Framework] delegation lens: builds security analysis capability while producing output that strengthens compliance posture.

**Monthly review:** [Brain Owner] reviews progress with [Peer Manager 2] ([Direct Report 2]'s manager). Items feed SOC 2 evidence pipeline and compliance_posture.md updates.

## Cross-References

| Brain File | Connection |
|-----------|-----------|
| `compliance-evidence.md` | Alerting Escalation Doctrine, PagerDuty service directory, BC/DR tabletop gaps |
| `datadog-observability.md` | Monitor types taxonomy, alerting best practices, security monitoring, synthetic tests, AI problem detection, [Your IDP Tool] MCP tools |
| `datadog-terraform.md` | Monitor patterns (composite, anomaly, forecast, SLO, synthetic), alert routing, log-based metrics for SLI implementation |
| `[your-org]-services.md` | Service architecture, ECS/RDS topology, sidekiq_segmentation OOM baseline |
| `11_compliance_security/_template_compliance_program.md` | IR tabletop gaps (identity revocation, untested runbooks), SOC 2 renewal timeline |
