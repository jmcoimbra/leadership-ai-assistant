# Cloud Modernization Practices

**Purpose:** Chapter-by-chapter extraction of migration/modernization patterns not covered in aws-cloud-architecture.md. Service-level details already captured are omitted.

## Part 1: Cloud Migration

### Ch 1: Cloud Transformation
- CapEx→OpEx shift: on-prem procurement 90-120 days vs cloud VM in minutes
- TCO drivers: hardware, IT ops staff, maintenance. Monitor cloud spending actively; migration alone does not cut costs
- Cloud adoption motivators: resilience (RTO/RPO), security (shared responsibility), cost optimization (up to 50% IT cost reduction), faster TTM (~40% with cloud-native CI/CD)
- Service model mapping: IaaS (manage OS/runtime/app/data), PaaS (app/data only), SaaS (data only). Map each workload before migrating
- Multi-cloud: vendor lock-in avoidance vs talent scarcity + cost tracking fragmentation + compliance complexity

### Ch 2: Understanding Migration
- 5-phase model: Discover > Plan > Migrate > Automate > Optimize. Skipping Discover = failure for complex dependencies
- Pre-flight blockers: no app visibility, no cloud-first mindset, talent shortage, no documented strategy, no security assessment
- Optimize checklist: monitoring, rollback capability, scaling, cost targets, RTO/RPO, runbooks, DevSecFinOps culture

### Ch 3: Preparing for Migration
- Cloud-first mindset: Assess (10,000-ft view) > Vision (future state) > Mission (measurable goals)
- Vendor lock-in mitigation: open data formats, REST APIs, containerization, Terraform, exit strategy before signing
- Pre-migration: SDLC/DevOps culture, IaC adoption, loosely coupled systems, open APIs

### Ch 4: Migration Strategies (6Rs)
- Rehost: lowest effort/risk. Tools: MGN, VM Import/Export
- Replatform: swap components with managed services (DB→RDS)
- Repurchase: replace with SaaS equivalent
- Refactor: full cloud-native rewrite. Highest risk/cost
- Retain: keep on-prem (recent investments, data residency)
- Retire: decommission no-value apps
- AWS tooling: Migration Hub, Application Discovery Service, MGN, DMS, SCT
- Migration waves: group by dependency clusters, least-dependent first. Migration factory = repeatable process per wave

## Part 2: Cloud Modernization

### Ch 5: Modernization in Cloud
- 5-step path: Align → Design → Connect → Implement → Enable
- 77% of modernization programs fail. Root cause: business-IT disconnect
- 3 stages: (1) Enable accessibility (SaaS), (2) Integrate cloud-native (most value), (3) Move complex legacy
- Migration = survival. Modernization = competitive advantage

### Ch 6: App Modernization Approaches
- Decomposition: edge services first → least-dependent → sticky features → data last
- Strangler fig: Transform → Run in parallel → Replace. Start with simple, well-tested, frequently-changed components
- Patterns: by Business Capability, by Subdomain (DDD), Fine-grained SOA
- Polyglot persistence: each microservice owns its data store
- Prerequisites: CD pipelines, distributed monitoring, service mesh, container orchestrator

### Ch 7-8: Compute + Serverless (delta only)
- 3-phase migration: Assess (Migration Evaluator + Hub) → Mobilize (6Rs) → Migrate & Modernize
- Lambda cost trap: 15-min limit. Use Step Functions for orchestration
- Fargate vs Lambda: Lambda max 3GB RAM. Fargate up to 30GB/4 vCPU

### Ch 9: Data + Analytics Modernization
- DB migration: homogeneous (DMS only) vs heterogeneous (SCT + DMS with CDC)
- Purpose-built selection: workload type × data structure × performance × ops overhead
- Data lake 5-layer: Ingestion → Storage → Catalog (Lake Formation) → Processing → Consumption
- Data mesh: centralized catalog + governance, decentralized data product ownership

## Parts 3-4: Security/Networking/Operations

### Ch 10: Security Transformation
- Shared responsibility shifts by service type: IaaS = OS patching/firewall. Managed = data encryption + access control
- DevSecOps: security in CI/CD pipeline. Zero-trust as cloud baseline

### Ch 11: Networking Transformation
- Hybrid: Direct Connect + Local Zones for phased migration
- Outposts: managed AWS on-premises for data residency
- VPC Lattice: app-layer service-to-service with IAM auth
- App Mesh (Envoy): mTLS, traffic routing, observability

### Ch 12: CloudOps / CCoE / FinOps
- CCoE: Cloud Business Office (governance) + Cloud Engineering (execution). 4 tenets: experiment-driven, optimize, reusable architectures, evangelize
- FinOps: Cost Allocation Tags + Cost Categories → CUR → CUDOS Dashboard
- CFM matrix: Organize → Report → Forecast/Budget → Purchase → Elasticity → Right-size
- Control Tower: landing zone factory. Guardrails = preventive (SCPs) + detective (Config)
- Incident Manager: Alert → Triage (P1-P5) → Investigate (SSM runbooks) → Post-incident

### Ch 13: Wrapping Up
- Migration prioritization: business importance × usage × dependency complexity × tech
- Lift-and-shift cost trap: Instance Scheduler = quick win
- Knowledge transfer: upskill teams in parallel with partner execution
