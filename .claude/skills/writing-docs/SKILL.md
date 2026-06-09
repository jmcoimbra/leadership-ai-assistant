---
name: writing-docs
description: Docs writing lens for PRDs, RFCs, runbooks, handbook entries, design docs, internal wiki pages, and release notes. Applies Diátaxis type routing, Minto SCQA structure, MECE grouping, Girouard 8 revision rules, and a cut-30% target. Defers voice to voice-profile.md. Auto-activates when writing or reviewing docs. Not for Slack messages, PR reviews, 1:1 notes, talent reviews, or brain file edits.
knowledge_file: context/knowledge/writing-docs.md
triggers:
  - writing a PRD, RFC, ADR, design doc, proposal
  - writing a runbook, postmortem, incident review
  - writing a handbook entry, wiki page, Notion knowledge page
  - reviewing any doc over ~150 words meant for future readers
  - reviewing or writing release notes for #releases or merchant-facing announcements
---

# Writing Docs Lens

Auto-triggered lens that checks doc structure and revision discipline before the draft lands. Not a standalone workflow.

Load `context/knowledge/writing-docs.md` when triggered. Sources: Barbara Minto (Pyramid Principle / SCQA), Diátaxis (Daniele Procida), Dave Girouard "A Founder's Guide to Writing Well" (First Round), MECE (McKinsey), Tremendous handbook "Writing Effectively" bundle.

## When Triggered

Auto-activates for documents authored for future readers, over ~150 words, plus release notes regardless of length (public-facing audiences require the same discipline):

- PRD, RFC, ADR, design doc, technical proposal
- Runbook, postmortem, incident review, operational SOP
- Handbook entry, internal wiki page, Notion knowledge page
- External candidate handbook or partner-facing doc
- README or docs/ entries in a repo
- Release notes for #releases channel or merchant-facing announcements (use the 9-item Release Notes Review Lens in `context/knowledge/writing-docs.md`)

Does NOT activate for (dedicated skills already cover these):

| Surface | Use instead |
|---------|-------------|
| Slack messages (DM, channel, thread) | `slack-communication` |
| PR review comments | `pr-review-patterns` |
| Meeting scripts / 1:1 prep | `meeting-prep` |
| Meeting ingestion artifacts | `meeting-ingest` |
| Personal/emotional email | `voice-profile.md` Email Drafting section |
| Talent review narratives | `feedback_no_figures_talent_review.md` |
| Brain file structure (owner/metric/escalation) | `00_foundation/brain_governance.md` |
| Stakeholder framing (WHY) | `why-lens` (co-activate when a proposal is long enough to be a doc) |

## What It Does

Four gates in order. A failure at gate N invalidates gates N+1 downstream. Flag the first failure, offer one concrete fix, stop.

### Gate 1 — Diátaxis type

Pick one. A doc mixing types fails before prose matters.

| Type | Purpose | Reader's job |
|------|---------|--------------|
| Tutorial | Learning by doing | "I want to start here as a beginner" |
| How-to | Task completion | "I have a specific job to get done" |
| Reference | Information look-up | "I need to know exactly what X is or does" |
| Explanation | Conceptual understanding | "I want to understand why this exists" |

If the draft mixes types, split it or declare the primary type and demote the rest to linked sub-docs.

### Gate 2 — Minto / SCQA structure

Lead with the answer. Default for non-trivial docs:

1. **Situation** — shared context the reader already accepts
2. **Complication** — what changed or is broken
3. **Question** — the decision or problem this doc resolves
4. **Answer** — the recommendation up front. Supporting logic follows

The answer sits in the first screen. For short docs (<300 words) SCQA compresses into the opening paragraph. For long docs the answer is a TL;DR block at the top.

### Gate 3 — MECE grouping

Each section or bullet group must be Mutually Exclusive and Collectively Exhaustive. No overlap. No gaps that force the reader to ask "what about X?".

Failure signals:
- Two bullets restating the same concern in different words → merge
- A "miscellaneous" or "other" bucket → rewrite the grouping
- Sibling sections at different abstraction levels → re-layer

### Gate 4 — Revision (Girouard 8 + cut-30%)

Apply before finalizing:

