---
name: pr-review-patterns
description: GitHub PR review posting, severity rules, team reviewer management, post-fix cleanup, and review workflows. Use when reviewing PRs, posting review comments, addressing review feedback, or managing PR review state.
---

# PR Review Patterns

## Pre-Open Review Gate (mandatory)

Before opening any PR (`gh pr create`, `git push` followed by PR creation), run a self-review pass and fix every finding. Order: **review, fix, then open.** Never reverse it.

- For [Your Company] repos with `[engineering-toolkit]:review` available: run it on the local branch in author mode.
- For repos without it: do an inline self-review against the [engineering-toolkit] review criteria (correctness, security, performance, deployment risk, reversibility, QA, a11y when UI files change). The review-criteria skill is the single source.
- Fix every finding before opening. If a finding is intentionally skipped, name it in the PR description under "Out of scope" with the reason. Do not surface findings to the reviewer that you already saw and chose to leave.
- The PR-author burden is to land a clean diff for review, not a draft for the reviewer to triage. Reviewer time is the limiting factor.

**Why:** Asking reviewers to catch issues you can self-detect wastes their cycles and trains them to expect noise. Author-side self-review is cheaper, faster, and produces a cleaner PR description.

**How to apply:** Applies to all PRs in all [Your Company] repos including the brain. Source: 2026-05-01 [Brain Owner] correction after PR #18 was opened without a pre-open self-review pass. Verbatim: "I want you to remember to do it even before opening the PR, moving forward."

## Robo[your-company] Per-SHA Review Pass (anticipate N+1 rounds)

`robo[your-company]` ([Your Company] review bot, configured on most [your-company]-org repos) fires a fresh review pass on EVERY new SHA pushed to the PR head. This means:

- A fix push that addresses N prior findings can surface M new findings on the now-touched code, including spec-style nits that didn't exist on the prior SHA.
- Budget for 3-5 rounds of fix-and-rebut on non-trivial PRs. The convergence is not always monotonic: a stylistic fix to one block can introduce a different cop violation elsewhere.
- The fix loop is bounded only when (a) all findings are addressed AND (b) no new findings surface on the next pass. Resolving threads (per the Post-Fix Cleanup sweep above) does NOT prevent new threads on the next SHA.

**Pre-flight rubocop / lint locally before push.** When `bundle install` is blocked (e.g. nexus credential-on-master in Gemfile.lock), use `qlty check --fix --level=low` on the touched files. Qlty wraps rubocop and catches most cops without running bundle. Skipping the local lint pass guarantees one extra cycle: the lint cop fails in CI, you push a fix-up commit, robo[your-company] reviews the fix-up, a new round starts.

**Common cops that bite on Ruby/RSpec PRs:**
- `RSpec/InstanceVariable`. `@foo` in `before`/`it` blocks. Replace with `let(:foo) { [] }` plus push into the let-returned array from `before`.
- `RSpec/MultipleExpectations`. Multiple `expect` in one `it`. Split into one `it` per `expect`, share fixtures via `let`.
- `Style/Lambda`. Use `->()` short form, not `lambda do ... end` for one-liners.
- `Style/ExplicitBlockArgument`. Pass `&block` explicitly instead of `yield`.

Source: 2026-05-19 nexus#290 JULI-251. 4 review rounds, each fix push surfaced new cop violations or new spec-style findings. Round 1: Lambda + ExplicitBlockArgument. Round 2: 5 new mediums (forbidden_fields drift, picker_columns sync). Round 3: 7 new mediums (instance-vars in `it`, multi-expect, context naming). Round 4: 1 medium (PCVC §2 doc gap). Final convergence at SHA `718777394b` after the PCVC blast-radius sentence was added to PR body.

## Review Posting

