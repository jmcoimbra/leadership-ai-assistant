# AWS Cloud Architecture

**Added:** 2026-04-02
**Last Updated:** 2026-04-02
**Owner:** [Brain Owner] | **Pillar:** Pillar 5 (Play Big) | **Measurable Outcome:** Brain auto-loads AWS context when infrastructure topics discussed | **Escalation Trigger:** If file exceeds 300 lines, compress or split by domain. Security split completed 2026-04-02 → `aws-security.md`

> Cross-references: `[your-org]-services.md` (account topology, SSM, ECS), `sre-operations.md` (runbooks, SLIs), `compliance-evidence.md` (GuardDuty, Drata), `datadog-observability.md` (CloudTrail monitoring)

---

## Compute

**EC2 Instance Family Quick Reference**
- T (T3/T4g): burstable, CPU credits. Watch credit exhaustion. Dev/test or variable workloads
- M (M6i/M6g): balanced. Start here if unsure
- C (C6g/C7g): compute-intensive. HPC, video encoding, ML training
- R (R6g): memory-intensive. In-memory DBs, analytics
- I (I4i): storage-optimized NVMe SSD. Low-latency I/O
- P/G/Inf: GPU (P4d training, G5 inference, Inf1 AWS Inferentia chip 70% lower cost)

**Graviton ARM**: 40% better price-performance. Use for web servers, containers, open-source stacks (Java, Python, Ruby, Node.js)

**Pricing Decision**: On-Demand (spikes) → Savings Plans (steady state, 72% off) → Spot (batch/stateless, 90% off, 2-min warning)

**Auto Scaling**: Target tracking (CPU 50%) as default. Step scaling for multi-threshold. Always deploy across 3+ AZs

**Lambda vs EC2 vs Fargate**
| Factor | Lambda | Fargate | EC2 |
|--------|--------|---------|-----|
| Max runtime | 15 min | Unlimited | Unlimited |
| Ops overhead | Zero | Minimal | Full |
| GPU | No | No | Yes |
| Cold start | 100ms-1s | None | None |
| Best for | Event-driven, short tasks | Containers, low ops | Full control, GPU, custom OS |

**Lambda specifics**: Memory 128MB-10GB (CPU proportional). Provisioned concurrency for cold start elimination. SnapStart for Java. ARM64 recommended. VPC access requires ENIs in subnets

---

## Networking

**VPC Design Rules**
- CIDR: largest /16, cannot be changed after creation. Plan bigger than current need
- Subnets: public (IGW route), private (NAT GW route), isolated (no internet). 3-tier pattern: LB/app/DB
- NAT Gateway: one per AZ for HA. Use over NAT Instance for production
- AWS reserves first 4 and last IP per subnet (.0 network, .1 router, .2 DNS, .3 future, .255 broadcast)

**VPC Peering vs Transit Gateway**: <10 VPCs needing mesh = peering. >10 or transitive routing = TGW. Peering scales as n(n-1)/2

**Security Groups vs NACLs**: SGs = stateful, allow-only, instance-level (primary control). NACLs = stateless, allow+deny, subnet-level (defense-in-depth for IP blocks)

**VPC Endpoints**: Gateway (free, S3/DynamoDB only). Interface/PrivateLink (paid, most services). Use for SSM/KMS/Secrets Manager to avoid NAT costs

**Load Balancers**: ALB (L7, HTTP, path/host routing, WAF, default choice) vs NLB (L4, static IP, PrivateLink, extreme throughput) vs GWLB (L3, firewalls/IDS)

**Route 53**: Simple | Weighted (canary) | Latency | Failover (active-passive) | Geolocation. Alias records = zero DNS query cost for AWS resources. 100% SLA

**CloudFront vs Global Accelerator**: CloudFront = HTTP caching + dynamic. GA = TCP/UDP, static anycast IPs, 30s failover

---

## Storage

**S3 Classes**: Standard (default) → Standard-IA (30d min, <1x/mo) → One Zone-IA (reproducible data only) → Glacier Instant (quarterly) → Glacier Flexible (min-hours) → Deep Archive ($0.00099/GB/mo, 12-48h)

**S3 Performance**: 3,500 PUT + 5,500 GET per prefix per second. Multipart upload >100MB. Transfer Acceleration for cross-region

**S3 Security**: Bucket Keys reduce KMS API calls 99%. Object Lock (WORM). Public Access Block at account+bucket level. Access Points for scoped policies

