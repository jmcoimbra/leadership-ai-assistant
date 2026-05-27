# Cloud Security Practices

## Ch 1: Principles and Concepts
- Defense in depth: 2 independent controls at 95% = 99.75% combined. Every control must have a backup
- Zero trust: encrypt + authenticate ALL connections. No implicit trust, even internal
- Least privilege applies equally to automation. Deny-by-default
- Asset-oriented threat modeling: protect data, identify attackers, place mitigations on trust boundaries
- Shared responsibility: data access = always customer. Most S3 breaches = assuming provider handles access
- Risk response: avoid, mitigate, transfer, accept (documented only). Undocumented acceptance = negligence
- Kerckhoffs: secure even if everything except key is public

## Ch 2: Data Asset Management and Protection
- Classify data: 3 levels max (public, private, confidential). Tag every resource
- Tokenization: replace sensitive data with random tokens. Best for credit cards
- Encryption layers: disk > platform/DB > application. Higher = more attacks blocked, fewer DB features
- Application-level encryption: crown-jewel only. Platform handles rest
- Encryption strategy: decide BEFORE creating storage resources
- Envelope encryption: CMK wraps DEK, DEK encrypts data. Wrapped DEK stored alongside ciphertext
- Cryptographic erasure: delete KEK to render all data unrecoverable instantly
- KMS encryption context (AAD): bind ciphertext to attribute, decryption fails on mismatch
- Quantum risk: AES-256 at rest safe. RSA/ECC key-wrapping needs quantum-safe migration

## Ch 3: Cloud Asset Management and Protection
- Cloud providers only track API-provisioned assets. Manual container contents invisible
- Four leak types: procurement (missed providers), processing (missed types), tooling (not scanned), findings (ignored)
- Start with security-relevant assets (storage + compute). Add types incrementally
- Ephemeral assets: track container images, not individual containers
- Immutable container model: single-concern, no admin logins, replace instead of update
- Tagging standard: function, environment, application, department, data classification. Case-sensitive
- DNS domains and TLS certificates: track registrars, expiration dates, automate renewal (ACME)

## Ch 4: Identity and Access Management
- Separate authentication from authorization. Revoke permission, not person
- IAM lifecycle: Request > Approve > Create/Grant > Authenticate > Review/Revoke
- Non-human identities need same lifecycle rigor as human
- MFA: FIDO2/passkeys strongest (phishing-resistant). SMS deprecated (SIM cloning)
- Step-up auth for high-risk transactions within authenticated sessions
- Long-lived tokens survive password changes. Offboarding must revoke ALL tokens
- SSO via SAML 2.0 / OIDC. Fewer credentials = smaller attack surface
- Shared IDs: every use attributable to individual. PAM/PIM for checkout + session recording
- Password hashes: scrypt, bcrypt, PBKDF2, Argon2 only. SHA-256 too fast for passwords
- Never store secrets in source code. Deployment = code + config + secrets from separate sources
- Prefer workload identity (SPIFFE/SPIRE) over static API keys

## Ch 5: Vulnerability Management
- Vuln mgmt != patch management. Includes misconfigurations, compensating controls
- Default: auto-apply patches + run automated tests. Manual only when patches cause problems
- SBOM: generate per application (CycloneDX/SPDX). Required by NIST SSDF
- Container scanning: (A) registry scan + block, (B) host-agent on running containers. Use both
- Replace containers weekly to limit attacker persistence
- Scanning tools by layer: network (external), agentless (login + check), agent-based (push), SAST/DAST/SCA/IAST
- False positive management: fast masking process or teams ignore all results
- Metrics: Tool Coverage target 100%, MTTR by severity, false positive rate, recurrence rate
- Measure vulnerable systems, not absolute count. Pentest findings prioritize above all

## Ch 6: Network Security
- Microsegmentation by business domain, not technology layer. One VPC per domain
- Default all services to private subnets. Most impactful single control
- Internal denied connections = lateral movement or misconfiguration. Both investigate
- TLS everywhere crossing any boundary. Exception: localhost, same K8s pod
- TLS 1.3 minimum. PFS ciphers (ECDHE). New private keys on every cert renewal
- Egress filtering: (1) SG/NACL port restrictions, (2) IP allowlisting, (3) forward proxy. Block DNS/ICMP tunneling
- IDS/IPS most value for internal lateral movement, not perimeter (WAF handles that)

## Ch 7: Detecting, Responding to, and Recovering from Security Incidents
- Mean time to identify breach: 277 days. <200 days saves $1M+
- MITRE ATT&CK cloud matrix + kill chains. Understand attacker TTPs
- Watch: privileged user access, defensive tool alerts, cloud metrics (CPU/network/I/O spikes), log flow cessation
- Separate toxic logs (may contain secrets) from sanitized logs (API actions)
- Aggregate to separate account. Attacker cannot wipe logs from compromised account
- Retain logs 1 year minimum. Hot + cold storage. NTP sync mandatory
- SIEM for correlation, rules, threat intelligence. Small orgs: log aggregation + simple alerts may suffice
- Threat hunting: hypothesis-driven, only after basics (collect/parse/alert) are running
- IR team: primary + backup technical + business leaders. Specialist coverage for each threat model area
- Tools: forensic VM images, separate IR cloud account, tested comms systems, contact lists, checklists
- Deception: honeypots, honey tokens, honey IDs. Never document outside core security team
- Automated response: can be leveraged by attackers for DoS. Balance operational vs security risk
- Tabletop exercises: test plans before incidents. Consider lockdown scripts (disable access, disable networking)
