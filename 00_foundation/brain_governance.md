# Brain Governance
> Owner: [Brain Owner] | Pillar: All | Status: Enforced | Last Audit: [YYYY-MM-DD]

## Purpose

This file is the constitution. Every other file in this repository must comply with the rules below. Non-compliant files are liabilities, not assets.

## Non-Negotiable Rules

### Rule 1 — No file without accountability
Every file must include in its header:
- **Owner** (named person)
- **Strategic pillar** (which of your defined pillars it maps to)
- **Status** (`draft` | `active` | `enforced` | `archived`)
- **Last audit date**

### Rule 2 — No initiative without execution criteria
Every initiative must specify:
- What is being built or changed
- By whom (named owner)
- By when (specific date, not "Q2" — a date)
- Measurable outcome (baseline → target)
- Escalation trigger (what happens if it stalls for 2 weeks)

### Rule 3 — No duplicate concepts
One source of truth per concept. If team authority is defined in `04_team_brains/<team>_authority_model.md`, no other file redefines it. Other files reference it.

### Rule 4 — No raw transcripts in core folders
Raw input goes to `99_archive/`. Core folders contain only distilled, enforceable models.

### Rule 5 — Deterministic language only
Banned words in initiative descriptions: *improve, enhance, support, explore, consider, leverage* (without specifics).
Required pattern: `[verb] [thing] from [baseline] to [target] by [date]`.

### Rule 6 — Quarterly refactor mandatory
See `07_operating_rhythms/quarterly_refactor_checklist.md`. Set the next refactor date during onboarding.

### Rule 7 — AI integration must be explicit
Every operational domain file must include a section: `## AI Integration` that defines how AI is used in that domain. No domain operates without an AI leverage point.

### Rule 8 — Execution bias enforcement
Every document must answer:
- What behavior changes?
- What metric moves?
- What gets built?
- By whom?
- By when?

If not, the document is conceptual drift and must be rewritten or archived.

### Rule 9 — People files are mandatory
Every direct report must have an individual development profile in `09_people/`. Files without a 1:1 entry in the past 21 days are flagged RED. When a new team member joins, their file must be created within 7 days.

### Rule 10 — Career trajectory is tracked
The brain owner's career development is encoded in `10_career/` and reviewed quarterly. If no progress on career trajectory milestones in a quarter, force a career development 1:1 with the brain owner's manager within 7 days.

### Rule 11 — Self-descriptive file names
Every file name must be understandable without external context. No internal acronyms, program names, vendor names, or jargon that requires knowledge beyond the file name itself. If a reader cannot guess the file's purpose from its name alone, rename it.

### Rule 12 — Sensitive data stays out of this repo
This template ships as a public repository. **Do not store inside this repo:** real financial figures, identified customer/merchant names tied to strategic context, employee wellness data, external-contact PII, compliance specifics (pentest targets, IR scenarios), or active partner-negotiation details.

For sensitive data: use a separate private system (encrypted vault, private repo with access controls, internal wiki). Reference it from this repo by topic name, never by content.

### Rule 13 — Knowledge file lifecycle
Knowledge files in `context/knowledge/` follow a lifecycle:
- **Split threshold:** When a file exceeds 200 lines AND contains 3+ unrelated topics, split into focused files.
- **Merge threshold:** When 2 files cover >60% overlapping entities, merge into one.
- **Archive threshold:** When a topic file has not been referenced by any skill or command for 90 days, archive to `99_archive/knowledge/` with date suffix.
- **Quarterly audit:** During quarterly refactor, run `wc -l context/knowledge/*.md` and flag files exceeding thresholds.

### Rule 14 — Skill-first behavioral patterns
New durable behavioral patterns go to `.claude/skills/<skill>/SKILL.md` so they auto-fire when the agent enters scope. Hard always-on constraints go to `AGENTS.md`. Reference data (URLs, IDs, contacts you maintain in a private system) goes to `context/knowledge/<topic>.md`. Active project state goes to `12_projects/<project>.md`.

| Pattern type | Destination | Why |
|--------------|-------------|-----|
| Hard constraint (always-on) | `AGENTS.md` Hard Constraints section | Loads every turn |
| Behavioral rule (in-scope only) | `.claude/skills/<skill>/SKILL.md` | Auto-fires via frontmatter triggers |
| Reference data (URLs, IDs, contacts) | `context/knowledge/<topic>.md` | Lazy-loaded via `categories/README.md` routing |
| Active project state | `12_projects/<project>.md` | Brain domain folder, surfaced by weekly review |

### Rule 15 — Spec lifecycle
Commands >200 lines OR with evaluator rubrics MUST have a behavioral spec in `context/specs/`. Specs describe WHAT a command does (behavioral contract), not HOW (implementation).

## Compliance Verification

Run `00_foundation/compliance_audit.md` against every file quarterly. Any file scoring below 4/6 is flagged RED and must be remediated within 2 weeks or archived.

## Cross-References

- `00_foundation/compliance_audit.md` - quarterly file-compliance scoring rubric used by Rule 1.
- `00_foundation/evolution_protocol.md` - how this constitution evolves.
