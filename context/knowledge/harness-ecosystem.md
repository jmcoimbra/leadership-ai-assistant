# [Your Company] Harness Ecosystem — Operational Knowledge
> Owner: [Brain Owner] | Pillar: Pillar 4 (Embrace AI at every level) | Status: Active | Last Audit: 2026-05-26
> Source: [Engineer] Slack thread 2026-04-17 (C08U0AXFERE/p1776438908665579). [Principal Eng] + [Your CDO] + [Peer Manager 2] callouts. Local scans of `example-ai-repo`, `[your-org]-agent-starter`, `claude-command-center`.

## Purpose

Record which personal AI harnesses exist inside [Your Company], what [Brain Owner] steals from each, and what gets rejected. Prevents re-discovery of the same decisions by future sessions.

> Measurable Outcome: 3 steal actions landed in brain by 2026-04-30 (capability lens encoded, sync-upstream skill adopted, abstraction-boundary rule extended in IDP drafting).
> Escalation Trigger: If none of the 3 actions land by 2026-04-30, force audit and drop or re-commit.

## Registered Harnesses ([your-org]-agent-starter/repo-list.yaml)

| Harness | Owner | Structure | Focus |
|---------|-------|-----------|-------|
| drn-dots | [Your CTO] (CTO) | Embedded in dotfiles | Foundational patterns, pioneered symlink + improve loop |
| example-claude-skills | [Your CDO] (CDO) | Flat `skills/` + `hooks/` + `claude-rules/` | Dev workflows (PR, debug, spec) |
| kosmin-claude-skills | Kosmin | Marketplace (`skills/` + `agents/`) | SOLID principles emphasis |
| jbarson-claude-skills | Jon | Marketplace | Personal utility |
| bertan-claude-skills | Bertan | Marketplace | Knowledge + context management |
| rstojano-claude-skills | Robert | Agents dir | Skill authoring ergonomics |
| [your-org]-[engineering-toolkit] | Org hub | Layer 3 | Promotes skills after 3+ adoptions |

[Brain Owner]'s brain is NOT registered. Decision: keep unregistered. Rationale: `09_people/`, `10_career/`, `context/knowledge/private/` contain IDPs, comp, talent review. Skills surface in the brain are not separable from leadership artifacts in a single-repo architecture. Re-evaluate if skills directory extracted to its own repo.

## Three-Layer Model (from [your-org]-agent-starter README)

| Layer | Scope | Owner | Example |
|-------|-------|-------|---------|
| 1. Personal | Individual workflow | IC/EM | This brain |
| 2. Project | Single codebase | Repo maintainer | `.claude/commands/` in [your-org]-api |
| 3. Team-wide | Org standards | [your-org]-[engineering-toolkit] | Cross-team review, investigation, ops |

Use when evaluating where a new skill belongs. Rule: start at Layer 1. Promote to Layer 2 when 1 other person uses it. Promote to Layer 3 when 3+ adopt.

## [Principal Eng]'s Capability Evolution Framing

From 2026-04-17 Slack thread:

> Prompt Engineering (2023/4) → Context Engineering (2025+, still relevant like `/rewind` in Claude Code) → Harness Engineering.
>
> _Orchestration_ is another axis: multi-agent coordination vs. Harness Engineering building how a single agent instance rides an LLM.

Vocabulary encoded in `03_ai_native_transformation/ai_how_layer.md` (Capability Artifact Lens section). Cross-reference for tier mapping in `03_ai_native_transformation/ai_adoption_roadmap.md`.

## Steal Decisions

