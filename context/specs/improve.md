# Improve Spec

**Owner:** [Brain Owner]
**Pillar:** Pillar 4 (AI Execution)
**Status:** Active
**Last Audit:** [YYYY-MM-DD]

## Behavioral Contract

The improvement loop captures repeatable lessons from a session and routes them to the smallest durable artifact that prevents recurrence.

## Inputs

- Current session transcript or summary.
- Files touched during the session.
- Relevant knowledge categories.
- Existing skills and hooks.
- Error correction log.

## Required Output

- Findings grouped by route: `AGENTS.md`, skill, hook, knowledge file, template, or no-change.
- Proposed diffs for any file change.
- Explicit approval before applying gated changes.
- Commit only after review and approval under the repository operating model.

## Success Criteria

- No duplicate rule is added when an existing rule can be tightened.
- Every new rule has a trigger condition and a verification path.
- Sensitive details are not copied into durable files.

## Failure Conditions

- The loop writes raw conversation content into core folders.
- The loop creates broad always-on rules for narrow one-off events.
- The loop skips verification before committing.
