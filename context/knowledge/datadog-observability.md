# Datadog Observability Patterns

**Added:** 2026-03-23
**Last Updated:** 2026-03-23
**Source:** Datadog Cloud Monitoring Quick Start Guide (Thomas & Kumar, Packt), mapped to [Your Company] 17-service AWS/ECS architecture
**Owner:** [Brain Owner]
**Pillar:** Pillar 2 (Partner Objections) + Pillar 5 (Play Big)
**Measurable Outcome:** PagerDuty incidents from ~3.2/day to <1/day by 2026-06-01; SLIs for 3 revenue-critical services by 2026-05-01
**Escalation:** If PD noise not reduced to <2/day by 2026-05-15, escalate to [Your CTO]

## Monitor Types Taxonomy

| Type | DD Type | Query Function | [Your Company] Use Case | Algorithm/Notes |
|------|---------|---------------|----------------|-----------------|
| Metric threshold | `metric alert` | Direct comparison | ECS memory >80%, disk >85% | Static. Known baselines only |
| Metric change | `query alert` | `change()` | Error rate 3x vs prior hour post-deploy | Catches deploy impact |
| Anomaly | `query alert` | `anomalies()` | Error rate, latency, traffic volume | `agile` for error rates (deploy-robust), `robust` for traffic (weekly restaurant seasonality), `basic` for stable infra metrics |
| Forecast | `query alert` | `forecast()` | ECS memory capacity, RDS disk | `linear` for steady growth, `seasonal` for cyclical. Alert 7 days before breach |
| Outlier | `query alert` | `outliers()` | One ECS task degraded vs peers | DBSCAN (topology) or MAD (median). Multi-host services only |
| Log | `log alert` | Log query | Security audit events, application errors | Event-based. Requires structured JSON logging |
| Composite | `composite` | Boolean on monitor IDs | Error rate + latency = page | Noise reduction. Combine 2-3 signals before PD |
| Process | `process alert` | Process query | Sidekiq process count | Requires `process_config.enabled: true` |
| Network | `network alert` | Network query | Inter-service connectivity | TCP state counts (ESTABLISHED, TIME_WAIT) |
| Synthetic | `synthetics alert` | HTTP/SSL/DNS/TCP | External availability, SSL cert expiry | Global locations. CI/CD blocking supported |

**Algorithm selection for [Your Company] services:**
- [your-org]-api, [your-org]-ordering, [your-org]-transaction error rates → `agile` (deploys shift baselines)
- Traffic volume on all services → `robust` (weekly Fri-Sun restaurant peaks)
- Infrastructure metrics (CPU, memory, disk) → `basic` (rolling average, stable)

## Alerting Best Practices

Three outputs only ([Your CTO], Mar 9, 2026):
- **Page:** PagerDuty. Revenue-critical only. Human must act NOW.
- **Ticket:** Jira. Partner-facing and internal-critical. Human must act within days.
- **Log:** Datadog. No immediate action. Available for forensics.

**Composite monitors as noise reduction:**
Combine error rate + latency spike before paging. Prevents single-metric false positives. Example: API error rate >5% AND p99 >1s = page. Either alone = ticket.

**Error budget burn-rate alerts:**
- 2% budget consumed in 1h = page (fast burn, incident in progress)
- 5% budget consumed in 6h = ticket (slow burn, degradation)
- 10% budget consumed in 24h = log (trend, capacity planning)

**`renotify_interval` standards:**
- Short-window monitors (30m-1h): 60 min
- Daily monitors: 720 min (12h)
- Must be set on ALL monitors. Prevents alert fatigue from repeated pages for same incident.

**`on_missing_data` by service tier:**
- Revenue-critical: `show_and_notify_no_data` (silence = incident)
- Partner-facing: `show_and_notify_no_data`
- Internal-critical: `resolve` during known low-traffic windows
- Internal-support: `resolve`

**Monitor promotion rule:** New monitors start at Slack/email. Promote to PagerDuty after: (a) low noise confirmed over 2+ weeks, (b) actionable with clear runbook, (c) sleep-worthy.

## Log Management Patterns

### Log Retention

- Default retention: ~15 days. Queries beyond this window return empty results silently (no error, zero logs, status "done").
- Before investigating incidents >2 weeks old, check if logs are within retention window. Empty results is NOT evidence of no errors.
- For historical analysis beyond retention: use [Your IDP Tool] `assistant_ask` (queries Snowflake long-term storage) or `snowflake_query` directly.
- Added 2026-03-26.

### Agent-Level Filtering

**Exclude health check noise (before indexing):**
```yaml
log_processing_rules:
  - type: exclude_at_match
    name: exclude_health_checks
    pattern: ^GET /health HTTP
```