- **Single-shot:** POST `/repos/{org}/{repo}/pulls/{n}/reviews` with `event`, `body`, `comments[]`, and `commit_id` in one call.
- **No attribution prefix.** Do not prepend `[your-company]:review ·` or any similar tag to review bodies or comments. GitHub already displays author and timestamp. The prefix is noise.
- **Review body = decision marker only.** One line: `REQUEST_CHANGES: N MEDIUM, M LOW. See inline.` plus one sentence on the most important blocker. Never restate findings that inline comments already carry.
- **No em dashes** in review body or inline comments. Voice rule from `context/knowledge/voice-profile.md` line 166. Grep for `—` before calling `create_pull_request_review` or `add_issue_comment`. The PreToolUse hook in `.claude/settings.json` blocks GitHub review/comment tool calls containing em dashes.
- **Always use GitHub `suggestion` blocks** when the fix can be expressed as a line replacement. For multi-line suggestions, use `start_line` + `line` params.
- Get latest commit SHA: `gh pr view --json commits --jq '.commits[-1].oid'`

## Severity → Outcome Rule (Deterministic)

- Critical / High / Medium → **REQUEST_CHANGES** (automatic, no override)
- Low only → **COMMENT**
- No findings → **APPROVE**
- "Medium but not blocking" is still REQUEST_CHANGES.
- If CHANGES_REQUESTED, associated task stays In Progress.

## Submit Immediately

- PENDING reviews are invisible in GitHub UI. Author must go to Files tab → "Finish your review" to see.
- After creating draft with comments, immediately submit via API.
- Only leave PENDING if user explicitly asks for draft-only.

## Team Reviewer Removal Bug

- Submitting a review as team member removes that team from `requested_reviewers`. GitHub considers team request "fulfilled."
- **Fix:** Snapshot `requested_teams` before posting, compare after, re-request removed teams.
- Must happen in EVERY review posting flow.
- **zsh trap:** Only reliable pattern: `echo "$VAR" | grep -q "$PATTERN"` with positive match, or `grep -c` and compare to 0.

## Line Number Resolution

- Agent-provided line numbers from diff analysis frequently drift from actual file line numbers.
- Always fetch file content via `gh api /repos/{org}/{repo}/contents/{path}?ref={sha}` and verify.
- Use `Accept: application/vnd.github.v3.raw` header for raw content.

## Post-Fix Cleanup (auto-fires after every review-fix push)

Every review comment / bot finding must be closed out on GitHub, not left dangling after a silent push.

**Mandatory trigger.** As soon as a commit lands that addresses one or more review threads (regardless of who pushed it, regardless of whether the user followed up to ask), execute the sweep below in the SAME chat turn as the push. Do not wait for the user to ask. Do not say "want me to resolve the threads?" — resolve them.

The trigger fires when ALL of these are true:
1. A commit has been pushed (or merged) on the PR.
2. That commit modifies code or docs flagged by ≥1 review thread (human or bot — qlty, CodeRabbit, robo[your-company]).
3. The threads are still in `isResolved: false` state.

**Acted on it (commit landed):**
1. Post a short reply on the thread naming the change: `Fixed in <SHA>: <one-line summary>` or `Resolved by <PR#> (<SHA>)`. Even a one-liner is fine — the goal is the author/reviewer can scan the thread and see what happened without diffing.
2. Mark the thread resolved via `resolveReviewThread` mutation (or the GitHub UI button). Outdated-and-unresolved is a worse signal than resolved-with-context.

**Won't act (intentional skip):**
1. Post a reply explaining why: severity (Low) + reason (scope creep, diminishing return, conflicts with another rule, etc.). One or two sentences.
2. Mark resolved.
3. **Surface the skip to [Brain Owner] in the same chat turn** — list which finding(s) were skipped and why. Do not bury skip decisions in a thread he won't see until much later. Comments on the PR are not commits; he needs the visibility to override.

**Pushed back (disagreed with the finding):**
- Leave UNRESOLVED. The original reviewer (or bot author) needs to see the disagreement and respond. Resolving a pushed-back thread silences the conversation.

