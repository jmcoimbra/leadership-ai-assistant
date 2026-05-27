# Datadog Terraform Patterns

**Added:** 2026-03-09
**Last Updated:** 2026-05-26 (Dashboard Tags Restriction section added: only `team` and `ai` keys accepted on datadog_dashboard; `service:` / `feature:` legal on monitors but not dashboards. Source: [your-org]-devops #1043 to #1046, App Preview dashboard apply-monitors regression). Earlier 2026-03-24 (on_missing_data discipline for trace-based monitors + Ruby logger breaks log-based metrics, from [Your IDP Tool] 69h Sidekiq outage).
**Source:** JULI-60 implementation session ([your-org]-devops monitors/app-reviews.tf, [PR #979](https://github.com/[your-org]/[your-org]-devops/pull/979) merged 2026-03-09)

## Provider & State

- **Provider:** DataDog/datadog ~> 3.90.0 (pinned in `monitors/main.tf`)
- **Terraform version:** 1.14.6
- **State:** S3 `[your-org]-terraform/monitors.tfstate`
- **Local install:** `tfenv install 1.14.6 && tfenv use 1.14.6`

## CI Pipeline ([your-org]-devops)

- **validate-format:** `terraform fmt -recursive -check .` — fails if any file not formatted
- **plan-monitors:** `terraform plan` in `monitors/` directory
- **CircleCI logs are client-side rendered.** No API access without token. Diagnose failures indirectly from job names and error patterns.

## Dashboard Layout

- **Use `layout_type = "free"`** with flat `widget { ... widget_layout { height, width, x, y } }` blocks
- **Do NOT use `layout_type = "ordered"`** with `group_definition` — unsupported or broken in provider v3.90.0
- **Pattern source:** `monitors/dashboards.tf` (Platform Health Dashboard)

## Dashboard Tags Restriction

`datadog_dashboard` accepts only two tag keys: `team` and `ai`. Any other key (`service:`, `feature:`, `env:`, `pos:`) is rejected by `/api/v1/dashboard` at apply time with:

```
Error: error creating dashboard from /api/v1/dashboard: 400 Bad Request:
{"errors":["Invalid tag format. Valid tag keys are: team, ai."]}
```

- `terraform validate` does NOT catch this. `plan-monitors` shows "1 to add" and only `apply-monitors` fails.
- The restriction is dashboard-specific. `datadog_monitor` accepts free-form tag keys, which is why `service:` / `feature:` / `pos:` appear across `monitors/*.tf` monitor resources.
- **Established repo pattern:** the three existing dashboards (`program_ensure_health`, `app_reviews_health`, `platform_health_dashboard`) declare NO top-level `tags` block. Default to omitting `tags` on new dashboards unless you genuinely need `team:` or `ai:` routing.
- **Source:** [your-org]-devops #1043 (App Preview dashboard) shipped with `service:[your-org]-[your-product-ui]`, `feature:app-preview`, `team:platform` and broke apply-monitors on master for 3 days (CircleCI job 185599). Fixed in #1046. Added 2026-05-26.

## Monitor Patterns

### Sidekiq Job Health (trace-based)

```hcl
query = "sum(last_30m):sum:trace.sidekiq.job.hits{env:production,resource_name:<job>,service:<service>-sidekiq}.as_count() < 1"
```

- `resource_name` = lowercased PascalCase: `syncappreviewjob`, `syncappstoreratingsjob`
- Verify resource names in Datadog APM: service → operation `sidekiq.job` → Resources list
- **Do NOT use `sidekiq.job_fetch`** — that shows queue fetch operations, not job executions
- **MUST set `on_missing_data = "show_and_notify_no_data"`** on ALL trace-based monitors. Without it, when the service/process dies, the trace metric stops entirely (no data points, not zero). Default Datadog behavior: silent "No Data" state, no notification. This caused a 69-hour [Your IDP Tool] Sidekiq outage (Mar 20-23 2026) to go undetected by Monitor 1 despite a 30-minute window. Added 2026-03-24.

### Error Rate (log-based metric)

```hcl
query = "sum(last_30m):sum:<metric>{env:production,status:failed}.as_count() / sum:<metric>{env:production}.as_count() > 0.1"
```

- Requires `datadog_logs_metric` resource with `group_by` on status field
- `on_missing_data = "resolve"` — no alerts when no data (expected during low-traffic)

### Zero Activity (log-based metric)

```hcl
query = "sum(last_1d):sum:<metric>{env:production}.as_count() < 1"
```

- `on_missing_data = "show_and_notify_no_data"` — alert when no data at all (indicates pipeline failure)

### `on_missing_data` Valid Values

Only four values accepted by Datadog API: `show_no_data`, `show_and_notify_no_data`, `resolve`, `default`.
- Only available for: APM Trace Analytics, Audit Trail, CI, Error Tracking, Event, Logs, RUM monitors
- NOT available for: Service Check, Composite, SLO monitors
- `terraform validate` does NOT catch invalid enum values — only `terraform plan` (API call) rejects them
- To extract valid enums from provider binary: `strings <provider-binary> | grep <attribute_name>`

## Log-Based Metrics

```hcl
resource "datadog_logs_metric" "example" {
  name = "[your-company].<service>.<metric_name>"
  compute {
    aggregation_type = "count"
  }
  filter {
    query = "env:production service:<service> @field:value"
  }
  group_by {
    path     = "@field_name"
    tag_name = "tag_name"
  }
}
```

- Depends on structured JSON logging in the application (`.to_json` hashes with parseable fields)
- Datadog parses `@field_name` from JSON log attributes
- Deploy structured logging BEFORE applying log-based metric monitors
- **Ruby standard logger breaks facet extraction.** `Rails.logger.info(data.to_json)` produces `I, [timestamp] INFO -- : {"key":"value"}`. Datadog indexes the JSON as a raw string inside `error.message`, not as structured attributes. `@field_name` facets never populate. The metric silently returns zero data points forever. Fix: use `SemanticLogger`, `Lograge`, or a Datadog log pipeline to parse the embedded JSON. Verified on [Your IDP Tool] Mar 9-24 2026: `[your-company].[your-idp-tool].reviews_ingested.count` had zero data points across 15 days. Added 2026-03-24.

## Widget Types — Known Gotchas

- **`manage_status_definition`** is the correct widget for monitor summary in dashboards. It is NOT deprecated despite AI-generated reviews claiming otherwise (2026-03-09).
- **`monitor_summary_definition` does NOT exist** in the Datadog Terraform provider (v3.90.0). `terraform validate` will fail with "unknown block type." This was hallucinated by an AI-assisted reviewer.
- Before renaming any Terraform resource type based on AI review feedback, verify it exists: `GH_TOKEN="" gh search code "<attribute>" --repo DataDog/terraform-provider-datadog`

## Monitor Best Practices

- **`renotify_interval`:** Set on all monitors to prevent alert fatigue. Values in minutes: 60 for short-window monitors (30m-1h), 720 (12h) for daily monitors.
- **Error rate windows:** 30m window is aggressive for cron jobs with 15m cycles. 1h window (4 cycles) gives sufficient signal. [Your CTO] feedback: "should be after multiple failures rather than one/two sync failure cycles."

## Log-Based Metric Aggregation

- `aggregation_type = "count"` — counts log lines matching the filter. Does NOT sum field values.
- `aggregation_type = "distribution"` with `path = "@field_name"` — sums the numeric field across matching logs.
- If dashboard shows "Reviews Ingested" but metric uses count, it shows sync events with reviews, not actual review volume. Label accordingly.

## Alert Routing

- `@slack-[Your Company]-<channel-name>` for Slack integration
- No PagerDuty for non-revenue-critical monitors
- Slack channel must exist and Datadog integration must be configured

### Channel Frequency Doctrine

Separate operational channels (visible to stakeholders) from alert channels (ops-only):
- **Operational channels** (e.g., #app-reviews): Only low-frequency alerts (24h+ eval window). These channels have non-engineering audience.
- **Alert channels** (e.g., #app-reviews-alerts): All monitor signals, any frequency. Ops audience expects noise.
- Rule: if `renotify_interval < 720` (12h), route to alerts channel only.
- Source: PR #996 [your-org]-devops (2026-03-24). Monitors 1 (30m) and 5 (1h) were routing to #app-reviews, removed per [Brain Owner] review.

## Existing Pattern Files

| File | Pattern |
|------|---------|
| `monitors/[your-org]-core_error-rate.tf` | Sidekiq job error rate |
| `monitors/multi-use-rewards.tf` | Log alert pattern |
| `monitors/push-notifications.tf` | Log metrics + monitors in one file |
| `monitors/dashboards.tf` | Free layout dashboard with manage_status widgets |

## Composite Monitor Pattern

Combine multiple signals before paging. Primary noise reduction tool (see `datadog-observability.md`).

```hcl
resource "datadog_monitor" "api_error_rate" {
  type    = "query alert"
  name    = "[P1] [your-org]-api error rate > 5%"
  query   = "sum(last_5m):sum:trace.web.request.errors{env:production,service:[your-org]-api}.as_count() / sum:trace.web.request.hits{env:production,service:[your-org]-api}.as_count() > 0.05"
  message = "Error rate elevated. Check APM traces."
  tags    = ["env:production", "service:[your-org]-api", "tier:revenue-critical", "team:mobile-team"]
}

resource "datadog_monitor" "api_latency_p99" {
  type    = "query alert"
  name    = "[P1] [your-org]-api p99 latency > 1s"
  query   = "avg(last_5m):p99:trace.web.request.duration{env:production,service:[your-org]-api} > 1"
  message = "P99 latency elevated. Check APM traces."
  tags    = ["env:production", "service:[your-org]-api", "tier:revenue-critical", "team:mobile-team"]
}

resource "datadog_monitor" "composite_api_degradation" {
  type    = "composite"
  name    = "[Composite] [your-org]-api degradation — error rate + latency"
  query   = "${datadog_monitor.api_error_rate.id} && ${datadog_monitor.api_latency_p99.id}"
  message = "@pagerduty-[your-org]-revenue-critical Both error rate AND latency elevated. Likely incident."
  tags    = ["env:production", "service:[your-org]-api", "tier:revenue-critical", "team:mobile-team"]
}
```

- `on_missing_data` is NOT available for composite monitors
- Composite query uses `&&` (AND), `||` (OR), `!` (NOT) operators on monitor IDs
- Individual monitors can alert to Slack; composite escalates to PagerDuty

## Anomaly Detection Pattern

```hcl
resource "datadog_monitor" "ordering_error_anomaly" {
  type    = "query alert"
  name    = "[Anomaly] [your-org]-ordering error rate deviation"
  query   = "avg(last_4h):anomalies(sum:trace.web.request.errors{env:production,service:[your-org]-ordering}.as_count(), 'agile', 3) >= 1"
  message = "Error rate anomaly detected. Algorithm: agile (deploy-robust). @slack-[Your Company]-engineering"
  tags    = ["env:production", "service:[your-org]-ordering", "tier:revenue-critical"]

  monitor_thresholds {
    critical          = 1.0
    critical_recovery = 0.0
  }
}
```

**Algorithm selection:**
- `agile`: Error rates. Handles level shifts from deploys. Deviation factor 3 = 3 standard deviations.
- `robust`: Traffic volume. Ignores weekly seasonality (restaurant Fri-Sun peaks). Deviation factor 2-3.
- `basic`: Infrastructure metrics (CPU, memory). Rolling average. Deviation factor 2.

## Forecast Monitor Pattern

```hcl
resource "datadog_monitor" "segmentation_memory_forecast" {
  type    = "query alert"
  name    = "[Forecast] sidekiq_segmentation memory exhaustion"
  query   = "max(next_7d):forecast(avg:ecs.memory.utilized{service:[your-org]-core-sidekiq,task_family:sidekiq_segmentation}, 'linear', 1) > 1900"
  message = "Memory projected to hit 1900MB within 7 days. Resize ECS task. @slack-[Your Company]-engineering"
  tags    = ["env:production", "service:[your-org]-core", "tier:internal-critical"]
}
```

- `linear` for steady growth (memory, disk)
- `seasonal` for cyclical patterns (request volume)
- Threshold 1900MB matches BUGS-4025 OOM baseline (24% of hourly windows peak >1900MB)

## SLO Pattern

```hcl
resource "datadog_service_level_objective" "api_availability" {
  name        = "[your-org]-api availability SLO"
  type        = "monitor"
  description = "99.9% availability for [your-org]-api (revenue-critical tier)"
  monitor_ids = [datadog_monitor.api_availability.id]

  thresholds {
    timeframe = "30d"
    target    = 99.9
    warning   = 99.95
  }

  tags = ["env:production", "service:[your-org]-api", "tier:revenue-critical"]
}
```

**Error budget burn-rate alerts** (pair with SLO):
- 2% budget consumed in 1h → page (fast burn)
- 5% budget consumed in 6h → ticket (slow burn)
- 10% budget consumed in 24h → log (trend)

Note: `on_missing_data` is NOT available for SLO monitors.

## Synthetic Test Pattern

```hcl
resource "datadog_synthetics_test" "api_health" {
  name      = "[your-org]-api health check"
  type      = "api"
  subtype   = "http"
  status    = "live"
  locations = ["aws:us-east-1", "aws:us-west-2"]

  request_definition {
    method = "GET"
    url    = "https://api.[your-company].com/health"
  }

  assertion {
    type     = "statusCode"
    operator = "is"
    target   = "200"
  }

  assertion {
    type     = "responseTime"
    operator = "lessThan"
    target   = "200"
  }

  options_list {
    tick_every = 300  # 5 minutes
    retry {
      count    = 2
      interval = 300
    }
  }

  message = "[your-org]-api health check failed from ${locations}. @pagerduty-[your-org]-revenue-critical"
  tags    = ["env:production", "service:[your-org]-api", "tier:revenue-critical"]
}

resource "datadog_synthetics_test" "ssl_cert" {
  name      = "[your-org]-api SSL certificate expiry"
  type      = "api"
  subtype   = "ssl"
  status    = "live"
  locations = ["aws:us-east-1"]

  request_definition {
    host = "api.[your-company].com"
    port = 443
  }

  assertion {
    type     = "certificate"
    operator = "isInMoreThan"
    target   = "30"  # days until expiry
  }

  options_list {
    tick_every = 86400  # daily
  }

  message = "SSL cert expires in <30 days. Renew immediately. @slack-[Your Company]-engineering"
  tags    = ["env:production", "service:[your-org]-api", "compliance:pci"]
}
```

## Log Management Agent Config

Agent-level configuration (in `datadog.yaml` or per-integration `conf.yaml`). Applied before logs leave the host.

```yaml
# Exclude health check noise
logs_config:
  processing_rules:
    - type: exclude_at_match
      name: exclude_health_checks
      pattern: "GET /health HTTP"
    - type: exclude_at_match
      name: exclude_internal_status
      pattern: "GET /status HTTP"

# PII scrubbing — data never reaches DD servers
    - type: mask_sequences
      name: redact_credit_card
      pattern: "\\b\\d{4}[- ]?\\d{4}[- ]?\\d{4}[- ]?\\d{4}\\b"
      replace_placeholder: "[CC_REDACTED]"
    - type: mask_sequences
      name: redact_email
      pattern: "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+"
      replace_placeholder: "[EMAIL_REDACTED]"
```

These are agent-level configs, NOT Terraform resources. Managed via ECS task definition environment or config file mounts.

## DogStatsD Custom Metrics

UDP port 8125. Zero auth, fire-and-forget. For application-level telemetry not available via APM or log-based metrics.

```python
from datadog import initialize, statsd

initialize(statsd_host="127.0.0.1", statsd_port=8125)

# Counter: increment on each event
statsd.increment("[your-company].api.requests.count", tags=["endpoint:/checkout", "status:200"])

# Histogram: track distribution of values
statsd.histogram("[your-company].api.request.duration_ms", duration_ms, tags=["service:ordering"])

# Gauge: point-in-time value
statsd.gauge("[your-company].worker.queue.depth", len(queue), tags=["worker:segmentation"])
```

**Naming convention:** `[your-company].<service>.<metric>` (matches existing log-based metric naming).

**When to use DogStatsD vs other sources:**
- APM traces available → use traces (zero application code changes)
- Structured JSON logs available → use log-based metrics (cheaper than full indexing)
- Neither available → DogStatsD (requires application code instrumentation)
