# Claude Code Hooks: Authoring Patterns

**Added:** 2026-04-28
**Last Updated:** 2026-05-01 (added brain-paths and names hooks alongside em-dash; three guards wired to the same outbound matcher; matcher expanded from 16 to 25 outbound surfaces; "Before Authoring a New Hook" checklist added near top after JSON-escape regression in brain-paths first-pass write; matcher re-evaluation rule added as gotcha #6 after silent-inheritance gap caught by user prompt)
**Owner:** [Brain Owner]
**Pillar:** Pillar 4 (AI Execution)
**Source:** Em-dash voice-rule guard implementation (2026-04-28 APS2-1114 session). Extended 2026-05-01 with brain-internal path leak guard and identity-correctness guard (names + [Peer Manager] pronouns).

Patterns for authoring Claude Code PreToolUse hooks in `.claude/settings.json`. Hooks are harness-enforced rules that block tool calls before execution. They are the safety net for failures that skill-text rules cannot prevent.

## Before Authoring a New Hook

Before writing any new `.claude/hooks/*.sh`, run this 4-step pre-flight or the same regressions will recur:

1. **Read the Authoring Gotchas section below.** All 6 gotchas apply to every new hook, not just the original em-dash hook. The JSON-escape rule (`(\\)?<char>` for any escapable boundary character) is the single most common miss.
2. **Re-evaluate the matcher.** When adding a hook to an existing matcher, the matcher is now responsible for N hooks, not 1. Identify outbound surfaces missing for the NEW threat model (e.g., brain-paths leak surfaces are wider than em-dash voice surfaces because path leaks happen on issue creation, KB articles, etc.). See gotcha #6.
3. **Run the Self-Test Protocol below** with at least 4 cases per hook: literal-bad, JSON-escaped-bad, lookalike-no-match, clean-pass.
4. **Verify the matcher list against the live tool registry.** New MCP tools land between sessions. Re-derive the outbound list from the current tool list, do not copy from a prior settings.json blindly.

Source: 2026-05-01 brain-paths first-pass write shipped without JSON-escape coverage and inherited the em-dash matcher's 16-surface gap. Both regressions were already documented (gotcha #1, gotcha #5) but did not fire at write time because the gotchas section sat below the Reference Implementation, not above. Section reordered for visibility.

## When to Use a Hook (vs. a Skill Rule)

| Failure mode | Right layer |
|--------------|-------------|
| Voice/style violations (em dashes, banned words, "I'm" vs "I am") | **Hook** |
| Workflow logic ("load file X before drafting Y") | **Skill** (instructional) |
| Tool-input validation needing AI judgment | Skill + agent self-check |
| Tool-input validation that is purely syntactic | **Hook** |

Skill-text rules enforce roughly 95 percent of cases. The last 5 percent leak through under cognitive load, time pressure, or when the rule is in CLAUDE.md but not surfaced at action time. A hook is the safety net.

**Recurrence test:** if a voice or style rule fails 3+ sessions in a row across multiple skills, the rule cannot be enforced via skill text alone. Build a hook. Trigger pattern observed in `deep-agent-evals.md` B10: 6 sessions of em-dash failures across pr-review, pr-sweep-reviewer, and em:review-checklist before the hook landed.

## Config Structure (`.claude/settings.json`)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "tool1|tool2|tool3",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.sh"
          }
        ]
      }
    ]
  }
}
```

Rules:
- `matcher` is a regex with `|` alternation. Enumerate by **outbound surface**, not by frequency-of-use. Infrequent surfaces are exactly where bypasses leak.
- `command` MUST use `${CLAUDE_PROJECT_DIR}` for path stability across cwds. Relative paths break in worktrees and subdirectory invocations.
- Multiple PreToolUse blocks are allowed if matchers do not overlap.

## Script Contract

The hook script receives the tool call payload as JSON via stdin:

```
{
  "session_id": "...",
  "transcript_path": "...",
  "cwd": "...",
  "tool_name": "...",
  "tool_input": { ... }
}
```

Exit codes:
- `0` allow the tool call to proceed
- `2` block the tool call. Stderr is shown to Claude as error context.
- Other non-zero non-blocking error logged to user.

## Reference Implementation: Em-Dash Voice Guard

`.claude/hooks/check-em-dash.sh` (`chmod +x`):

```bash
#!/bin/bash
INPUT=$(cat)
if printf '%s' "$INPUT" | grep -qE '—|\\u2014'; then
  cat >&2 <<'MSG'
Em dash detected in outgoing content.
Voice rule: no em dashes. Use periods or rewrite, then retry.
MSG
  exit 2