**Why:** Threads that linger as "unresolved" after a push hide whether each finding was addressed, deliberately skipped, or forgotten. Reviewers re-read the whole list each time. Closing with context turns the thread itself into the audit trail. Surfacing skips prevents the "I assumed you'd fix that one" gap. Asking the user "want me to resolve?" after every fix wastes their cycle on a step they have already delegated.

**How to apply:** Apply to bot findings (qlty, CodeRabbit, robo[your-company]) the same as human reviewer comments. After any commit that addresses ≥1 thread, sweep all threads on the PR and close them with the right disposition. Run this BEFORE the end-of-turn summary, not after it. The existing GraphQL flow:

```bash
# List unresolved threads
GH_TOKEN="" gh api graphql -f query='query { repository(owner: "{o}", name: "{r}") { pullRequest(number: {n}) { reviewThreads(first: 50) { nodes { id isResolved path line comments(first: 1) { nodes { author { login } body } } } } } } }'

# Resolve one thread
GH_TOKEN="" gh api graphql -f query='mutation { resolveReviewThread(input: {threadId: "<id>"}) { thread { id isResolved } } }'
```

After all threads handled, find Slack thread where reviewers were notified, draft response confirming fixes (and skips, if any).

**Reinforced 2026-05-06** after [your-company]-[engineering-toolkit]#173: pushed commit `8bf81e7` addressing 7 of 8 robo[your-company] threads, then waited for [Brain Owner] to ask before resolving. Verbatim correction: "can you resolve the convos you resolved? This is something you should remember in the brain project moving forward, I don't want to remind you about this again." The rule existed in this skill before that day; the failure was application, not encoding. Sweep MUST happen in the same turn as the push.

## Brain File Updates After Review

- Always log performance observations for direct reports. No approval needed.
- Target: `09_people/<first>_<last>.md` → Performance Observations table.
- Match PR author GitHub username against `config/team.yaml`.
- Category: "Positive - [theme]" or "Constructive - [theme]". "Shared with person?" = "No" initially.

## GH CLI Quirks

- `gh pr list --author` only works within a single repo. Use `gh search prs --author=<user> --state=open` for cross-repo.
- `gh pr reviews` is NOT a valid subcommand. Use `gh api repos/{org}/{repo}/pulls/{n}/reviews`.
- Always prefix with `GH_TOKEN=""` to fall back to keyring token.
- **`gh pr view` repo+PR syntax.** Positional arg uses `--repo <org>/<repo> <PRNUM>`. Hash form `<org>/<repo>#<PRNUM>` returns `no pull requests found for branch`. Hash works only when reading PR references in PR/issue bodies, not as a CLI positional.
- **[Your CTO]'s GitHub username:** `drn`

## Author CI-Status Claim Verification

When a PR author claims "all CI green" (DM, comment, Slack thread), verify `statusCheckRollup` on the head SHA before any sign-off:

```bash
GH_TOKEN="" gh pr view <N> --repo <org>/<repo> --json statusCheckRollup,headRefOid
```

Any `state: ERROR` or `conclusion: FAILURE` on the head SHA is grounds to send back, even with `reviewDecision: APPROVED`. The status `description` field is usually the smoking gun (e.g., `"Error calling workflow: 'sync-rn-upgrade-branch'"`). Quote it verbatim in the pushback.

Author-claimed SHA may differ from current head SHA if the author pushed additional commits after the claim. Confirm head includes the claimed commit before flagging as a mismatch.

**Why:** Sign-off then catch the failure costs a full round-trip. The check takes 5 seconds.

**Source:** 2026-05-04 [your-company]-[mobile-app] #4037. Author DM said "all 3 CI green". Head `bbaa4223` had CircleCI Pipeline=`error` on the new `sync-rn-upgrade-branch` workflow (`when: not is_app_update` plus `branches: only: master` filter left zero runnable jobs on the feature-branch pipeline).

## Permission-Grant Migration Sign-Off

