# Citation Verification Protocol

**Owner:** [Brain Owner]
**Pillar:** Pillar 4 (AI Execution)
**Measurable Outcome:** Zero fabricated citations in outbound content (chat drafts, email drafts, private workspace pages, meeting scripts) over rolling 4 weekly reviews. Baseline: set during onboarding in `context/knowledge/error-correction-log.md`. Target: 0 by the next quarterly refactor.
**Escalation Trigger:** Any user correction of a fabricated citation that reached outbound content. Log to `context/knowledge/error-correction-log.md` and audit which gate failed.

Before any agent writes a citation into outbound content, run the mechanical check that matches the citation type. Verification is not a hope or a vibe. It is a tool call.

## Why This Exists

CLAUDE.md already mandates "evidence-first, no guesses". This file converts the principle into a procedure. The diffity-review pattern (`nilbuild/diffity`) names the failure mode: a wrong reference is worse than no reference because the reader trusts it. Slack-triage's Step 3.5 Gate C is the proven local instance (root-cause fix 2026-04-22 after fabricated answers to Bailey's three questions). This protocol generalizes Gate C across every brain skill that produces outbound content.

## Citation Types and Mechanical Checks

| Citation type | Mechanical check before citing |
|---------------|-------------------------------|
| File path (brain or repo) | `Read` or `ls` the path. Never write a path you have not opened in this session. |
| File path with line number (`file.md:42`) | `Read` the file at that line range. The cited content must match the claim. |
| Person name | `Read` `09_people/_template_team_roster.md` or `config/team.yaml`. Never guess spelling. Never infer language preference. |
| URL (any kind) | Must be (a) given by the user in this conversation, (b) present in a brain file you just read, or (c) returned by an MCP tool in this session. Never construct URLs from patterns. |
| Private workspace page or DB ID | Fetch it with the configured connector, or read the canonical list in the private adapter file. Never claim a page exists without fetching. |
| Jira ticket | `getJiraIssue` or `searchJiraIssuesUsingJql` before claiming state, ownership, or status. Stale ticket state is the most common failure mode. |
| GitHub PR | `gh pr view <N>` (with `GH_TOKEN=""` prefix) before classifying as open / merged / approved / needs-review. |
| Looker dashboard, metric, or number | Query the canonical source (Notion DB, Sheet, Looker URL) directly. Brain dashboard summaries drift. The source is authoritative. See `contextual-rules.md` "Brain dashboards drift" rule. |
| Calendar event or meeting time | `mcp__claude_ai_Google_Calendar__list_events` or `mcp__google-calendar__list_events`. Never call something a meeting without confirming it on the calendar. |
| Decision or commitment | Search `99_archive/` and recent meeting-ingest commits before asserting "X was decided". See `contextual-rules.md` "Before deferring an answer to a future person/meeting" rule. |
| Project status, owner, or metric | Read the project file under `12_projects/` or query the canonical tracker. Do not cite from memory of prior sessions. |
| Quote attributed to a person | Read the source transcript or message. Quoted text must match verbatim. |
| Pillar reference | Always expand with readable name. See `contextual-rules.md` "Referencing pillars". |

## Three Outcomes Per Citation

Each citation produces exactly one of these:

- **VERIFIED**: mechanical check confirms the citation. Cite as planned.
- **WRONG**: mechanical check returns a different value. Fix the citation (correct spelling, update number, fix path) before drafting.
- **UNVERIFIABLE**: mechanical check cannot be run (MCP unavailable, source not accessible, ambiguous reference). Either omit the citation, or label it `"unverified, confirm at [moment]"` per CLAUDE.md hard constraint.

Never proceed with a citation in any other state.

## When This Protocol Applies

Mandatory before any of:

- Slack draft send (any channel, any recipient, any tool)
- Email draft creation
- Private workspace page create or update
- Meeting script generation (Stage 3 of `meeting-prep`)
- Weekly review topic body generation
- Brain file edit that asserts external state (status, ownership, metric, person)

Skippable when:

- The agent is asking the user a clarifying question (not asserting)
- The output is internal-only TaskList content
- The citation is already labeled `"unverified, confirm at [moment]"`

## How to Apply (Drafting Skills)

Sequence inside any skill that produces outbound content:

1. **Draft the content with citations marked.** Use `[VERIFY: <citation>]` placeholders during composition.
2. **Resolve placeholders before output.** Walk the placeholders, run the mechanical check per citation type, replace with VERIFIED text or fix per WRONG / UNVERIFIABLE.
3. **Final scan.** Grep the draft for any remaining `[VERIFY:` markers. Any remaining marker = gate failure. Either resolve it or label UNVERIFIABLE.

This is mechanical. It is not "carefully consider whether the citation is right". It is "run the tool call and compare the result".

## Audit Hook

Any user correction of a fabricated citation in outbound content gets logged to `context/knowledge/error-correction-log.md` with:

- Date of the incident
- Citation type that failed
- Which gate would have caught it
- Why the gate did not fire (skill did not invoke this protocol, citation type missing from the table above, mechanical check skipped under time pressure)

The log feeds quarterly audits of this file. Patterns surface new citation types or expose gaps in the mechanical-check table.