| Source | Item | Decision | Action |
|--------|------|----------|--------|
| example-ai-repo | `/spec-writer` abstraction boundary rule | **EXTEND** existing IDP drafting rules with same doctrine: pages must reference public behavior, not private implementation notes | Update `context/knowledge/idp-patterns.md` drafting rules section in next edit pass |
| example-ai-repo | `hooks/` infra (log-skill-use, log-skill-read, log-slash-command) | **SHIPPED 2026-05-14** | Installed under `~/.claude/hooks/`. Wired into settings.json UserPromptSubmit + PostToolUse(Skill\|Read). TSV logs at `~/.claude/skill-usage.tsv` + `skill-reads.tsv`. Restart required to activate. |
| example-ai-repo | `/skill-audit` skill | **SHIPPED 2026-05-14** | Installed at `~/.claude/skills/skill-audit/SKILL.md`. Runs after 2-4 weeks of usage data to prune dead skills. |
| example-ai-repo | `/mcp-prune` skill | **SHIPPED 2026-05-14** | Installed at `~/.claude/skills/mcp-prune/SKILL.md`. Writes `disabledMcpServers` to project `.claude/settings.local.json`. |
| example-ai-repo | `/set-topic` + `remind-session-topic.sh` + `statusline.sh` | **SHIPPED 2026-05-14** | Session-keyed topic files under `~/.claude/session-topics/`. Reminder fires from turn 3 if topic unset. Statusline renders topic ALL-CAPS, context bar, git status. |
| example-ai-repo | `tp` CLI (markdown checkbox flipper) | **SHIPPED 2026-05-14** | arm64 binary at `~/.local/bin/tp`. Commands: `done`, `pass`, `fail`, `partial`, `skip`, `untick`. Cheaper than Read+Edit for tick-heavy files (`12_projects/*.md`, weekly review). |
| [your-org]-agent-starter | `/sync-upstream` skill | **STEAL** | Add skill that diffs starter repo, proposes pulls. Target: 2026-04-30 |
| [your-org]-agent-starter | `/browse-skills` skill | **DEFER** | Useful for discovery but low urgency. Revisit after sync-upstream lands |
| [your-org]-agent-starter | Three-layer model | **ADOPT** as vocabulary | Encoded here. Apply when evaluating new skill placement |
| claude-command-center | Budget governance (hourly/daily limits) | **SKIP for personal, SHARE with [Your CTO]** | Conductor/[Your IDP Tool] team may want this. Log in `project_claude_projects_[your-idp-tool].md` |
| claude-command-center | Worktree isolation | **SKIP** | Conductor handles this |
| claude-command-center | Multi-source todo aggregation | **SKIP** | Orthogonal to brain use case |
| example-ai-repo | `/improve` Plannotator integration | **SKIP** | Existing `/improve` works. Plannotator dependency not worth the coupling |
| example-ai-repo | `/steal` skill | **SKIP** | `/knowledge` + this file cover the same role |
| example-ai-repo | OpenSpec / spec-driven dev workflow | **SKIP** | Brain is not a code repo. Useful for `[your-org]-*` engineering work but not for the brain itself. |
| example-ai-repo | `claude-rules/` snippet-compiled CLAUDE.md | **DEFER** | One-day refactor to split monolithic CLAUDE.md into numbered snippets (`010-plan-formatting`, `070-testing`, etc.). Revisit when CLAUDE.md hits hard governance limit. |

### Stealing-from-upstream rule (2026-05-14)

When porting a hook or script from an external repo, **trust the script header over the README**. the external README claimed `remind-session-topic.sh` was a `Stop` hook; the script header declared `UserPromptSubmit`. README documentation drifts faster than code. Verify the event type, matcher, and exit semantics by reading the script before wiring it into `settings.json`.

## Runtime Replacement (2026-05-24)

New scope: not "what skills to steal" but "what tools replace Conductor.build + vanilla `claude` CLI at the runtime layer." Different question, different answer than the steal-decisions table above. Driven by four pain points: Conductor multi-agent orchestration broken at memory peak, vanilla CLI sub-agent visibility insufficient even with `claude agents` Agent View, Atlassian re-auth every 10-20 min, no pre-flight MCP review before agents fire.