When a migration grants a permission to specific users (e.g., `ENABLED_EMAILS = ['alice@example.com', 'bob@example.com']`):

- Do not add "DM the grantee pre-deploy" as a sign-off condition. The audit log of the granted action (e.g., `log_tool_execution`) is the contract.
- Author smoke-tests with one of the listed grantees (themselves or a peer in the same migration list). If smoke-test passes, deploy lands.
- The grantee discovers the capability via normal use; the audit trail covers accountability.
- A pre-deploy heads-up DM is a round-trip without risk reduction. Skip it.

**Source:** 2026-05-04 [your-company]-[your-idp-tool] #463. A migration enabled `app_reviews_write` for several users. Initial review proposed a pre-deploy DM to the granted user; [Brain Owner]'s correction: smoke-test with [Director], audit log handles the rest.

## Migration Data Context Rule

Before flagging NULL backfill concerns on migrations:
1. Check if table is new (CREATE TABLE in same PR series) — if new, no backfill concern
2. Check if PR description states "no existing data" — if yes, trust author
3. Check if code queries new columns with comparisons that skip NULLs — if no such queries, irrelevant
4. **When uncertain, frame as a question:** "Are there existing records?" not "Existing records have NULLs"
5. Only flag as MEDIUM when all three conditions confirmed: table predates PR + NULLs skipped by queries + functional gap

*Derived from <repo>#<pr-number> false positive: flagged NULL timestamps on empty table.*

## Re-Review Workflow

When re-reviewing after author pushed fixes:
1. Fetch all reviews + commits to identify fix commits after review date
2. Fetch current diff, verify each previous finding is addressed
3. Use light mode (no 4-agent pipeline needed)
4. If all resolved and no new issues: APPROVE
5. Reference previous findings in approval body

## Self-Authored PR Workflow

When PR author == [your-github-handle]:
1. Skip review posting (no comments to self)
2. Clone, rebase, fix issues directly
3. Force push fixes
4. Resolve ALL outdated review threads via GraphQL
5. Nudge reviewer in Slack

## [Engineering Toolkit] Pre-PR Review (Hard Rule)

Run a [engineering-toolkit]-style review on the diff itself, twice, and fix every finding before any PR moves forward. No exceptions.

**When to run:**
1. **Before opening a PR.** First [engineering-toolkit] pass on the local diff. Fix all findings. Then open the PR.
2. **If the PR is already open** (you came in mid-flight or pushed a hotfix without an initial review). Run [engineering-toolkit] first, before any other PR work (merge ask, slack ping, smoke test).
3. **After landing fixes from the first pass.** Run [engineering-toolkit] a second time on the updated diff. The second pass catches what the first-pass fix introduced (latent dependencies, wrong default values, missing wiring). Skipping the second pass has shipped real bugs.

**How to run** (delegate to a general-purpose agent, do not eyeball):
- Read the diff via `git diff origin/main...origin/<branch>`.
- Brief the agent: load the four review-agent rubrics (`~/Development/[your-company]-[engineering-toolkit]/agents/review/review-{correctness,security,reversibility,qa}.md`), apply them to the diff, return a severity-tagged punch list with file:line. Cap at 250 words.
- Do NOT skip even when CI is green and bot tools are clean. They catch different blind spots.

**Severity to action:**
- Critical / High: fix before any merge ask, no negotiation.
- Medium: fix unless [Brain Owner] explicitly accepts the trade-off in writing.
- Low / nit: fix if cheap (one-liners, doc fixes); skip if it widens scope.

**Why:** 2026-04-29 [your-company]-app-preview PR #11. Initial fix shipped a critical bug (`next-auth/react` signIn defaulting to wrong basePath) that the first [engineering-toolkit] pass caught. Without the review, the OAuth flow would have stayed broken in production. Then the second pass on the fix surfaced a P2 drift-risk (three sources of truth for `/app-preview`), also worth catching before ship.

