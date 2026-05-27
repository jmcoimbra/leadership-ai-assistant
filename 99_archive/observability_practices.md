# Observability Practices

## Ch 1: Observability 101
- Three pillars: metrics (health), logs (why), traces (request flow). All three required
- Observable system: read any state variable + understand how it got there + no code deployment needed
- Shift alarms from low-level (CPU, memory) to user-experience (error rate, page load, conversion) as scale grows
- Structured logs (JSON key-value) over unstructured. Machine queryable across services

## Ch 2: Overview of AWS Observability Landscape
- AWS-native: CloudWatch (metrics, logs, alarms), X-Ray (traces), Container Insights, Lambda Insights
- Managed open source: AMP (Prometheus), AMG (Grafana), OpenSearch
- ADOT: universal OTEL collector. Fan-out to all backends. Config-only backend switching

## Ch 3: CloudWatch Deep Dive
- Default EC2 metrics 5-min. Detailed monitoring = 1-min. Custom metrics via agent (StatsD, Collectd)
- Retention: <60s→3h, 1-min→15d, 5-min→63d, 1h→15mo
- Four alarm types: static, anomaly detection (ML, 2-week training), composite, metric math
- Metric math: IF()+TIME_SERIES() for dynamic thresholds. FILL() for missing values
- Track alarm changes via Config rules. Horizontal/vertical annotations on dashboards
- Agent config: store in SSM Parameter Store. Deploy fleet-wide via SSM Run Command
- Logs Insights: 7 commands (display, fields, filter, stats, sort, limit, parse). Up to 20 log groups
- Metrics Insights: SQL-based, 3h window. Contributor Insights: top-N analysis from logs
- Application Insights: auto-discover resources, auto-install agent, auto-alarms

## Ch 4: X-Ray Distributed Tracing
- Segments (per-service), subsegments (downstream), traces (shared ID), service graph
- Sampling rules control cost. Annotations = indexed/searchable. Metadata = non-indexed
- Three levels: auto, library, manual. Daemon on port 2000
- ServiceLens: traces + metrics + logs correlated. Log correlation Java SDK only
- Service map: size = volume, red = 5xx, orange = 4xx

## Ch 5: CloudWatch Insights
- Logs Insights auto-discovers JSON fields. `parse` with regex for non-JSON
- Metrics Insights: SQL for real-time aggregation across namespaces
- Contributor Insights: top-N contributors (IPs, URLs) from log data
- Cost tip: metric filters on log streams cheaper than multi-dimension custom metrics

## Ch 6: Container Observability
- EKS/EC2: CloudWatch agent + Fluent Bit as DaemonSets (separate for metrics/logs)
- EKS/Fargate: ADOT as StatefulSet (no kubelet access)
- ECS Container Insights: account-level or per-cluster activation. Control costs
- ECS logging: FireLens (Fluent Bit) as sidecar. IAM: IRSA over node role
- App Mesh + X-Ray: ENABLE_ENVOY_XRAY_TRACING=1 for network metrics without code changes
- Performance logs at /aws/ecs/containerinsights/<cluster>/performance

## Ch 7: Serverless Observability
- Five metrics: Invocations, Errors, Throttles, Duration, ConcurrentExecutions
- Cold start query: filter @type="REPORT", stats count(@initDuration)
- Lambda extensions: invocation-lifecycle only. Lambda Insights via layer ARN
- Powertools: Logger (structured, cold start flag), Metrics (EMF→CW), Tracer (X-Ray + annotations)
- API Gateway: Latency - IntegrationLatency = gateway overhead
- X-Ray active tracing: TracingConfig.Mode Active + API Gateway TracingEnabled true

## Ch 8: End User Monitoring
- Synthetics: Lambda Chromium canaries, 1-60 min. Blueprints: heartbeat, API, broken link, visual diff
- Canary Recorder Chrome extension. GUI Workflow Builder for credentialed flows
- Output: metrics, X-Ray traces (Node.js), logs, HAR + screenshots to S3
- RUM: real user telemetry. JS crashes, latencies, browser/geo, bounced sessions
- Evidently: A/B testing + feature flags. Gradual dial-up. Auto-rollback via alarms

## Ch 9: OpenTelemetry on AWS
- ADOT not vanilla collector. Auto-collects AWS metadata. 3 signals: traces, metrics, logs
- Deploy: agent/sidecar or gateway mode. OTLP/gRPC for production
- Batch processing required: BatchSpanProcessor, PeriodicExportingMetricReader
- Exports to X-Ray, CloudWatch (EMF), AMP, 10+ third-party via config
- ALB X-Amzn-Trace-Id: convert OTEL trace ID to X-Ray format for correlation
- Vendor lock-in mitigation: instrument once, switch backends via config only

## Ch 10: Amazon Managed Prometheus
- PromQL-compatible. Multi-AZ. Auto-scales. Two ingestion: Prometheus remote_write or ADOT
- IAM: aps:RemoteWrite (Amazon Managed Prometheus IAM action), K8s service account, OIDC trust. Queries require SigV4
- Pair with AMG. Community dashboards: 3119/741/747/1471
- Pushgateway for short-lived jobs. Exporters: Node, Blackbox, Redis, Apache

## Ch 11: OpenSearch Service (ELK)
- Elasticsearch 7.10.2 fork. Logs + traces, NOT metrics. Query: DSL, SQL, PPL
- Nodes: Leader, Data, UltraWarm (90% cheaper), Cold. Production: dedicated masters, Multi-AZ, VPC
- Trace pipeline: OTEL > Data Prepper > OpenSearch (2 indices: raw + service-map)
- Log pipeline: App > Fluent Bit > OpenSearch HTTP
- Anomaly detection: RCF unsupervised ML. 3 storage tiers. 3 PB scale. 14-day auto backups

## Ch 12: DevOps Guru
- ML-powered AIOps. Learns from metrics/logs/events/CloudTrail. 2-3h baseline
- Boundaries: CFn stacks, tags, account, organization. Insights: reactive + proactive
- RDS requires Performance Insights. Integrations: SSM OpsCenter, SNS, CodeGuru

## Ch 13: Best Practices at Scale
- Dedicated monitoring account. Cross-account observability (no cost). CFn per source account
- Organizations method over individual linking. Metrics Explorer: tag-based dynamic dashboards
- Encrypt log groups. PII data protection policies. Monitor CW service quotas

## Ch 14: Well-Architected Operational Excellence
- Automate agent deployment via CFn/SSM/SAM. Never manual at scale
- Separate monitoring accounts (SEC01-BP01). Centralize logs to OpenSearch
- Config Conformance Pack: "Operational Best Practices for CloudWatch"
- Cost: set log retention, use metric math, filter agent output

## Ch 15: Cloud Adoption Framework
- Observability maturity: reactive (break-fix) > proactive (anomaly detection) > predictive (ML-powered)
- Subscribe to AWS Health Dashboard for observability service outages
- Agent config in S3/Git, push via SSM as change management
