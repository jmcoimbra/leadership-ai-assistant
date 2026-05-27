# AWS Observability Patterns

**Added:** 2026-04-02
**Last Updated:** 2026-04-02
Concepts ported from a published observability handbook; raw chapter notes in `99_archive/observability_practices.md`

**Owner:** [Brain Owner] | **Pillar:** Pillar 5 (Play Big) | **Measurable Outcome:** Brain auto-loads AWS observability context when monitoring/tracing topics discussed | **Escalation Trigger:** If file exceeds 400 lines, split by subdomain (cloudwatch-patterns.md, otel-patterns.md)

> Cross-references: `datadog-observability.md` (Datadog-specific monitors, SIEM, security signals), `sre-operations.md` (SLIs, error budgets, alerting doctrine), `aws-cloud-architecture.md` (compute, networking), `cloud-security.md` (incident response monitoring)

---

## Observability Fundamentals

- Three pillars: metrics (quantitative health), logs (why it malfunctioned), traces (end-to-end request flow). All three required for full observability
- Observable system: read any variable affecting state + understand how it reached that state + no new code deployment needed
- Shift alarm targets from low-level (CPU, memory) to user-experience metrics (error rate, page load, conversion) as system scale grows
- Use structured logs (JSON key-value) over unstructured. Enables machine querying, slicing, aggregation across hundreds of services
- Distributed tracing: unique ID propagated via request headers across service boundaries. Required for microservices

---

## CloudWatch Metrics & Alarms

- Default EC2 metrics: 5-min intervals. Enable detailed monitoring for 1-min resolution on critical workloads
- **Retention:** <60s kept 3h, 1-min kept 15 days, 5-min kept 63 days, 1h kept 15 months
- Custom metrics: publish app/business metrics to custom namespaces via CloudWatch agent (StatsD, Collectd, procstat)
- Four alarm types: static threshold, anomaly detection (ML bands), composite (group related to reduce noise), metric math expressions
- Anomaly detection model trains on 2 weeks of data. Exclude known anomalous periods (promos). Predicts up to 2h ahead
- Use metric math IF()+TIME_SERIES() for dynamic weekday/weekend thresholds. FILL(REPEAT|LINEAR|static) for missing values
- Track alarm config changes via AWS Config rules: alarm-settings-check, alarm-resource-check, alarm-action-enabled-check
- Horizontal annotations encode tacit knowledge (SLA lines). Vertical annotations mark deployments/changes
- Cost optimization: use metric filters on log streams to create metrics (cheaper than publishing multi-dimension custom metrics)

---

## CloudWatch Logs & Insights

- Hierarchy: log event > log stream (same source) > log group (shared retention/ACL). Set retention per log group
- CloudWatch agent: IAM role (CloudWatchAgentServerPolicy), config JSON, deploy via SSM Run Command fleet-wide
- Store agent config in SSM Parameter Store for standardized deployment across fleet
- **Logs Insights:** 7 commands only: display, fields, filter, stats, sort, limit, parse. Queries up to 20 log groups simultaneously
- Auto-discovers JSON fields. For non-JSON use `parse` with regex
- **Metrics Insights:** SQL-based, real-time metric aggregation across namespaces. Limited to 3h window
- **Contributor Insights:** identify top-N contributors (IPs, URLs, accounts) causing load patterns
- **Application Insights:** auto-discovers resources, auto-installs CloudWatch agent, sets up alarms + anomaly detection

---

## X-Ray Distributed Tracing

- Vocabulary: segments (per-service), subsegments (downstream calls), traces (shared trace ID), service graph (nodes + edges)
- Sampling rules control cost: default captures representative sample. Custom rules for sensitive paths
- **Annotations** = indexed (searchable via filter expressions). **Metadata** = non-indexed. Use annotations for investigation dimensions
- Three instrumentation levels: auto (no code changes), library (SDK per language), manual (full control)
- X-Ray daemon on port 2000, auto-restarts. Deploy alongside CloudWatch agent
- ServiceLens correlates traces + metrics + logs in single view. Log correlation limited to Java SDK
- Service map: node size = request volume. Red borders = 5xx. Orange = 4xx

---

## Container Observability (ECS/EKS)

