# Agile Frameworks (Industry Vocabulary)

> Owner: [Brain Owner] | Pillar: Pillar 5 (Graduate from scrappy startup. Play Big) | Last Updated: 2026-05-20

Canonical industry-vocabulary reference for product-engineering collaboration. Use when mapping the [Your Company] SDLC pipeline to widely-known agile vocabulary, or when answering "what does agile say about this?" in R&D Leadership discussions. [Your Company]-specific phase detail lives in `sdlc-pipeline.md`. This file is the framework dictionary; `sdlc-pipeline.md` is the operational pipeline that those frameworks map into.

## Three Amigos (refinement ritual)

**Origin:** George Dinwiddie, ~2009. Adopted heavily in BDD (Behavior-Driven Development) and Specification by Example.

**Mechanic:** Before a story crosses Definition of Ready, three voices sit together for 15-60 minutes per story.

- **Product / Business:** what problem, what value, what is in scope.
- **Development:** how would we build it, what is feasible, what is the risk.
- **QA / Test:** how do we know it works, what are the edge cases, what breaks.

Output is shared understanding plus concrete examples (often Gherkin Given / When / Then). Story moves to Ready, back to refinement, or is split.

**Variants:** Example Mapping (Matt Wynne, stickies for rules / examples / questions / story), Story Kickoff (10-minute lightweight version), the same three voices inside Refinement / Backlog Grooming.

**[Your Company] mapping:** Sits between Phase 0 Discovery exit and Phase 1 Design entry in `sdlc-pipeline.md`. The `/[engineering-toolkit]:test-suite-prd` pipeline (Notion PRD into BDD scenarios per behavior) is the artifact-level expression: the conversation is the ritual, the BDD output is the contract. The thread evidence below shows the cost of skipping the ritual.

## Dual-Track Agile (discovery + delivery)

**Origin:** Jeff Patton (user-story-mapping circles). Adopted by SVPG (Marty Cagan).

**Mechanic:** Two tracks run in parallel.

- **Discovery track:** validate viability (does the business want it), feasibility (can engineering build it), usability (will users use it), value (will it deliver outcomes). Output: validated PRD ready to commit. Spikes (timeboxed engineering investigations) live here.
- **Delivery track:** sprint-level execution against committed PRDs.

The discovery track is timeboxed and de-risks before commitment.

**[Your Company] mapping:** Phase 0 Discovery in `sdlc-pipeline.md` is the discovery track for Initiative scale. Patch and Feature scale skip the formal Discovery gate but the principle (validate before commit) applies via Phase 1 Design. A missed partner-API spike (Toast Promo API not discovered before scoping commit, per the 2026-05-19 thread) is a dual-track agile failure.

## Empowered Product Teams (Cagan / SVPG)

**Origin:** Marty Cagan. "Inspired" and "Empowered" (Silicon Valley Product Group canon).

**Four risks the product trio owns:**

- **Value:** will customers buy or use it. Product owns.
- **Viability:** does it work for the business legally, ethically, financially, partnership-wise. Product owns.
- **Usability:** will users figure out how to use it. Design owns.
- **Feasibility:** can engineering build it with available time, skills, tech. Engineering owns.

**Stance:** Discovery is a team sport. PM does not hand off a finished PRD. PM, designer, and tech lead investigate together. PM ensures stakeholder and partner access. Engineering does technical feasibility validation. Design owns the usability artifact.

**[Your Company] mapping:** `sdlc-pipeline.md` Phase 0 names the Technical PM as Discovery owner with this stance: "Discovery is the Technical PM's phase. Output describes WHAT is controlled and for WHOM, never HOW." That matches Cagan's value / viability framing. Engineering enters at Phase 1 Design owning HOW (feasibility). The [Your Company] pipeline does not name a separate Design role; Cagan would flag the gap.

## Continuous Discovery (Torres)

**Origin:** Teresa Torres, "Continuous Discovery Habits."

