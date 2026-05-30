# PR Review Patterns Spec

**Owner:** [Brain Owner]
**Pillar:** Pillar 4 (AI Execution)
**Status:** Active
**Last Audit:** [YYYY-MM-DD]

## Behavioral Contract

PR review patterns convert review observations into actionable comments with severity, file reference, and requested change.

## Inputs

- PR diff.
- Repository conventions.
- Relevant code-delivery knowledge files.
- Voice profile.

## Required Output

- Findings ordered by severity.
- Each finding states impact, affected line or function, and exact requested change.
- Distinguish blocker, suggestion, and question.
- Avoid praise, hedging, and generic style commentary.

## Success Criteria

- Every blocker describes a concrete bug, regression, security risk, data risk, or operability failure.
- Every suggestion is labeled as non-blocking.
- No comment reveals private brain paths or internal-only context.

## Failure Conditions

- The review leads with summary instead of findings.
- The review asks vague questions where a requested change is possible.
- The review comments on untouched code without tying it to the diff risk.