**EBS Types**: gp3 (default, 3K baseline IOPS, independent tuning, 20% cheaper than gp2) | io2 (sub-ms latency, databases) | st1 (sequential HDD) | sc1 (cold HDD)

**EFS**: NFSv4.1, multi-AZ, elastic. Linux only. Standard + IA tiers. Use FSx for Windows (SMB) or Lustre (HPC)

---

## Databases

**Selection Flowchart**: Relational+ACID → Aurora (default) or RDS. Key-value → DynamoDB. Document/MongoDB → DocumentDB. Graph → Neptune. Time-series → Timestream. Search → OpenSearch. Analytics → Redshift/Athena

**Aurora Key Properties**: 6 copies across 3 AZs. Up to 15 read replicas (<10ms lag). Auto-scaling storage 10GB-128TB. Serverless v2 (instant scaling, no cold start). Global Database (<1s cross-region replication)

**Multi-AZ vs Read Replicas**: Multi-AZ = HA/failover (synchronous, not readable). Read Replicas = read scaling (async, cross-region possible)

**RDS Proxy**: Connection pooling. Required for Lambda→RDS (prevents connection exhaustion). 66% faster failover. Enforces TLS

**DynamoDB Design**: Partition key = high cardinality. GSI (default, anytime, eventually consistent) vs LSI (creation-only, 10GB limit, strong consistency). On-Demand for unpredictable, Provisioned+Auto Scaling for steady state. Item max 400KB

**DynamoDB Streams**: CDC with 24h retention. Triggers Lambda. Use for replication, materialized views, event-driven flows

**Caching**: ElastiCache Redis (default choice: persistence, replication, pub/sub, data structures) vs Memcached (simple string cache, multithreaded). DAX for DynamoDB-only microsecond reads

**Caching Strategies**: Cache-Aside (lazy, default) | Write-Through (always fresh, higher write latency) | Write-Behind (lowest write latency, data loss risk) | Refresh-Ahead (pre-emptive, eliminates miss latency)

---

## Security & IAM

> Full coverage moved to `cloud-security.md`. Quick reference kept here; deep patterns (defense-in-depth, microservice security, encryption, IAM advanced, incident response) in dedicated file.

**Policy Evaluation**: Explicit Deny > SCPs > Permission Boundaries > Identity-based > Resource-based. All denied by default

**IAM Quick Ref**: Roles over users. IMDSv2 required on EC2. IAM Access Analyzer for least-privilege. Permissions Boundaries for delegation

**Encryption Quick Ref**: KMS (CMK for control, CloudHSM for FIPS L3). EBS default encryption per region. S3: SSE-S3 default, SSE-KMS for audit trail

**Compliance Stack**: CloudTrail → Config → GuardDuty → Security Hub → Macie

---

## Containers

**ECS Fargate vs EC2**: Fargate = zero ops, per-task billing, no GPU, no privileged containers. EC2 = fleet management, GPU support, Reserved pricing for steady state. Start with Fargate, move to EC2 for GPU or 30%+ cost savings on reserved

**ECS Networking**: awsvpc (recommended, each task gets ENI+IP, required for Fargate). Task def: `executionRoleArn` for ECS agent, `taskRoleArn` for app code

**ECS Blue/Green**: CodeDeploy manages two ALB target groups. Strategies: AllAtOnce, Canary (10%→90%), Linear (10% every N min). AppSpec defines task def ARN

**EKS over ECS**: Multi-cloud portability, existing K8s expertise, complex scheduling (affinity, StatefulSets). Otherwise ECS is simpler

**ECR**: Enable `scanOnPush`. Lifecycle policies to expire untagged images. Immutable tags for production repos

---

## Serverless & Microservices

**API Gateway**: REST API (caching, WAF, usage plans, higher cost) vs HTTP API (70% cheaper, simpler). Direct DynamoDB integration skips Lambda for simple CRUD

**Step Functions**: Standard (1yr max, exactly-once, $0.025/1K transitions) vs Express (5min max, at-least-once, $1/1M executions). Type is immutable

**Messaging Decision**: SQS (single consumer, pull-based, work queue) | SNS (fan-out, push) | EventBridge (content-based routing, SaaS events, cross-account) | Kinesis (real-time streaming, ordered, replay)

**SQS**: Long polling always (WaitTimeSeconds=20). DLQ always configured. FIFO only when ordering/dedup non-negotiable (300 TPS limit). Max 256KB, use S3 for larger

