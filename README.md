<p align="center">
  <img src="favicon.svg" alt="Leadership AI Assistant" width="120" />
</p>

# Leadership AI Assistant

**An AI-native operating system for Senior Engineering Managers.**

Not documentation. An operating system that encodes behavior, enforces accountability, and surfaces failure early.

## Who This Is For

Senior Engineering Managers who want an AI-native brain that:
- Holds their voice, governance rules, and operating rhythms in one place
- Pairs with Claude Code, Cursor, or any agent that reads the filesystem
- Enforces deterministic language and prevents drift via hooks
- Scales from one team to multiple teams without restructuring

## How to Adopt

1. **Clone this repo locally.** Do not push your filled-in copy to a public remote — it will contain your team's data.
2. **Read `AGENTS.md`** to see the always-on rules your agent will follow.
3. **Run the first-use checklist** in `FIRST_RUN.md`.
4. **Choose your tool adapter** in `ADAPTERS.md`.
5. **Customize the placeholders:**
   - `[Brain Owner]`, `[Your CTO]`, `[Your CEO]`, `[Your Company]`, etc. — search and replace.
   - `00_foundation/brain_governance.md` — set your pillars and dates.
   - `config/team.yaml.example` — copy to `config/team.yaml`, fill in your teams.
   - `.claude/names.txt` — add forbidden patterns for the names hook.
6. **Capture YOUR voice.** The shipped `context/knowledge/voice-profile.md` is a starting voice, not yours. Run the `voice-capture` skill (`.claude/skills/voice-capture/SKILL.md`) with 10-20 samples of your own writing (Slack, commits, docs) and let it rewrite the voice profile to match how you actually communicate.
7. **Fill the templates** in `09_people/`, `10_career/`, `11_compliance_security/`, `12_projects/`. Use the `_template_*.md` files as starting points.
8. **Run validation** with `python3 scripts/audit_brain.py`.
9. **Run your first weekly review** using `07_operating_rhythms/weekly_review.md`.

## Structure

| Directory | Purpose |
|-----------|---------|
| `00_foundation/` | Governance rules, evolution protocol, compliance audit |
| `01_strategy/` | Strategic pillars (placeholder — define your own) |
| `02_leadership/` | Async communication standard, audience-density doctrine, PR hygiene mandate |
| `03_ai_native_transformation/` | AI adoption roadmap, baseline assessment, how layer |
| `04_team_brains/` | One folder per team you lead. Template provided. |
| `07_operating_rhythms/` | Weekly review, mid-cycle checkpoint, 1:1 protocol, quarterly refactor |
| `08_metrics/` | Scorecard templates |
| `09_people/` | Individual development profiles (templates only — fill with your team) |
| `10_career/` | Career trajectory (template only) |
| `11_compliance_security/` | Compliance program reference (sensitive data stays out of repo) |
| `12_projects/` | Active initiatives + project template |
| `99_archive/` | Distilled concepts from technical and leadership books |
| `context/knowledge/` | Reusable patterns for AI, observability, testing, integrations |
| `.claude/` | Skills, hooks, commands the agent loads |
| `context/specs/` | Behavioral contracts for long-running skills and command-like workflows |
| `scripts/` | Provider-neutral validation scripts |

## Design Principles

- **Density over volume.** Short files with hard edges beat long narratives.
- **Deterministic language.** "Increase X from A to B by [date]" not "improve X".
- **Self-enforcing.** Hooks audit the brain at write time. The constitution audits itself quarterly.
- **AI-native.** Every file is structured for machine consumption. Clean markdown, explicit sections, no ambiguity.
- **Execution bias.** If a file does not change behavior or move a metric, it does not belong here.

## Customization Checklist

- [ ] Search and replace placeholders (`[Brain Owner]`, `[Your CTO]`, etc.) across all files
- [ ] Update `00_foundation/brain_governance.md` Rule 6 with your quarterly refactor date
- [ ] Define your pillars in `01_strategy/` (this repo ships without — you decide)
- [ ] Copy `config/team.yaml.example` → `config/team.yaml`, fill in your teams (gitignored by default)
- [ ] Populate `04_team_brains/` with one folder per team you lead
- [ ] Create `09_people/<name>.md` per direct report
- [ ] Create `10_career/career_trajectory.md` from the template
- [ ] Set your forbidden-pattern list in `.claude/names.txt`
- [ ] Customize `.claude/hooks/check-pillar.sh` with your pillar names (if you keep pillars)
- [ ] Run `python3 scripts/audit_brain.py` and fix every error

## What Was Stripped

This is a public template. The author's personal team data, named-person 1:1 logs, career trajectory, compliance evidence, and stakeholder maps are not in this repo. Templates and frameworks are.

## License

MIT. See `LICENSE`.

## Contributing

Pull requests welcome for: better template language, additional generic knowledge patterns, new skills that generalize across orgs. Do not submit company-specific patches. See `CONTRIBUTING.md`.