**Mechanic:** Weekly partner / customer touchpoints owned by a Product Trio (PM, designer, engineer). Opportunity Solution Tree maps desired outcome to opportunities (unmet needs) to solutions to assumption tests.

**Stance:** Engineers are in partner conversations from week one. No hard handoff between PM "discovers" and Eng "delivers." Continuous, not batch.

**[Your Company] mapping:** [Your Company] does not run a formal Trio cadence. The `sdlc-pipeline.md` Discovery phase is batch (one PRD per Initiative), not continuous. Torres-style continuous discovery is a candidate evolution if the eng-product handoff debate ([Your CDO] / [Your CEO] 2026-05-19) keeps recurring.

## Definition of Ready (DoR) and Definition of Done (DoD)

**Origin:** Scrum convention, not in the official Scrum Guide. Widely adopted.

**Definition of Ready (typical contents):**

- User story has acceptance criteria.
- External dependencies identified.
- External APIs validated (often via spike).
- Cross-functional dependencies named.
- Estimable by the team.
- Three Amigos session complete.

**Definition of Done (typical contents):**

- Code merged to main.
- Tests pass.
- Code reviewed.
- Documentation updated.
- Deployed to production (or shippable increment).
- Acceptance criteria verified.

**[Your Company] mapping:** Phase 0 Discovery exit gate in `sdlc-pipeline.md` is the [Your Company] Definition of Ready: ten required artifacts (Problem Statement, Ubiquitous Language, Entity Model, Technical Feasibility, Blast Radius, Debt Pre-Assessment, UI Reconnaissance, Transition Plan, Audit-Surface Reuse) must be present. Phase 4 Deploy exit gate is the [Your Company] Definition of Done. The [Your Company] pipeline is more rigorous than typical DoR / DoD by virtue of the ten-artifact gate.

## Where the [Your Company] Debate Sits

The 2026-05-19 [Your CDO] / [Your CEO] / [Peer Manager] Slack thread (`[CHANNEL_ID]` / [message-ts]) debated who owns partner-API research before engineering accepts a PRD.

- **[Your CDO] (CDO):** Product anticipates, builds breadcrumbs (partner contacts, dev support rosters, customer roster), Engineering executes the validation calls. Product spot-checks via async updates.
- **[Your CEO] (CEO):** Calls market and partner research "definitively Product Management's job." Stance: complete the research before handoff to Engineering. Calls the Toast Promo API miss "embarrassing" and "massive yield loss."
- **[Peer Manager] (peer):** PRD acceptance phase is where Engineering pushes back. Accepted PRDs can fall out of a quarter if Engineering discovers something undesirable.

Mapped to frameworks:

- **Cagan / SVPG:** Trio (PM + Design + Eng) does it together in discovery. Closest to [Your CDO]'s "Eng executes calls with PM-provided breadcrumbs."
- **Torres (continuous discovery):** Engineering is in partner calls from week one. Both [Your CDO] and [Your CEO] assume a hard handoff exists that Torres rejects.
- **Classical Scrum:** Silent on partner research. PO writes stories, dev team implements. Gray area.
- **Dual-track agile:** Discovery track validates partner APIs via spikes before commitment. The Toast Promo API miss is a missing spike. Closest to [Your CEO]'s "should have been done in advance."

The agreement: once Engineering accepts the PRD, Engineering owns the outcome ([Your CEO] + agile + Cagan converge here). The disagreement: who emails the partner before acceptance. Modern product practice (Cagan, Torres) assumes the trio is in the room together rather than handing off, which makes the "who emails" question disappear by design.

## Cross-References

- `sdlc-pipeline.md`: [Your Company]-specific phases, gates, and artifacts. Authoritative for operational use.
- `team-topologies.md`: team-organization patterns (enabling, platform, stream-aligned). Different lens than refinement rituals.
- `decision-frameworks.md`: CS-grounded decision-quality frameworks. Different lens than process rituals.