**Include only error paths (cost reduction):**
```yaml
log_processing_rules:
  - type: include_at_match
    name: include_errors_only
    pattern: (ERROR|FATAL|status:(4|5)\d{2})
```

### PII Scrubbing at Agent Level

Critical for PCI DSS and SOC 2. PII never reaches DD servers.

```yaml
log_processing_rules:
  - type: mask_sequences
    name: redact_credit_card
    pattern: "\\b\\d{4}[- ]?\\d{4}[- ]?\\d{4}[- ]?\\d{4}\\b"
    replace_placeholder: "[CC_REDACTED]"
  - type: mask_sequences
    name: redact_email
    pattern: "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+"
    replace_placeholder: "[EMAIL_REDACTED]"
  - type: mask_sequences
    name: redact_ssn
    pattern: "\\b\\d{3}-\\d{2}-\\d{4}\\b"
    replace_placeholder: "[SSN_REDACTED]"
```

Connects to Lucas's data pipeline PII concern (Snowflake ingestion). Same principle: scrub at source.

### Log-Based Metrics vs Full Indexing

| Approach | Cost | Use Case |
|----------|------|----------|
| Full indexing | $$$ per GB | Debugging, audit trails, compliance evidence |
| Log-based metrics | $ per metric | Error rates, request counts, latency distributions |
| Archive only | $ per GB | Compliance retention (S3/GCS). Rehydrate for ad-hoc analysis |

**Decision:** Use log-based metrics for SLI tracking. Full indexing only for revenue-critical services and compliance-required logs. Archive everything for SOC 2 retention.

### Log Pipeline Processors

Grok Parser → Date Remapper → Status Remapper → Category Processor. Applied in DD UI or Terraform. Require structured JSON logging ([Your Company] uses Fluent Bit → DD).

## Security Monitoring

### 112 Predefined CORE Rules (out of box)

Categories: authentication attacks, privilege escalation, lateral movement, data exfiltration, compliance violations. Examples:
- "Anomalous AWS user executed a command" (HIGH, CloudTrail)
- "Auth0 user logged in with breached password" (MEDIUM)
- "AWS CloudTrail configuration modified" (HIGH, CIS-AWS-3.5)
- "Anonymous Request Authorized" (INFO, Kubernetes)

**Activation cost:** Enable Security Monitoring in DD. Configure log sources. Rules auto-apply. Estimated 4-8h for initial setup.

### Security Signals

Alert equivalent for threat events. Created when log content matches a security rule. Route to same notification channels as infrastructure alerts. Triage in DD Security → Signals view.

### Runtime Security (Cloud Workload Security)

Detects system-level anomalies in ECS containers:
- Unexpected file modifications (e.g., binary changes in production)
- Unauthorized process execution (e.g., shell spawned in API container)
- Privilege escalation attempts
- Network connections to unexpected destinations

Requires DD Agent sidecar with security module enabled. Connects to Lucas backlog item #7 (identity revocation): detects compromised container behavior from stolen credentials.

### Compliance Findings

Continuous audit against PCI DSS and CIS Benchmarks:
- Misconfigured security groups
- Unencrypted storage
- Exposed ports
- IAM policy drift

