# Specs Index

**Owner:** [Brain Owner]
**Pillar:** Pillar 4 (AI Execution)
**Status:** Active
**Last Audit:** [YYYY-MM-DD]

## Purpose

Registry of behavioral specs for long-running skills and workflows. The session learning capture skill reads this file before checking whether session behavior matched the intended contract.

## Registered Specs

| Workflow | Spec | Scope |
|----------|------|-------|
| improve | `context/specs/improve.md` | End-of-session learning capture and routing |
| pr-review-patterns | `context/specs/pr-review-patterns.md` | PR review finding shape and severity discipline |
| weekly-review | `context/specs/weekly-review.md` | Weekly operating review inputs, outputs, and failure modes |

## Maintenance Rule

When a skill exceeds 200 lines or carries an evaluator rubric, add a row here and create a spec in `context/specs/`.

## AI Integration

Use AI during the session learning capture workflow to compare session behavior against the registered spec and classify drift as `SPEC-MATCH`, `SPEC-DRIFT`, `SPEC-GAP`, or `SPEC-WRONG`.
