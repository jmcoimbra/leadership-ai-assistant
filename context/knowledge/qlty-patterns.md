# Qlty Integration Patterns

**Added:** 2026-04-23
**Last Updated:** 2026-05-15 (Total vs Diff Coverage Gate section added: nexus disabled `Send 'qlty coverage' Commit Status` after PR #156 false-fail driven by path-filter-gate + partial-coverage upload; `qlty coverage diff` at 80% / 20 min diff size is now nexus's only coverage gate; gate config lives in qlty Cloud Review Configs UI, not qlty.toml or CLI; nexus master not branch-protected so failing status was informational only). Earlier 2026-05-08 (Local qlty MCP server scaffolded at `~/.claude/mcp-servers/qlty/server.py`: FastMCP + uv PEP 723 single-file, 10 read-only tools, verified live against `[your-company]` workspace token; POST `/fixes` + `/fixes/batch` excluded from v1 surface; `https://api.qlty.sh/openapi.json` is canonical OpenAPI source, `/api/openapi.yaml` doc page returns 404). Earlier 2026-04-30 (master full-scan OOM resolution: nexus PR #163 flipped master from `qlty check --all` to `qlty check --upstream=HEAD~1` after `--all` exited 137 at ~80% scan in `cimg/base:stable`; partial-clone backfill must extend to master arm when master is also `--upstream`-scoped, same `object not found` failure mode applies; smells + metrics stay on `--all` (non-blocking via `|| true`). Earlier 2026-04-30: coverage-fanout session: dashboard ⚠️ icon reflects DEFAULT BRANCH coverage, not PR; GitHub `qlty coverage: SUCCESS` check is NOT authoritative for "data delivered" — verify via CircleCI publish step stdout (Token line + Uploaded XX KiB); workspace token format `**********/<project>` confirms single org env var routes per-project via token suffix; nexus multi-service coverage is trivial because `collate-html.rb` already emits unified `coverage-merged/html/lcov.info` via SimpleCov.collate + simplecov-lcov; `circleci_job_logs` MCP returns step metadata + presigned `output_url`, not stdout — must `curl` the presigned URL to read actual qlty CLI output. Earlier 2026-04-29: CI CLI knobs + [your-org]-services-orb workaround: qlty CLI exposes `--all` and `--upstream=<ref>` (no `--since-commit`); qlty.toml has NO per-plugin `args`/`extra_args` field — the trufflehog plugin runs `trufflehog filesystem --only-verified` regardless, and there is no qlty-config syntax to override args without a full driver script (verified against qlty source 2026-04-29). [your-org]-services-orb `qlty-checks` job hardcodes `qlty check --all` AND wraps every command with `|| true`, neutering `mode = "block"` in CI (verified by fetching `repos/[your-org]/[your-org]-services-orb/contents/src/jobs/qlty-checks.yml` via gh api). Custom CircleCI job pattern landed in nexus PR #99 to bypass the orb. Earlier 2026-04-27: severity granularity + FP suppression asymmetry vs standalone Semgrep)
**Source:** Qlty PR sprint 2026-04-23 (PRs: [your-org]-ordering #3193, nexus #99, [your-org]-devops #1018, [your-org]-mobile-app #4047, [your-org]-consumer-ui #105, [your-org]-[your-product-ui] #3491, [your-org]-ordering-ui #3775)
**Production Change Validation:** [Notion page](https://www.notion.so/wiki-example/qlty-security-framework-rollout-7-repos-ordering-nexus-devops-mobile-app-consumer-ui-[your-product-ui]-34ba84ed40248126a4facfdb53203f32)

## Qlty Cloud Diff-Scoping

**qlty cloud's PR check is diff-scoped, not baseline-scoped.** A baseline finding only fails `qlty check` on a PR when the PR's diff touches the file containing the finding. Verified on PR #3193: 414 baseline findings across 3 plugins (11 semgrep + 290 gitleaks + 113 osv-scanner); `qlty check` passed with "No blocking issues" because diff was TOML-only.

**Implication for mode strategy.** Flipping a plugin to `mode = "block"` does NOT immediately fail every open PR. It fails only PRs whose diff intersects with a file containing a block-severity finding. This is the argument for "experiment-first" block rollout: flip all plugins to block, accept that specific file edits will surface findings at the point of change, add allowlist entries as false positives emerge, revert via 5-line TOML change if noise is unworkable.

**Counterpoint (where block IS dangerous).** Files touched by nearly every PR (`Gemfile.lock` in a Ruby monorepo, `package.json` in a JS monorepo) anchor plugin findings that will block every dep bump. `osv-scanner` block + an EOL Rails version = every Gemfile.lock change rejected until upgrade. For these plugins, drain the findings (upgrade + suppress) before block flip.

## Severity Granularity & FP Suppression vs Standalone Semgrep

**qlty has no per-severity blocking knob.** Plugin-level only: `disabled / monitor / comment / block`. There is no qlty.toml syntax to "block on medium+ severity" or "block only HIGH". If you need per-severity gating, you either (a) accept all-or-nothing block at plugin level (acceptable in practice because diff-scoping limits CI failures to PRs that touch flagged files, see Diff-Scoping section above), or (b) ship a custom driver script in `[plugins.definitions.<plugin>.drivers.lint]` that filters by severity (the same override pattern used for Semgrep Registry pack composition).

**qlty FP suppression methods are NOT inline.** Two paths only:
1. **qlty.sh web UI ignores** — fingerprint-based, scopes per-instance / per-check / per-path / per-glob. Stored in qlty cloud DB. Removable via UI.
2. **`.qlty/qlty.toml` config-level entries** — source-controlled. Suppressed at generation time.

There is no equivalent to standalone Semgrep's `// nosemgrep: rule-id` inline code suppression. Implication for repos that run BOTH standalone Semgrep AND qlty Semgrep: developers face two suppression workflows for two scanners. Doc the pattern explicitly when split-stack rolls out.

**AI agent rules in qlty AGENTS.md additions do NOT include FP-handling guidance.** The current section (see "AI Agent + Human Dev Setup" below) only instructs `qlty fmt` on commit and `qlty check --fix --level=low` before task end. There is no rule for what an AI agent should do when qlty surfaces a false positive. Follow-up PR: add an FP-handling section to the qlty AGENTS.md template before agent-driven commits run against qlty-enabled repos at scale, otherwise agents may blanket-ignore findings via the easiest path.

Source: 2026-04-27 Ben Brenner Slack DM session. WebFetch of qlty `analysis-configuration` + `triaging-issues` + `automated-code-review` docs confirmed plugin-level mode and web-UI / qlty.toml suppression as the only paths.

## Semgrep Driver Override (Registry pack composition)

**Problem:** qlty's default semgrep plugin hardcodes `--config .semgrep.yaml` in the driver script (confirmed at `qltysh/qlty-plugins/linters/semgrep/plugin.toml`). [Your Company] does not maintain a `.semgrep.yaml`. Semgrep itself has no YAML-level mechanism to compose multiple Registry packs (`p/security-audit`, `p/ruby`, etc.); the only way to combine packs is repeated `--config` CLI flags.

**Fix:** override the driver script in the project-level `.qlty/qlty.toml`:

```toml
[[plugin]]
name = "semgrep"
mode = "block"

[plugins.definitions.semgrep.drivers.lint]
script = "semgrep --metrics=off --disable-version-check --config=p/security-audit --config=p/ruby --sarif --output=${tmpfile} ${target}"
success_codes = [0, 1]
output = "tmpfile"
output_format = "sarif"
cache_results = true
batch = true
output_missing = "parse"
```

**Behavior:** qlty cloud honors the driver override (verified via `qlty check --all` locally + qlty GitHub App check on PR #3193). Registry packs download on each CI run.

**Feb 27 claim ("qlty cloud ignores driver overrides") is outdated.** That attempt tried `--config auto` which failed for reasons unrelated to override acceptance. The current plugin version (tested v0.588) applies script overrides as expected. Do not treat 60-day-old qlty behavior claims as still-true without re-verification.

**Trade-off — Registry availability.** Block mode + live-fetch from Semgrep Registry creates a CI dependency on registry uptime. robo[your-company] flagged this on PR #3193. Mitigation documented in rollback section: flip `mode = "block"` → `"monitor"` in `.qlty/qlty.toml` during a Semgrep Registry outage (<5min merge cycle). Alternative: vendor rulesets via `semgrep show --config=p/<pack>` into a local `.semgrep.yaml`, at the cost of rule drift. We chose live-fetch until outages become recurring.

## Pack Selection by Stack

| Stack | Semgrep packs | Coverage category |
|---|---|---|
| Ruby ([your-org]-ordering, nexus services) | `p/security-audit` + `p/ruby` | SAST |
| Next.js ([your-org]-consumer-ui, [your-org]-ordering-ui) | `p/security-audit` + `p/javascript` + `p/typescript` + `p/react` + `p/nextjs` | SAST |
| React Native ([your-org]-mobile-app) | `p/security-audit` + `p/javascript` + `p/typescript` + `p/react` | SAST (p/react has react-dom bias; expect RN noise) |
| React + Flow ([your-org]-[your-product-ui]) | `p/security-audit` + `p/javascript` + `p/react` | SAST (no `p/typescript`; Flow annotations cause parse errors — expect baseline noise) |
| IaC ([your-org]-devops) | None | SAST not applicable; use IaC plugins instead |

## Full Security Framework (5 categories)

qlty's "security framework" maps to 5 plugin categories. At [Your Company] this rollout implemented all 5 across the relevant stacks:

| Category | Plugin(s) | Applied to |
|---|---|---|
| SAST | `semgrep` | All 6 Ruby/JS repos + [your-org]-branded-apps; NOT [your-org]-devops |
| SCA | `osv-scanner` | Ruby + JS repos with lockfiles + [your-org]-branded-apps; NOT [your-org]-devops (no app lockfiles, scanner is no-op on pure IaC) |
| Secrets | `gitleaks` + `trufflehog` | All 8 repos (overlapping rule surfaces) |
| CI/CD | `actionlint` | Ruby/JS repos with `.github/workflows/`; NOT [your-org]-branded-apps or [your-org]-[your-idp-tool] (no workflows directory) |
| IaC | `trivy` + `checkov` + `hadolint` + `shellcheck` | [your-org]-devops AND [your-org]-branded-apps (Rails app + ops/*.tf + Dockerfile + bin/ scripts) |

All 8 qlty plugin names match the canonical qlty-plugins default source slugs exactly. No typos observed in a parallel review pass.

## Mixed-Stack Plugin Set (Ruby app + IaC + Docker + shell)

**[your-org]-branded-apps PR #115 (merged 2026-05-26)** is the first repo to merge the Ruby-app plugin set with the IaC/Docker/shell set in a single `.qlty/qlty.toml`. Rationale: branded-apps-service is a Rails service AND carries `ops/{module,production,staging,sandbox}/*.tf` Terraform, a top-level `Dockerfile`, and `bin/` shell scripts. Three surfaces the [your-idp-tool]-style Ruby-only set leaves un-scanned.

**Pre-write inspection rule.** Before authoring a new repo's `.qlty/qlty.toml`, run:

```bash
ls -d ops/ Dockerfile* bin/ .github/workflows/ 2>/dev/null
```

For each surface present, add the matching plugin(s):

| Surface present | Add plugin |
|---|---|
| `ops/**/*.tf` or `**/*.tf` | `trivy`, `checkov` |
| `Dockerfile` | `hadolint` |
| `bin/*` or `**/*.sh` | `shellcheck` |
| `.github/workflows/*.yml` | `actionlint` |

The [your-idp-tool] template (4 plugins: gitleaks + trufflehog + osv-scanner + semgrep) is the **Ruby-only floor**, not the complete config. When the user emphasises "all possible features enabled" on a mixed-stack repo, the 4-plugin floor is incomplete. Slip caught only by the pre-PR `/review` pass on branded-apps-service, then expanded to 8 plugins before opening.

Source: branded-apps-service PR #115 commit `b2b45a3` (expanded from initial 4-plugin set after self-review caught the IaC/Docker/shell scope gap).

## Monorepo Pattern (Nexus)

**Root config, not per-service.** qlty cloud reads `.qlty/qlty.toml` from the repo root; per-service configs at `services/*/.qlty/qlty.toml` are orphaned and silently ignored. The Nexus monorepo shipped with 5 orphaned per-service configs post-cutover (2026-04-20) — the CI step `[your-org]-services/qlty-checks` ran but exited with "No qlty config file found" and was silently passing (non-blocking step).

**Fix (PR #99):** add root `.qlty/qlty.toml` covering all services via the default source; delete the 5 orphaned per-service configs to prevent future contributor confusion (someone editing `services/<svc>/.qlty/qlty.toml` expecting it to take effect would ship a dead change).

**Alternative (not used):** per-plugin `prefix` key in qlty.toml scopes a plugin to a subdirectory. Useful when services need different plugin modes. Not needed for [Your Company]'s single-policy-per-monorepo approach.

## AI Agent + Human Dev Setup

Every qlty-enabled repo has a `## Qlty — Code quality + security` section in `CLAUDE.md` / `AGENTS.md`:

```
### AI agent rules (required)

- **Before committing:** run `qlty fmt` to auto-format.
- **Before finishing a task:** run `qlty check --fix --level=low` to address low-severity findings.

### Human dev setup (one-time)

- Install qlty CLI via Homebrew: `brew install qltysh/brew/qlty` (preferred; verifiable signatures via Homebrew). For other install paths see https://docs.qlty.sh/cli/quickstart.
- Install git hooks: `qlty githooks install`
  - Pre-commit hook runs `qlty fmt`
  - Pre-push hook runs `qlty check`
- Bypass a hook when needed: `git push --no-verify`

### Enrollment

Project is enrolled in the [Your Company] qlty workspace. The qlty GitHub App reports findings on every PR.
```

Git hooks are per-developer (live in `.git/hooks/`, not tracked). Documented in CLAUDE.md rather than committed to the repo.

**Install-path supply-chain doctrine (2026-04-24).** Do not recommend `curl <url> | bash` in dev-setup docs. Copilot flagged this on PR #3193 as an unverifiable remote-script execution. Prefer Homebrew (`brew install qltysh/brew/qlty`) — verifiable via Homebrew's signature pipeline — and link to qlty's official docs for alternate install paths. Same rule applies to any CLI install recommendation in CLAUDE.md / AGENTS.md across repos. Mirror the same install line across sibling repos in one sweep when changing it.

**CLAUDE.md ↔ AGENTS.md symlink direction varies by repo.** [Your Company] pattern is not uniform:

| Repo | Direction | Tracked file |
|---|---|---|
| [your-org]-ordering | `AGENTS.md → CLAUDE.md` | `CLAUDE.md` |
| [your-org]-consumer-ui | `AGENTS.md → CLAUDE.md` | `CLAUDE.md` |
| [your-org]-devops / [your-org]-mobile-app / [your-org]-[your-product-ui] / [your-org]-ordering-ui | no `AGENTS.md`, only `CLAUDE.md` | `CLAUDE.md` |
| nexus | `CLAUDE.md → AGENTS.md` | `AGENTS.md` |

**Consequence:** `git add CLAUDE.md` silently no-ops in nexus (git tracks the symlink target). When mirroring a doc fix across multiple repos, inspect symlink direction per repo and `git add` the real file. The 2026-04-23 brew-install mirror-sweep hit this bug on nexus; eventual fix was `git add AGENTS.md`. For future multi-repo CLAUDE.md mirrors: precompute the tracked-file-per-repo map before staging.

## Tool Coverage Matrix (qlty vs CodeRabbit vs robo[your-company])

These overlap but target different blind spots — not substitutes for one another.

| Dimension | qlty | CodeRabbit | robo[your-company] |
|---|---|---|---|
| Type | Cloud-hosted scanner catalog | AI-powered PR reviewer | [Your Company]-internal [engineering-toolkit]:review bot |
| Primary scope | SAST, SCA, secrets, IaC, CI-YAML, complexity, duplication, coverage | Generic correctness + style on any diff | [Your Company]-specific correctness, security logic, perf, deploy-risk |
| Block/merge gate | Per-plugin `mode = block` / `monitor` | Informational; does not block | Severity-deterministic (HIGH/MEDIUM → REQUEST_CHANGES) |
| Diff scoping | Yes — baseline only fails PRs that touch the file | Yes — reviews each push's diff | Yes — re-runs on every push |
| Where deployed at [Your Company] | 7 repos (this rollout) | [Your Company] GH org | All [Your Company] repos |
| Typical catches | OWASP Top 10, leaked secrets, CVE, Dockerfile/Terraform misconfig, GHA lint | Subtle correctness bugs: logic errors, edge cases, comment/code drift, validation-order issues | [Your Company] doctrine (interactor patterns, migration safety, feature-flag gaps) |
| Blind spots | No repo-context reasoning; can't reason across files unless rule supports it | AI hallucination; noisy on large diffs | Repost-on-every-push flood; limited to known [Your Company] doctrine |
| Cost | Pro plan $24/dev/month | Per-seat SaaS pricing | Built in-house; maintenance on [engineering-toolkit] repo |

When the same finding fires in 2+ tools: escalate one severity level (same-severity duplicates dedupe).

**Outbound PCV doctrine (2026-04-24):** do not cite personal-repo or non-[Your Company]-sourced evidence in Production Change Validation docs. CodeRabbit's catches in `[your-github-handle]/*` and `lamp-hosting` are valid learnings for personal-knowledge files, but PCV docs route 100% [Your Company]. Use generic category language ("logic errors, edge cases, comment/code drift") when no [Your Company]-sourced CodeRabbit evidence exists. Scrub pass: after any PCV doc edit, grep for `[your-github-handle]`, `lamp`, and personal project names before publish.

## Production Change Validation Pattern for CI-Only Changes

qlty.toml-only changes are classic low-risk config changes: no runtime code, no migrations, no feature flags. Validation log is terse but still required. Standard framing:

- **Engineer concern:** block mode failing PRs touching baseline-finding files → **MITIGATED** by diff-scoping.
- **Revenue / financial liability / indirect impact:** all SAFE (config runs in CI only).
- **Operational friction:** specific failure modes per plugin (e.g., osv-scanner blocks Gemfile.lock changes until Rails upgrade). Escape hatch: 5-line TOML revert per repo.
- **Rollback:** git revert one file. <5min. Semgrep-specific: during Registry outage flip block → monitor.

See `context/knowledge/checklist-review-patterns.md` for the broader PCV template.

## qlty CLI Knobs in CI (PR Diff Scope vs Master Full Scan)

**Verified against qlty source 2026-04-29** (`qlty-config/src/config/plugin.rs` `EnabledPlugin` schema; `qlty-cli/src/commands/check.rs`; `qlty-plugins/plugins/linters/trufflehog/plugin.toml`):

| Knob | Where | Behavior |
|---|---|---|
| `qlty check --all` | CLI flag | Scans entire repo. Default for orb-driven CI (see "[your-org]-services-orb workaround" below). |
| `qlty check --upstream=<ref>` | CLI flag | Diff mode: only re-checks files that differ between HEAD and `<ref>`. Use on PRs against `origin/master` for fast feedback. |
| `qlty check` (no flags) | CLI flag | Changed-files-only, but resolution is fragile in CI; prefer explicit `--upstream` or `--all`. |
| `--since-commit=<sha>` | DOES NOT EXIST | Earlier hypothesis was wrong. qlty's trufflehog plugin runs `trufflehog filesystem --only-verified` (filesystem mode), not `trufflehog git`, so `--since-commit` is not a knob qlty surfaces. |
| Per-plugin `args` / `extra_args` in qlty.toml | DOES NOT EXIST | `EnabledPlugin` schema supports `name`, `version`, `mode`, `triggers`, `prefix`, `package_filters`, `fetch`, `config_files`, `affects_cache`, `drivers`, `skip_upstream`, `extra_packages`, `package_file`. No `args`. To pass custom args to a plugin you must override the full driver script (see Semgrep Driver Override section). |
| `CheckTrigger` enum | qlty.toml | `manual`, `ide`, `agent`, `pre-commit`, `pre-push`, `build`. NO `pr` / `master` / branch-aware triggers. PR-vs-master logic lives in CI, not in qlty.toml. |

## [your-org]-services-orb `qlty-checks` Workaround

**The orb's `qlty-checks` job is non-blocking by construction.** Source (`[your-org]-services-orb` repo, `src/jobs/qlty-checks.yml`):

```yaml
- run:
    name: Run Qlty security and complexity checks
    command: |
      set +e
      ~/.qlty/bin/qlty check --all || true
      ~/.qlty/bin/qlty smells --all || true
      ~/.qlty/bin/qlty metrics --all || true
```

Two consequences:

1. **`mode = "block"` is a CI no-op when invoked through this orb.** The plugin's `mode = "block"` makes the qlty CLI exit non-zero on findings, but `|| true` swallows the exit code. Block mode only takes effect locally (pre-commit/pre-push hooks) — never in CircleCI via the orb.
2. **Wall-time scales linearly with monorepo size.** `--all` scans the full repo every push. On nexus this measured ~44 min per PR (vs ~11s on master where the root qlty.toml had not yet landed and qlty had nothing to scan).

**Custom job pattern (nexus PR #99, commit `19cf2734ad`).** Replace the `- [your-org]-services/qlty-checks:` invocation with a custom job that:

- Runs `qlty check --upstream=origin/master` on PR builds (diff scope, seconds).
- Runs `qlty check --all` on master builds (full scan).
- Drops `|| true` from `qlty check` (so block mode actually blocks).
- Keeps `qlty smells` and `qlty metrics` non-blocking (they are reporting tools, not gates).

```yaml
qlty-checks:
  docker:
    - image: cimg/base:stable
  steps:
    - checkout
    - run:
        name: Install qlty CLI
        command: curl -sSf https://qlty.sh | bash
    - run:
        name: Fetch master + backfill blobs (PR builds only)
        command: |
          if [ "$CIRCLE_BRANCH" != "master" ]; then
            git config --unset-all remote.origin.partialclonefilter 2>/dev/null || true
            git config --unset-all remote.origin.promisor 2>/dev/null || true
            git fetch --unshallow 2>/dev/null || true
            git fetch --refetch origin master:refs/remotes/origin/master
            git rev-parse origin/master >/dev/null
            git merge-base HEAD origin/master >/dev/null
          fi
    - run:
        name: qlty check (blocking)
        command: |
          if [ "$CIRCLE_BRANCH" = "master" ]; then
            ~/.qlty/bin/qlty check --all
          else
            ~/.qlty/bin/qlty check --upstream=origin/master
          fi
```

**Why `--refetch` matters.** CircleCI's `checkout` leaves historical blobs absent (see `[your-org]-services.md` CircleCI Executor Notes for the diagnosis). Without backfill, qlty's libgit2 walks the merge-base tree, misses a blob, and exits 99 with a cryptic `object not found - cannot read header for <SHA>` error. `--refetch` re-downloads master with all blobs.

**Anti-patterns observed during this fix iteration:**

- `git fetch --no-tags --prune origin master:refs/remotes/origin/master` — `--prune` with a single-ref refspec deleted `origin/master` instead of updating it (CircleCI step output: `- [deleted] (none) -> origin/master`). Drop `--prune` from single-ref fetches.
- `git fetch --depth=50 origin master` — depth-based fix when the missing object was a blob, not a commit. Setting depth larger does nothing if the partial clone is filtering blobs. Diagnose blob-vs-commit first via `git cat-file -t <SHA>` before reaching for `--depth`.

**Follow-up: upstream the `mode` + `upstream` parameters into `[your-org]/[your-org]-services-orb`** so other repos ([your-org]-ordering, etc.) get diff-scope + actual blocking without forking the job. Until landed, every repo using the orb's `qlty-checks` is silently in monitor mode regardless of its qlty.toml `mode = "block"` declaration.

## Master Full-Scan OOM Resolution (Nexus PR #163)

**Source: 2026-04-30 nexus PR #163, build #32394 verified.**

The custom job from PR #99 kept master on `qlty check --all`. The full nexus monorepo scan does not fit in `cimg/base:stable`'s default Docker memory: master runs hit exit 137 (OOM-killed) at ~80% of the scan ([CircleCI 31820](https://circleci.com/gh/[your-org]/nexus/31820)). Failure surfaced ~10h after PR #99 merged, flagged by Yun.

**Fix.** Flip master to diff scope as well, using `HEAD~1` as the upstream ref (the previous master commit on a fast-forward push):

```yaml
if [ "$CIRCLE_BRANCH" = "master" ]; then
  ~/.qlty/bin/qlty check --upstream=HEAD~1
else
  ~/.qlty/bin/qlty check --upstream=origin/master
fi
```

**Backfill must extend to master.** The partial-clone unshallow + `--refetch` block from PR #99 only ran on PR builds. With master also in `--upstream` mode, qlty's libgit2 walks `HEAD~1`'s tree on master too — same `object not found` failure mode applies. Move the backfill outside the `!= master` gate; differentiate only the validation step (`git rev-parse HEAD~1` on master, `git merge-base HEAD origin/master` on PRs).

**Tradeoff acknowledged.** Master loses its periodic full-repo `check` baseline. Acceptable because PRs already block in `mode = "block"` against `origin/master`; any blocking finding must pass through a PR before reaching master. The full master scan was redundant insurance, not the only gate.

**Smells + metrics stay on `--all`.** They are non-blocking (`|| true`), so an OOM there fails silently. Keep them for trend reporting; revisit only if the failure noise becomes audible.

**When to bump resource_class instead.** If `--upstream=HEAD~1` ever OOMs on a giant single-commit change (multi-thousand-file refactor merged as one squash), the fix is bumping `resource_class` (medium → large), not dropping diff scope. Diff scope is already the floor.

Verified: nexus master commit `9187afcea4` (post-merge of PR #163) ran `qlty-checks` build #32394 to SUCCESS, no exit 137.

## Coverage Publishing for Node/Jest (CLI direct, not the orb)

**The `[your-org]-services/qlty-coverage` orb is rspec-only.** It consumes `coverage_results/.resultset-*.json` (RSpec / SimpleCov format) and has no Jest/lcov path. For Node repos, use the upstream `qlty coverage publish` CLI directly. This is the qlty.sh-documented Node path.

**CircleCI wiring (validated against [your-org]-app-preview PR #14, 2026-04-29):**

```yaml
- run:
    name: Test
    command: yarn test --coverage
- store_artifacts:
    path: coverage
    destination: coverage
    when: always       # preserve lcov when tests fail; that's when you most need it
- run:
    name: Verify qlty coverage token present
    command: |
      if [ -z "${QLTY_COVERAGE_TOKEN:-}" ]; then
        echo "QLTY_COVERAGE_TOKEN is not set. Provision in qlty Cloud Project Settings Coverage."
        exit 1
      fi
- run:
    name: Install qlty CLI
    command: curl -fsSL https://qlty.sh | sh
- run:
    name: Publish coverage to qlty
    command: |
      export PATH="$HOME/.qlty/bin:$PATH"
      qlty coverage publish --format=lcov coverage/lcov.info
```

**Token guard placement is deliberate.** Fails CI fast with an actionable error rather than silently no-op'ing the publish. The first PR that introduces this guard will block its own CI until the token is provisioned. That is by design (forces the operator step).

**Jest config additions:**

```ts
collectCoverageFrom: [
  'src/**/*.{ts,tsx}',
  '!src/**/*.d.ts',
  '!src/generated/**',
  '!src/**/*.test.{ts,tsx}',
  '!src/**/__tests__/**',
],
coverageReporters: ['lcov', 'text-summary', 'json-summary'],
coverageDirectory: 'coverage',
```

`json-summary` is the file the qlty.sh diff-coverage check reads. `lcov` is what `qlty coverage publish` uploads.

## CircleCI Context Attachment is Workflow-Level, Not Job-Level

CircleCI org-level contexts (where `QLTY_COVERAGE_TOKEN` lives in the `circleci` context for [your-company]) are exposed to a job by attaching the context **at the workflow's job invocation**, not in the job definition itself.

**Wrong (does nothing):**

```yaml
jobs:
  ci:
    executor: node
    context:           # this key is ignored at the job-definition level
      - circleci
    steps: [...]
```

**Right:**

```yaml
workflows:
  build-test:
    jobs:
      - ci:
          context:
            - circleci      # attaches at invocation
          filters: [...]
```

Source: [your-org]-app-preview PR #14 commit `6f9ff1b`. First push had the token guard but no workflow-level `context:` line. CircleCI job 93 failed with exit 1 at the guard step because the env var was unset. Fixed by adding `context: - circleci` at both `build-test/ci` and `deploy-production/ci_main` invocations. The pattern matches the `aws-production` context already attached to the `deploy` job in the same file.

**For multi-workflow files:** every workflow that invokes the same job needs its own `context:` attachment. There is no inheritance from a "default" or another workflow.

## Local CLI Flag Quirks

- **`qlty check --format=json` does not exist.** The flag is `--no-formatters` (suppresses pretty output for machine parsing). For JSON output, run `qlty smells --format=json` or pipe to `jq` from the SARIF/result file in `.qlty/results/`.
- **`qlty check --no-fail` does not exist.** There is no `--no-fail` flag on `qlty check` or `qlty smells`. Use `qlty check --all || true` if you need to ignore exit codes.
- **`qlty smells <path>` is the single-file similar-code/complexity scan.** Use this to verify a refactor cleared a similar-code finding before pushing. Empty stdout = clean.
- **trivy plugin install can 404** with messages like `https://api.github.com/repos/aquasecurity/trivy/releases/tags/0.66.0: status code 404`. Transient qlty-plugin-installation failure (qlty pins specific plugin versions; if upstream releases shift, the pinned version may temporarily 404). Workaround: re-run after qlty CLI auto-updates, or run `qlty smells` (skips the trivy install).

Source: 2026-04-29 [your-org]-app-preview PR #14 local verification session.

## qlty.sh Dashboard Column Semantics

**Source: 2026-04-30 coverage-fanout session.**

The Projects index dashboard (`https://qlty.sh/gh/[your-org]/projects`) COVERAGE column reflects **default-branch coverage state**, not PR-branch uploads. The ⚠️ icon means "no default-branch coverage uploaded yet," NOT "no upload received."

| Project state | Dashboard column shows |
|---|---|
| Default branch has had ≥1 successful coverage publish | Letter grade + percentage (e.g., F 49.6%) |
| Project enrolled, only PR-branch uploads exist | ⚠️ warning triangle |
| Project enrolled, coverage intentionally not configured (IaC repo) | 🛡️ shield icon |
| Project not enrolled in qlty cloud | (no row) |

**Implication for rollout.** A repo that just shipped its first qlty coverage publish step on a PR will show ⚠️ until merge. The PR upload IS reaching qlty.sh (verifiable in `https://qlty.sh/gh/[your-org]/projects/<repo>/pull/<n>/coverage`), but the index column updates only after master gets a coverage commit. App-preview was the first [your-company] repo to flip out of ⚠️ because its PR #14 included a master-branch CI flow that ran post-merge.

**Don't use the index column as a "did publish work?" signal.** Use the CircleCI publish step stdout instead (next section).

## Verifying Coverage Upload (the actually authoritative signal)

**Source: 2026-04-30 coverage-fanout session.**

Three layers, only one is authoritative:

| Signal | Authoritative? | What it actually means |
|---|---|---|
| GitHub PR check `qlty coverage: SUCCESS` | NO | qlty.sh GitHub App passed the PR-level coverage analysis. Returns SUCCESS even when no upload exists for the commit (passes by default for "no diff coverage to compute"). Misread once during this session: `gh pr view ... --json statusCheckRollup` showed all SUCCESS while user's dashboard screenshot showed ⚠️. |
| qlty.sh dashboard COVERAGE column | NO (default-branch only) | See section above. |
| CircleCI publish step stdout (qlty CLI banner) | YES | The qlty CLI banner explicitly prints `Token: **********/<project>`, `Upload ID: <uuid>`, `Uploaded XX KiB in 0.0Xs!`, and a `View report:` URL when the upload succeeded. |

**How to fetch the authoritative signal.** The `mcp__claude_ai_[your-idp-tool]__circleci_job_logs` MCP tool returns step metadata + a presigned `output_url` per step, NOT the actual stdout. To read the qlty CLI output, `curl` the presigned URL:

```bash
curl -fsSL "<output_url>" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for m in d:
    print(m['message'])
" | grep -E "Coverage|Token:|Uploaded|Upload ID|Pull Request|Branch:"
```

The presigned URL expires (token lifetime ~1 day), so capture/cache the output if you need it later.

## Workspace Token Per-Project Scoping

**Source: 2026-04-30 coverage-fanout session.**

Each [Your Company] repo's qlty CLI publish step output prints a token suffix that names the destination project:

```
AUTHENTICATION
    Auth Method: Workspace Token
    Token: **********************/[your-org]-ordering-ui
```

Verified across 5 PRs in one session (`[your-org]-[your-product-ui]`, `[your-org]-ordering-ui`, `[your-org]-consumer-ui`, `[your-org]-mobile-app`, `[your-org]-[your-idp-tool]`) — each printed a distinct project suffix.

**Implication.** A single `QLTY_COVERAGE_TOKEN` env var in the CircleCI `circleci` org context works for all [Your Company] repos. The qlty CLI auto-detects the destination project from the git remote URL of the workspace it runs in; the token suffix is metadata visible in the upload banner, not configuration. **No per-repo token provisioning is required** as long as the project is enrolled in the [Your Company] qlty workspace (one-time qlty.sh "Add Project" UI step).

This contradicts an earlier hypothesis ("each project gets its own token, the org context can't possibly carry one token for all"). Drop that mental model.

## Multi-Service Monorepo Coverage (Nexus Pattern)

**Source: 2026-04-30 nexus PR #160.**

**The naive "non-trivial multi-service coverage" assessment is wrong for nexus.** Initial Phase 1 audit deferred coverage as requiring per-service `--tag=<svc>` calls or a custom merge step. Reading `.circleci/coverage/collate-html.rb` revealed that the existing `coverage-report` job ALREADY produces a single unified `coverage-merged/html/lcov.info` covering all 7 services via `SimpleCov.collate` + `simplecov-lcov` (the gem was added 2026-04 to support the HTML report). Coverage publish was a 1-step add to the same job, not a new pipeline.

**Wiring (PR #160, 2026-04-30):**

```yaml
# In coverage-report job, after `Merge coverage resultsets + render summary`:
- run:
    name: Publish merged coverage to qlty
    when: always
    working_directory: ~/nexus
    command: |
      if [ ! -s coverage-merged/html/lcov.info ]; then
        echo "No lcov.info to publish (all test-<svc> jobs halted by path-filter-gate). Skipping."
        exit 0
      fi
      if [ -z "${QLTY_COVERAGE_TOKEN:-}" ]; then
        echo "QLTY_COVERAGE_TOKEN is not set. Provision in qlty Cloud"
        echo "(Project Settings -> Coverage) and add to the CircleCI"
        echo "'circleci' org context."
        exit 1
      fi
      curl -fsSL https://qlty.sh | sh
      export PATH="$HOME/.qlty/bin:$PATH"
      qlty coverage publish --format=lcov coverage-merged/html/lcov.info
```

Plus `context: [github, circleci]` added to the workflow's `coverage-report` invocation (was `[github]` only — `github` provides `GITHUB_API_TOKEN` for the existing PR comment step).

**Two guard rails worth preserving for any monorepo coverage-publish step:**

1. **Empty-lcov skip.** When `path-filter-gate.sh` halts every `test-<svc>` job (docs-only PRs touching nothing under `nucleus/` or `services/`), no resultsets are persisted and `collate-html.rb` writes a stub `index.html` but no `lcov.info`. The `[ ! -s coverage-merged/html/lcov.info ]` check exits 0 cleanly so docs PRs don't fail the publish step. For the more common single-service PR case (where `path-filter-gate` halts SOME test jobs but not all), see "Total vs Diff Coverage Gate (Monorepo Reality)" below.
2. **Missing-token explicit failure.** Exits 1 with an actionable message rather than silently no-op'ing. The first PR to introduce this guard surfaces the operator step (attach the `circleci` context).

**robo[your-company] and qlty.sh are complementary, not substitutes.** Both consume the same `lcov.info`. robo[your-company] posts the per-service breakdown comment via `post-pr-comment.sh`; qlty.sh writes the data to its dashboard for trend tracking + diff-coverage checks. Running both adds one CLI call per coverage-report run (~2-3s) and zero duplicate test execution. When asked "are we duplicating effort?" the answer is no — the data source is shared, the surfaces are different.

**Investigation rule.** Before declaring a multi-service coverage publish "non-trivial," READ the existing coverage pipeline scripts. Specifically grep for `lcov.info` in the repo's `.circleci/` and `script/` directories — if a unified lcov already exists (common when an HTML coverage report is already in place), publishing is a single CLI call.

## Total vs Diff Coverage Gate (Monorepo Reality)

**Source: 2026-05-15 nexus PR #156 false-fail.**

**Symptom.** Dev opens a single-service PR with 100% diff coverage. qlty.sh GitHub check posts `Merging this pull request will decrease total coverage on master by X%` (observed: 6.46% on PR #156). Total-coverage status fails; diff-coverage status passes.

**Root cause.** `path-filter-gate` skips `test-<svc>` jobs for services the PR does not touch. The `coverage-report` job runs `collate-html.rb` against only the persisted resultsets, so `coverage-merged/html/lcov.info` contains coverage for the touched service only. `qlty coverage publish` uploads that partial payload. qlty.sh compares it to master's full-repo coverage and reports the missing services as a drop. No actual regression occurred.

This is distinct from the docs-only edge case in the Multi-Service section above (where `path-filter-gate` halts every test job and the publish step skips via the empty-lcov guard). Here, the publish step runs successfully with partial data.

**Where the gate is configured.** Total-coverage and diff-coverage gates are NOT configured in `.qlty/qlty.toml` (no `[coverage]` section exists) and NOT via `qlty coverage publish` CLI flags. They live in qlty Cloud:

`qlty.sh -> Settings -> Review Configs -> [config name] -> Code Coverage`

Two independent toggleable subsections:

| Subsection | Toggle | Threshold field |
|---|---|---|
| DIFF COVERAGE GATE | Send 'qlty coverage diff' Commit Status | Diff Coverage (fail below %) + Minimum Diff Size (skip below N lines) |
| TOTAL COVERAGE GATE | Send 'qlty coverage' Commit Status | Total Coverage Variation (fail if total drops by more than %) |

Disabling the "Send Commit Status" toggle stops qlty from posting that status entirely. The status simply does not appear on PRs; nothing fails because nothing is reported.

**Decision shipped 2026-05-15 for nexus.** Disabled `Send 'qlty coverage' Commit Status` (total). Kept `Send 'qlty coverage diff' Commit Status` ON with Diff Coverage = 80, Minimum Diff Size = 20. Diff-gate is now the only coverage signal that posts to PRs. Total coverage remains visible on the qlty.sh dashboard for trend tracking.

**Why diff-only, not carry-forward.** Two fixes existed:
1. **Diff-only gate (shipped).** Disable the total status. Devs see coverage feedback only on what they touched. Trade-off: lose detection of indirect coverage drops on untouched files.
2. **Carry-forward coverage (deferred).** Modify the publish step to merge per-service lcov uploads with master's last-known lcov for skipped services. Restores the total signal. Trade-off: requires per-service publish + state management of master baselines.

Picked option 1 because the indirect-drop catch rate at [Your Company] is low-value vs the noise it generates (every single-service PR triggered a false fail). If a future audit shows real indirect drops are slipping through, revisit carry-forward.

**Branch protection state matters.** `[your-org]/nexus` master is NOT branch-protected as of 2026-05-15 (`gh api repos/[your-org]/nexus/branches/master/protection` returns 404). The failing total-coverage status was informational, not a merge blocker. Devs could merge anyway; the friction was perceived-block + confusion, not enforced-block. Note for future required-status-checks rollouts: protect master before tightening qlty gates, otherwise the noise has no enforcement cost and the signal is ignored.

**Generalizes to other monorepos.** Same pattern applies to any repo with selective CI execution (path-filter, codeowners-driven test selection, affected-projects matrices). When the publish step uploads partial coverage relative to master's full baseline, the total gate produces false fails. Default to diff-only gate on these repos; revisit only with carry-forward in place.

**Verify Before Open-PR rule.** When a user asks "open a PR" for a configuration change, verify the change surface lives in code before branching. qlty gate config is one of several vendor-UI-only configurations at [Your Company] (also: qlty.sh ignores/triage UI, GitHub branch protection, CircleCI org-context env vars). Doc-only PRs that pretend to be the fix are worse than no PR: they imply the change shipped without the actual operator step.

## Local qlty MCP Server (Claude Code)

**Source: 2026-05-08 session.**

Personal-scope MCP server wrapping the qlty REST API for in-conversation queries on [Your Company] repo health.

**File:** `~/.claude/mcp-servers/qlty/server.py` (single file, PEP 723 inline metadata, ~200 lines, FastMCP + httpx).
**Token:** `~/.config/qlty/token` (chmod 600), env override `$QLTY_TOKEN`.
**Workspace:** defaults to `[your-company]`, env override `$QLTY_WORKSPACE`, per-call override via `owner` arg. The token verified against `GET /workspaces` returns a single accessible workspace (`key: [your-company]`); no other workspaces are visible to a [your-github-handle]-scoped token.
**Registration:** `claude mcp add --scope user qlty -- uv run --script ~/.claude/mcp-servers/qlty/server.py`. Lands in `~/.claude.json` under `mcpServers.qlty`.

**Tool surface (10 read-only):** `list_projects`, `get_project`, `project_metrics`, `list_issues`, `list_files`, `file_coverage`, `list_components`, `component_metrics`, `rate_limit`, `current_user`. Surface-aligned with the OpenAPI GETs at `https://api.qlty.sh/openapi.json`.

**Cache TTLs (in-process, per-session):** 15 min for project / file / component metrics, 5 min for issues, 1 hour for `current_user`, no cache for `rate_limit`. The 1k req/hr per-workspace API limit never matters within a session at these TTLs.

**POST endpoints intentionally excluded.** The OpenAPI exposes `POST /fixes` and `POST /fixes/batch` (request AI fix suggestions for qlty-detected issues). Skipped from the v1 surface because: (a) Claude already edits files directly, so single-issue fixes route through Edit, not the MCP; (b) batch-fixes (up to 15 issues per call) are the only place qlty's rule-specialist model materially beats Claude on cost + consistency, and the use case has not yet shown up in this workflow. Re-add as `request_fixes_batch` if a code-quality blitz pattern emerges.

**API base verification.** `https://api.qlty.sh/openapi.json` is the canonical OpenAPI source; the published `/api/openapi.yaml` doc page returns 404. Use the JSON spec when extending the tool surface.

**Smoke-test pattern.** stdio MCP handshake (`initialize` + `notifications/initialized` + `tools/list` + `tools/call`) piped to `uv run --script` validates the full path before `claude mcp add` registration. Catches import / dep / token-load errors that would otherwise show as silent connection failures in `claude mcp list`.

## Cross-References

- `[your-org]-services.md` — Nexus monorepo structure (why root config pattern); CircleCI partial clone + missing-blob diagnosis
- `github-pr-patterns.md` — PR review severity rules; shallow-clone refspec fix surfaced during this rollout
- `slack-patterns.md` — URL formatting rules tested by qlty rollout announcement drafts
- `mcp-notion.md` — Data Source ID pattern for PCV page creation
- `checklist-review-patterns.md` — PCV template
- `mcp-tools.md`: `claude mcp add` registration pattern (general MCP doctrine)
