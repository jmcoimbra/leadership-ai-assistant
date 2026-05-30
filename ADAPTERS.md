# Agent Adapter Guide

This brain is provider-neutral at the file layer and provider-specific at the execution layer. Every agent must read `AGENTS.md` first. Tool-specific adapters below define what else the agent can load or enforce.

## Claude Code

Claude Code has the richest native support in this repository.

1. Open the repository root in Claude Code.
2. Read `AGENTS.md`.
3. Claude loads `.claude/settings.json` for permissions and outbound hooks.
4. Claude discovers `.claude/skills/*/SKILL.md` by frontmatter description.
5. Use `/weekly-review`, `/voice-capture`, `/improve`, and other skills directly.

Expected enforcement:
- Hooks block em dashes, private brain paths, forbidden names, and bare `Pillar N` references in outbound MCP writes.
- Skill frontmatter routes task-specific behavior.
- `scripts/audit_brain.py` catches template drift before commit.

## Codex

Codex reads `AGENTS.md` automatically when the workspace is opened, but it does not execute Claude hooks or slash skills natively.

1. Open the repository root in Codex.
2. Ask Codex to read `AGENTS.md` and the relevant skill file before acting.
3. For a weekly review, say: `Read .claude/skills/weekly-review/SKILL.md and run the mid-week check-in mode.`
4. Before any commit, run `python3 scripts/audit_brain.py` and fix every error.
5. For outbound drafts, ask Codex to run the hook scripts manually against the draft text when the surface matters.

Codex adapter rule: Claude skill files are source material, not executable commands. Codex must apply their procedure explicitly.

## Cursor

Cursor can use the repository as a rules-backed knowledge base.

1. Keep `AGENTS.md` open as the root rule file.
2. Add a Cursor project rule that says: `Read AGENTS.md first. Load .claude/skills/<skill>/SKILL.md when the user names the skill or the task matches its description.`
3. Run `python3 scripts/audit_brain.py` before committing.
4. Use `.claude/hooks/*.sh` as manual validators for outbound drafts.

Cursor adapter rule: do not assume hook enforcement exists unless Cursor has been configured to call the shell scripts.

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
