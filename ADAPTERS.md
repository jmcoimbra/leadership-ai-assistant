# Agent Adapter Guide

This brain is provider-neutral at the file layer and provider-specific at the execution layer. Every agent must read `AGENTS.md` first. Tool-specific adapters below define what else the agent can load or enforce.

## Skill Model

Use this model across every tool:

1. `AGENTS.md` sets always-on constraints.
2. Operator workflows live in `.claude/skills/` and are loaded explicitly when the task matches.
3. Auto-activation lenses also live in `.claude/skills/`, but they are overlays, not user-facing entrypoints.
4. `context/knowledge/skill-runtime.md` holds shared runtime guidance that used to live in command-era scaffolding.

Core operator workflows in this skeleton:
- `weekly-review`
- `voice-capture`
- `career-brief`
- `improve` (session learning capture)
- `pr-review-patterns`

Core auto-activation lenses:
- `decision-protocol`
- `why-lens`
- `writing-docs`
- `management-lens`
- `staff-development`

## Claude Code

Claude Code has the richest native support in this repository.

1. Open the repository root in Claude Code.
2. Read `AGENTS.md`.
3. Claude loads `.claude/settings.json` for permissions and outbound hooks.
4. Claude discovers `.claude/skills/*/SKILL.md` by frontmatter description.
5. Load the relevant skill file before acting. Some workflows may also appear in Claude's slash UI when `user_invocable: true` is set, but that is optional convenience, not the contract.

Expected enforcement:
- Hooks block em dashes, private brain paths, forbidden names, and bare `Pillar N` references in outbound MCP writes.
- Skill frontmatter routes task-specific behavior.
- `scripts/audit_brain.py` catches template drift before commit.

## Codex

Codex reads `AGENTS.md` automatically when the workspace is opened. Skills are auto-discovered from `.agents/skills/` (symlinked to `.claude/skills/`). Codex does not execute Claude hooks natively and has no frontmatter-based auto-activation.

1. Open the repository root in Codex.
2. Codex reads `AGENTS.md` on startup — constraints and voice rules apply immediately.
3. Use the **Skill Routing** table at the bottom of `AGENTS.md` to identify which skill file matches the task.
4. Load the skill file explicitly: `Read .agents/skills/<skill>/SKILL.md and follow its procedure.`
5. Before any commit, run `python3 scripts/audit_brain.py` and fix every error.
6. For outbound drafts, run the relevant `.claude/hooks/*.sh` scripts manually against the draft text.

Codex adapter rule: skill files are source material, not the product contract. Apply the procedure explicitly — Codex does not auto-execute them.

## Cursor

Cursor can use the repository as a rules-backed knowledge base.

1. Keep `AGENTS.md` open as the root rule file.
2. Add a Cursor project rule that says: `Read AGENTS.md first. Load .claude/skills/<skill>/SKILL.md when the user names the skill or the task matches its description.`
3. Run `python3 scripts/audit_brain.py` before committing.
4. Use `.claude/hooks/*.sh` as manual validators for outbound drafts.

Cursor adapter rule: do not assume hook enforcement exists unless Cursor has been configured to call the shell scripts.

## Conductor

Conductor runs agents in isolated workspaces. This repo ships a shared `.conductor/settings.toml` for settings that help every adopter and leaves machine-specific details in `.conductor/settings.local.toml`.

Inside Conductor:

1. Open the workspace root and read `AGENTS.md`.
2. Use `ADAPTERS.md` to choose the right operator workflow or lens.
3. Prefer skill-first prompts over command-era phrasing.
4. Treat Claude slash invocation as optional. The shared repo contract is still `AGENTS.md` plus skill files.

## Generic CLI Agents

Any filesystem-based agent can use the brain with this read order:

1. `AGENTS.md`
2. `context/knowledge/categories/README.md`
3. One to three category files matching the task
4. One skill file from `.claude/skills/` when a task-specific workflow exists
5. The domain file being edited or reviewed

Before final output:
- Run `python3 scripts/audit_brain.py` after file changes.
- Run the relevant `.claude/hooks/*.sh` scripts against outbound drafts.
- Do not send external communication without the brain owner's explicit approval.

## Git Safety

Git read commands can run in parallel. Git commands that mutate repository state must run alone: `git add`, `git commit`, `git merge`, `git rebase`, `git cherry-pick`, `git push`, and any command that writes `.git/index`. After a merge conflict, resolve files, run `git add` only after no other git process is active, then run the audit before committing.

## Adapter Maintenance

When adding a new durable behavior:

1. Put always-on rules in `AGENTS.md`.
2. Put scoped procedures in `.claude/skills/<skill>/SKILL.md`.
3. Add provider-neutral validation to `scripts/audit_brain.py` when the rule can be checked mechanically.
4. Update this file only when the behavior changes how a tool should run the brain.