- EKS on EC2: deploy CloudWatch agent + Fluent Bit as DaemonSets (separate: one metrics, one logs)
- EKS on Fargate: no kubelet access. Use ADOT as StatefulSet instead of CloudWatch agent DaemonSet
- **ECS Container Insights:** activate at account level or per-cluster to control costs on non-production
- ECS log routing: FireLens (Fluent Bit-based) as sidecar in task definition
- IAM: avoid CloudWatchAgentServerPolicy on worker node role (grants all pods CW write). Use IRSA (IAM Roles for Service Accounts)
- App Mesh + X-Ray: `ENABLE_ENVOY_XRAY_TRACING=1` for per-service latency/error/request metrics without code changes
- Container Insights performance logs: `/aws/ecs/containerinsights/<cluster>/performance`. Query with Logs Insights for CPU/memory by task

---

## Serverless Observability (Lambda)

- Five critical metrics: Invocations, Errors, Throttles, Duration, ConcurrentExecutions. Track P50/P90/P95 duration
- Cold start detection: `filter @type = "REPORT" | stats count(@initDuration) as coldStarts, (count(@initDuration)/count(@type))*100 as pct by bin(5m)`
- Lambda extensions: run only during invocation lifecycle. Lower cost than always-on agents
- **Lambda Insights** via layer ARN: CPU, memory, network per-invocation without code changes
- **Lambda Powertools:** Logger (structured JSON, cold start flag), Metrics (EMF to CloudWatch namespace), Tracer (X-Ray subsegments + annotations)
- API Gateway overhead: `Latency - IntegrationLatency` quantifies gateway vs backend duration
- Enable X-Ray active tracing: Lambda `TracingConfig.Mode: Active` + API Gateway `TracingEnabled: true`. No code needed for service map
- **SNS→Lambda single-subscriber silent-failure pattern:** when the Lambda is the only subscriber to a topic and does not raise on downstream API errors, every SNS message succeeds from SNS's perspective while 100% of downstream calls silently fail. CloudWatch `Errors` stays at 0. Fix requires BOTH (a) handler raises on non-ok responses, (b) alarm on `AWS/Lambda Errors >= 1 over 5m` routed to on-call. Fixing (a) without (b) makes post-fix state worse-monitored than the bug. Source: 2026-04-16 [your-org]-devops#988 — `slack-alert-router` swallowed `chat.postMessage` `not_in_channel` errors for all 51 invocations over 3 days.

---

## End User Monitoring

- **CloudWatch Synthetics:** Lambda-based headless Chromium canaries (1-60 min). Blueprints: heartbeat, API canary, broken link, visual diff
- Canary Recorder: Chrome extension generates scripts. GUI Workflow Builder for credential flows via Secrets Manager
- Output: metrics (2xx/4xx/5xx, duration), X-Ray traces (Node.js), logs, HAR files + screenshots to S3
- VPC canaries for internal/intranet monitoring
- **CloudWatch RUM:** real user telemetry. JS crashes, latencies, browser/geo aggregation, bounced sessions
- **CloudWatch Evidently:** A/B testing + feature flags. Gradual traffic dial-up. Auto-rollback via alarms

---

## OpenTelemetry on AWS (ADOT)

- Use AWS Distro for OpenTelemetry (ADOT), not vanilla collector. Auto-collects AWS metadata (region, account, resource ARN)
- Three signal types: traces (spans), metrics (counter, histogram), logs (optional span correlation)
- Deploy modes: agent/sidecar (simpler, higher per-task overhead) or gateway (one per team/AZ, scales independently)
- OTLP/gRPC for production (faster than HTTP). Console exporter for local dev only
- Batch processing required: `BatchSpanProcessor` for traces, `PeriodicExportingMetricReader` for metrics
- ADOT exports to: X-Ray (traces), CloudWatch (metrics via EMF, logs), AMP (Prometheus), and 10+ third-party backends via config-only change
- Vendor lock-in mitigation: instrument once with OTEL SDK, switch backends by changing collector config. No app code changes
- ALB injects `X-Amzn-Trace-Id`. Convert OTEL trace ID to X-Ray format for cross-service correlation

---

## Amazon Managed Prometheus (AMP)