**How to apply:**
- Treat [engineering-toolkit] review as a build step, not an optional QA gate. Two passes minimum.
- The "ship it" verdict from a [engineering-toolkit] pass with zero P0/P1 findings unblocks merge approval. Until both passes return clean, the PR is not ready for review/merge.
- Document follow-ups deliberately skipped (with reason) so the next session can revisit.

## Merge Approval Gate (Hard Rule)

Never merge a PR (including with `--admin` bypass) without an explicit "merge" / "go ahead" / "yes merge" / "ship it" from [Brain Owner] on this specific PR. Holds even when:
- All CI checks are green
- All [engineering-toolkit] / qlty / CodeRabbit findings are addressed
- Earlier PRs in the same series were already merged

**Why:** 2026-04-28 [your-company]-app-preview migration. PRs #1-#4 were admin-merged, #5 was queued for merge before [Brain Owner] had a chance to inspect Qlty Cloud UI triage state. Auto-merging would have shipped before the inspection completed. Merge is non-reversible and team-visible. Pause cost is ~30 seconds; unwanted-merge cost is a revert PR.

**How to apply:**
- After CI passes, present the merge-ready state and ask: "Want me to merge this, or are you reviewing first?"
- Do NOT treat "fix all findings" or "wait for CI" as implying "merge when green."
- The "merge" verb (or equivalent) must be explicit and tied to the current PR number.
- Applies to ALL repos.

## Stale Local Branch Trap

When a PR branch has remote-only commits:
```bash
git fetch origin
git reset --hard origin/<branch>   # sync to remote HEAD
git rebase origin/main             # now replays ALL commits
```

## Reviewer Assignment

- Always add reviewers after creating a PR: `gh pr edit <N> --add-reviewer <username>`.
- If PR addresses someone's review, add them as reviewer.
- **Team reviewer request fails for PR author.** Workaround: add individual team members instead.

## Receiving Review Feedback: Triage Protocol

Before fixing any review comment on your own PR, run this protocol. The reflex to "fix each comment in order" hides patterns, mixes noise with signal, and produces fixes that conflict with each other. Triage first, fix second.

**Trigger.** Any time review comments land on a PR you authored (human or bot: robo[your-company], qlty, CodeRabbit, Codex). Mandatory for PRs with 3+ comments. For 1-2 trivial comments, fix inline and skip Steps 3-4.

**Step 1: Gather.** Pull every comment into one list before touching code:
- Top-level review summaries
- Inline review comments
- Bot findings (qlty, robo[your-company], CodeRabbit, Codex)

Use the Bot Findings Ingestion queries above. Dedupe by `path:line + author`. One source of truth with columns: author, severity, path:line, body.

**Step 2: Filter (per-comment).** Three dispositions:

- **Legit (Yes):** real issue, will fix. Capture *why we missed it during implementation* in one line. Examples: "no test for empty case", "did not read schema before writing the query", "missed the migration ordering rule", "assumed types without verifying". This "why missed" is the input to Step 3.
- **Not legit (No):** not actionable (noise, wrong context, already addressed elsewhere, reviewer misread). Reply on the thread with the reasoning, mark resolved.
- **Pushback:** disagree with the finding. Leave thread unresolved, post the reasoning so the reviewer can respond. See Post-Fix Cleanup for the unresolved-thread rule.

Every actionable comment is blocking until code is updated OR a justified pushback is posted. Output: per-comment table with disposition + (for Yes) the one-line root cause.

**Step 3: Zoom out (pattern analysis).** Once filtered, look across all Yes comments together:

