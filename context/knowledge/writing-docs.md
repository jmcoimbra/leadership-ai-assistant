# Writing Docs

**Owner:** [Brain Owner]
**Pillar:** Pillar 4 (AI Execution)
**Last Updated:** 2026-05-26 (PR Description Review Lens added: 5-item check + Doc-Type Cheatsheet row; doctrine "behaviour/rationale over ticket references" generalized from blb451's nit on [your-org]-devops #1044 code comments to PR bodies, after #1046 first-draft was Slack-post-mortem-style). Earlier 2026-04-28 (Shared SOP Authoring Rules section added: no individual names in shared docs, no brain-local slash command references, grep stale strings after large rewrites, no reviewer-rotation framing unless user named it, track-variant scope is the audience's call). Earlier 2026-04-27 (Release Notes Review Lens + Product Guide Adoption Lens added; Doc-Type Cheatsheet gained release-notes and CS-adoption-guide rows)
**Wired into:** `.claude/skills/writing-docs/SKILL.md`

Knowledge base for the `writing-docs` lens. Covers doc-type routing, structural frameworks, revision rules, and anti-patterns. Voice rules live in `voice-profile.md`; governance lives in `00_foundation/brain_governance.md`. This file does not duplicate either.

## Sources

| Source | Contribution |
|--------|-------------|
| Barbara Minto, *The Pyramid Principle* (via Harrison Metal tribute) | SCQA, pyramid structure |
| Daniele Procida, *Diátaxis* (diataxis.fr) | Doc-type routing (tutorial / how-to / reference / explanation) |
| Dave Girouard, *A Founder's Guide to Writing Well* (First Round Review) | 8 revision rules |
| *MECE principle* (McKinsey / Barbara Minto) | Sibling grouping discipline |
| Tremendous Handbook — *Writing Effectively* bundle | Reader-first stance; cut aggressively; scannability |
| Paul Graham — *Write Simply*, *Write Like You Talk* | Plain words; conversational test |
| Venture Hacks — *Writing Like Great Entrepreneurs* | "Customer service problem"; delete half the words |
| *Nicely Said* (Redish & Kissane) | Clear/concise/honest/considerate; consistent terminology |

## Gate 1 — Diátaxis Type Routing

Four types, each answers a different reader need. A doc that mixes types fails regardless of prose quality.

| Type | Reader's job | Writer's job | Anti-pattern |
|------|--------------|--------------|--------------|
| **Tutorial** | Learn by doing (new to the topic) | Hand-hold through a guaranteed-success exercise | Dumping reference material mid-exercise |
| **How-to** | Complete a known task | Assume competence, show the task's goal-driven path | Teaching concepts the reader already has |
| **Reference** | Look up a fact | Describe the machine exhaustively, neutrally | Telling a story or walking through use cases |
| **Explanation** | Understand why | Discuss context, trade-offs, alternatives | Providing step-by-step instructions |

**Routing questions to apply:**
1. Is the reader new to this topic and learning? → Tutorial
2. Does the reader have a specific job to finish? → How-to
3. Does the reader need to verify a fact? → Reference
4. Does the reader want to understand why it works this way? → Explanation

If a draft answers two, split it. A PRD, for example, mixes explanation (why this matters) and reference (what ships). The explanation section stays short; the reference section takes the bulk. Label the sections.

## Gate 2 — Minto Pyramid / SCQA

Lead with the answer. The pyramid puts the main point at the top and supporting arguments MECE-grouped beneath.

**SCQA opening pattern:**

- **Situation** — shared context the reader already accepts. One or two sentences.
- **Complication** — what changed, broke, or newly applies. Creates the tension.
- **Question** — the implicit question the reader now has.
- **Answer** — the recommendation up front. Everything that follows supports it.

**Example (internal doc opener):**

> S: We deploy [your-org]-ordering weekly on Tuesdays. C: The last three deploys each required hotfixes for the same race condition. Q: Should we block the next deploy on a fix? A: Yes — merge PR #4712 before Tuesday's cut.

For long docs, the answer is a TL;DR block at the top. For short docs (<300 words), SCQA compresses into the opening paragraph. Either way, no answer below the fold.

