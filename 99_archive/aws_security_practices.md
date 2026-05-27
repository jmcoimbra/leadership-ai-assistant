# AWS Security Practices

**Purpose:** Raw chapter-by-chapter extraction of enforceable rules. Narrative and tutorial boilerplate discarded. Technical/Infrastructure Lens applied: decision trees, AWS-native service patterns.

## Ch 1: Introduction to AWS Security

- Shared responsibility model: AWS secures OF the cloud (physical, host OS, hypervisor, network enforcement). You secure IN the cloud (configuration, application vulnerabilities, credential safety).
- AWS responsibility ≠ guarantee. Spectre/Meltdown example: AWS responsible to patch, but window of vulnerability exists.
- All actions in AWS denied unless explicitly permitted by IAM policy. Default-deny posture.
- VPC = private network within a region. Subnets = component subnetworks (public = route to IGW, private = no route to internet).
- Security groups = stateful firewall on instances. NACLs = stateless firewall on subnets.
- Bastion host pattern: public subnet bastion → SSH → private subnet instances. 14 CloudFormation resources for 2-host SSH access.
- DevSecOps shift: managed services reduce ops headcount, security responsibility moves to developers.
- Speed of infrastructure change requires automated security (can't manually audit auto-scaling fleets).

## Ch 2: Identity and Access Management

- Two credential types: password (console only) + access key (programmatic: access key ID + secret access key). User can have both.
- Identity policy document: Statement → Effect (Allow/Deny) + Action (service:method) + Resource (ARN) + optional Condition.
- Explicit Deny always wins. Deny overrides any Allow from any policy.
- Resource block: `*` required for list/create operations (unknown ARN). Otherwise specify exact ARN.
- Condition block: IpAddress, DateGreaterThan, StringEquals, etc. Enables context-aware policies.
- NotAction/NotResource: avoid. NotAction "Deny ec2:Terminate" actually allows ALL non-EC2 actions. Confusing. Don't use without very good cause.
- Inline vs Managed policies: inline = embedded on entity, can't share. Managed = separate resource, reusable across entities. Max 10 managed policies per user, 1500 per account.
- Resource policies: attached to resources (S3 buckets, KMS keys, Lambda, IAM roles). Have Principal block. Either resource OR identity policy sufficient for Allow. Explicit Deny from either wins.
- Groups: collections of permissions applied to multiple users. Attach policies to groups, not users. Reduces API calls (14 vs 30 for 10 users × 3 policies).
- Roles: no permanent credentials. AssumeRole → temporary credentials (15 min–12 hours). Trust policy = resource policy determining who can assume. Always need identity policy on caller allowing sts:AssumeRole + identity policy on role for actual permissions.
- Policy attachment best practice: attach to groups and roles, never directly to users.

## Ch 3: Managing Accounts

- Multi-account = blast radius reduction. Logical barrier between accounts. Even admin in Account A can't touch Account B resources.
- Cross-account roles: resource policy with Principal referencing entity in another account. AssumeRole with cross-account role ARN → temporary credentials for target account.
- AWS Organizations: central management account. Service Control Policies (SCPs) restrict permissions across all member accounts. SCPs only deny, never allow new.
- SCP application: attach to organization root → applies to all accounts including central.
- SAML federation (Active Directory): AD Connector (easy, console only, requires VPN/Direct Connect) or SAML 2.0 provider (harder, supports programmatic access, works with any SAML IdP).
- Web identity federation (OIDC): AssumeRoleWithWebIdentity + auth token from provider (Google, Facebook). Temporary credentials, no hardcoded keys in mobile apps.

## Ch 4: Security Best Practices & Least Privilege

- Best practice framework: Security Value vs Convenience Cost. Evaluate against threat model.
- Threat modeling starter: architecture diagram → data sensitivity mapping → STRIDE analysis (Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege).
- Why create best practices: (1) save decision time, (2) consistency across org, (3) measurable compliance baseline.
- MFA decision: require for high-risk users (admins), optional for low-risk. Cost/benefit varies by org.
- Enforceable via IAM password policy: min length, character requirements, max age, prevent reuse. Applied account-wide. Expiration enforced immediately; complexity on next password change.
- Least privilege is hard because: (1) policies hard to write for exact permissions, (2) needed permissions unknown during prototyping, (3) nearly impossible to enforce comprehensively.
- Policy wildcards: `dynamodb:*` matches 36 actions. Most users don't need global tables, transactions, continuous backups. Use ABAC (tags) if resources change frequently, explicit ARNs if stable.
- Ban wildcards as best practice, with exceptions for auditor-type roles needing all-resource access.
- IAM Access Analyzer: analyzes resource policies for external access, generates least-privilege policies from CloudTrail activity. Use to shrink overly broad policies.
- Credential rotation: access keys should rotate every 90 days. Password expiration via password policy. Rotation reduces window of compromised credential usefulness.
- IAM reviews: periodic audit of users, groups, roles, policies. Check for unused permissions, inactive users, stale access keys. Automate with Access Analyzer + Config rules.

## Ch 5: VPC Network Security

- VPC = isolated network within region. CIDR block defines IP range. Use private ranges (10.0.0.0/8, 172.16.0.0/12). Don't overlap between VPCs if peering planned.
- Subnets exist in single AZ. Public = route to IGW. Private = no direct internet route. AWS reserves 5 IPs per subnet.
- Default VPC: 172.31.0.0/16, preconfigured with public subnets + IGW. Don't use for production—create custom.
- ENI = virtual NIC. EIP = elastic IP (public IPv4). Both auto-created with EC2 instances. Manual EIP for persistent public IP across instance lifecycle.
- IGW: bidirectional internet access. NAT Gateway: outbound only (private subnet → internet, no inbound). NAT lives in public subnet, routes through IGW. Egress-only IGW = NAT for IPv6.
- Route tables: destination CIDR → target (local, IGW, NAT GW, etc.). More specific route wins. Main route table auto-created with local route. Associate custom route tables to subnets.
- Security groups: stateful firewall on ENI. Inbound rules (source, protocol, port). Outbound rules (destination, protocol, port). Default: allow all outbound, allow inbound from same SG only. Up to 5 SGs per instance.
- SG self-referencing: instances in same SG can communicate freely. Use for internal cluster communication.
- NACLs: stateless firewall on subnets. Rules have priority number (lower = evaluated first). Must define both inbound AND outbound rules (stateless). Default: allow all.
- **SG vs NACL decision matrix:** SG = per-instance, stateful, allow-only rules. NACL = per-subnet, stateless, allow + deny rules with priority. Use SGs as primary, NACLs as defense-in-depth.
- VPC peering: private connection between two VPCs (same or different accounts/regions). Non-transitive. Must update route tables in both VPCs. CIDR blocks must not overlap.
- Site-to-Site VPN: encrypted tunnel between VPC and on-premises network via Virtual Private Gateway.

## Ch 6: Network Protection Beyond VPC

- VPC endpoints: private connection to AWS services without IGW. Interface endpoints (most services) = ENI in subnet. Gateway endpoints (S3, DynamoDB only) = route table entry.
- PrivateLink: create VPC endpoint services for your own APIs. Consumers create interface endpoint → you approve. One-directional, single endpoint. More restrictive than VPC peering.
- Why avoid public traffic: removes entire class of network attacks. No IGW = no accidental public exposure. If only reason for IGW is AWS service access, switch to VPC endpoints.
- AWS WAF: layer-7 firewall. Blocks based on HTTP request content (body size, headers, query strings, IP reputation). Attaches to CloudFront, ALB, or API Gateway—not instances.
- WAF rules: size constraints (block >1KB body), rate limiting, managed rule groups (OWASP Top 10, SQL injection, known bad inputs, OS-specific). Web ACL = container for rules.
- Managed rule groups: AWS-provided (CommonRuleSet, KnownBadInputs, SQLi, AdminProtection, IP Reputation) + third-party via Marketplace.
- WAF pricing: $5/web ACL/month + $1/rule/month + $0.60/million requests.
- Rate-based rules: block IPs exceeding threshold in 5-minute window. Simple DDoS mitigation.
- AWS Shield Standard: free, automatic, protects against common DDoS (SYN floods, UDP reflection, etc.). Covers all AWS resources.
- AWS Shield Advanced: paid ($3K/month). DRT (DDoS Response Team), cost protection during attacks, enhanced detection for ELB/CloudFront/Route 53/Global Accelerator.
- Third-party firewalls: available via AWS Marketplace. Next-gen firewalls, IDS/IPS. Deploy via Gateway Load Balancer (GWLB) for transparent inline inspection.

## Ch 7: Protecting Data in the Cloud

- Data security framework: Confidentiality (prevent unauthorized read) + Integrity (prevent unauthorized write) + Defense in Depth (redundant controls).
- Start with data flow diagrams. At each storage/transit point evaluate all three concerns.
- Encryption at rest: KMS for key management. CMK (Customer Master Key) → symmetric (default) or asymmetric. Encrypt/Decrypt API calls. Metadata in ciphertext identifies CMK—no need to specify on decrypt (symmetric only).
- Server-Side Encryption (SSE): built into S3, DynamoDB, RDS, Aurora, EBS, Redshift, CloudWatch Logs, SQS, SNS, Kinesis, etc. Two options: AWS-managed key (easier) or customer-managed KMS key (more control).
- S3 encryption: `put-bucket-encryption` with AES256 or aws:kms. Only encrypts NEW objects. Need kms:Encrypt/kms:Decrypt permissions for KMS-encrypted buckets.
- S3 bucket policies for access control: Deny + NotPrincipal pattern to restrict to specific role. Secure transport enforcement: Deny all actions where `aws:SecureTransport = false`.
- S3 ACLs: additional access mechanism. Canned ACLs (private, public-read, public-read-write, etc.). `public-read-write` = world-writable. Avoid.
- S3 versioning: enables recovery from tampering/deletion. Restores any previous version. Even deleted objects recoverable.
- DynamoDB encryption: `--sse-specification Enabled=true,SSEType=KMS` at table creation. Always encrypted in transit (HTTPS only).
- DynamoDB backups: CreateBackup + RestoreTableFromBackup. Point-in-time recovery (PITR) for continuous backups.
- Data in transit: HTTPS/TLS mandatory. S3 bucket policy enforcing SecureTransport. AWS SDK/CLI use HTTPS by default.
- Amazon Macie: ML-based classification of sensitive data in S3. Detects PII, financial data. Generates findings for unauthorized access patterns.
- Defense in depth example: S3 bucket policy (layer 1) + KMS encryption (layer 2). Even if bucket policy misconfigured, data still encrypted.

## Ch 8: Logging and Audit Trails

- Audit logs critical for: (1) verify attack happened, (2) identify vulnerability exploited, (3) determine attack extent, (4) notification requirements.
- CloudTrail: logs ALL management events (API calls, console actions). Management events = create/delete/modify resources. Data events (read/write records) = opt-in for S3, Lambda.
- Trail setup: create S3 bucket + create trail pointing to bucket. Multi-region by default. Global events (IAM) included.
- CloudTrail event record: userIdentity (type, principalId, ARN), eventTime, eventSource, eventName, sourceIPAddress, userAgent, requestParameters, responseElements.
- LookupEvents: filter by username, event name, resource type, access key, event source, read-only flag.
- Real-world investigation pattern: unexpected billing → CloudTrail EC2 events → found RunInstances for p3.16xl by compromised user at unusual hours → credential compromise confirmed.
- AWS Config: tracks resource configuration changes over time. Timeline view shows what changed and when. Links to CloudTrail events that caused changes.
- Config setup: S3 bucket + IAM role + subscribe command. Tracks all resource types.
- Config vs CloudTrail: CloudTrail = what API calls happened. Config = what was the state of resources over time. Config answers "when was this bucket first made public?" directly.
- Config conformance packs: groups of Config rules for compliance standards. Enforce across org via Organizations.
- CloudWatch Logs: centralize application logs. Agent on EC2 instances ships logs. Insights for query language (filter, aggregate, stats).
- VPC Flow Logs: capture network traffic metadata (source/dest IP, ports, protocol, action, bytes). Enable per VPC, subnet, or ENI. Stored in CloudWatch Logs or S3.
- **Org trail:** create CloudTrail trail in management account → logs all member accounts. Single source of truth.

## Ch 9: Continuous Monitoring

- Ad hoc scanning: boto3 scripts checking individual best practices (e.g., S3 encryption). Works but doesn't scale.
- Prowler: open-source CLI tool, 100+ security checks, free. Run against all resources. Output: terminal, CSV, JSON.
- Continuous monitoring: run scans on schedule (Fargate + SNS + CloudWatch Events). Issues: fixed interval (arbitrary), deduplication needed, wasteful API calls for unchanged resources.
- AWS Config rules: trigger on resource change (not polling). Managed rules for common checks (password policy, public IPs, encryption, backups, CloudTrail enabled, VPC Flow Logs). Custom rules via Lambda.
- Config rules evaluate compliance per-resource. Compliance history view shows when resource went in/out of compliance.
- Security Hub Standards: grouped Config-rule-like controls matching compliance frameworks. Available: CIS AWS Foundations, PCI-DSS, AWS Foundational Security Best Practices.
- Enable via `batch-enable-standards` with standard ARN. Shows overall score + per-control compliance.
- Amazon Inspector: agent-based host vulnerability scanner. Install agent on EC2 instances. Scans for CVEs, insecure host configurations (SSH protocol, password policies). Assessment templates, findings with severity.
- Inspector findings: CVE detection + CIS benchmark compliance (e.g., "SSH Protocol set to 2"). Severity scoring, recommendations.
- Amazon GuardDuty: analyzes CloudTrail logs, VPC Flow Logs, DNS logs. Detects: unauthorized access, compromised instances, malicious IPs, cryptocurrency mining, unusual API calls.
- GuardDuty finding types: Recon (port scanning), UnauthorizedAccess (credential compromise), CryptoCurrency (mining), Trojan (C&C communication).
- GuardDuty triage: HIGH = immediate action. MEDIUM = investigate within 24h. LOW = informational.

## Ch 10: Incident Response & Remediation

- Three tips: (1) centralize alert tracking, (2) create incident response plans (playbooks), (3) automate response.
- Security Hub core: aggregates findings from Inspector, GuardDuty, Config, Prowler (via ASFF format import), third-party tools.
- Workflow status tracking: NEW → NOTIFIED → RESOLVED / SUPPRESSED. Track progress, filter stale findings.
- Security Hub Insights: predefined + custom analytics. "Top AMIs with most findings", "IAM roles with critical findings". GroupBy attribute for aggregation.
- Playbooks: flowchart-style incident response recipes. Anyone on team should be able to follow. Steps must be specific enough for non-expert execution.
- Example playbook: S3 encryption alert → check DataClassification tag → if Sensitive, enable encryption + encrypt existing objects → resolve.
- Automated remediation: Lambda function implementing playbook logic. Triggered via EventBridge from Security Hub findings.
- Custom actions: Security Hub console button → EventBridge → Lambda. One-click remediation from dashboard.
- Fully automated response: EventBridge rule matching specific finding type (e.g., PCI.S3.4) → Lambda auto-remediates without human intervention.
- SOAR (Security Orchestration, Automation, and Response): category of tools for scaling automated incident response.

## Ch 11: Securing a Real-World Application

- Threat modeling workflow: features list → architecture diagram → data flow diagrams → OWASP Top 10 threat identification → mitigation strategies.
- OWASP Top 10 threats identified: injection (NoSQL), credential stuffing, brute forcing, cryptographic failures, broken access control, security misconfiguration (public S3), XSS, insufficient logging.
- NoSQL injection: DynamoDB FilterExpression string concatenation with user input. Attacker injects expression operators to bypass filters (e.g., bypass `private = false` filter).
- Mitigation: parameterized queries, input validation, never concatenate user input into expressions.
- Cognito user pools: managed authentication. Password complexity (min length, numbers, special chars, upper/lower). MFA via SMS or TOTP.
- Cognito advanced security: adaptive authentication (risk-based MFA: low-risk=allow, high-risk=require MFA or block) + compromised credential checks (compare against known breached credentials).
- Brute force mitigation: rate limiting on API Gateway + strong password requirements via Cognito.
- Broken access control mitigation: code review, two-person rule for manual changes, periodic IAM audits, IAM Access Analyzer.
- Config rules for admin access: `iam-policy-no-statements-with-admin-access`, `iam-user-mfa-enabled`, `iam-root-access-key-check`, `root-account-mfa-enabled`.
- Data classification system: Highly Sensitive (private photos, PII) → Sensitive (metadata, public photos) → Public (usernames, web assets). Different protections per tier.
- Highly sensitive: encrypt at rest (S3 SSE, DynamoDB KMS), enforce HTTPS (SecureTransport bucket policy), data-plane CloudTrail logging, Config rules for monitoring.
- S3 misconfiguration: never use random naming as security. Security researchers scan continuously for public buckets.
- XSS defense: input sanitization (primary) + WAF rules (secondary defense-in-depth).
- API Gateway authorization: Cognito authorizer for user APIs, IAM_AUTH for admin APIs, no auth for public endpoints. Misconfiguration = elevation of privilege.