| Tool | Decision | Role | Source |
|------|----------|------|--------|
| **cmux** (native macOS, vertical-tab panes, embedded browser, socket API) | **ADOPT v0.1** | L1 runtime, replaces Conductor's Mac UI + tab management | Jon Barson rec, 2026-03-27 #ai-show-and-tell |
| **worktrunk** (Rust CLI, `wt switch --create`, sibling worktree layout) | **ADOPT v0.1** | L2 parallel worktrees, replaces Conductor's `.claude/worktrees/` | Jon Barson rec, 2026-03-27 #ai-show-and-tell |
| **disler/claude-code-hooks-multi-agent-observability** | **ADOPT v0.1** | L3 real-time sub-agent + tool-call dashboard built on Claude Code hook events | Show HN 2026 |
| **`[your-github-handle]/jai` autonomy-bridge** (`PostToolUse` + `PermissionDenied` hooks; opt-in `/preflight` verbose mode) | **BUILD v0.1** (custom, novel) | L4 autonomous-by-default watcher. Silent on success. Surfaces fix-it prompts on auth failure, missing MCP, permission deny, new-system drift. | This brain |
| **Obsidian + claudian plugin** | **ADOPT v0.1** | L5 markdown knowledge anchor; brain repo opens as vault | Darshan rec, 2026-04-10 #ai-show-and-tell |
| **claude-command-center (CCC)** | **ADOPT v0.1, fork to `[your-github-handle]/claude-command-center`** (REVISED from earlier "SKIP for personal, SHARE with [Your CTO]") | Sidecar command-center: todos / PRs / calendar / sessions | [Your CDO]'s repo, daily-driver via fork |
| **claude-squad** (smtg-ai) | **DEFER** | SSH-only fallback for runtime when cmux unavailable | OSS |
| **hoangsonww/Claude-Code-Agent-Monitor** | **DEFER** (re-evaluate v0.2) | Heavier observability dashboard if disler's hook approach proves thin | OSS |

Why cmux over claude-squad: native macOS UI plus persistent workspaces match the Mac-native ergonomic [Brain Owner] had in Conductor. claude-squad is tmux-based and works in SSH but does not match the Mac UI muscle memory.

Why disler over hoangsonww's Monitor: disler is hook-event-driven on Claude Code's own infrastructure. Same hook substrate feeds L4 (pre-flight). One hook handler, two views.

Why CCC moved from SKIP to ADOPT: the prior decision was scoped to "steal skills into the brain." The runtime question is different. CCC's session launcher, PR tab, calendar / todo aggregation, and console overlay are exactly the daily-driver surface Conductor + vanilla CLI fail at. Krisp source plugin (replacing CCC's [other-transcription-tool] coupling) deferred until daily-driver use exposes the actual friction.

Full plan belongs in the private planning system when it contains owner-specific details.

## AI Integration

Harness awareness is itself an AI leverage point: knowing which peer harness to steal from compounds adoption velocity. When a new team member builds a custom skill, check this file before re-designing. When a peer publishes a new skill, log the candidate here before deciding.

## Cross-References

