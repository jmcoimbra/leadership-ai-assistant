# Claude Plugin Ecosystem at [Your Company]

**Owner:** [Brain Owner]
**Pillar:** Pillar 4 (AI Execution)
**Status:** Active
**Last Audit:** 2026-05-24
**Measurable Outcome:** Cut zero-information lookups for "where does X plugin live" to under 30 seconds. Prevent re-proposing existing repos.
**Escalation Trigger:** Any session where a new `[your-org]-<team>-claude-plugins` repo is proposed before this file is consulted.

**Added:** 2026-05-24
**Source:** Session correction after I proposed `[your-org]-ai/mobile-team-ai`, `qa-ai`, `devsupport-ai` as new infrastructure without checking the existing org repos.

## Why this file exists

Before proposing a new team plugin repo, new personal skill pack, or new plugin marketplace, check this file. The [Your Company] Claude plugin ecosystem already has a canonical naming convention, four mature team marketplaces, and one in-use personal-pack pattern. Reinventing wastes turns and produces wrong recommendations.

## Naming conventions (canonical)

| Pattern | Location | Use |
|---------|----------|-----|
| `[your-org]/[your-org]-<team>-claude-plugins` | [your-company] org, private | Team-scoped plugin marketplace |
| `[your-org]/<name>-claude-skills` | [your-company] org, private | Personal skill pack, org-internal |
| `[your-org]-ai/<name>` | [your-org]-ai org, private | Cross-team or platform tooling ([engineering-toolkit], gstack fork, sherlock, general-skills) |
| `<owner>/<name>` (personal GitHub space) | public | Personal-brand artifact, public reference ([Your CDO] uses this) |

## Team plugin marketplaces (all active)

| Repo | Plugin name | Version | Domain |
|------|-------------|---------|--------|
| `[your-org]/[your-org]-mobile-team-claude-plugins` | `mobile-team` | v0.35.0 | Release cuts, ios-deploy, certificates, custom fonts, hotfixes, app updates, iOS/Android builds, certificate renewal, expedite iOS review |
| `[your-org]/[your-org]-qa-claude-plugins` | `qa` | v0.6.0 | Test suite generation, bug triage, PR QA checks, QA automation |
| `[your-org]/[your-org]-ds-claude-plugins` | `ds` | v0.15.0 | Partner ticket triage, API certification, credentials, integration troubleshooting, workspace handoff |
| `[your-org]/[your-org]-manager-plugins` | `em` | v1.6.0 | Sprint reports, 1:1 prep, PR health, meeting follow-up, team metrics, project status |

All four use the same template:

```
.circleci/                # CI pipeline (Jest tests)
.claude-plugin/           # marketplace.json
.claude/                  # embedded skills for contributors
plugins/<team>/           # the shipped plugin
plugins/_template/        # scaffold for new plugins
tests/                    # Jest test suite
.markdownlint.json
CLAUDE.md
jest.config.js
package.json
```

## Org-wide and cross-team

| Repo | Domain |
|------|--------|
| `[your-org]-ai/General-skills` | Org-wide skills available to every [Your Company]er |
| `[your-org]-ai/gstack` | [Your Company] fork of `garrytan/gstack`. Upgrade via `/gstack-upgrade`, upstream merge via `/upstream-sync` |
| `[your-org]-ai/sherlock` | Plugin name `baker_st`. Data investigation tools |
| `[your-org]-ai/[your-org]-[engineering-toolkit]` | Engineering toolkit, cross-team. Internal structure documented in `plugin-architecture.md` |

## Personal skill packs (pattern in use)

Format: `[your-org]/<name>-claude-skills`. Active examples in the [your-company] org:

- `[your-org]/matthew-claude-skills` (Matthew Funcke)
- `[your-org]/yun-claude-skills`
- `[your-org]/kosmin-claude-skills` (Cosmin)
- `[your-org]/bertan-claude-skills`
- `[your-org]/darshan-claude-skills`
- `[your-org]/steve-[your-org]-claude-skills`
- `[your-org]/amanda-claude-backups` (backup pattern, not active development)

## Public personal pack (deliberate exception)

`example-user/ai` ([Your CDO]) is in his personal GitHub space, public. Used as a CTO-trajectory artifact and a reference implementation for spec-driven workflow. [Your CDO] is the only [Your Company]er running a public personal pack to date.

## Adjacent (not standard plugin marketplaces)

- `[your-org]-ai/product-claude-workflows` (Product team workflows)
- `[your-org]-ai/b-AI-ley` (Bailey's AI workspace)
- `[your-org]-ai/PartnerAId` (Partner ops skills)
- `[your-org]-ai/nedAI`, `[your-org]-ai/recoveryai`, `[your-org]-ai/sales-skills`, `[your-org]-ai/sales-daily-digest`, `[your-org]-ai/chris-ai-workspace`
- `[your-org]-ai/claude-workflows` (Collection of Claude Code configurations)
- `[your-org]/claude-workflows`

## Pre-proposal checklist

Before recommending any new repo with `claude`, `plugin`, `skill`, `ai`, `agent`, or `prompt` in the name:

1. Run `gh repo list [your-company] --limit 200 --json name | jq -r '.[].name' | grep -iE 'claude|plugin|skill|ai|agent|prompt'`
2. Run the same against `[your-org]-ai`.
3. If the proposed name (or a near-synonym) already exists, reframe the work as "extend or contribute to the existing repo" instead of "create new".
4. If the proposed repo truly fills a gap, note the gap explicitly: which team, which doctrine, what is missing from the existing options.

## Decision tree for "where should this skill live"

```
Is the skill operator-specific (governance, voice, personal habits)?
├─ Yes, org-internal use → [your-org]/[your-github-handle]-claude-skills (or current personal repo)
├─ Yes, public/CTO-trajectory artifact → <name>/<pack> in personal GitHub space (like example-user/ai)
└─ No, team-scoped doctrine
   ├─ [Mobile Team] team → contribute to [your-org]-mobile-team-claude-plugins
   ├─ QA chapter → contribute to [your-org]-qa-claude-plugins
   ├─ Dev Support → contribute to [your-org]-ds-claude-plugins
   ├─ EM doctrine → contribute to [your-org]-manager-plugins
   └─ Cross-team → [your-org]-ai/General-skills or [your-org]-ai/[your-org]-[engineering-toolkit]
```

## Related knowledge

- `plugin-architecture.md` covers internal structure of `[your-org]-[engineering-toolkit]` plugins (commands/agents/skills triad)
- `harness-ecosystem.md` covers Claude Code harness layout, hooks, plan-mode, MCP loading
- `github-pr-patterns.md` covers gh CLI patterns for inspecting plugin repos
