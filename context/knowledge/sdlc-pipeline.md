# SDLC Pipeline

> Owner: [Brain Owner] | Pillar: Pillar 4 (Embrace AI at every level) + Pillar 5 (Graduate from scrappy startup. Play Big)
> Measurable Outcome: 100% of Initiative-scale work passes Discovery gate before Design starts by 2026-07-31
> Escalation: Initiative bypassing Discovery gate: EM flags to team, requires completion before Design. Repeated bypasses or strategic disagreements: R&D Leadership
> Last Updated: 2026-04-26 (Design Reference Library added to Phase 1 Design: Top 5 Trade-offs, Fantastic Four NFRs, 12-Spoke Security Wheel from ByteByteGo Big Archive 2024)

Full lifecycle pipeline from "should we build this?" to "it's retired cleanly." Each phase has entry/exit criteria (quality gates), required artifacts, and cross-references to existing brain files. This file is a routing table, not an encyclopedia. Detail lives in the referenced files.

## Scale Classification

| Scale | Examples | Required Phases |
|-------|----------|----------------|
| Patch | bugfix, typo, config, dependency bump | Build, Validate, Deploy |
| Feature | new endpoint, significant refactor, UI feature | Design, Build, Validate, Deploy, Operate |
| Initiative | new service, platform migration, cross-repo | Discovery, Design, Build, Validate, Deploy, Operate |

**Classification signals:** Patch = no new behavior. Feature = new behavior, single repo or bounded cross-repo. Initiative = new service, >3 repos, or strategic investment. Default = Patch. Escalate only when signals present.

## Phase 0: Discovery (Initiative only)

**Entry:** Product idea, technical initiative, or strategic proposal exists.

**Stance:** Discovery is the Technical PM's phase. Output describes WHAT is controlled and for WHOM, never HOW. No models, tables, endpoints, middleware, or implementation choices. Those belong in Design (the HOW layer).

**Required artifacts:**

1. **Adoption Criteria** via `/[engineering-toolkit]:review-adoption-criteria` or `/[engineering-toolkit]:pamf-interview`. Score above threshold.
2. **Problem Statement** (1 paragraph): what problem, for whom, quantified impact.
3. **Ubiquitous Language & Taxonomy** (DDD-style). Before any capabilities are written:
   - Pick the **canonical term** for every domain noun the project introduces or redefines (person, department, service user, role, scope, tenant, etc.).
   - List **rejected synonyms** explicitly ("department" canonical → "group", "team", "org unit" rejected). Prevents drift.
   - **Code alignment check**: if the product extends an existing system, grep the repo. The canonical term must match what code already uses, or the project commits to a rename with its cost in scope. Vocabulary that does not match the code is a debt entry, not an optional cleanup.
   - Every capability, spec, and test must use canonical terms. Reviewers reject synonyms.
4. **Entity & Hierarchy Model** (WHAT level, no schema):
   - **Entities controlled** (nouns the product governs): list with one-line definition each.
   - **Hierarchy rules**: which entity contains/implies which. Example: "Department contains people. A role granted to a department reaches every person in it."
   - **Precedence rules**: when grants conflict, who wins. Example: "Person-level deny overrides department-level grant. Person-level grant is additive to department default."
   - **Super-entity rules**: if a root actor exists (super-admin, tenant owner), state who can grant that role, whether it is delegable, and the blast radius of its absence.
   - **Lifecycle defaults** (state transitions that trigger automatic behavior):
     - On entity **creation** (new department, new merchant, new tenant): what defaults apply?
     - On **membership change** (person joins / moves / leaves): what updates automatically? What requires explicit action?
     - On **deactivation** (person leaves, service retired): what cascades? What must survive (e.g. service-user tokens must not die with the human who created them)?
     - On **addition to a growing surface** (new tool, new endpoint, new feature flag, new integration): what gate runs before the new item becomes usable? Is adding an item automatic-grant to existing actors, or explicit-grant-only? If a sensitivity classification attaches to each item (read-gated, write/admin, privilege tier), the **onboarding gate is itself a product-discovery capability**, not a technical detail.
   - **Read-gating**: the default is not "everyone can read." Sensitive sources (sales-only data in Gong, Salesforce; financial queries in Snowflake; PII surfaces) are named and gated from day one. Public reads are the exception, not the rule.