| File | Connection |
|------|-----------|
| `03_ai_native_transformation/ai_how_layer.md` | Capability Artifact Lens — Prompt/Context/Harness/Orchestration |
| `03_ai_native_transformation/ai_adoption_roadmap.md` | Tier → expected artifact level mapping |
| `context/knowledge/idp-patterns.md` | AI Tier pointer + drafting rules |
| `context/knowledge/zapier-ai-fluency.md` | 4-tier fluency rubric (not to be confused with [Your CEO]'s 7-tier) |
| `12_projects/projects_tracker.md` | idp-convergence initiative referencing 7-tier ladder |

## Memory Tier Elimination (2026-04-27)

Brain converged to drn/dots architecture in a single session. All 4 waves shipped same-day, 4 weeks ahead of the 2026-05-25 deadline.

**Central architectural distinction (the routing axis):** Skills auto-fire via frontmatter triggers; knowledge files lazy-load via intentional pull. Behavioral rules (must fire even when not asked) belong in skills. Reference data (loaded when topic is in scope) belongs in knowledge. **A "topic-router tier inside memory" was killed by the Plan agent's stress-test** because lazy-loaded routers in the auto-loaded memory tier create silent rule misses — the agent only fetches them when it notices a topical match, but behavioral rules need to fire even when the agent does not notice. Generalizable: when designing AI-native architecture, run a Plan agent stress-test before committing. The agent caught an over-engineered tier I had drafted as "the leap."

**Final routing table (per `00_foundation/brain_governance.md` Rule 14):**

| Pattern type | Destination | Activation contract |
|--------------|-------------|---------------------|
| Hard constraint | `CLAUDE.md` Hard Constraints | Auto-loads every turn |
| Behavioral rule (in-scope) | `.claude/skills/<skill>/SKILL.md` Operating Rules | Auto-fires via frontmatter |
| Reference data | `context/knowledge/<topic>.md` | Lazy-pulled via categories routing |
| Active state | `12_projects/<project>.md` | Surfaced by `/weekly-review` |

**What aligned with drn/dots:** No memory tier. Behavioral rules inline in skills. CLAUDE.md as hard-constraint constitution. Knowledge files as lazy reference. **What diverged (justified):** `12_projects/`, `09_people/`, `10_career/` — leadership-state domains drn/dots does not carry. Drn/dots is an engineer's tool repo; the brain is a leadership operating system.

**Closed-loop self-correction:** `/improve` Step 0.5 detects any new `memory/*.md` write as RED-flag anti-pattern. `/dream` is dormant — fires only when /improve catches a rogue write, then routes it. Future sessions cannot accidentally re-introduce the memory tier.

**Source:** private initiative plan, captured as a generic pattern here on 2026-04-27.

## v0.2 Argus Pivot (2026-05-26)

The Runtime Replacement table from 2026-05-24 (cmux + worktrunk + disler + claudian + CCC sidecar) is **SUPERSEDED**. New runtime: `drn/argus` ([Your CTO]'s terminal-native multi-agent orchestrator). Argus subsumes cmux + worktrunk + disler + claudian in one Go binary plus adds a PWA mobile dashboard via Tailscale.

**Trigger ([Your CDO] DM `D06NB2R5TL6/p1779834503394429`, 2026-05-26 19:28 PT, verbatim):**

> merged, but fwiw, this pattern served me so well I turned it into a full blown application that I'm still polishing (`github.com/example-user/example`) - it plugs into argus, [Your CTO]'s own CLI tool. I've built a plugin architecture for argus and plan on plugging CCC into argus, too.
>
> Anyway, the orchestrator skills are kinda MVP / version 1.0 of this concept and I'm deep into 2.0 work.

**Strategic signal:** [Your Company] CTO ([Your CTO]) and CCC author ([Your CDO]) both converging on Argus as the orchestrator platform. Adoption inside [Your Company] will tilt that way.

**Argus capability map** (per `github.com/drn/argus` README, 2026-05-27):

| Layer v0.1 | v0.2 equivalent in Argus |
|------------|--------------------------|
| cmux multiplexer | TUI is the multiplexer (one binary, many panes) |
| worktrunk | built-in: `~/.argus/worktrees/<project>/<task>` per task |
| disler observability | Argus TUI + PWA mobile dashboard |
| CCC sidecar (todos/PRs/calendar) | Replaced by MCP-driven `task_*` / `kb_*` / `schedule_*` |
| Obsidian + claudian | Built-in Obsidian vault indexer to SQLite FTS5 over MCP (`kb_search`, `kb_read`, `kb_list`, `kb_ingest`) |
| iPhone + SSH + tmux | PWA over Tailscale (xterm.js + SSE), Web Push notifications |

**Install:** `go install github.com/drn/argus/cmd/argus@latest`. Pure Go, no CGO. Daemon on port 7743 (REST + PWA). MCP on port 7742. Master token at `~/.argus/api-token`. Auto-start via `argus daemon install` (launchd plist).

**State files:** `~/.argus/argusd` (symlink to binary), `daemon.sock`, `daemon.pid`, `data.sql*`, `ux.log`.

**Caveat:** Argus TUI panics in non-TTY environments (Bash tool, CI runners) inside tcell's mouse enable path. `argus daemon status` and other non-TUI subcommands work fine without TERM. Surface this when debugging: it is NOT a binary corruption.

**Microsoft "Conductor" disambiguation reaffirmed:** Microsoft's "deterministic orchestration" library (Open Source Blog 2026-05-14) is unrelated to `conductor.build` and unrelated to `drn/argus`. Three different products sharing language.

## Patterns observed during CCC fork work (2026-05-25 -- 2026-05-26)

These are reusable across any maintainer-built tool you fork or extend.

### Ship-what-you-use anti-pattern: hardcoded maintainer identity

When a maintainer ships a personal tool ("Ship what you use", per CCC docs/roadmap), their own identity often leaks into the codebase as hardcoded strings. Forks then operate as if they ARE the maintainer.

**CCC example:** [Your CDO]'s first name was hardcoded in 3 places:
1. `internal/refresh/sources/slack/slack.go` `commitmentPhrases` var (12 third-person phrases like `"<name> will"`, `"<name> is going to"`)
2. `internal/refresh/sources/slack/slack.go` `searchQueries` inside `fetchSlackCandidatesViaSearch` (Slack search.messages API queries)
3. `internal/refresh/sources/slack/llm.go` LLM commitment-extraction prompt body

For a [Brain Owner]-as-operator fork, the searches still "Just Worked" against Slack (because Slack search returns matches from any channel the operator can read, which includes the maintainer's messages in shared channels), so the fork's dashboard fills with the MAINTAINER's commitments addressed to him, not the fork user's. Subtle, easy to miss.

**Fix pattern (shipped as `<external-repo>#<pr>`, MERGED 2026-05-26 18:44 UTC):**

- Add `user_first_name` to Config.
- Replace hardcoded name strings with `firstPersonCommitmentPhrases` (name-independent) plus a `thirdPersonCommitmentTemplates` table (printf templates like `"%s will"`, `"%s is going to"`) materialized at runtime via methods on the source type.
- LLM prompt: `fmt.Sprintf` substitution with name; fall back to `"the user"` when name empty.
- Empty name disables third-person scanning entirely; first-person scanning still works generically.

**When auditing a fork-able tool:** grep the source for the maintainer's first name in lowercase and uppercase. Every hit is a potential generalization site.

### Skill silent failure: missing `user_invocable: true` frontmatter

Claude Code requires `user_invocable: true` in a skill's YAML frontmatter to expose it as a slash command. Skills without the flag are loaded but never appear in the `/` autocomplete and never fire on typed invocation.

**CCC example:** 2 of 4 orchestrator-pattern skills lacked the flag.

| Skill | `user_invocable: true`? | Visible in `/` menu? |
|-------|--------------------------|----------------------|
| `orchestrator` | No (shipped without) | No |
| `ask-orchestrator` | No (shipped without) | No |
| `orchestrate` | Yes | Yes |
| `check-messages` | Yes | Yes |

User typed `/orchestrator my-week` repeatedly with nothing happening. Diff of the 4 frontmatters surfaced the issue. Two-line fix, no logic touched.

**Rule:** every user-typed slash command needs `user_invocable: true` explicit. Absence is silent failure, not error. When debugging "my skill does nothing," check the flag first.

Shipped upstream as `<external-repo>#<pr>` (pending review at 2026-05-26).

### gh CLI stale env token: `GH_TOKEN=""` prefix as [Your Company] convention

Conductor (and many shell init paths) inject `GH_TOKEN` and `GITHUB_TOKEN` env vars with stale or wrong-scope tokens. gh CLI honors env over keychain, so every `gh` call returns 401 Unauthorized despite `gh auth status` showing logged-in.

**Fix pattern at source-code level** (shipped to CCC fork as commit `df6e501`, NOT yet PR'd upstream):

```go
// internal/refresh/sources/github/exec.go
func ghCommand(ctx context.Context, args ...string) *exec.Cmd {
    cmd := exec.CommandContext(ctx, "gh", args...)
    cmd.Env = filterGHTokenEnv(os.Environ())
    return cmd
}

func filterGHTokenEnv(env []string) []string {
    out := make([]string, 0, len(env))
    for _, e := range env {
        if strings.HasPrefix(e, "GH_TOKEN=") || strings.HasPrefix(e, "GITHUB_TOKEN=") {
            continue
        }
        out = append(out, e)
    }
    return out
}
```

Route ALL gh invocations through `ghCommand`. Stripping the vars at the binary level is what makes any tool inheriting CCC's env behave consistently. The brain rule that told every caller to prefix `GH_TOKEN=""` by hand was retired on 2026-08-05, once the export was removed from the shell rc: the root cause is the export, not the call site.

**Verification trick:** if a gh CLI call returns 401, run `env -u GH_TOKEN -u GITHUB_TOKEN gh ...` to confirm the env vars are the cause. If that works, the fix is to strip them in the calling code.

### [Your CDO] review cadence (2026-05-26 observation)

Clean, single-purpose upstream PRs to [Your CDO]'s repos merge fast. PR #2 (slack name generalization, 184 +/-/63) merged ~17 minutes after push. PR #3 (2-line skill flag fix) pending at end of session. Implications when contributing to `<external-user>/*`:

- Single-commit, single-purpose PRs ride the fast path.
- Body should lead with the bug story (concrete repro), not the patch summary.
- Include backward-compat note explicitly; reduces reviewer questions.