- **Related?** Same file, same feature, same layer? Cluster them.
- **Pointing to a deeper issue?** Three NULL-handling comments may mean "no empty-state tests anywhere in this file." Five Medium findings on a migration may mean "no migration safety checklist." The cluster is the signal, not the individual finding.
- **Review noise or real pattern?** Single missed edge case = noise. Three of the same shape in one PR, or a repeat across PRs, = pattern.
- **Mock/source drift is a recurring class.** When a refactor changes how source calls a function (e.g. `t('title')` → `t(\`titles.${kind}\`)`, or a Redux action shape change), every co-located mock that intercepts that function in tests must update in the same commit. The mock is part of the contract surface. Symptom: tests pass locally but CI fails on a string-match assertion against the production output, OR worse, tests pass on CI with the mock returning the literal namespace key path that no human noticed in the test output. Source: 2026-05-18 [your-company]-[your-product-ui] JULI-215 — `PreviewSlot` source switched to slot-scoped `t(\`titles.${kind}\`)`; `mockTranslations` lookup table in `index.test.tsx` was not updated; regex-based assertion failed; two CI cycles were burned debugging before catching the stale mock.
- **Prevention.** If a pattern is found, encode it where it auto-fires next time:
  - Behavioral rule: add to a skill (this one, `clean-code`, or domain skill)
  - Pre-PR checkable: add to the Pre-Open Review Gate criteria
  - Reference lookup: encode in `context/knowledge/` and link from the skill
  - Surface the pattern to [Brain Owner] explicitly: "Three comments point to X. Propose adding rule Y to skill Z." Never silently encode patterns into the brain without his read.

**Step 4: Sequence the fixes (TDD-first).** Do not fix in review-order. Order by:

1. **Failing test first.** For each behavior bug in the Yes list, write the failing test BEFORE the fix. The test makes the bug concrete and proves the fix works. **Stash-and-rerun verification (mandatory):** after writing the test AND the fix, `git stash` the source-side fix, run the test, confirm it FAILS for the expected reason, then `git stash pop`. This is the only proof that the regression test catches the regression — without it, a co-evolved broken-test-plus-broken-source can pass review. Skip TDD for non-behavior comments (naming, style, docs). Source: 2026-05-18 [your-company]-[your-product-ui] — JULI-210 agent did stash-and-rerun, JULI-215 agent did NOT, two CI cycles burned on the latter.
2. **Dependencies.** Foundation changes first (schema, types, shared helpers). Leaves (callers, tests of callers) after.
3. **Severity.** Critical / High before Medium before Low. Within a tier, smallest diff first to build momentum.
4. **Conflict avoidance.** If two fixes touch the same lines, sequence so the second rebases cleanly. Note conflicts in the plan.

Output: ordered checklist of [test/fix] tasks. Use Conductor TODOs when 3+ steps. Surface the plan to [Brain Owner] before the first fix lands so he can re-order or override.

**After fixes:**
1. Re-run [engineering-toolkit] review on the diff to catch what the fixes introduced (see [Engineering Toolkit] Pre-PR Review, two-pass rule).
2. Push, then run Post-Fix Cleanup in the same turn: reply on each thread (`Fixed in <SHA>: …`), resolve, surface skips.
3. If Step 3 identified a pattern, confirm the prevention rule landed in the right file (skill, knowledge, or checklist) before declaring work complete.

**Why:** Without filter, you fix noise as signal. Without zoom-out, you fix three symptoms instead of one cause. Without TDD sequencing, the second fix invalidates the first. The triage protocol turns a flat list of comments into a structured plan that addresses root causes and prevents recurrence.

**How to apply:** Run on any PR with 3+ comments before the first fix commit. Skip for 1-2 trivial comments. The triage output (legit count, skip count, patterns found, ordered fix plan) goes to [Brain Owner] in the same turn before code lands.

## Pipeline Timing

- Full 4-agent review: ~3 min for 6-file PR
- Spec-only PRs: only correctness agent productive. Consider `--light`.
- Plugin repo .md PRs: `--light` for pure instruction changes. Full pipeline if embedded scripts.

## CI Branch Lookup

Use `headRefName` from PR metadata — do not guess branch names:
```bash
GH_TOKEN="" gh pr view $PR --repo $ORG/$REPO --json headRefName --jq '.headRefName'
```