**Pyramid logic below the answer:**
- Group supporting arguments under the answer.
- Each group is mutually exclusive and collectively exhaustive (see Gate 3).
- At each level, the child nodes add up to their parent. Readers can skip any subtree without losing the main argument.

## Gate 3 — MECE Grouping

**Mutually Exclusive:** no two siblings overlap in scope.
**Collectively Exhaustive:** siblings cover the full parent scope; no "other" bucket.

**Checks:**
- Can two bullets plausibly contain the same fact? → overlap, merge.
- Does a section titled "Miscellaneous" or "Other" exist? → rewrite the grouping around a better axis.
- Are siblings at different abstraction levels? ("Performance", "Security", "Button color") → re-layer.
- Is there a fact a reader would expect but can't find? → gap, add a branch.

**Useful grouping axes** (pick one axis per level):
- By time (before / during / after)
- By actor (what the user does / what the system does)
- By state (happy path / error / recovery)
- By layer (data / logic / UI)
- By stakeholder (Engineering / Product / CS)

Mixing axes at one level produces overlap. Commit to one axis, then switch axes at the next level down.

## Gate 4 — Revision (Girouard 8 + Cut-30%)

### The 8 rules

1. **Short, simple words.** Target Gunning Fog Index ~9-10 (5th grade reading level). "Sell" beats "divest". "Use" beats "utilize". "Buy" beats "procure".
2. **Strong verbs do the work.** Replace adjective+noun with a single verb. "Quickly reviewed" → "scanned". "Made a decision" → "decided".
3. **Eliminate filler.** Cut "very", "rather", "somewhat", "just", "really", "quite", "basically", "actually", "simply". Read the draft with these words removed; meaning holds.
4. **Simple tenses.** Prefer present / past / future simple. Perfect continuous tenses add cognitive load. "Has been being updated" → "is updating".
5. **Active voice.** "Ms. Perkins gave Jasper an F" beats "Jasper was given an F by Ms. Perkins". Passive hides agency. Allowed when the agent is unknown or irrelevant.
6. **Structure signal.** First sentence summarizes the paragraph. Paragraphs defend their first sentence. If a reader reads only first sentences, they get the argument.
7. **No buried lede.** Critical information in the first screen. Context and caveats later.
8. **Break rules with reader empathy.** Rule-breaking is legitimate only when it serves the reader. "The founder could not be reached" is better active? Not if the point is the non-reachability.

### Cut-30%

Default target on second pass. Tactics:

- Delete sentences that restate the prior sentence.
- Delete conclusions that restate the opener.
- Delete "it is important to note that", "I just wanted to flag", "I think maybe", "perhaps we should consider".
- Delete adjectives that add no information ("significant improvement" → "improvement"; the improvement is either significant-enough to mention or not worth mentioning).
- Read aloud. Anything awkward in the ear is flab in the draft.

If the draft is already terse (common for [Brain Owner]), the cut target is 0-10%. Don't pad to claim a cut.

## Doc-Type Cheatsheet

Minimum required sections per common artifact:

