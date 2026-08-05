# Skill Runtime Guidance

Shared runtime guidance for local skills in this skeleton.

## Configuration Sources

- Team routing: `config/team.yaml` when present, otherwise `config/team.yaml.example` for structure only.
- Forbidden names: `.claude/names.txt` when present, otherwise `.claude/names.txt.example` for structure only.
- Voice rules: `context/knowledge/voice-profile.md`.
- Knowledge routing: `context/knowledge/categories/README.md`.

## External Systems

External systems are optional and adapter-specific. Do not assume Notion, Slack, Jira, GitHub, Google Calendar, or any MCP server exists until the current agent session exposes it.

When a skill references a missing external system:

1. Use local brain files first.
2. Label unresolved external facts as `unverified, confirm at [moment]`.
3. Do not invent page IDs, channel IDs, ticket IDs, calendar events, URLs, quotes, metrics, or owners.

## GitHub CLI

Call `gh` directly; it authenticates through the keyring. Never export `GH_TOKEN` or `GITHUB_TOKEN`.

## Output Boundary

Draft external communication only. The brain owner sends chat messages, email, tickets, calendar events, and PR comments unless they explicitly approve the agent action in-session.
