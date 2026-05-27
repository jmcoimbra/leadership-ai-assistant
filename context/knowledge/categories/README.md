# Knowledge Categories

Agent-facing taxonomy for loading only relevant knowledge files per task.

**Why:** Loading the entire knowledge base every session wastes context. Categories let an agent pick 1-3 topical files and load only what is relevant to the current task.

## How Agents Use This

1. Read this README to see the master category list
2. Pick 1-3 categories that match the current task
3. Open those category files to get scoped knowledge lists
4. Load only those knowledge files — not the whole index

**Domains vs Categories:**
- Domains = where a file physically lives (`context/knowledge/*.md`). One domain per file.
- Categories = what topics a file covers. Many categories per file. Tracked in category files, not in knowledge file frontmatter.

## Master Category List

| Category | File | When to Load |
|----------|------|--------------|
| Leadership | `leadership.md` | Coaching, talent review, IDPs, manager practice, voice |
| Code Delivery | `code-delivery.md` | PR reviews, deploys, SDLC, writing docs |
| AI Execution | `ai-execution.md` | Agents, prompts, plugins, skills, hooks, harness patterns |
| Observability & Infra | `observability-infra.md` | Datadog, AWS, Looker, React Native, cloud architecture |
| Compliance & Security | `compliance-security.md` | Cloud security, AWS security, IAM, defense-in-depth |
| Integrations | `integrations.md` | MCP, Google Sheets, LaunchDarkly, Zapier, dbt |
| Testing | `testing.md` | Playwright CT, WireMock, test infrastructure |

## Adding a Category

1. Create `<category>.md` with frontmatter (see any existing file)
2. Add "When This Category Applies" section
3. Add "Knowledge Files" table mapping to files in `context/knowledge/`
4. Register in the Master Category List above

## Adding a File to Categories

When a new knowledge file is created, assign it to 1-3 categories by appending to each category's "Knowledge Files" table. File membership is tracked here, not in the file's frontmatter — avoids per-file edits when categories change.