Feeds evidence into Drata (connects to Lucas backlog item #1).

### GuardDuty → DD Integration

Pattern: AWS GuardDuty finding → CloudWatch Events → DD Log Intake → DD Security Signal → Notification → PD (HIGH/CRITICAL only).

Lucas's GuardDuty triage runbook (backlog item #5) should use DD as the single-pane triage interface, not AWS Console.

### SIEM Capability

DD functions as SIEM by ingesting security product logs:
- AWS: CloudTrail, GuardDuty, WAF, Shield, Inspector
- Identity: Okta, Auth0, Google Workspace, Azure AD
- Infrastructure: Docker, Kubernetes, EKS audit logs
- Secrets: HashiCorp Vault

## Synthetic Monitoring

### HTTP/HTTPS Endpoint Checks

Revenue-critical services: [your-org]-api, [your-org]-ordering, [your-org]-transaction.
- `/health` endpoint checks from multiple global locations
- Response time assertions (<200ms for health checks)
- Status code assertions (200)
- Body content validation

### SSL Certificate Expiry

`datadog_synthetics_test` with SSL check type. Alert 30 days before expiry. SOC 2 + PCI evidence.

### CI/CD Blocking Gate

Set `CI/CD EXECUTION: Blocking` on critical synthetic tests. Failed synthetic = blocked pipeline. Use for ordering checkout flow validation post-deploy.

### Browser Tests

Record real user workflow via DD browser plugin. Simulates Chrome/Firefox from multiple locations. Use for ordering checkout end-to-end validation.

## Tagging Strategy

### Foundation Tags (required on all resources)

| Tag | Values | Purpose |
|-----|--------|---------|
| `env` | `production`, `staging` | Environment filtering |
| `service` | `[your-org]-api`, `[your-org]-ordering`, etc. | Service filtering |
| `team` | `mobile-team`, `qa`, `dev-support` | Ownership |
| `tier` | `revenue-critical`, `partner-facing`, `internal-critical`, `internal-support` | Maps to sre-operations.md risk tolerance |

### Tag Enforcement

- Terraform monitors: all must include `env`, `service`, `tier` tags
- Dockerfile: `LABEL "com.datadoghq.ad.logs"='[{"source":"<service>","service":"<service>"}]'`
- ECS task definitions: propagate tags from task definition to container

### Tag Naming Convention

Lowercase, no spaces, hyphens for multi-word: `team:dev-support`, `tier:revenue-critical`.

## API Automation

All repeatable operations must be API-first, not click-based.

| Operation | Endpoint | When |
|-----------|----------|------|
| Mute host | `POST /api/v1/host/{hostname}/mute` | Pre-deploy maintenance |
| Schedule downtime | `POST /api/v1/downtime` | Planned maintenance windows |
| Post deploy event | `POST /api/v1/events` | Deploy start/end markers |
| Query metrics | `GET /api/v1/query` | Programmatic SLI calculation |
| Create monitor | `POST /api/v1/monitor` | Automated monitor provisioning |

**Authentication:** `DD-API-KEY` + `DD-APPLICATION-KEY` headers. Service user with minimum required role (not admin key in automation).

**Deploy integration:** POST event at deploy start/end with `alert_type: info` and deploy tag. Creates timeline marker on all dashboards for RCA correlation.

**DogStatsD (application-level telemetry):**
UDP port 8125. Zero auth, fire-and-forget. For high-frequency metrics not available via APM.
```python
from datadog import statsd
statsd.increment('[your-company].api.requests.count', tags=["endpoint:/checkout","status:200"])
statsd.histogram('[your-company].api.request.duration_ms', duration_ms, tags=["service:ordering"])
statsd.gauge('[your-company].worker.queue.depth', len(queue), tags=["worker:segmentation"])
```
Naming convention: `[your-company].<service>.<metric>`.

## APM & Service Map

### Trace-Based Monitoring

APM traces feed SLI metrics:
- Latency SLI: `p99:trace.web.request.duration{service:$service}`
- Error SLI: `trace.web.request.errors{service:$service}` / total
- Throughput: `trace.sidekiq.job.hits{service:$service}`

### Service Map

Auto-generated topology of 17 [Your Company] services at `APM | Service Map`. Shows requests/latency/error rate per service edge. Use during incidents to trace degradation path.

### Continuous Profiler

CPU and memory hotspot identification per service. Method-level breakdown. Enable via `dd.profiling.enabled=true`. Use for OOM root cause analysis (sidekiq_segmentation).

## AI Problem Detection via DD

Channels Lucas's AI anxiety into concrete, monitorable signals.

### [Engineering Toolkit] Access Monitoring

- Log-based metric: `[your-company].[engineering-toolkit].api_calls` grouped by `user`, `endpoint`, `source_ip`
- Anomaly detection (`agile`) on per-user call volume
- Security rule: API calls from unknown IPs or outside business hours
- Addresses Lucas's concern: "[Engineering Toolkit] access too broad (customer service doesn't need it)"

### Token Usage Anomaly Detection

- DogStatsD metric: `[your-company].[engineering-toolkit].token_usage` with tags `model`, `user`, `endpoint`
- Forecast monitor: alert at 80% monthly budget
- Anomaly: single user consuming 3x normal = investigation trigger

### AI Model Response Time/Error Rate

- APM traces on [Engineering Toolkit] API endpoints
- SLI: p99 <5s (standard queries), <30s (complex analysis)
- Error rate composite: error rate >5% AND response time >10s = page

### Unauthorized AI Tool Usage

