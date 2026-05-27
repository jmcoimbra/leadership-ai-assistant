# Team Topologies — Applied Classifications

**Added:** 2026-03-18
**Last Updated:** 2026-04-24 ([Your CTO] Q1 one-pager review 2026-04-24 validated all three framings verbatim; [Brain Owner] clarified canonical language: [Mobile Team] is "self-service now, platform team destination" not "platform enablement" alone; Dev Support is "Solutions Architect path, improving TAM our way" with "our way" = platform-first + partner-enablement + AI-native; QA remains enabler team per Team Topologies, not "guardrails". Rule codified in meeting-ingest-patterns.md Team Framing Verbatim section.)
**Source:** Team Topologies book (Skelton & Pais) applied to [Brain Owner]'s 3 teams. Decisions made in session with [Brain Owner].

## Team Classifications

| Team | Type | Primary Interaction Mode | Size |
|------|------|------------------------|------|
| QA Chapter | Enabling Team + Emergent Platform | Facilitating + X-as-a-Service | 2 ([Direct Report], [Senior IC]) |
| [Mobile Team] | Complicated-Subsystem → Platform Team | Collaboration → X-as-a-Service (transitioning) | 4 ([Team Lead] lead, [Senior IC], [Direct Report], [Direct Report]) |
| Dev Support | Stream-Aligned (Partner Integration Stream) | Collaboration + some X-as-a-Service | 2 ([Direct Report], [Direct Report]) |

## Key Decisions (2026-03-18)

1. **QA owns the quality platform long-term.** Cognitive load constraint acknowledged. Practical rule: track enabling work and platform work separately. When one crowds the other, that is the escalation signal.
2. **Dev Support SA trigger defined.** SA identity is reached when: (a) partners view them as go-to resource from 1st contact naturally, (b) they communicate as SAs not ticket handlers, (c) they know platform surface areas well enough to improve code.
3. **[Mobile Team] first self-service target: custom email domain.** Today = manual [Mobile Team] ticket. Target = self-service workflow where requesting team follows the system.

## [Mobile Team] Platform Transition

- Current: complicated-subsystem (Apple/Google app infra that stream-aligned teams cannot maintain)
- Target: platform team (self-service AppOps Platform)
- Transition metric: **% of inbound tickets resolved without human [Mobile Team] involvement**
- Current split: ~40% operate / 60% build. Target: 20/80.
- Four blocking dependencies: release cut (devs wait), app updates (CSMs wait), Google/Apple Pay (CSMs + Olo), merchant onboarding (4 parties)
- AI adoption IS the platform transition. Every automation that replaces manual ticket handling moves [Mobile Team] toward platform.

## QA Cognitive Load Rule

QA owns two workstreams:
- **Enabling** (embedded in Innovation/Stability): does NOT scale, requires human presence
- **Platform** (CI gates, test generators, [your-org]-qa): scales through automation

Practical rule: minimum 1 person-day/week/person reserved for platform building/maintenance. Enabling work fills the rest. If enabling demand would reduce platform time below floor, sequence to next cycle.

Watch metrics: repos with programmatic quality gates active, teams that ran test cycle without QA involvement.

## Apple Account Holder Operational Work: Dev Support, not [Mobile Team]

Routing rule for Apple-related work across the 90+ branded variants.

| Work type | Owner |
|---|---|
| Mobile app code ([your-org]-mobile-app iOS / Android, Apple/Google Pay integration, iOS deploy automation builds, app review pipeline) | [Mobile Team] |
| Apple Account Holder credential management, agreement-acceptance runbooks, 2FA pickup, fleet rollout coordination, custom-app-onboarding insertion | Dev Support |
| 1Password TechOps vault holding merchant Apple ID credentials | Dev Support owns. [Mobile Team] scoped read access for build / cert tasks. |
| Trusted phone numbers + Slack channel bridging SMS / voice 2FA | Dev Support owns. |

Test: if the work is "build or change app code", [Mobile Team] owns. If the work is "manage merchant Apple Account credentials and operational responses to Apple platform changes" (Account Holder agreements, 2FA challenges, cert renewals as merchant-facing operations), Dev Support owns.

Source: 2026-05-08 [Your CTO] 1:1 prep. Initial routing of the [partner-agreement] operationalization ([External Counterparty] consent agreement + 27 blocked merchants) assigned the operational build to [Mobile Team]. User corrected: "No, this lands in Dev Supp. [Mobile Team] will have access to the secrets vault." See `12_projects/apple_developer_shared_access.md` and `context/knowledge/ios-deploy-patterns.md` Apple Developer Account Roles section.

## Dev Support Dual Mandate

Two cadences in one team:
- Support work (Front tickets, API questions): steady, reactive
- SA work (live partner meetings, certification): bursty, proactive

Primary identity = partner integration / external developer experience. Ticket resolution = operational floor, not ceiling.

**Canonical framing (2026-04-24 [Your CTO] validation):** Solutions Architect path, improving TAM our way. SA trajectory is the mechanism, TAM expansion is the outcome, "our way" is the differentiator: platform-first, partner-enablement, AI-native. [Your CTO] unprompted: "Adaptability and broad span of control is what I look for in individuals. Dev Support getting requests, extending the platform, pushing back on partner asks when it doesn't make sense. That's exactly where we're aligned." Onosys new-endpoint AI-first SDLC validated as SA practice case.

## Three Interaction Modes (Book Reference)

| Mode | When | Duration |
|------|------|----------|
| Collaboration | Discovery, new tech, domain spans two teams | Time-bounded |
| X-as-a-Service | Well-understood domain, delivery predictability | Ongoing |
| Facilitating | Capability transfer, clearing impediments | Weeks to months |

## Cognitive Load Heuristics (Book Reference)

- Simple domain: team handles 2-3
- Complicated domain: max 1 per team
- Complex domain: exactly 1, nothing else alongside it
- Three types: Intrinsic (domain knowledge), Extraneous (tooling friction — eliminate), Germane (productive learning — maximize)

## Notion Reference

Full chapter-by-chapter analysis with applied callouts: [Team Topologies — Applied to QA, [Mobile Team], Dev Support at [Your Company]](https://www.notion.so/327a84ed402481349018cbd8b1d88ea5) in Books DB.