1. Short, simple words. 5th-grade reading level. Cut jargon.
2. Strong verbs. No weak constructions, no adverb padding.
3. Eliminate filler. Target minus 30% on second pass. No "very", "rather", "somewhat", "just".
4. Simple tenses. Prefer present/past/future simple.
5. Active voice.
6. First sentence summarizes the paragraph; paragraphs defend their first sentence.
7. No buried lede. Critical info in the first screen.
8. Break rules only with reader empathy in mind.

## Output Format

Append to the reply drafting the doc:

```
### Docs Lens

**Type:** [Tutorial | How-to | Reference | Explanation] — [one-line justification]
**Structure:** [SCQA present? If not, what's missing in plain terms]
**MECE:** [overlap or gap flagged, or "clean"]
**Revision:** [which Girouard rule needs work, or "clean"]
**Cut target:** [N% estimate based on observed padding, or "at target"]
```

5 lines max. No rewrite unless explicitly asked.

If all four gates pass, produce no lens output. Silence is the correct signal when there is nothing to fix.

## Voice

Voice is owned by `context/knowledge/voice-profile.md`. This skill does not re-state voice rules (em dashes, "Hi" not "Hey", no hedging, deterministic language, PT-BR accentuation). If the draft violates voice, reference voice-profile.md; do not duplicate its rules here.

## Governance

For brain files (`00_foundation/`, `07_operating_rhythms/`, `09_people/`, `10_career/`, `11_compliance_security/`, `12_projects/`), defer to `00_foundation/brain_governance.md` for owner, measurable outcome, and escalation trigger requirements. This skill handles prose discipline; governance handles file structure.

## Rules

- Never rewrite the doc. Flag the first failing gate and offer one concrete fix.
- Never use framework jargon in the output ("Minto", "SCQA", "Diátaxis", "MECE", "Pyramid Principle") unless the reader is a doc practitioner who asked for it. Describe the gap in plain engineering terms.
- Never produce lens output if all four gates pass. Silence is correct.
- Cut-30% is the default target. If the draft is already terse, say "at target" and move on.
- Co-activate with `why-lens` on stakeholder proposals. Co-activate with `intelligence-layers` on AI-feature design docs. Combine outputs; do not duplicate.
- Keep lens output under 5 lines. This is a lens, not a report.

## Step-Body Micro-Structure (per step in any tour, runbook, RFC, or PRD)

Each step in a multi-step doc follows: **transition (1 line)** -> **explanation (2-4 lines)** -> **takeaway (1 line)**. Total per step: 150-300 words.

- **Transition:** picks up from the prior step. Names what just happened or what changes now. Never start a step as if the reader arrived out of context.
- **Explanation:** the substance. Why this step exists, what it accomplishes, what the reader sees or does.
- **Takeaway:** the one thing the reader should remember. A pointer forward (next step) or a constraint they must carry.

**Over 400 words per step:** the step is covering two things. Split it. Tightening prose past 400 rarely helps; structure does.

**Under 150 words per step:** either the step is trivial enough to fold into a neighbor, or it is missing context.