- Custom Security Signal rule: API key used from unrecognized service/IP
- Log-based detection: [Engineering Toolkit] API calls bypassing approved entry points
- Identity correlation: cross-reference with access review automation (Lucas backlog #2)

## [Your IDP Tool] MCP Tool Reference

| Tool | Purpose | Key Params |
|------|---------|-----------|
| `datadog_logs` | Query logs | `service:X container_name:Y`. Use instead of `ecs_task_logs` for Fluent Bit containers |
| `datadog_metrics` | Query metrics | Custom metrics and APM metrics |
| `datadog_monitors` | List/inspect monitors | Monitor IDs, status, tags |
| `datadog_services` | Service catalog | Dependencies, topology |
| `datadog_spans` | APM trace spans | Specific operation traces |

**Response schema for `datadog_logs`:** `{logs: [{id, type: "log", attributes: {message, timestamp, status, tags, attributes: {task, http, duration}}}], log_count, meta}`. Tags include `cluster_name`, `container_name`, `task_arn`, `task_family`, `task_version`.

## Cross-References

| Brain File | Connection |
|-----------|-----------|
| `datadog-terraform.md` | Implementation patterns (HCL), provider gotchas, alert routing |
| `sre-operations.md` | Service tiers, SLI templates, alerting doctrine, PD noise target, Lucas backlog |
| `[your-org]-services.md` | 17-service architecture, ECS topology, Fluent Bit log driver |
| `compliance_posture.md` | PCI DSS, SOC 2, IR tabletop gaps |
| `compliance-evidence.md` | Alerting Escalation Doctrine source, PagerDuty service directory |
| `lucas_ventura.md` | Cybersecurity backlog items 1, 4, 5, 7 intersect with DD security |

## Investigation via Browser (No Datadog MCP)

When a Datadog alert posts to Slack and you need the monitor details, the bot body is not surfaced by the Slack API (see `slack-patterns.md` "Datadog Bot Bodies Are Not in the Slack API"). Permalinks return empty `Text:`. Default investigation path:

1. **Ask the user for the Datadog URL.** Do not chase a Datadog MCP, DD CLI, or 1Password CLI first. There is no Datadog MCP server in the [Your Company] surface. The `[engineering-toolkit]:investigate:datadog-context` agent confirms "No Datadog access available." `op item list` requires interactive authorization. Round-trip on those alternatives is 4+ tool calls before producing zero data.
2. **Navigate via claude-in-chrome.** The extension attaches to any Chromium browser (Chrome, Brave) and uses the user's existing authenticated session. No browser switch required when a tab is already active.
3. **Use `read_page` (accessibility tree), not `get_page_text`.** Datadog is JS-rendered; `get_page_text` returns "No text content found." Pass `depth=8` and `max_chars=60000` for monitor detail pages. Default 30k overflows.
4. **Anchor extraction on these accessibility refs:**
   - Heading: monitor name (e.g., `[Release Cut] Total Error Count - iOS`)
   - Event Details `Message`: `[Warn|Alert on {tag:value}]` template + threshold values
   - `Query`: the `sum(last_Xh):...` expression. Gives metric, scope, threshold.
   - `Groups`: scoping tags (`version:49.2.2-49.2.2`)
   - `Suggested Resources`: dashboard links routed off the monitor
   - `Message Sent To`: Slack channel routing string

Source: 2026-05-24 Datadog alert in the release monitoring channel. First attempt chased DD MCP/CLI/1Password CLI; second attempt delegated to `[engineering-toolkit]:investigate:datadog-context` which reported no access. Browser path produced full monitor details in one `read_page` call after the user shared the URL.

## [Mobile Team] Release-Cut Monitor Inventory

Owner: [Your CTO]. All routed to the release monitoring channel and scoped by `version:<release>-<release>` tag.

| Monitor ID | Name | Platform |
|------------|------|----------|
| 265683274 | [Release Cut] App Launch Errors - Android | Android |
| 265904738 | [Release Cut] App Launch Errors - iOS | iOS |
| 265045163 | [Release Cut] Total Error Count - Android | Android |
| 265904739 | [Release Cut] Total Error Count - iOS | iOS |

**Total Error Count - iOS (265904739) thresholds:**
- Query: `sum(last_1h):sum:rum.measure.error{env:production, os.name:iOS} by {version}.as_count()`
- Warn: > 3000/hr
- Alert: > 6000/hr
- Source: RUM (`rum.measure.error`)

**Companion dashboards:**
- `/dashboard/wnu-ht9-w3g/branded-app-health` (Branded App Health)
- `/dashboard/dku-2fd-ar4/release-cut-health` (Release Cut Health)
- `/dashboard/9fv-84r-w73/branded-app-health---release-cut-monitor` (Release Cut Monitor companion)

**Interpretation:** Raw SUM grows mechanically with rollout coverage. Compare per-session rate, not raw count, before treating a Warn as a regression signal. Multiple Warn fires within an hour can be the rolling 1h SUM brushing the threshold as it slides forward; not necessarily two distinct events.

Source: 2026-05-24 hotfix rollout monitoring. Monitor 265904739 fired Warn twice (3156/hr against 3000/hr warn, 47% below 6000/hr alert). Both events same monitor, same condition, 23 min apart.