## Bot Findings Ingestion (Before Reviewing)

Fetch existing reviewer comments BEFORE running the review agent. Prevents duplication, escalates structural findings, catches convergence signals.

```bash
# qlty (static analysis — similar-code, file-complexity)
GH_TOKEN="" gh api repos/{o}/{r}/pulls/{n}/comments --jq '.[] | select(.user.login == "qltysh[bot]") | {path, line, body}'
# robo[your-company] ([engineering-toolkit] automated review)
GH_TOKEN="" gh api repos/{o}/{r}/pulls/{n}/comments --jq '.[] | select(.user.login == "robo[your-company]") | {path, line, body}'
# other human reviewers
GH_TOKEN="" gh api repos/{o}/{r}/pulls/{n}/comments --jq '.[] | select(.user.login != "[your-github-handle]" and .user.login != "qltysh[bot]" and .user.login != "robo[your-company]") | {user: .user.login, path, line, body}'
```

**Rules:**
- Do NOT restate findings already flagged by a bot or reviewer. Cross-reference via one-liner only when escalating severity.
- qlty `similar-code` mass >100 → MEDIUM. `file-complexity` count >50 prod code → MEDIUM, >80 → HIGH. Specs: one level lower each.
- Convergence boost: same issue flagged by bot AND human → escalate one severity level (max HIGH).
- Source: 2026-04-21 [your-company]-ordering#3154 — qlty flagged 44-line duplication across 5 spec files that no human reviewer caught; robo[your-company] + v3rron caught correctness issues qlty missed. Complementary tools, different blind spots.

## Operating Rules (migrated from memory tier 2026-04-27)

- **Verify mutations after `gh api`.** Exit code 0 is not proof the mutation applied. Prefer typed subcommands (`gh issue edit --add-assignee`, `gh pr edit --add-reviewer`) and always read back the resource to confirm the change took effect.
- **Draft-first default.** Never auto-post review comments without user approval. Exception: `/pr sweep --reviewer` auto-posts per severity rules. Every other path drafts inline first.
- **Review pass non-negotiable.** PR feedback from [engineering-toolkit] / qlty / human reviewers represents AI blind spots, not code-quality theater. Treat each finding as a real signal until validated otherwise. Run the review pass before declaring a PR done.
- **`[your-company]-app-preview` workflow:** PR + CI + [engineering-toolkit] review before merge. No direct push to master; that repo gets the same discipline as production code despite being personal.
- **`asdf` for Node version.** Repos with `.tool-versions` use asdf, not nvm. `asdf install nodejs <version>` then `asdf local nodejs <version>`. Don't suggest nvm fixes when `.tool-versions` is present.
- **Independent branches in Terraform.** One branch per environment. Never stack environments on one branch (dev → staging → prod chain). Each plan/apply runs against an isolated branch.
- **Personal repos (`[your-github-handle]/*`):** assignee only, no reviewers. The repos exist for solo work or external sharing; review is internal mental discipline, not GitHub teammate review.
- **Cross-team repo nudges → `#rnd-operations`.** Never DM individual maintainers for shared repos ([your-company]-devops, [your-company]-cli, [your-company]-deploy). Channel-level nudge respects team triage and avoids the DM-as-priority-injection pattern.
- **Jira ticket = use the pipeline.** Transition statuses (To Do → In Progress → In Review → Done) on every ticket. Review loop FIRST, then fix loop. The pipeline is the contract; skipping it makes status invisible to managers and dashboards.
- **No individual repo ownership assumptions.** Don't claim "X owns repo Y" without verifying CODEOWNERS or asking. Repos are shared; ownership is operational, not assigned.
- **[Mobile Team] = AppOps (branded merchant apps).** [Mobile Team] is NEVER the owner of AWS / [your-company]-devops / SNS / GuardDuty / IAM PRs. Those route to other teams (typically Stability or DevOps). Don't mis-route work into [Mobile Team].