fi
exit 0
```

Matcher in `.claude/settings.json` (25 outbound surfaces, expanded 2026-05-01):
- Notion: `notion-create-comment`, `notion-create-pages`, `notion-update-page`
- Slack: `slack_send_message_draft`, `slack_send_message`, `slack_schedule_message`, `slack_create_canvas`, `slack_update_canvas`, `slack-stable__send_message`
- Jira (both MCP namespaces): `addCommentToJiraIssue`, `createJiraIssue`, `editJiraIssue`
- GitHub: `create_pull_request_review`, `add_issue_comment`, `create_pull_request`, `create_issue`, `update_issue`
- Gmail: `create_draft`
- Front: `create_comment`, `update_comment`
- Zendesk: `create_article`, `update_article`

## Reference Implementation: Brain-Path Leak Guard

`.claude/hooks/check-brain-paths.sh` (`chmod +x`):

Blocks any outbound containing a brain-internal path prefix (`00_foundation/`, `01_strategy/`, ..., `13_infrastructure/`, `99_archive/`, `context/knowledge/`). Concepts named in those files are fine; only the path is private.

Source rule: CLAUDE.md Contextual Rules. "No brain-internal file path may appear in outbound content."

## Reference Implementation: Identity-Correctness Guard

`.claude/hooks/check-names.sh` (`chmod +x`):

Two checks in one script:
1. Name and tool typos (case-insensitive): `Coimbra-Prado`, `Giovanni`, `[other-transcription-tool]`. Past slips logged in CLAUDE.md.
2. [Peer Manager] pronoun violation: blocks when `[Peer Manager]` and any of `she/her/hers` co-occur in the input. Known false positive when "[Peer Manager]" and a feminine pronoun referring to a different person appear in the same message; error guides restructuring.

Source rules: CLAUDE.md Hard Constraints. Names, Pronouns, Tools.

All three hooks (em-dash, brain-paths, names) are wired to the **same outbound matcher** in `.claude/settings.json`. Any outbound surface (Notion, Slack, Jira, GitHub, Gmail) runs all three sequentially.

## Authoring Gotchas

1. **JSON-escaped vs. literal Unicode.** Claude can serialize the same character as `—` literal or `—` escape. Hook regex MUST match BOTH: `'—|\\u2014'`. Verified via stdin self-test.
2. **Do not `set -e` on `grep -q`.** `grep -q` returns 1 on no-match (the success-path for an "allow" hook). `set -e` would mis-treat that as fatal.
3. **`printf '%s'` over `echo`.** Preserves multi-byte chars without word-splitting and never interprets escapes.
4. **Heredoc body for stderr messages.** `cat >&2 <<'MSG' ... MSG` (single-quoted delimiter prevents shell expansion). The body is plain text shown back to Claude or user, so emitting an em dash in the rule explanation is fine; that is UI, not outgoing content.
5. **Matcher coverage by outbound surface, not frequency.** Enumerate every tool that produces content read by others. Notion page-update was missed in the first pass and caught in self-review.
6. **Matcher re-evaluation when adding a hook.** When wiring a new hook into an existing matcher, do NOT silently inherit the prior coverage list. Each hook has its own threat model. Em-dash threat = voice slip on outbound communication. Brain-paths threat = private path leak on any text seen by others. Names threat = identity-correctness on every outbound surface mentioning a person. Threats with broader surfaces require broader matchers. 2026-05-01 regression: brain-paths and names hooks inherited the em-dash matcher's 16 surfaces and missed GitHub `create_issue`/`update_issue`, Slack canvas/schedule, Front comments, Zendesk articles. User prompt forced the extension. Coverage went from 16 to 25 surfaces in commit `da0a84ad`.

## Self-Test Protocol

Before merging a hook, test 3 cases:

```bash
# Block (literal)
printf '%s' '{"text":"hello — world"}' | .claude/hooks/<script>.sh; echo $?  # expect 2

# Block (JSON-escaped)
printf '%s' '{"text":"hello \\u2014 world"}' | .claude/hooks/<script>.sh; echo $?  # expect 2

# Pass (clean)
printf '%s' '{"text":"hello world"}' | .claude/hooks/<script>.sh; echo $?  # expect 0
```

Verify settings.json is valid JSON:
```bash
python3 -c 'import json; json.load(open(".claude/settings.json"))'
```

## Cross-References

- `voice-profile.md` line 166 em dash rule definition
- `error-correction-log.md` "Em dashes in outgoing content" entry
- `.claude/skills/slack-communication/SKILL.md` Guardrails references the hook
- `.claude/skills/pr-review-patterns/SKILL.md` Review Posting references the hook
- `.claude/skills/review-checklist/SKILL.md` Step 6 references the hook
- `deep-agent-evals.md` B10 voice-compliance entries recurrence history

## Open Items

- `_pr-review.md` Step 3d sanitization (added 2026-04-27 PR #459 retro) and `_pr-sweep-reviewer.md` Step 4.7 sanitization (added same date) should reference the hook as the harness backstop. Skill files were not edited in the 2026-04-28 hook landing session due to /improve auto-apply scope (knowledge-only). Apply on next session that touches those skills.
