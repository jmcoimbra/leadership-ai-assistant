# First Run Checklist

Use this checklist after cloning the template. Complete it before relying on the brain for leadership decisions or outbound drafts.

## 1. Identity

- [ ] Replace `[Brain Owner]`, `[Your Company]`, `[Your CEO]`, `[Your CTO]`, and equivalent placeholders in non-template files.
- [ ] Set the owner, role, teams, manager reference, and pillars in `AGENTS.md`.
- [ ] Replace the header in `00_foundation/brain_governance.md` with a real owner and audit date.

## 2. Local Configuration

- [ ] Copy `config/team.yaml.example` to `config/team.yaml`.
- [ ] Fill owner handle, timezone, teams, team leads, and direct-report routing identifiers.
- [ ] Copy `.claude/names.txt.example` to `.claude/names.txt`.
- [ ] Add forbidden name misspellings, pronoun slips, and tool-name claims to `.claude/names.txt`.

## 3. Strategic Frame

- [ ] Create `01_strategy/strategic_pillars.md` from `01_strategy/_template_strategic_pillars.md`.
- [ ] Define three to five pillars with baseline, target, and date.
- [ ] Update `.claude/hooks/check-pillar.sh` if your outbound rule needs named pillar replacements.

## 4. Voice Capture

- [ ] Gather 10 to 20 chat messages written by the brain owner.
- [ ] Gather five commit messages.
- [ ] Gather two to three longer documents.
- [ ] Gather one or two feedback notes.
- [ ] Run `.claude/skills/voice-capture/SKILL.md` with those samples.
- [ ] Replace `context/knowledge/voice-profile.md` with confirmed patterns only.

## 5. Minimum Operating Data

- [ ] Create one team brain from `04_team_brains/_template_team_brain.md`.
- [ ] Create one team scorecard from `08_metrics/_template_team_scorecard.md`.
- [ ] Create one direct-report profile from `09_people/_template_individual_development_profile.md`.
- [ ] Create `09_people/team_roster.md` from `09_people/_template_team_roster.md`.
- [ ] Create one active project from `12_projects/_template_project.md`.
- [ ] Create `10_career/career_trajectory.md` from `10_career/_template_career_trajectory.md`.

## 6. Validation

- [ ] Run `python3 scripts/audit_brain.py`.
- [ ] Fix every `ERROR`.
- [ ] Review every `WARN` and either fix it or confirm it is template-only.
- [ ] Run `shellcheck .claude/hooks/*.sh run_agent.sh.example` if `shellcheck` is installed.

## 7. First Weekly Review

- [ ] Read `.claude/skills/weekly-review/SKILL.md`.
- [ ] Run `check-in` mode if the brain has only partial data.
- [ ] Run full mode after team, people, metrics, projects, and career files exist.
- [ ] Convert review output into dated decisions, owner assignments, and deadlines.

## 8. Commit

- [ ] Run `python3 scripts/audit_brain.py` again.
- [ ] Review the diff for private data.
- [ ] Commit with a present-tense subject under 72 characters.