**Quality checklist (apply to each step before output):**
- Does the transition reference the prior step (or, for step 1, frame the doc's entry point)?
- Does the explanation answer "why this step now" without restating the prior step?
- Does the takeaway leave the reader knowing what changed or what to carry forward?
- Word count between 150 and 300?

Pattern source: nilbuild/diffity tour skill, "step body structure". Direct upgrade to the brain's "execution density" rule, which was previously a vibe and is now measurable.

## Specialized Surface Rules (migrated from memory tier 2026-04-27)

- **Exec docs:** no inline names of individuals, no internal-only items, one metric per cell. Audience is a CEO/CDO scanning a one-pager; remove anything that requires Slack-context to interpret.
- **Numbered rows with pipes = table cell mapping.** When the user lists `1. cell A | cell B | cell C` style content, treat it as a table row, not prose. Render as a markdown table.
- **Status indicators use emoji**, not text: 🔴 / 🟡 / 🟢, not RED / YELLOW / GREEN. Emoji scans faster in dashboards.
- **Talent review narratives:** remove figures, numbers, and dates that pad achievement. Keep only gap-evidence numbers + structural band/cadence markers ("3 PRs reviewed weekly", "Tier-3 → Tier-4 trajectory"). No project-by-project metric lists.
- **No Jira ticket IDs or Notion DB paths in talent-review narratives.** Project names are fine; breadcrumbs out. The reviewer is reading a person, not a workstream tracker.
- **Expand acronyms on first use.** Apple PLA = Program License Agreement. [Mobile Team] = AppOps. PCV = Production Change Validation. CS / Impl, TechOps, OOO all need parenthetical expansion in scripts and tables. Audience defaults to outside-the-team.
- **Direct-report asks: drop "I'm presenting to R&D Leadership and..." framing.** Manager-direct reason only. Leadership context is a leak; the ask should stand on its own merit to the recipient.
- **Drive doc findings: per-finding Ctrl+F anchors.** When commenting on a Drive doc the user already owns, give them text anchors they can paste into Ctrl+F to land on the exact spot. Do not give folder URLs or full file URLs.
- **Never assert claims not carried by evidence.** Thin evidence = rewrite as a question ("Is X confirmed?"). Stale evidence (>14 days, project moved on) = cut the line entirely. No self-commits in async drafts.
- **Throughput-acceleration projects:** exit criteria must measure the throughput verb (lead time, cycle time, units shipped), not compliance deliverables ("audit doc done"). Compliance is a side-effect of throughput, not the goal. Reframe drafts that flip this.
- **Looker dashboards built manually in UI, not via API.** When a doc references a Looker dashboard build, do not propose API-driven build automation. Looker builds are intentional manual UI work; the dashboard URL is the artifact, not the build script.
- **Single-line policy flip = single-line doc.** When the change is a policy reversal in a SKILL.md / AGENTS.md / CLAUDE.md / README.md surface (e.g., "never include X" → "always include X"), the replacement text is one line. Justification (rationale, downstream metric impact, supported variants, source-of-truth references) goes in the PR description, not the doc. Source: 2026-05-06 [engineering-toolkit] Co-Authored-By policy flip — first draft wrote a 27-line block + 5-agent matrix + [Your IDP Tool] aggregator explainer; correct version is one bullet citing the canonical trailer.
- **Name structural references explicitly.** When a doc uses A/B/C, 1/2/3, tiers, levels, phases, or any other enumerated identifier the reader must understand, define what each one means in the doc itself or link to the canonical map. Never reference "Phase B" / "Tier 2" / "Level 3" without binding the series. **Why:** 2026-05-06 — [Team Lead]'s repo phase doc referenced "Phase B in-progress work" and "C1-C9 scope" without enumerating Phase A or B, forcing reviewer to grep the TechOps Projects DB to reconstruct the series. **How to apply:** when authoring or reviewing a doc, scan for unbound enumerated references; either inline a one-line phase/tier map at the top or link to the canonical definition. Same rule applies to runbooks and playbooks: if a series exists, the doc must require the author to name it.
- **No opaque short-form cross-section references in outbound docs.** Never write `§N`, `§5-B`, `§6`, or any other section-symbol shorthand alone when pointing to another section of the same doc. Spell out the target section with its heading on first reference (`section 5 part B (Peer-reviewer execution)`, `section 6 (How will you know it is working / broken)`, `the layer-1 rollback in section 8 (Rollback plan), which is the LaunchDarkly flag-flip in under 30 seconds`). Subsequent references in the same paragraph can shorten (`the rollback plan`, `the break-signal subsection`) once the binding is established. **Why:** 2026-05-18 user correction on the PR #250 PCVC entry. Notion body had 13 `§N` cross-section references; user reaction: "I have no clue on what you are describing." Short-form refs force the reader to context-switch back to the table of contents before they can act on a sentence. The PCVC template at [your-company]/wiki uses `§` ergonomically for its authors but readers (peer reviewers, EM countersigners, downstream auditors) lose context every time. **How to apply:** applies to Notion PCVC entries, Notion reviewer checklists, RFCs, design docs, runbooks, postmortems, handbook entries, Slack/email/Jira drafts. Does not apply to internal scratch files in `.context/`, brain `12_projects/` files that stay internal, or code comments.
