# Cloud Security Patterns

**Added:** 2026-04-02
**Last Updated:** 2026-04-02
**Sources:**

**Owner:** [Brain Owner] | **Pillar:** Pillar 5 (Play Big) | **Measurable Outcome:** Brain auto-loads cloud security context when infrastructure security topics discussed | **Escalation Trigger:** If file exceeds 400 lines, split by subdomain (network-security.md, iam-patterns.md)

> Cross-references: `aws-cloud-architecture.md` (compute, networking, storage basics), `sre-operations.md` (SLIs, error budgets), `compliance-evidence.md` (SOC 2 controls, Drata), `datadog-observability.md` (security monitoring, GuardDuty integration), `aws-observability.md` (CloudWatch, X-Ray, OTEL)

---

## Security Principles

- **Defense in depth:** any single control must have a backup. Ask "what if this fails?" for every control. 2 independent controls at 95% effectiveness = 99.75% combined
- **Zero trust:** require encryption + authentication for ALL connections, even within "trusted" networks. Challenge trust at every boundary
- **Least privilege** applies to automation equally (arguably more) than humans. Deny-by-default. A component reading a DB must not have write credentials
- **Asset-oriented threat modeling:** identify what to protect (data), who attacks it (criminals, insiders, state actors), where trust boundaries are. Mitigations go on trust boundary crossings
- **Shared responsibility model:** data access security is ALWAYS customer responsibility. Most S3 breaches stem from assuming the provider handles access control
- **Risk response options:** avoid (turn off), mitigate (reduce likelihood/impact), transfer (cloud provider), accept (documented + stakeholder-approved). Undocumented acceptance = negligence
- **Kerckhoffs's principle:** system must be secure even if everything except the key is public knowledge. Never rely on algorithm secrecy

---

## IAM & Access Control

- Separate authentication (proving identity) from authorization (granting access). Revoke the permission, not the person
- IAM lifecycle: Request > Approve > Create/Grant > Authenticate > Review/Revoke. Missing review = permission drift guaranteed
- Non-human identities (service accounts, automation) need same lifecycle rigor as human identities
- MFA non-negotiable for: console/API access, sensitive data, password resets, privileged ops. FIDO2/passkeys strongest (phishing-resistant). SMS deprecated (SIM cloning)
- Step-up authentication: require additional factors for high-risk transactions within authenticated sessions
- Long-lived tokens survive password changes and identity deletion. Offboarding must revoke ALL tokens
- SSO via SAML 2.0 or OIDC: fewer credentials = smaller attack surface + better UX
- Never store secrets in source code. Deployment = code + config + secrets, each from separate sources
- Prefer workload identity (SPIFFE/SPIRE, instance metadata) over static API keys
- RBAC for microservices: create roles per task, apply PoLP separately to (a) what role can do and (b) who can assume role
- Password hashes: scrypt, bcrypt, PBKDF2, or Argon2 only. SHA-256 is fast by design = terrible for passwords

---

## Data Protection & Encryption

- Classify data: 3 levels max (public, private, confidential). Tag every cloud resource with classification. Tags are free
- **Encryption strategy:** decide BEFORE creating storage. Changing later is painful
- Encryption layers bottom to top: disk > platform/DB > application. Higher = more attack types blocked, fewer DB features (no search/sort/index on encrypted fields)
- Application-level encryption: crown-jewel data only (PII, financial). Platform handles the rest
- **Envelope encryption:** CMK (stays in KMS, never leaves) wraps DEK. DEK encrypts data. Wrapped DEK stored alongside ciphertext. Plaintext DEK deleted after use
- **Cryptographic erasure:** delete the KEK in KMS to instantly render all data unrecoverable. Faster than overwriting terabytes
- KMS encryption context (AAD): bind ciphertext to non-secret attribute (e.g., username). Decryption fails if context mismatch. Logged in CloudTrail
- KMS has account-wide throughput limits per region. Envelope encryption with cached DEKs avoids KMS call per row
- Tokenization: replace sensitive data with random tokens (same format). Best for credit cards. Combine with encryption
- Quantum risk: AES-256 at rest safe for foreseeable future, but RSA/ECC key-wrapping needs quantum-safe migration. Harvest-now-decrypt-later is active threat
- Break-glass for encryption keys: must exist, must be noisy (alerts + audit trail), must not be usable undetected
- SQS transit security: enforce `aws:SecureTransport` condition in resource-based IAM policy to deny non-TLS connections

---

## Network Security

- **Microsegmentation** by business domain (bounded context), not technology layer. One VPC per domain. Bad DDD = excessive cross-VPC traffic
- Two-phase approach: Phase 1 (Isolate) segments into domain-specific VPCs. Phase 2 (Connect) enables only legitimate cross-domain links with controls
- Default all services to private subnets. Public subnet only for internet-routable components. Single most impactful network control
- Internal segmentation denied connections are either lateral movement or misconfiguration. Both must be investigated. Internal denials are signal
- Service endpoints make managed services reachable only via VPC virtual IP. Even with stolen credentials, attacker must be inside VPC

### TLS & Transit Security
- TLS everywhere crossing a physical or virtual boundary. Exception: localhost/loopback within same VM or same K8s pod
- Enforce TLS 1.3 minimum. Enable PFS ciphers (ECDHE). PFS ensures compromising server key does not expose recorded sessions
- Generate new private keys on every certificate renewal. Automate via ACM or Let's Encrypt
- ACM Private CA for internal microservice mTLS. Host private CAs in dedicated AWS account. Share via RAM
- ALB always terminates TLS (L7 inspection). For end-to-end encryption, re-encrypt behind ALB or use NLB with TLS passthrough
- mTLS: App Mesh + ACM-PCA automates cert distribution to Envoy sidecars. Certs stored in memory only, auto-renew within 35 min. Enable strict mode