**Microservices Patterns**: Saga (Step Functions for orchestration, EventBridge for choreography). Circuit breaker (App Mesh/Envoy). Service discovery (Cloud Map). Event-driven > synchronous chains

---

## Architecture & Well-Architected

**6 Pillars**: Operational Excellence (IaC, runbooks) | Security (IAM, encryption, detection) | Reliability (Multi-AZ, DR strategies) | Performance (right-sizing, caching) | Cost (Savings Plans, tagging) | Sustainability (region selection, utilization)

**DR Strategies** (ascending cost/RTO):
| Strategy | RTO | RPO | Cost |
|----------|-----|-----|------|
| Backup & Restore | Hours | Hours | $ |
| Pilot Light | 10min | Minutes | $$ |
| Warm Standby | Minutes | Seconds | $$$ |
| Multi-Site Active/Active | Near-zero | Near-zero | $$$$ |

**CAP Theorem on AWS**: DynamoDB = AP (eventually consistent default, optional strong). Aurora = CP (strong consistency, availability via Multi-AZ). ElastiCache Redis = AP (replication lag)

**Scaling Evolution**: Single server → Separate DB → Multi-AZ → Read replicas → Caching → Auto Scaling → CDN → Microservices → Event-driven

**IaC Decision**: CloudFormation (AWS-native, tight integration) vs CDK (programmatic, generates CFN) vs Terraform (multi-cloud, state management). [Your Company] uses Terraform

---

## Big Data & Analytics

**Streaming**: Kinesis Data Streams (custom consumers, sub-second) vs Kinesis Firehose (S3/Redshift delivery, 60s+) vs MSK (Kafka compatibility)

**ETL**: Glue (serverless Spark, catalog-driven) vs EMR (full Hadoop ecosystem). Start with Glue, EMR for non-Spark engines or fine-grained tuning

**Query**: Athena (serverless SQL on S3, $5/TB scanned, use Parquet+partitions for 90% cost reduction) vs Redshift (persistent cluster, columnar OLAP, Spectrum for S3 data)

**Data Lake Zones**: Raw (untouched, append-only) → Staging (cleaned, transformed) → Analytics (Parquet, partitioned) → Data Mart (domain-specific)

**File Optimization**: Parquet/ORC for analytics. 128MB-1GB optimal for Spark/Athena. Schedule compaction jobs after streaming ingestion

---

## AI/ML Services

**No-code Services**: Rekognition (image/video) | Textract (OCR+tables) | Comprehend (NLP, PII redaction) | Translate | Polly (TTS) | Lex (chatbots) | Personalize (recommendations) | Forecast (time-series)

**SageMaker**: Training (spot instances 90% savings with checkpointing) | Endpoints (real-time, serverless, async, batch) | Model Monitor (drift detection) | Pipelines (ML CI/CD)

**Inference Hardware**: Inferentia chips 2.3x throughput, 70% lower cost vs GPU. Use for production scale. GPU for experimentation

---

## Cost Optimization

**Pricing Tiers**: On-Demand → Savings Plans (72% off, 1-3yr) → Reserved (specific instance, 72% off) → Spot (90% off, interruptible)

**Quick Wins**: gp3 over gp2 (20% cheaper). Graviton instances (40% better price-perf). S3 Intelligent-Tiering for unknown access. NAT Gateway VPC endpoints. Lambda ARM64. Right-size before reserving

**Tools**: Cost Explorer (analysis) | Budgets (alerts) | Compute Optimizer (right-sizing) | Trusted Advisor (cost checks)

---

## System Design Patterns (from Use Cases)

**URL Shortener**: Base62 encoding (7 chars = 3.5T URLs). Key Generation Service with pre-generated IDs. DynamoDB + ElastiCache for reads. Separate Creator (write) from Redirector (read) services

**Hotel Reservation**: Optimistic locking (version numbers) for low contention. Redis SET NX EX for room holds with auto-expiry. Idempotency keys in DynamoDB with TTL. CDC → Elasticsearch for search

**Universal Patterns**: Rate limiting (token bucket). Consistent hashing (for distributed cache). CDC for search index sync. Read replicas for read scaling. Geohash for location search (6 chars ~ 1.2km)

---

## Cloud Migration