- Fully managed Prometheus-compatible. PromQL, scrape format. Multi-AZ default. Auto-scales
- Two ingestion paths: (1) Prometheus server `remote_write`, (2) ADOT collector with Prometheus receiver + AMP exporter
- IAM: `aps:RemoteWrite` (Amazon Managed Prometheus IAM action) permission, K8s service account annotated with IAM role ARN, OIDC trust relationship
- API queries require SigV4 signing. Use `awscurl` or SigV4 Proxy
- Pair with Amazon Managed Grafana (AMG). AMG auth: IAM Identity Center or SAML
- Community dashboards: 3119 (cluster CPU/mem), 741 (deployment-level), 747 (pod-level), 1471 (app request rate/error/latency)
- Pushgateway required for short-lived jobs/batch processes
- Exporters: Node Exporter (system), Blackbox (probes), Redis, Apache. Deploy as standalone or sidecar

---

## Amazon OpenSearch Service (ELK)

- OpenSearch = Elasticsearch 7.10.2 fork (Apache 2.0). Includes security, ML, alerting. Use for logs + traces, NOT metrics
- Node types: Leader (cluster mgmt), Data (indexes + search), UltraWarm (S3-backed read-only, 90% cheaper), Cold Storage (S3, attach on-demand)
- Production: dedicated masters, Multi-AZ. Deploy inside VPC (private endpoint). Public access for dev/test only
- **Trace ingestion:** OTEL collector > Data Prepper 2.0 > OpenSearch HTTPS. Two indices: `trace-analytics-raw` + `trace-analytics-service-map`
- **Log ingestion:** Application > Fluent Bit > OpenSearch via HTTP output plugin
- Anomaly detection: Random Cut Forest (unsupervised ML). Configurable interval (default 10 min). Real-time + historical
- Three storage tiers: Hot (full perf) > UltraWarm (90% cheaper, read-only) > Cold (cheapest, attach-on-demand)
- Security: KMS encryption, node-to-node encryption, HTTPS, IAM/Cognito/SAML auth, fine-grained access. HIPAA/PCI/SOC/ISO compliant
- Query: OpenSearch DSL, SQL, PPL. Free automated backups 14 days. Single cluster scales to 3 PB

---

## ML-Powered Observability (DevOps Guru)

- ML-powered AIOps. No ML experience needed. Learns from metrics, logs, events, CloudTrail
- Boundaries: CloudFormation stacks, tags, account-level, or organization-level
- Two insight types: reactive (MTTR reduction) and proactive (predict before disruption)
- RDS: enable Performance Insights first. DevOps Guru detects problematic SQL, resource exhaustion
- Integrations: SSM OpsCenter, SNS (Slack/ServiceNow), CodeGuru Profiler
- Allow 2-3 hours after enabling for baseline learning

---

## Best Practices at Scale

- Multi-account: dedicated monitoring account under Infrastructure OU. CloudWatch cross-account observability (no additional cost)
- Cross-account: monitoring account queries source accounts. Data stays in source. CFn template per source account
- Prefer AWS Organizations method over individual account linking
- CloudWatch Metrics Explorer: tag-based dynamic dashboards. Auto-adds new resources (ASG instances)
- Encrypt log groups with KMS. Enable data protection policies for PII masking
- Monitor CloudWatch service quotas via metric math dashboards
- Agent config: store in S3/Git, push via SSM automation as change management

---

## Decision Matrix: When to Use Which

| Need | Tool | Why |
|------|------|-----|
| Multi-backend export or vendor lock-in risk | OTEL/ADOT | Instrument once, switch backends via config |
| AWS-only, minimal config | CloudWatch SDK | Native integration, alarm-based alerting |
| Prometheus/PromQL expertise, K8s-heavy | AMP + AMG | Grafana dashboards, PromQL queries |
| Full-text log search, trace analytics, anomaly detection | OpenSearch | DSL/SQL/PPL, RCF ML, 3 PB scale |
| Simpler log aggregation, Insights queries | CloudWatch Logs | Tighter AWS-native integration |
| Universal collector | ADOT | Fan-out to CloudWatch, AMP, OpenSearch, third-party |

**Cost hierarchy:** CloudWatch (per metric/log/query) < AMP (per samples) < OpenSearch (per instance + storage). Choose based on scale breakpoint.