5. **Technical Feasibility** checked against [[your-org]-tech-radar](https://github.com/[your-org]/[your-org]-tech-radar). New technology not on radar: propose via tech radar PR, discuss with R&D Leadership. Pipeline routes discussion, does not block new tech.
6. **Blast Radius Pre-Assessment** (ref: Blast Radius section below).
7. **Debt Pre-Assessment**: what existing debt blocks/complicates this? What debt will this create?
8. **UI & System Reconnaissance** (required when extending an existing product; skip for greenfield). Before the capability list is final:
   - Inventory what **already exists** in the product surface (admin UI, menus, models, policies, config fields). One file per concrete artifact: path + one-line role.
   - List the **gaps** the project must close. A gap is "this exists but is inert" (e.g. a menu with no enforcement), "this is missing entirely," or "this exists but its default is wrong for the product goal."
   - **Growing-surface check**: if the product controls a surface the org keeps adding to (tools, endpoints, flags, integrations, merchants), inventory both the current set **and** the lifecycle for adding new items. Who onboards? What classification attaches? What is the default-grant rule for existing actors on a new item? The onboarding lifecycle is a product-discovery capability when policy decisions attach at addition time.
   - Tie each capability to either "extends existing X" or "introduces new Y." Prevents accidental parallel implementations.
9. **Transition Plan (expand → contract shape)** (required when the Initiative modifies an already-live system with current users depending on current behavior; skip for greenfield):
   - Describe the **current enforcement posture** explicitly ("everyone reads everything," "flat `manager?` gates all writes," "tokens tied to humans"). The posture is the starting contract the transition must not break silently.
   - Lay out phases as a table: phase name → enforcement posture in that phase → what lands → named exit criterion. Minimum structure: a Configure-and-Observe phase (new primitives available, zero enforcement, shadow-log records what decisions *would* fire), a Narrow-Enforcement phase (deny on the highest-sensitivity subset only), a Per-Surface Enforcement phase (tighten one Tool/category/module at a time, each with its own shadow-log window), and a Steady-State phase.
   - State the **observe-before-deny principle**: no cutover without a shadow-log window, no surface enforced in the same PR that introduces the primitive. If observation reveals unintended denies, rollback is to shadow, not to allow-all.
   - Name what the current posture maps to in the new world. Preserving current behavior through early phases is a deliberate choice, not a compromise.
10. **Audit-Surface Reuse Inventory** (required when the Initiative introduces audit/tracking/logging requirements; skip if the product creates no attribution stakes):
   - Inventory existing tracking surfaces in the repo: every log table, event table, execution record, query log, webhook record. One row per surface: what it captures, join key back to Person/ServiceUser/Token, which of the new product's attribution needs it already covers.
   - State the **delta** — the *only* new audit stream this Initiative creates. One bounded target. Refuse a parallel catch-all table when existing surfaces cover the per-action trail.
   - **Scope-creep guard** written as a rule: "any request to audit X where X is already captured in an existing log row is answered by a join, not a new write." Traceability expands only where existing surfaces genuinely lack attribution.
   - Migration-name correction habit: verify every referenced table actually exists. Migration names can mislead (e.g. `add_request_ip_to_audit_logs.rb` added columns to three `*_query_logs` tables, not an `audit_logs` table).
11. **Self-Raised Enquiries**. The Technical PM raises the questions the stakeholder forgot to ask. Minimum: 2 per entity × 3 per lifecycle transition × 3 per precedence rule. These feed Open Questions and the Stress Test. Asking "did you mean X or Y?" at Discovery is cheaper than rework at Build.
12. **Stress Test** via `/devils-advocate` before presenting to R&D Leadership.

**Spec-oriented output rule.** Discovery deliverables read like a PRD, not an essay. Capabilities are verifiable statements ("As [actor], I can [action] so that [outcome]"). Lifecycle transitions are state → trigger → result rows. Specs live in a dedicated appendix; narrative paragraphs are limited to Problem Statement and Scope.

**Exit gate:** Adoption criteria pass. Problem statement approved. Ubiquitous Language defined with rejected synonyms. Entity & Hierarchy model complete (entities, hierarchy, precedence, lifecycle defaults, read-gating). Tech radar checked (new tech proposed if needed). Blast radius mapped. Debt acknowledged with plan. UI recon produced when extending existing product. Transition plan produced when modifying already-live behavior. Audit-surface reuse inventory produced when attribution is at stake. Self-raised enquiries logged. Capabilities written as specs, not prose.

## Pre-Design Bridge (Feature + Initiative)

Before entering Design, generate a BDD-style test suite draft:
- **Initiative:** After Discovery exit gate passes and PRD exists.
- **Feature:** When work item is scoped and PRD/spec exists (no Discovery gate required).

Run `/[engineering-toolkit]:test-suite-prd` against the Notion PRD. Output: BDD scenarios in Given/When/Then format, one per PRD behavior. This becomes the behavioral contract between PRD and code.

```
Scenario: [PRD behavior in plain English]
  Given [precondition]
  When [action]
  Then [expected outcome]
```

## Phase 1: Design (Feature + Initiative)

**Entry:** Discovery gate passed (Initiative) or work item scoped (Feature). BDD test suite draft available.

**Required artifacts:**

1. **Architecture diagrams** (scaled):
   - Feature: sequence diagram for key flows + data model changes
   - Initiative: C4 Context + Container diagrams, sequence diagrams for critical paths, data flow diagram
2. **Blast Radius Analysis** (ref: Blast Radius section). Persist to local artifact per issue.
3. **Deployment Strategy** (ref: Deployment Strategy section).
4. **Observability Design**: which SLIs affected, monitors needed, service tier, dashboards (ref: `sre-operations.md`). **Adoption measurement**: PAMF tracker spec (events, actors, first/last use definitions, success metric threshold). Must align with Adoption Criteria from Discovery.
5. **Test Strategy (BDD-driven)**: refine BDD scenarios from Pre-Design Bridge. For each scenario: assign test layer (unit/integration/E2E), target repo, owner. Every PRD behavior must map to at least one test scenario. Gaps = PRD coverage holes to flag to Product before Build starts. Coverage targets per repo (ref: `04_qa_brain/qa_coverage_framework.md`).
6. **Feature Flag Plan** (if user/merchant-visible): flag name, rollout plan, cleanup ticket (ref: `[your-org]-dev-workflow.md`).
7. **ADR**: Initiative = formal ADR (template below). Feature = lightweight "Decision" section.
8. **Risk Classification**: Standard/High/Critical per `[your-org]-dev-workflow.md`.
9. **Debt Ledger Entry**: debt introduced (with payoff timeline) + debt being paid down.
10. **Estimation (AI-Driven)** (ref: Estimation section). Produced at Design, not before.

**Design Reference Library** (cheat sheets to anchor reviews):

- **Top 5 Trade-offs**: Cost vs Performance, Reliability vs Scalability, Performance vs Consistency, Security vs Flexibility, Development Speed vs Quality. ADR "Consequences" must name which axis the decision lands on.
- **Fantastic Four (NFRs)**: Scalability, Availability, Reliability, Performance. Architecture diagrams (artifact #1) must label components against these four.
- **12-Spoke Security Wheel**: Authentication, Authorization, Encryption, Vulnerability, Audit/Compliance, Network Security, Terminal Security, Emergency Responses, Container Security, API Security, 3rd-Party Mgmt, Disaster Recovery. Cross-check with Risk Classification (artifact #8); gaps escalate the tier.

Source: ByteByteGo, *System Design: The Big Archive (2024)*. Notion entry: [📚 System Design: The Big Archive](https://www.notion.so/34ea84ed4024819d99b5e6d649eee764).

**ADR Template:**
```
Title | Date | Status (Proposed/Accepted/Superseded)
Context: what forces are at play
Decision: what we chose
Consequences: trade-offs accepted
Alternatives Considered: what we rejected and why
```

**Exit gate:** Architecture reviewed by domain-context engineer. Blast radius and deployment strategy reviewed. Observability design reviewed against SRE tiers. Test strategy covers all affected repos. Flag naming follows conventions. ADR accepted. Risk tier assigned. Estimation produced and communicated.

## Phase 2: Build (All scales)

**Entry:** Design gate passed (Feature/Initiative) or ticket exists (Patch).

**Required artifacts:**

1. Branch with ticket-ID-first naming (ref: `[your-org]-dev-workflow.md`).
2. **Blast Radius (Patch scale)**: 5-minute [Your IDP Tool] `search_code` for callers across 16 deployable repos + grep for config consumers. "What calls this?" (ref: Blast Radius section).
3. **TDD cycle (Feature/Initiative):**
   - Take BDD scenarios from Design's Test Strategy
   - Write failing tests first (Red). Translate Given/When/Then into test framework (RSpec, Jest, Detox)
   - Write code to make tests pass (Green)
   - Refactor (ref: `clean-code.md`, `intelligence-layers` skill, `techstack-compliance` skill)
   - Repeat per scenario
   - **Patch scale:** Write the failing test reproducing the bug first, then fix
4. **PRD Coverage Matrix** (Feature/Initiative):
   ```
   | PRD Behavior | Test File:Line | Layer | Status |
   |-------------|---------------|-------|--------|
   ```
   Any PRD behavior without a test = blocked. Discuss with Product: dropped, deferred, or missed?
5. **PAMF tracker implementation** (Feature/Initiative): ship tracker alongside feature code via `/[engineering-toolkit]:pamf-implement`. Tracker PR merges with or before feature PR. Tracker events must map 1:1 to Adoption Criteria from Discovery.
6. Debt tickets for shortcuts (no "fix later" without Jira ticket + timeline).
7. API docs, README updates for public interfaces.

**Exit gate:** All BDD scenarios have passing tests. PRD coverage matrix complete (100% behaviors mapped). No new smells. Tech stack compliant. Blast radius confirmed (Patch). PAMF tracker built (Feature/Initiative). Debt tracked. PR opened.

## Phase 3: Validate (All scales)

**Entry:** PR opened. Build gate passed.

### Review Loop (state machine)

```
PR opened (Draft) -> CI + /[engineering-toolkit]:review
    |
Findings? -> Fix code -> CI + /[engineering-toolkit]:review (loop)
    |
Exit: 0 findings OR only justified LOW findings + CI green -> Move PR to Ready for Review
```

**Rules:**
- PR starts as Draft. No peer review until loop exits clean.
- Each iteration: fix findings, re-run `/[engineering-toolkit]:review`, confirm CI green.
- LOW findings: may be justified with inline comment. Justified LOWs do not block.
- MEDIUM or HIGH findings: block. Fix or downgrade with EM approval.
- PR moves to published/Ready for Review only after loop exits.

**Required artifacts (after review loop exits):**

1. `/[engineering-toolkit]:review` clean exit (0 findings or justified LOWs, CI green).
2. **PRD Coverage Review (EM gate):** EM reads test descriptions (Given/When/Then) to verify PRD compliance via the PRD Coverage Matrix. Gaps found: back to Build. This is how the EM verifies delivery without reading every line of implementation.
3. Production Change Validation Checklist via `/[engineering-toolkit]:validate-change`.
4. **PAMF tracker review** (Feature/Initiative): `/[engineering-toolkit]:pamf-review` on tracker PR. Verifies async safety, backfill scope, idempotency, and match to Adoption Criteria.
5. Peer review (1+ approval, domain-context for High/Critical per `[your-org]-dev-workflow.md`). Starts after PR published.
6. EM sign-off (informed by PRD Coverage Review).
7. Sandbox testing (ordering repos).
8. **Observability pre-deploy**: monitors/dashboards from Design created BEFORE deploy.
9. **Debt checkpoint**: no untracked debt. Planned payoff in PR if promised.

**Exit gate:** Review loop clean. PRD coverage 100%. All PR gates pass. PAMF tracker approved (Feature/Initiative). Observability deployed. Debt clean.

**Monitoring-gap rule:** When `/[engineering-toolkit]:validate-change` agents flag a missing alarm, DLQ, or signal that the current change introduces (e.g., removing a fallback path without adding a replacement signal, fixing a silent-failure bug without adding the alarm that would have caught it), expand PR scope to close the gap before drafting the Notion checklist. Do not file a follow-up — post-deploy state must not be worse-monitored than the bug. Re-calibrate risk level after the gap closes. Source: 2026-04-16 [your-org]-devops#1016 (Lambda raise-on-error + CloudWatch alarm + staging sync added in-PR).

## Phase 4: Deploy (All scales)

**Entry:** Validate gate passed. EM approved.

**Required artifacts:**

1. **Execute Deployment Strategy from Design**: service order, migration timing, flag sequence. Patch: standard cadence. Feature/Initiative: Design phase deployment strategy is the runbook.
2. **Pre-deploy blast radius confirmation**: re-verify blast radius hasn't changed since Design (new commits, dependency updates). Quick delta check.
3. **PAMF deployment coupling** (Feature/Initiative): tracker live before feature flag flips. If tracker deploy fails, hold feature rollout.
4. Feature flag rollout per plan (if applicable).
5. Post-deploy: 15min monitoring, error rate vs SLIs, rollback plan confirmed.
6. `/[engineering-toolkit]:verify-fix` to validate the change works in production.
7. **PAMF post-deploy check** (Feature/Initiative): `/[engineering-toolkit]:pamf-monitor` at 24h and 7d. Confirms tracker firing and first adoption signal.

**Exit gate:** Deploy successful. No error budget burn above threshold. Flag at target %. Verify-fix passes. PAMF tracker firing (Feature/Initiative).

## Phase 5: Operate (Feature + Initiative)

**Entry:** Deploy gate passed. Feature live at 100%.

**Required artifacts:**

1. **Adoption tracking** via `/[engineering-toolkit]:pamf-monitor` (weekly) and `/[engineering-toolkit]:pamf-pulse` (fleet-wide health). Metrics compared against Adoption Criteria threshold from Discovery. Adoption below threshold after 30d: trigger Retire gate review or iterate.
2. SLI monitoring producing data.
3. Debt paydown: tickets scheduled, no debt >90 days without escalation.
4. Flag cleanup: 2-4 weeks post-GA.
5. Docs updated to reflect as-built (not as-designed).
6. **AI Agent Readiness:**
   - [Your IDP Tool] `knowledge_add` for new patterns, services, or APIs
   - `context/knowledge/` file updated if documented pattern changed
   - Specs updated or created for new commands/skills (per Governance Rule 15)
   - README updated for new services or significant API changes
   - Blast radius artifact archived to local knowledge (feeds future Discovery phases)

**Exit gate:** Adoption meeting targets (PAMF-confirmed). SLIs stable. Debt on track. Flag cleaned. AI agents can discover and work with the change.

## Phase 6: Retire (When applicable)

**Entry:** Decision to retire feature/service/capability.

**Required artifacts:**

1. Impact assessment: cross-repo dependencies, downstream consumers.
2. Migration plan: traffic/data destination, timeline.
3. Observability teardown: remove monitors, dashboards, SLIs.
4. Infrastructure cleanup: Terraform destroy, ECS removal, DNS.
5. Documentation archive: move to `99_archive/`, update cross-refs.
6. **AI Agent Cleanup:** remove/archive [Your IDP Tool] knowledge entries. Remove CLAUDE.md trigger rules. Archive skills. Update `[your-org]-services.md` topology. Clean blast-radius artifacts referencing retired components.

**Exit gate:** No active traffic. No orphaned infra. Monitors removed. Docs archived. AI agents no longer reference retired components.

---

## Cross-Cutting: Blast Radius Analysis

Applies at every scale. Hybrid data sources:

| Source | What It Provides | When |
|--------|-----------------|------|
| [Your IDP Tool] `knowledge_search` | Service dependency graph, integration points | Design, Validate |
| [Your IDP Tool] `search_code` | Call sites, consumers of changed methods/endpoints | All scales |
| Local `[your-org]-services.md` | Service topology, DB ownership, gRPC contracts | Design, Deploy |
| Local blast-radius artifact (per-issue) | Persisted analysis, delta-checked at Deploy | Deploy |
| `/[engineering-toolkit]:validate-change` Section 4 | Cross-repo impact assessment | Validate |

**Deployable repos** ([your-org]-cli/projects/deployable.go): [your-org]-nucleus, [your-org]-core, [your-org]-api, [your-org]-mobile, [your-org]-admin, [your-org]-merchant-api-new, [your-org]-signup-ui, [your-org]-[your-product-ui], [your-org]-sms, [your-org]-feedback, [your-org]-pos, [your-org]-transaction, [your-org]-ordering, [your-org]-ordering-ui, [your-org]-dbt, [your-org]-looker.

These 16 repos are the minimum scope. Any change touching a deployable repo must answer: "which other deployable repos are affected?"

**Scale-appropriate depth:**
- **Patch:** 5-minute `search_code` for callers + grep. "What calls this?"
- **Feature:** Full dependency analysis. Affected services, queues, DB tables. Persisted artifact.
- **Initiative:** Complete service dependency map across all 16. gRPC contract review. Shared DB table audit ([your-org]-nucleus shared models). Migration impact. Non-deployable repos ([your-org]-devops, [your-org]-protorepo, [your-org]-scripts) checked for infrastructure/contract dependencies.

## Cross-Cutting: Deployment Strategy

Every Feature and Initiative gets an explicit deployment plan at Design phase:

1. **Service deploy order**: which repo merges/deploys first? Safe partial-deploy state?
2. **Data migration timing**: before code (forward-compatible)? After code (backward-compatible)? Both (expand-contract)?
3. **Feature flag sequence**: which flags flip in what order? Cross-service coordination?
4. **Rollback steps per service**: not just "revert the PR." Data migrated? Flag mid-rollout?
5. **Deploy window**: ordering Tuesday? Daily non-ordering? Maintenance window needed?
6. **Dependency coordination**: shared gems ([your-org]-nucleus), protobuf changes, gRPC contract updates.

## Cross-Cutting: AI Agent Readiness

After changes land, AI agents (Claude Code, [Engineering Toolkit], [Your IDP Tool], Conductor) must discover and work with the updated code. Without this, the next developer's AI session starts blind.

- **Patch:** No action unless fix changes documented behavior or a known pattern.
- **Feature:** [Your IDP Tool] `knowledge_add` for new APIs/patterns. Update `context/knowledge/` if documented pattern changed. Update/create specs per Rule 15.
- **Initiative:** All Feature items plus: new CLAUDE.md triggers, new skills, README for new services, [Your IDP Tool] entries for new topology, blast radius artifact archived.

## Cross-Cutting: Estimation (AI-Driven)

**When:** Design phase (after architecture is clear). Updated at Build if scope changes.

**Model:**

1. **AI generates baseline**: code complexity ([Your IDP Tool] `search_code`), repos touched (blast radius), test surface (BDD suite), deployment complexity, historical velocity (`/[engineering-toolkit]:cycle-time`). Output: effort breakdown by phase in human-hours.
2. **Human applies judgment**: domain knowledge gaps (multiplier), known unknowns, team capacity, external dependencies.
3. **AI-compression factor** (explicit, not hidden):
   - Test writing: AI drafts, human reviews (2-3x compression)
   - Code generation: AI for boilerplate, human for business logic (1.5-2x)
   - PR review: [engineering-toolkit]:review loop catches issues earlier (reduced rework)
   - Documentation: AI generates, human verifies (3-5x)
   - Blast radius analysis: AI runs in minutes, human validates (10x+)

**Output:**
```
Estimate: [X human-days] (with AI assistance)
Without AI: [Y human-days] (for calibration)
Confidence: [Low/Medium/High] (Low = >2 unknowns, Medium = 1-2, High = 0)
Key risks: [list]
```

**Rules:** Never estimate before Design. Always show AI-compression explicitly. Re-estimate at Build if blast radius changes. Track estimate vs actual to calibrate.

## Cross-Cutting: TDD/BDD as PRD Verification

Tests are the contract between PRD and code. BDD makes behaviors readable. TDD enforces they drive development.

**Chain:** PRD (Notion) -> `/[engineering-toolkit]:test-suite-prd` -> BDD scenarios (Given/When/Then) -> Design assigns layers/repos/owners -> Build uses TDD (Red/Green/Refactor per scenario) -> Validate: EM reads test descriptions to verify PRD compliance.

**EM Review Protocol:**
1. Open the PRD Coverage Matrix. Every PRD behavior should have a test reference.
2. Read test descriptions. Do they accurately capture PRD intent?
3. Check for missing edge cases the PRD implied but didn't state explicitly.
4. Test description doesn't match PRD language: flag to developer (alignment issue).

**Mutation testing:** After tests pass, intentionally break the implementation to verify tests catch it. Prevents trivial tests. For each BDD scenario: mutate the code under test (flip condition, remove return), re-run test. Test still passes: test is weak, rewrite.

**References:**
- [GitHub Spec Kit](https://github.com/github/spec-kit): specify/plan/tasks/implement chain
- [Tweag Agentic TDD](https://tweag.github.io/agentic-coding-handbook/WORKFLOW_TDD/): "TDD gives structure, agentic coding gives speed"
- [Antoniel's Agentic BDD](https://dev.to/antoniel/my-agentic-engineering-process-from-vibe-code-to-bdd-2ne): Gherkin + mutation validation
- [TDAD Paper](https://arxiv.org/html/2603.17973): graph-based impact analysis, 97.2% regression safety
- [GitHub Next Agentics](https://github.com/githubnext/agentics): Daily Test Improver workflow
- [Your Company] [Engineering Toolkit]: LLM-as-Evaluator, Self-Consistency, Selector Fallback

## Cross-Cutting: Learning Capture

After Deploy (all scales) or Operate reviews (Feature/Initiative):

1. **Estimation accuracy**: estimate vs actual, what was off and why.
2. **Blast radius surprises**: missed dependency? Update [Your IDP Tool] knowledge and local topology.
3. **Process friction**: which gate added value vs ceremony? Feed into quarterly pipeline review.
4. **AI effectiveness**: which tools compressed delivery? Calibrate AI-compression factors.

**Artifact:** 5-10 lines per issue. Not a postmortem. What surprised us, what to remember.
**Escalation:** Same surprise 3+ times: pipeline change proposal to R&D Leadership.

## Cross-Cutting: Stakeholder Communication

| Phase | Who | Channel | What |
|-------|-----|---------|------|
| Discovery exit | Product, R&D Leadership (Initiative) | Notion, Slack | Adoption criteria passed, moving to Design |
| Design exit | Engineering, Product | Slack #eng, Notion | Architecture reviewed, estimation, deploy plan |
| Build -> Validate | Reviewers, EM | GitHub, Slack | PR ready for review |
| Deploy | #eng | Slack | Deploy notification per cadence |
| Operate | Product, R&D Leadership (Initiative) | Notion, Slack | Adoption metrics vs targets |
| Retire | All stakeholders | Slack #eng, Notion | Migration plan and timeline |

Maps to existing channels and cadences. No new communication overhead.

## Technical Debt Classification

| Type | Definition | Rule |
|------|-----------|------|
| Intentional | Known shortcut, documented | Jira ticket + payoff date. Max 90 days |
| Accidental | Discovered during work | Log immediately, create ticket before PR merge |
| Environmental | Tech upgrade needed | Track in quarterly tech radar review |

## Pipeline Execution Rules

1. **No obvious questions.** Deliver everything possible. Do not ask whether to split code, add tests, or write RFCs. Have artifacts ready for review.
2. **No repo ownership assumptions.** All [Your Company]ers work on shared repos. Code discussions go to R&D Leadership.
3. **Self-review with agents.** Every artifact reviewed by at least one other agent before presenting. Code: `/[engineering-toolkit]:review`. Brain artifacts: general-purpose critic. Skills: LLM-as-Evaluator rubric.
4. **Defer only genuine judgment calls.** Stakeholder positioning, org politics, priority trade-offs: defer to EM. Everything else: deliver.

## Phase Composition with Existing Skills

| Phase | Skills/Commands Composed |
|-------|------------------------|
| Discovery | [engineering-toolkit]:review-adoption-criteria, [engineering-toolkit]:pamf-interview, techstack-compliance, devils-advocate, [Your IDP Tool] knowledge_search |
| Pre-Design Bridge | [engineering-toolkit]:test-suite-prd (BDD scenarios from PRD) |
| Design | sre, techstack-compliance, intelligence-layers, clean-code, [Your IDP Tool] knowledge_search + search_code, [engineering-toolkit]:pre-deploy-check, [engineering-toolkit]:cycle-time, [engineering-toolkit]:pamf-interview (refine criteria if new evidence) |
| Build | clean-code, techstack-compliance, intelligence-layers, [Your IDP Tool] search_code, [engineering-toolkit]:pamf-implement |
| Validate | [engineering-toolkit]:validate-change, [engineering-toolkit]:review, [engineering-toolkit]:pamf-review, sre |
| Deploy | sre, [engineering-toolkit]:verify-fix, [engineering-toolkit]:pamf-monitor (24h + 7d), blast radius delta check |
| Operate | [engineering-toolkit]:pamf-monitor (weekly), [engineering-toolkit]:pamf-pulse (fleet health), sre, [Your IDP Tool] knowledge_add |
| Retire | sre, techstack-compliance |

## Cross-Cutting: Adoption Measurement (PAMF)

**Framework owner:** UJ (DATA-4893). Each EM ensures their projects ship a PAMF tracker per phase below; the framework itself is UJ-owned. PAMF tracker reliability issues (e.g., `LimitedTimeMarketplaceRewardTrackingJob` failures) route to UJ, not to per-EM teams unless the failing tracker is owned by that team's project.

Adoption measurement is not optional. Every Feature/Initiative ships with a PAMF tracker. "Deployed" does not count until PAMF confirms usage.

| Phase | PAMF action |
|-------|-------------|
| Discovery | Define Adoption Criteria: event, actor, success threshold, measurement window (`/[engineering-toolkit]:pamf-interview`) |
| Design | PAMF tracker spec in Observability Design: events, actors, first/last use, backfill scope |
| Build | Tracker implementation via `/[engineering-toolkit]:pamf-implement`. Tracker PR ships with or before feature PR |
| Validate | Tracker PR reviewed via `/[engineering-toolkit]:pamf-review` (async safety, idempotency, criteria match) |
| Deploy | Tracker live before feature flag flips. `/[engineering-toolkit]:pamf-monitor` at 24h + 7d post-deploy |
| Operate | Weekly `/[engineering-toolkit]:pamf-monitor`. Fleet health via `/[engineering-toolkit]:pamf-pulse`. Below threshold 30d: Retire review |
| Retire | Archive tracker or keep for historical baseline. Update criteria file |

**Anti-patterns to block at Validate:**
- Feature ships without tracker ("we'll add it later"). Reject.
- Tracker with no backfill plan for existing merchants. Reject or document scope.
- Adoption Criteria undefined at Discovery but claimed "measurable." Reject at Design exit.

## Sub-Playbooks (Team-Specific Variants)

Sub-playbooks specialize this pipeline for a specific team's workflow. Each is the canonical source for that team's day-to-day execution; this file remains the umbrella reference.

**TechOps AI-Powered Development Workflow** ([Notion](https://www.notion.so/34da84ed402481fdb47bdf407c9245ae)). [Mobile Team] + Dev Support innovation, release, and partner-cert work. Three-phase model: Product Discovery → Technical Investigation → Code Delivery (maps to Discovery → Design → Build/Validate/Deploy here). Track Selector: Innovation / Release / Partner-certification. Reference example: [[Your IDP Tool] RBAC](https://www.notion.so/345a84ed4024812ea896e51f1efa0ef2). Adds beyond the umbrella pipeline:
- **PDR (Product Decision Records).** §9 of every Phase 1 doc carries one subpage per scope cut, deferred feature, or partner ask declined. Format: Date, Status (Proposed / Accepted / Rejected), Context, Decision, Consequences, Alternatives Rejected, Trigger to revisit. Title pattern: `PDR 000N — <decision title>`. Mirrors the ADR shape used in Phase 2 but for product/policy decisions, not architectural ones.
- **Per-track quality gate matrix as hard exit.** Phase 3 cannot exit until every track-relevant gate is green: BDD pass, coverage, mutation, contract tests, security, accessibility, performance, observability, PCL, documentation, track-specific (Innovation: cleanup PR; Release: iOS deploy automation + screenshot diff + rollback rehearsed; Partner-cert: first prod transaction observed clean + tier promoted), retrospective.
- **Continue / Defer / Cancel decision logged at every phase exit.** Not optional. Drives the kill gate so 30-40% of low-value work dies at Phase 1 or 2 instead of bleeding into delivery.
- **AI draft-mode declaration.** Callout names which sections are AI-led vs human-led before drafting begins. Domains where AI is not yet trusted (payment flows, mobile cert chains, partner credential isolation, accessibility audit, chaos experiments, security exception decisions) require human-led drafting with AI assist.
- **AI-failure failover.** Triggers: 3+ review rounds rewriting AI output, reviewer rewrites >50% of draft, AI content not grounded in source. Author logs the trigger so future similar shapes skip AI-first.
- **Phase Staleness Sweep.** SLAs: Product Discovery 14 days, Technical Investigation 21 days, Code Delivery 30 days. No commit / no comment / no review activity inside the window auto-flags at next TechOps weekly.
- **Quarterly Playbook Retrospective.** April / July / October / January. Phase-time per phase, AI draft acceptance rate, scope changes (PDR + ADR count vs Phase 1 scope), retrospective frequency, quality gate failures.

Out of scope for this sub-playbook: Patch / Feature work that follows the standard SDLC phases above; existing TechOps Projects & Delivery workflow for Automation/Improvements (Capture Signal → Planning → Execution → Rollout); Pundit/ActiveAdmin policy changes; QA Chapter delivery (the playbook governs [Mobile Team] + DS code delivery only — "QA" inside it means the quality bar [Mobile Team] + DS code must clear, not the QA Chapter as a team).

Last Updated 2026-04-28 (registered after [Direct Report]'s Qualifying Rewards Phase 1 doc was processed end-to-end against playbook v1.5: 7 compliance edits + 4 PDR subpages + 5 substantive blocker comments).
