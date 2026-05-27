# Zapier AI Fluency Rubric — Operational Knowledge
> Source: Zapier blog (Wade Foster, May 2025; V2 March 2026), @aschwags3 tweet (April 2026) | Owner: [Brain Owner] | Pillar: Pillar 4 (Embrace AI at every level) | Last Updated: 2026-04-09

Zapier's 4-tier AI fluency framework applied to hiring, onboarding, and team development. V2 (March 2026) raised the Capable bar from "used AI with purpose" to "AI embedded in core work with repeatable systems and measurable impact." Used as descriptive vocabulary alongside [Your CEO]'s [Your Company] AI 7-tier ladder. [Your CEO]'s 7-tier ladder is the scoring system of record (definitions TBD — see `03_ai_native_transformation/ai_tier_framework.md`).

> Measurable Outcome: Zapier V2 levels referenced in every IDP hiring scorecard by 2026-05-31
> Escalation Trigger: If hiring begins for [Brain Owner]'s teams without AI fluency bar defined in interview scorecard

## Cross-Framework Crosswalk

Approximate crosswalk of Zapier V2 and peer EM frameworks. Used for translating historical 1:1 logs. [Your Company] AI 7-tier is canonical — these are descriptive references only.

| Zapier V2 | [Peer Manager] Perf Eval | [Peer Manager 2] Measuring Doc | Description |
|-----------|----------------|------------------|-------------|
| Unacceptable | — | Not yet | No AI usage, resistant or no mention |
| Capable | Basic | Using | AI as reference tool, ad-hoc, copy-paste |
| Adaptive | Integrated | Reflexive | AI as daily co-pilot, 50/50 human-AI |
| Transformative | Accelerating | Championing | AI as autonomous workflow, human designs and reviews |
| — | Multiplying | — | Re-engineers how the team/org operates with AI |

Source threads: #rnd-leadership Apr 8 (Zapier rubric + hiring), Apr 17 ([Your CEO] 7-tier adopted as canonical).

## What Zapier Adds

### Hiring Application

Zapier assesses AI fluency at 4 touchpoints. Adapted for [Your Company] hiring:

1. **Resume screen** — Look for AI fluency signals: AI tools mentioned, AI-assisted projects, brain repos, automation evidence, prompt libraries
2. **Interview** — Role-specific AI probes (see Hiring Application section in `ai_tier_framework.md`)
3. **Take-home** — AI-resistant evaluation design per `ai-resistant-evals.md`. Require AI transparency, OOD sub-problems, process artifacts
4. **Executive** — AI fluency slope: trajectory and learning momentum matter, not just current level

**Minimum bar:** Walk-entry (Zapier's "Capable V2"). Cannot hire anyone who treats AI as a search engine.

**Manager bar:** Run minimum. Must demonstrate team-wide AI adoption leadership, psychological safety creation, workflow redesigns.

**AI fluency slope** (Zapier concept): A candidate at Walk who moved from Crawl 3 months ago and shows acceleration is more valuable than a candidate who has been at Walk for a year with no trajectory. Probe: "Where were you with AI tools 6 months ago? What changed?"

### [Peer Manager]'s Interview Questions ([Your Company]-specific, from Apr 8 thread)

Standard AI questions (every phone screen):
- "How do you use AI tools in your daily development work?"
- "How have you driven AI adoption for developer productivity? Not AI features you ship, but how you and your team work day to day."
- "Show me something reusable you have built with AI. A workflow, a tool, a prompt library. Not a one-off."
- "Tell me about a time AI gave you a wrong or misleading answer. How did you catch it and what did you change?"

Follow-up probes (signal differentiators):
- **Compounding probe:** "What have you done to make sure the gains are not just individual? Built anything others can reuse?"
- **Context switch challenge:** "You have five agents working for you. Don't you find the context switch has just shifted elsewhere?"
- **Tool specificity:** "Have you used Claude Code specifically? Built any MCPs? Connected your dev environment to external data?"
- **The redirect:** When candidate describes RAG pipeline: "That is impressive but I am asking about how you work day to day, not what you ship."

### Accountability Axis (V2)

Zapier V2 added a 4th evaluation axis: responsibility for AI-generated outputs. Pairs with blind-delegation detection:

- Self-Assessment Q4: "Walk me through one decision you changed from what AI suggested. Why?"
- If candidate cannot explain a specific implementation choice in their own AI-produced output = delegating, not collaborating
- Downgrade tier regardless of output volume
- Cross-ref: `ai-resistant-evals.md` Rule 3 (AI Collaboration Required, Not Banned)

### [Peer Manager]'s Key Finding

AI score 5 does not predict hiring. Three of the strongest AI candidates were rejected at architecture/live coding stages. "AI sophistication in conversation does not equal execution ability under pressure." Weight AI fluency as meaningful signal alongside other competencies, not standalone gate.

Research backing: Anthropic (Tristan Hume, 2025) found standard engineering problems are training-data-vulnerable. A candidate scoring 5 on AI fluency may delegate effectively without understanding output. See `ai-resistant-evals.md`.

## Gaps in Zapier's Rubric

1. **No blind-delegation detection.** Zapier does not address engineers who appear Transformative but delegate without understanding. [Your Company] probe Q4 catches this
2. **Shallow behavioral indicators.** "Using popular tools with <3 months experience" is vague vs [Your Company] evidence bar ("AI tool open during active work, at least 1 task per day where AI produces the first draft")
3. **No evaluation stage gates.** Zapier is descriptive. [Your Company] AI Tier framework defines formal transition requirements with evidence
4. **No cross-functional teaching.** No expectation that engineers extend AI thinking beyond their function
5. **No escalation triggers.** Descriptive rubric without enforcement mechanisms

## [Peer Manager 2]'s Measuring AI-Native Teams Framework

Notion doc: `317a84ed4024815995c6d28ccc826562`. Three measurement layers:

1. **Layer 1: Individual Adoption** — Active users, usage volume, unprompted AI mentions, maturity level per person
2. **Layer 2: Workflow Impact** — Bug resolution cycle time (AI-assisted vs not), PR throughput, investigation time
3. **Layer 3: Automation Progress** — Bug lifecycle stages (triage → investigation → fix → review → validation), current vs target AI involvement

IDP template: `33ca84ed40248174a3d8c8258b68647d`. Uses [Peer Manager]'s Basic/Integrated/Accelerating/Multiplying labels. AI competency woven into goals, not a separate checkbox. Expected by seniority: L3=Integrated, L4=Accelerating, L5=Multiplying.

## Cross-References

| File | Connection |
|------|-----------|
| `03_ai_native_transformation/ai_tier_framework.md` | [Your Company] AI 7-tier framework (single source of truth for tier assignment) |
| `context/knowledge/ai-resistant-evals.md` | Take-home evaluation design, blind-delegation detection |
| `context/knowledge/ai-agents-in-action.md` | 7-component diagnostic for AI systems |
| `03_ai_native_transformation/ai_baseline_assessment.md` | Per-team current state baselines |
| Notion `33da84ed402481c9905aeec78fa74d72` | [Peer Manager]'s Proposed Job Posting Updates with AI Competency Requirements (all 5 engineering roles). Claude Code as primary tool, Rails reframed as preferred not required for 4+ AI candidates |
