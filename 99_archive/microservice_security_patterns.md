# Microservice Security Patterns

## Ch 1: Introduction to Cloud Microservices
- Microservices + DDD = bounded contexts aligned to business domains. Security benefits: blast radius isolation
- Shared responsibility model: IaaS (customer secures OS+app), PaaS (provider secures platform), SaaS (provider secures all)
- Fargate/Lambda: AWS secures infrastructure. Customer only secures application code

## Ch 2: Authorization and Authentication Basics
- RBAC for microservices: roles per task, PoLP on what role can do AND who can assume role
- Block containers from reaching host metadata service unless same trust level
- Instance metadata / workload identity preferred over static API keys
- Three auth patterns: API keys (simplest, no rotation), OAuth 2.0 (delegated, scoped), SAML 2.0 (enterprise SSO)
- JWT: signed claims. Verify signature + expiry + audience at every service. Never trust unsigned

## Ch 3: Foundations of Encryption
- Never implement custom crypto. Use NIST-standardized library implementations only
- KMS key types: AWS-managed (free, no control), CMK (full control, audit trail), CloudHSM (FIPS L3)
- SSE (server-side): provider handles DEK creation/wrapping. Default and sufficient for most
- CSE (client-side): encrypt before sending. Required when you don't trust storage service
- KMS throughput limits per region. Cached DEKs via envelope encryption avoid per-row KMS calls
- Break-glass for keys: must exist, must be noisy, must not be usable without detection

## Ch 4: Security at Rest
- S3: SSE-S3 (default, free), SSE-KMS (audit trail, cross-account access control), SSE-C (customer key, customer responsibility)
- S3 Object Lock (WORM): compliance mode (nobody can delete) vs governance mode (admins can override)
- RDS encryption: enable at creation (cannot enable later). Covers: storage, backups, snapshots, read replicas
- DynamoDB: encryption at rest default (AWS-owned key, no audit). CMK option for CloudTrail audit trail
- EBS: enable default encryption per region. Covers volume + snapshots. gp3 default

## Ch 5: Networking Security
- Microsegmentation two-phase: Isolate (domain VPCs) then Connect (legitimate links with controls)
- Private subnets default. Public only for internet-routable
- Service endpoints: managed services reachable via VPC virtual IP only. Stolen creds useless without VPC access
- Internal denied connections = signal (lateral movement or misconfiguration)
- AZ IDs differ across accounts. Never reference AZs by name in cross-account configs

## Ch 6: Public-Facing Services
- Minimize edge business logic. Core in private backend
- API Gateway: single entry point. VPC links keep backend private
- Three authorizers: IAM (SigV4), Cognito (JWT), Lambda (custom). Every request authenticated
- Rate limiting: sustained + burst per account. Per-client via usage plans + API keys. 429 triggers backoff
- CloudFront OAI restricts S3 to CF only
- Lambda@Edge: inject security headers on viewer response. Bot mitigation on viewer request
- Bastion: dedicated subnet, NACLs, VPN-required. Prefer SSM Session Manager

## Ch 7: Security in Transit
- TLS 1.3 minimum. PFS (ECDHE) mandatory. Validate certificates against trusted CA always
- ACM Private CA: internal mTLS. Dedicated AWS account. Share via RAM
- CA hierarchy: root CA for central services, subordinate CAs per domain
- ALB terminates TLS. For end-to-end: re-encrypt behind ALB or NLB passthrough
- App Mesh mTLS: Envoy sidecars, certs in memory only, auto-renew 35 min. Enable strict mode
- App Mesh limitation: app-to-sidecar communication unencrypted
- SQS: enforce `aws:SecureTransport` condition. Combine with KMS at rest
- VPN adds complexity without security gain when TLS already in place

## Ch 8: Security Design for Organizational Complexity
- Multi-account: one per bounded context. OrganizationAccountAccessRole auto-created
- OUs mirror org hierarchy. SCPs = permission ceiling per OU
- Permission boundaries: cap delegated admin permissions. Prevent escalation
- Privilege elevation: (1) SSM Run Command for known incidents, (2) BTG for unknown
- BTG: pre-create emergency roles. Senior adds dev to trust boundary. Revoke after. CloudTrail logs everything
- Conway's law applies to security. STOSA pattern: align accounts to bounded contexts
- SCP examples: deny creation without tags, restrict resource types, prevent CloudTrail disable

## Ch 9: Monitoring and Incident Response
- NIST IR-4: Design/Prep > Detection/Analysis > Containment > Forensics > Eradication > Post-Incident
- CloudTrail: 3 event types: Management (free, control plane), Data (high-volume, optional), Insights (anomaly aggregation)
- VPC flow logs: logged outside network path (no latency impact). Establish baseline, detect deviation
- CloudWatch vs CloudTrail: CW = application logs, CT = API/infrastructure logs
- Composable monitoring: multiple specialized tools loosely coupled. Right tool per microservice language/domain
- EventBridge: stream all account events, filter via rules, route to SNS/Lambda for response
- Containment: compromised infra = snapshot > freeze > isolate (NACLs) > deregister from LB/ASG > tag for forensics
- Containment: compromised app = isolating infra insufficient, redeployment replicates breach
- Forensics: live-box (preserves memory, efficient) vs dead-box (snapshot-based, parallel analysis, loses memory)
- Securing security infra: encrypt CloudTrail (SSE-KMS), enable log validation (digital signatures), purpose-built logging accounts
- Purpose-built account: separate S3 buckets, no delete/read from production account, analyst roles read-only
- Macie: ML-based PII discovery in S3. Identifies sensitive data across bounded contexts
- Iterate: vulnerability may not be fully patched. Prepare to repeat steps 2-5
