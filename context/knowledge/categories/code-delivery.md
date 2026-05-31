---
category: code-delivery
description: PR reviews, SDLC, writing docs, deploy planning, agile cadence
parent: null
aliases: [pr, code-review, sdlc, deploy, docs]
---

# Code Delivery

PR authoring, review, deployment, SDLC gates, and code-quality doctrines.

## When This Category Applies

Load when the task involves:
- Writing or reviewing a PR
- Deploy planning, risk tiering
- SDLC phase gates, BDD/TDD, PRD coverage
- Writing technical documentation (RFCs, runbooks, ADRs)
- Agile cadence (sprint, retro, planning) decisions
- dbt CI debugging or incremental model design
- LaunchDarkly feature-flag rollouts

## Knowledge Files

| File | Why Load |
|------|----------|
| `sdlc-pipeline.md` | Phase gates, Patch/Feature/Initiative, embedded adoption tracking |
| `agentic-sdlc-decision-flow.md` | Decision-flow doctrine for AI-native SDLC gates |
| `agile-frameworks.md` | Scrum/Kanban/Discovery rituals, PRD acceptance, capacity tradeoffs |
| `writing-docs.md` | Docs structure, audience-aware framing, RFC patterns |
| `dbt-patterns.md` | state:modified cascade, incremental multi-source, long-lived branch rebase |
| `launchdarkly-patterns.md` | Flag rollout strategies, evaluation rules, kill-switch design |
| `qlty-patterns.md` | Static-analysis plugin selection, mixed-stack repo coverage |