**6Rs Decision Framework**
| Strategy | Effort | When to Use | AWS Tooling |
|----------|--------|-------------|-------------|
| Rehost (lift-and-shift) | Low | DC lease terminations, quick wins, cloud beginners | MGN, VM Import/Export |
| Replatform (lift-tinker-shift) | Medium | Short timeline + tangible benefit (e.g., self-managed DB→RDS) | DMS, Elastic Beanstalk |
| Repurchase (drop-and-shop) | Low-Med | Third-party deps, standard functions only | AWS Marketplace |
| Refactor/Rearchitect | High | All-in cloud, decoupling monoliths, long-term optimization | ECS/EKS, Lambda, Step Functions |
| Retain | None | Recent investments, strict data residency, incompatible legacy | N/A |
| Retire | None | No production value, duplicate functionality, vulnerable | N/A |

**Migration Phases**: Assess (discovery, dependency mapping, TCO) → Mobilize (landing zone, 6Rs rationalization) → Migrate (wave-based, non-disruptive testing) → Modernize (optimize post-migration)

**Migration Tooling**: Migration Hub (central dashboard) | Application Discovery Service (dependency mapping, feeds TCO) | MGN (automated lift-and-shift, replaces CloudEndure) | DMS (database migration with CDC for zero-downtime) | SCT (schema conversion for heterogeneous migrations)

**Migration Waves**: Group apps by dependency clusters. Least-dependent first. Migration factory = repeatable process (discover→design→build→integrate→validate→cutover) per wave

---

## Application Modernization

**Decomposition Sequence**: (1) Simple edge services → (2) Least-dependent services → (3) Sticky features incrementally → (4) Data stores last (hardest). Prerequisites: CD pipelines, distributed monitoring, service mesh, container orchestrator operational

**Strangler Fig (Migration-Level)**: Transform → Run in parallel (incremental traffic shift) → Replace. Start with simple, well-tested, frequently-changed, low-tech-debt components

**Decomposition Patterns**: By Business Capability (stable hierarchical) | By Subdomain (DDD-based) | Fine-grained SOA. Polyglot persistence: each microservice owns its data store

**Modernization Stages**: (1) Enable accessibility (SaaS) → (2) Integrate with cloud-native (most value) → (3) Move complex legacy. Migration = survival. Modernization = competitive advantage

---

## Cloud Governance

**Landing Zones**: Control Tower orchestrates Organizations + IAM Identity Center + Service Catalog. OU hierarchy: Security, Infrastructure, Workloads, Sandbox. Account vending via Service Catalog

**Guardrails**: Preventive (SCPs) | Detective (AWS Config rules). Mandatory always-on. Recommended per org risk appetite

**CCoE**: Cloud Business Office (governance, evangelism) + Cloud Engineering (execution, cost mgmt, reference architectures). Tenets: experiment-driven, continuous optimization, reusable architectures, active evangelism

---

## Cloud Economics / FinOps

**TCO Analysis**: On-prem (hardware + facilities + staffing + licensing) vs cloud (compute + storage + transfer + managed). Include migration costs. Look beyond cost: security, TTM, innovation velocity

**FinOps Stack**: Cost Allocation Tags + Cost Categories → CUR → CUDOS Dashboard (QuickSight). Dedicated CCoE team owns cross-org spend

**CFM Matrix**: Organize (tags) → Report (CUR + Cost Explorer) → Forecast/Budget (Budgets with alerts) → Purchase (RI/SP/Spot) → Elasticity (Auto Scaling + Instance Scheduler) → Right-size (Compute Optimizer)

**Instance Scheduler**: Stop EC2/RDS when idle. Quick win to avoid lift-and-shift cost trap

---

## Data Modernization

**DB Migration**: Homogeneous (same engine, DMS only) vs heterogeneous (SCT for schema + DMS with CDC for zero-downtime). Purpose-built selection: workload type × data structure × performance × ops overhead

**Data Lake Architecture**: Ingestion (AppFlow/DMS/Kinesis) → Storage (S3/Redshift) → Catalog (Lake Formation) → Processing (EMR/Glue) → Consumption (Athena/QuickSight/SageMaker)

**Data Mesh**: Centralized catalog + governance (Lake Formation). Decentralized data product ownership. Hub-and-spoke model

---

## Hybrid & Edge Networking

**Hybrid Connectivity**: Direct Connect + Local Zones for ultra-low latency during phased migration. Patterns: Network-to-VPC, Remote access-to-VPC, VPC-to-VPC

**Outposts**: Managed AWS on-premises (42U rack or 1U/2U server). Data residency, local processing, hybrid consistency

**VPC Lattice**: App-layer service-to-service connectivity across EC2/containers/serverless with IAM-native auth

**Wavelength**: Compute at 5G edge for single-digit ms latency (connected vehicles, AR/VR)