### Public-Facing & Edge Security
- Minimize business logic at edge. Core functionality in private backend. Edge: auth, rate limiting, request validation only
- API Gateway as single entry point. VPC links (NLB/ALB) keep backend private. Three authorizer types: IAM (SigV4, service-to-service), Cognito (JWT, end-user), Lambda (custom auth)
- CloudFront OAI: restrict S3 access exclusively to CloudFront. Disable all other public paths
- AWS WAF on CloudFront/API Gateway/ALB. Enable managed rule sets (SQLi, XSS) as baseline. Add rate-based rules. WAF without maintained rules = compliance theater
- Shield Standard: always-on L3/L4 DDoS. Shield Advanced: NACLs promoted to AWS border during attacks, DDoS Response Team, cost protection credits
- Autoscaling during DDoS without perimeter protection = paying to absorb malicious traffic. Shield + WAF must block at edge first
- Egress filtering: (1) SG/NACL outbound port restrictions, (2) IP allowlisting, (3) explicit forward proxy (most effective). Block DNS/ICMP tunneling
- IDS/IPS adds most value for internal lateral movement detection, not perimeter (WAF covers that)

---

## Organizational Security Design

- **Multi-account structure:** one AWS account per bounded context. Single-account = blast radius of root compromise is everything
- SCPs at each OU level define maximum permissions (ceiling, not floor). Effective permissions = intersection of SCP and IAM policy
- Permission boundaries: cap maximum permissions delegated admin can grant. Prevent privilege escalation
- **Break-the-Glass (BTG) protocol:** pre-create emergency roles. Senior stakeholder adds developer to role trust boundary during incident. Revoke immediately. Log everything via CloudTrail
- If developers trust BTG process, they accept stricter day-to-day PoLP. Invest in BTG to make least privilege sustainable
- Conway's law applies to security: account structure mirrors org structure. Align accounts to bounded contexts (STOSA pattern)
- SCP enforcement: deny resource creation without required tags, restrict resource types per team, prevent disabling CloudTrail/CloudWatch

---

## Vulnerability Management

- Vuln management != patch management. Includes misconfigurations, feature disablement, compensating controls
- Default action in cloud: auto-apply security patches + run automated tests. Only manually evaluate when patches cause problems
- SBOM: generate for every application (CycloneDX or SPDX). Required by NIST SSDF
- Container scanning: (A) scan images in registry, block vulnerable images. (B) host-agent scans running containers. Use both
- Immutable containers: replace weekly to limit attacker persistence. If image rated vulnerable, replace all running instances
- False positive management: document fast masking process. Without it, teams ignore all scan results
- Key metrics: Tool Coverage (% scanned, target 100%), MTTR by severity, false positive rate, vulnerability recurrence rate
- Measure vulnerable systems, not absolute count. One critical vuln = same risk as five on same system
- Pentest findings: prioritize above all except user reports. If pentest finds things scanners missed, fix scanning pipeline

---

## Incident Detection & Response

- **NIST IR framework:** Design/Prep > Detection/Analysis > Containment/Isolation > Forensics > Eradication > Post-Incident
- MITRE ATT&CK cloud matrix: understand attacker TTPs. Kill chains (reconnaissance > weaponization > delivery > exploitation > C2 > action)
- Mean time to identify breach: 277 days (industry average). Companies identifying <200 days save $1M+

### What to Watch
- Privileged user access: all logins, all API actions via CloudTrail. Watch for unusual timing, location, or account
- Defensive tool alerts: WAF, IDS, antivirus. False positive feedback loop mandatory. Tune per app, not globally
- Cloud service metrics: CPU spikes (cryptomining/ransomware), network traffic (exfiltration), storage I/O (ransomware), database queries (data theft)
- Log flow cessation: alert when logs stop. May be malfunction or active attack covering tracks

### Log Architecture
- Separate toxic logs (may contain secrets: SSH sessions, kubectl exec) from sanitized logs (API actions, auth events)
- Aggregate logs to separate account with different credentials. Attacker cannot wipe logs from compromised production account
- Retain logs minimum 1 year. Hot storage (instant query) + cold storage (retrieval needed). Structure: aggregation > parsing > search/correlation > alerting
- Time sync (NTP) + consistent timezone on all systems. Prerequisite for cross-system correlation

### Containment Playbook
- Compromised infrastructure: (1) snapshot EBS/RDS, (2) freeze auto-termination, (3) isolate to separate subnet via NACLs, (4) deregister from LB/ASG, (5) tag for forensics
- Compromised application: isolating infrastructure insufficient (redeployment replicates breach). Microsegmented systems easier to contain
- Forensics: live-box (analyze running system, preserves memory) vs dead-box (recreate from snapshots, parallel analysis, loses in-memory data)
- Secure the security infrastructure: CloudTrail encryption (SSE-KMS), log validation (digital signatures), purpose-built logging accounts
- Deception: honeypots, honey tokens, honey IDs. Advanced technique. Never document presence outside core security team

### Automated Response Caution
- Automated response can be deliberately leveraged by attackers to cause outages (port scan triggers auto-shutdown = easy DoS)
- Accept small risk of delayed response over automated disruption in most cases. High-security environments may prefer opposite trade-off