| Artifact | Diátaxis type | Minimum sections |
|----------|---------------|------------------|
| PRD | Explanation + Reference | Problem, Success metric, Scope (in/out), User flow, Open questions, Launch plan |
| RFC | Explanation | Context, Proposal, Alternatives considered, Trade-offs, Decision, Rollout |
| ADR | Explanation (short) | Status, Context, Decision, Consequences |
| Runbook (operational) | How-to | Symptom, Diagnosis steps, Mitigation, Root-cause investigation, Escalation |
| Product guide (CS-facing self-service) | How-to | When-to-use callout (retires prior path), Admin URL, Before-you-start (input sourcing), Field reference, Status lifecycle, Stuck-status decision table, Merchant email templates, Troubleshooting, Escalation, Expected timelines |
| Postmortem | Explanation | Impact (quantified), Timeline, Contributing factors, Action items with owners |
| Handbook entry | Reference or Explanation | One clear purpose, scannable body, no duplicated content from sibling entries |
| Design doc | Explanation + Reference | Goal, Non-goals, Current state, Proposal, Risks, Rollout |
| Release notes | Reference + Explanation | Headline (verb + outcome), Author + ship date, Why it matters (baseline + recovered metric), Status visual (lifecycle/state), Audience-specific actions (CS/Ops, Eng, Merchants), 30-day success check |
| PR description | Reference + Explanation | Behavior (what's broken or what changes), Fix (what this PR does + why this shape over alternatives), Verification (observable outcomes a reviewer can confirm). See "PR Description Review Lens" below. |

**Self-test for every artifact:** Can a reader from outside the originating team act on this without a DM to the author? If no, the doc is incomplete.

## PR Description Review Lens

PR descriptions fail by carrying the author's chronology into the reviewer's context (pipeline numbers, commit SHAs, "fixes #1043", post-mortem timelines). Reviewers want behavior, fix, verification. Apply this 5-item check before opening the PR or after rewriting from draft.

| # | Check | Pass | Fail |
|---|-------|------|------|
| 1 | Lead with behavior, not history | "`datadog_dashboard` rejects tag keys other than `team` and `ai`" | "apply-monitors broke at commit 237b736 on pipeline 73222 ..." |
| 2 | Cross-references only when load-bearing | Cite a PR / ticket / commit only when the reviewer needs it to act | Decorative "introduced in #1043, inherited by #1044, #1045 ..." tables |
| 3 | Rationale for fix shape | "Drop the block; matches the three other dashboards in this directory, none of which declare top-level tags" | "Removes the tags block" (the what, not the why) |
| 4 | Verification framed as observable outcomes | "`apply-monitors` on master will turn green and create the dashboard in Datadog" | "Should work after merge" / "Tested locally" |
| 5 | Ticket linkage in body, not title | One-line "Linked: JULI-XXX" or branch name carries the ID for GitHub-Jira auto-link | Title prefixed with "JULI-XXX:" when the title would read cleaner without it (judgment call; ticket-prefix titles are still fine when integration depends on it) |

**Source:** 2026-05-26 [your-org]-devops #1046. First draft was a Slack-post-mortem (5-row pipeline forensics table, 5 PR/commit cross-refs, who-flagged-who narrative). Benjamin's nit on #1044 ("Generally prefer comments that clarify behaviour or rationale to specific ticket references") applied to the body; rewrite cut all cross-refs and led with the Datadog API constraint.

**Doctrine origin:** the nit was about code comments, but the principle generalizes: PR bodies, commit messages, and code comments all serve a reader who lacks the author's session context. Chronology is the author's scaffolding, not the reader's load.

## Release Notes Review Lens

Release notes target a #releases-style channel: short, scannable, action-oriented for mixed audiences. They fail by carrying writer's scaffolding into reader's context. Apply this 9-item check before publishing.

| # | Check | Pass | Fail |
|---|-------|------|------|
| 1 | Framework labels removed | Bold lead lines or short subheads ("Why it matters", "Action") | "What / So What / Now What" or any framework name visible |
| 2 | Zero em dashes | `:`, `,`, or split sentences | Em dashes mid-sentence ([Your Company] voice rule) |
| 3 | Hedges replaced with numbers | "Manual tickets: ~10–20/month → ≤1/month residual" | "Near-zero", "real-time", "true exceptions", "one of our most" |
| 4 | Acronyms expanded on first use | "[Mobile Team] ([Mobile Team])" | Bare acronym in mixed-audience channel |
| 5 | Runbook link inline | Link directly under the audience bullet that needs it | Link only in parent doc, readers do not navigate up |
| 6 | No prose duplication of visual elements | Either visual (lifecycle arrow) or prose, not both | Prose narrating the same flow shown as `pending → … → completed` |
| 7 | No non-update bullets | Bullet only when audience behavior changes | "No change in experience for X", cut or convert to deterministic value |
| 8 | 30-day success metric present | "30-day check (DATE): metric ≤ threshold" | Announcement without measurable check |
| 9 | Author + ship date at top | "Shipped by [team], [DATE]" | Anonymous or undated post |

**Audience structure:** every release note for #releases needs explicit per-audience action lines. Default audiences: Engineering (FYI / pageable conditions), CS / Ops (workflow change + runbook link), Merchants (experience change). Cut audiences with no behavior change.

**Source:** 2026-04-27 review of release notes review.

## Product Guide Adoption Lens

CS-facing product guides for new self-service admin tools. Adoption is the success metric: if CS routes around the new UI back to the prior path (Jira to engineering, manual handoff), the platform shift has not landed regardless of doc prose quality. Apply this 5-item check before the guide goes wide.

| # | Check | Pass | Fail |
|---|-------|------|------|
| 1 | "When to use this" callout retires the prior path | Top-of-doc callout: "Use this for X. Replaces Y. Do not Z." | Reader cannot tell whether this replaces an existing workflow |
| 2 | Admin URL is inline in the guide | First action step: "Open: <URL>" | URL only in launch announcement / Slack message |
| 3 | "Before you start" input-sourcing | "Gather X (from Catalyst), Y (from merchant), default Z" with named source per input | Form fields documented but reader cannot start cold |
| 4 | Status-anchored "stuck?" decision table | Rows = status × time-stuck, column = action | Symptom-first prose troubleshooting only |
| 5 | Merchant-facing email templates for common follow-ups | Copy-paste templates for the 2-3 follow-ups CS writes most | CS translates technical instructions into merchant-ready prose on the fly |

**Self-test:** Could a CS rep submit their first request in the new tool, get stuck on day 3, and write a sensible merchant follow-up, without opening Slack? If no, the guide will not drive adoption.

**Source:** 2026-04-27 review of product guide review. The 4 edits applied (When-to-use callout, Before-you-start, status-anchored stuck table, merchant email templates) instantiated checks 1, 2/3, 4, and 5 respectively.

## Shared SOP Authoring Rules

Apply when authoring or editing any SOP, playbook, runbook, or process doc whose audience is multi-team (TechOps, R&D, cross-chapter) and whose readers may not have access to the author's local tooling.

| Rule | Check before publish |
|------|---------------------|
| **No individual names in body or callouts.** Use team or role labels (TechOps, [Mobile Team], Dev Support, Engineering Manager, domain reviewer). | Grep the rendered doc for first names of team members before publish. The exception is the EM role label when it is a function name, not a personal reference. |
| **No brain-local slash command references.** Only commands that ship in a shared plugin (`[your-org]-ds-claude-plugins`, `[your-org]-[engineering-toolkit]`, etc.) or are deployed to all readers' environments may appear. Personal `.claude/commands/` and skills file under `~/.claude/projects/` are off-limits. | Before referencing `/foo`, confirm the command is installed for the doc's audience. If unsure, omit. |
| **No reviewer rotation framing unless the user named it.** A comment that says "TechOps review" is a label change, not a rotation policy. Do not add rotation lists or schedules. The author nudges the reviewer pool; the doc says so. | If the input did not contain "rotation" / "schedule" / "rotate", do not add it. |
| **Grep the rendered doc for stale terms after large rewrites.** Multi-section `update_content` batches in Notion can leave deprecated phrases in untouched sections (footers, "What this replaces" lists, template inline references). | After any rewrite of >5 ops, fetch the page and grep for the deprecated terms (old phase numbers, old role names, old command references). Do not report done before the grep is clean. |
| **Track variant scope is the audience's call, not the author's.** When an SOP serves multiple delivery shapes (innovation vs release vs partner-cert), per-track templates need each team's input. Do not invent track variants without confirming the affected team will adopt them. | If the author is not a member of the track team, either confirm with that team before publishing or scope the variant as draft. |

**Source:** 2026-04-28 TechOps AI-Powered Development Workflow playbook v1.5 rewrite. Initial drafts violated rules 1, 2, and 3 across two iterations before user corrections converged the authoring scope. Rule 4 caught 3 stale references that survived a 25-op atomic batch. Rule 5 came from the user's choice to apply v1.5 best options now and let team members review afterward, rather than defer to a co-authored session.

## External-Facing Operational Guides

Apply when authoring or editing a guide that will be shared with a counterparty (merchant, partner, vendor) whose signed contract governs the relationship the guide operationalizes.

| Rule | Check before publish |
|------|---------------------|
| **Mirror the signed contract's scope language.** If the contract uses a single constraint ("X shall not be used for any purpose unrelated to the Services"), the guide echoes that constraint verbatim. Do NOT enumerate "won't transfer ownership, won't modify IP, won't share with third parties" unless those prohibitions are in the signed text. Invented prohibition lists (a) introduce categories of risk the contract never raises, (b) signal distrust to the merchant, (c) diverge from what was legally negotiated. | Read the signed contract before drafting any "what we will / will not do" section. Quote or echo. Never invent. |
| **Lift the contract's consumer-facing intro paragraph into the guide opener.** Most consumer-facing contracts drafted by counsel include a soft-sell paragraph explaining why the agreement exists. Lift it verbatim (or near-verbatim) into the operational guide. The merchant reads the legal doc and the operational doc in close succession; voice consistency between them is a trust signal. | Open the contract Google Doc, copy the intro paragraph, drop into the guide H1+intro slot. Trim only for length, not tone. |
| **No canonical email addresses, page IDs, file paths, or internal handles in the body.** A guide that ships to a counterparty cannot embed `developer.support@example.com` or `360a84ed-4024-...` as load-bearing references. Use the recipient's known contact ("Your [Your Company] contact") and named documents ("Apple Developer Account Access and Credential Sharing Agreement"), not infrastructure pointers. | Grep the rendered guide for `@example.com`, UUID patterns, and `context/`/`12_projects/` paths before publish. |
| **Surface safety guarantees inline at each revocation step.** When a guide enumerates "how to revoke access", each step that is independently sufficient to revoke must say so on the same line, not in a separate paragraph below the list. The reader scans the list, sees "remove the phone (this alone blocks [Your Company])", and stops worrying. | After drafting the revocation list, re-read each step and ask "if a reader stopped here, would they know they are safe?" If not, add the parenthetical guarantee. |

**Source:** 2026-05-18 Apple Developer Account Holder Access program rollout. Initial draft included a "Will not do" list with invented prohibitions ("won't transfer ownership", "won't modify IP", "won't share with third parties"). User pushback: "I think we can sacre [scare] the account owner trusting us... we shiould stick with the contract, what was written in the contract?" Recovery: read the signed contract via Drive MCP, rewrote scope section to mirror [External Contact]'s single constraint, lifted contract intro paragraph verbatim into the guide opener.

## Collaborative Doc Reframe ([Coaching Framework])

Apply when an outbound doc reads as a unilateral directive ("my update", "what I propose", "what I need from you") but the actual work is a joint engagement between two owners. Common shape: meeting pre-reads, working-session anchors, status updates that ride on shared accountability.

The reframe converts a directive doc into a joint working doc using 7 frameworks. Anti-pattern: leaving the doc in "my update" voice when the audience is a co-owner whose authority you need to honor. The doc then reads as assignment, not collaboration.

| [Coaching Framework] framework | Reframe move |
|----------------|--------------|
| F (Win-Win) + N (Triple Win) | Add an explicit "What we both gain" section. Name the peer's win, your win, and the company win. If the peer's win is missing, you do not have a joint doc; you have a directive in joint clothing. |
| H (Interests over Positions) | Replace "owner" with "closest owner + partner". The closest-owner column names the person whose authority moves the lever; the partner column names who needs to be in the loop. This converts position-coded ownership into interest-coded responsibility. |
| I (Questioning Technique) | Replace closed questions ("Does X still hold", "Can you commit") with open ones ("What does X look like now", "How do we want to commit"). Drop "why" entirely. Default to "what" and "how". |
| J (Empathic Listening) | Before adding your own findings, restate the peer's contribution and credit it. Cite their source (Slack thread, ticket, doc) so the doc shows you read their work carefully. |
| L (Reverse Result Chain) | Lead with the desired joint result (e.g., "0 manual segments + both teams bandwidth-freed by end of Q2"), then derive the levers. Not "here are the levers, here is the implied result". |
| R (Communication FOR the receiver) | Voice balance: "we / you / I" not just "I". Address the receiver directly where their authority lives ("What works for your team"). |
| T (Observation over Judgment) | "Closest owner" instead of "owner" (more accurate). "How we package the data" instead of "whose signal pushes priority" (less assignment-coded). |
| G (Courage × Consideration) | Replace unilateral escalation triggers ("If X, I escalate to Y") with joint ones ("If we hit a wall, we align on the escalation message together"). Shared accountability requires shared escalation. |

**Self-check before publishing a doc you call collaborative:**
1. Is there an explicit "What each side gains" section, or is it implied? If implied, the reader will read the doc as assignment.
2. Are open questions ("what / how") or closed ones ("does / can / will")? Closed questions force a binary; open ones invite the peer's framing.
3. Does the doc credit the peer's prior contribution before introducing your own findings? If your findings come first, you signal that yours is the load-bearing input.
4. Does the escalation language say "I" or "we"? Unilateral escalation belongs in a status update to your manager, not in a doc shared with the co-owner.

**Source:** 2026-05-25 [Director] segments one-pager. Initial draft framed the work as "my update" with "what I want to align with [Director]" and a unilateral escalation trigger ("If auto-approve is not on a shipping schedule by end of May, I escalate to [Your CTO]"). User direction: "frame this doc as a collaborative approach between me and [Director]. Apply any [Coaching Framework]'s perspective here to help." Reframe pass produced new "Why we are working on this together" opener, "What we both gain when we get to zero" Triple-Win section, "Closest owner + partner" lever table, all open-form questions, "If we hit a wall" joint escalation. User accepted: "I am OK with this doc."

## Scannability

- **Headings every 150-300 words** on any doc over one screen.
- **Bold** only on terms a scanning reader must notice. Bolding sentences defeats the purpose.
- **Lists** for 3+ parallel items. 2 items stay in a sentence.
- **Tables** for comparison (options × criteria). Not for narrative.
- **Code blocks** for commands, config, and identifiers that must be copied exactly.
- **Links inline**, no "click here". Link the noun.

## Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|--------------|-------------|-----|
| Lede buried in paragraph 4 | Reader bails before the point | Move lede to paragraph 1 |
| "Other considerations" section | MECE violation: the grouping axis is wrong | Re-layer around a coherent axis |
| Mixed Diátaxis types in one doc | Tutorial trapped inside reference | Split into two docs, link |
| Passive voice hiding owner | "Will be done" → who? | Name the actor |
| Adjective stack ("critical, important, significant") | Padding without signal | Keep one or remove all |
| Conclusion restates opener | Reader reads the same idea twice | Cut the conclusion |
| Jargon without definition | Locks out cross-functional readers | Define on first use or drop the jargon |
| "We should probably consider" | Unclear whether it's a proposal | Assert or drop |
| Table with one column | Not a table | Rewrite as a list |
| Screenshot as the only source of truth | Unsearchable, rots with UI | Caption + link to canonical source |
| Recommendations in a "discussion starter" doc | User asked for surface, the draft delivered fixes | Cut "should/recommend/we propose" lines. Pure observation only. Closing line opens questions, does not answer them. Source: 2026-04-27 PRD scope drift Section 4 v1 overshoot |
| Operational hot-fix cited as PRD scope drift | Conflates runtime/ops issues with spec gaps | PRD scope drift = spec missed the requirement at write-time. Operational hot-fix = launch worked but operational state needs ongoing tuning. Drop the example if it is the latter. Source: 2026-04-27 email-domain hotfix miscategorized as [Mobile Team] PRD-drift evidence |

## Co-Activation with Other Skills

| Skill | When to combine | How |
|-------|-----------------|-----|
| `why-lens` | Stakeholder proposals, cross-functional doc, initiative pitch | Run `why-lens` first (framing), then `writing-docs` (structure/revision) |
| `intelligence-layers` | Docs proposing AI features or automations | `intelligence-layers` checks correctness of the architecture in the doc; `writing-docs` checks doc structure |
| `clean-code` | Docs embedding code samples or API references | `clean-code` reviews the code inside the doc |
| `techstack-compliance` | Docs proposing a new tool or service | `techstack-compliance` validates the choice; `writing-docs` validates the proposal prose |

Do not duplicate. Each skill produces one lens block; combine into a single review if all fire.

## Self-Check Before Lens Output

1. Is this doc over ~150 words and authored for future readers? If no, do not produce lens output.
2. Did any gate actually fail? If all four pass, do not produce lens output.
3. Did I flag more than one gate? If yes, cut to the first failure only.
4. Did I use framework jargon in the output? If yes, rewrite in plain engineering terms.
5. Is my output under 5 lines? If no, cut.
