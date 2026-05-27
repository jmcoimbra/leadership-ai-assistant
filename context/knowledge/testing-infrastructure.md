# Testing Infrastructure

**Added:** 2026-03-07
**Last Updated:** 2026-03-07
**Source:** Repo audit via [Your IDP Tool] read_file across 5 frontend repos

## Frontend Repo Testing Stacks

| Repo | React | Playwright | Jest | RTL | MSW | CI test job | Notes |
|------|-------|-----------|------|-----|-----|-------------|-------|
| [your-org]-[your-product-ui] | 16.13.1 | None | 26 | v12 | 1.3.1 | test-unit | 12 test files. test-integration disabled (flakey). No required status checks. |
| [your-org]-ordering-ui | 17.0.2 | None | Yes | ? | ? | Yes | Next.js 12.x, Storybook |
| [your-org]-consumer-ui | 19.2.3 | @playwright/test 1.54 | 30 | v16 | 1.2.5 | test | Next.js 15, greenfield for tests. No test files yet. |
| [your-org]-mobile-app | 18.2.0 (RN) | None | ? | ? | ? | ? | React Native. Playwright CT incompatible |
| ordering-ui-lib | No React | None | Vitest | No | No | No | Shared logic library |

## Playwright CT Compatibility

- `@playwright/experimental-ct-react` requires React 18+
- `@playwright/experimental-ct-react17` exists for React 17
- React 16 has no verified Playwright CT support
- React Native is incompatible with Playwright CT (browser-based)
- **Best pilot repo for Playwright CT: [your-org]-consumer-ui** (React 19, Playwright already installed)

## [Your CTO]'s E2E Vision (Mar 6 DM)

[Your CTO] wants E2E integration tests, NOT component tests:
- Ephemeral backend booted in CI (API + ordering via gRPC)
- No sandbox dependency
- No API mocking. Run real API with seeded data
- Only mock downstream integration partners (POS, payment)
- Playwright browser tests against this ephemeral environment

This is a different layer from [Senior IC]'s component test plan. Both are valid (different pyramid layers).

## QA Testing Gate Strategy (Mar 7)

Three parallel tracks:
1. **[your-product-ui]:** Jest+RTL gate (existing stack, no blockers)
2. **consumer-ui:** Playwright CT pilot (modern stack, proves browser-based component tests)
3. **E2E in CI with ephemeral backend:** [Your CTO]'s project, sharing ~Mar 9-10

## Sidekiq Testing Patterns (migrated from memory tier 2026-04-27)

### WireMock Scope

Free / open-source WireMock mocks **HTTP APIs only**. No database, queue, or non-HTTP protocol mocking in any tier. When a test needs DB / queue mocking, use a different tool (Testcontainers, Sidekiq testing modes, etc.).

### Sidekiq Testing ([Your Company]-relevant)

- `Sidekiq::Testing.fake!` — jobs queue in memory, never execute. Assert with `MyWorker.jobs.size`, drain with `MyWorker.drain`.
- `Sidekiq::Testing.inline!` — jobs execute synchronously in calling thread. Good for asserting side effects.
- `Sidekiq::Testing.disable!` — real Redis, real async. Integration tests only.
- Rails ActiveJob layer: `have_enqueued_job` matcher, `perform_enqueued_jobs` helper.
- Real Redis only needed for: retries, scheduling, rate limiting, unique jobs, batches (Pro/Enterprise features).

### Queue Testing Decision Matrix

| Use case | Tool |
|----------|------|
| Unit tests / speed | Sidekiq inline or fake mode |
| Integration tests / protocol fidelity | Testcontainers with real broker |
| AWS queues (SQS/SNS) | LocalStack |
| No Docker available | Inline mode or embedded broker |

### Database Mocking (Reference)

- In-memory: pg-mem (Node), SQLite, H2 (Java)
- Containers: Testcontainers with real Postgres/MySQL/Redis
- Application-level: mock repository/DAO layer (RSpec mocks)
- Factories: FactoryBot (Ruby), factory_boy (Python)

## Jest CLI Quirks

- **`--testPathPattern` was renamed to `--testPathPatterns` (plural).** Newer Jest versions error on the singular: `Option "testPathPattern" was replaced by "--testPathPatterns". "--testPathPatterns" is only available as a command-line option.` Use the plural form to filter to a specific test file: `yarn test --testPathPatterns AppPreview`. Affects `jest@30+`. Source: 2026-04-29 [your-org]-app-preview (`jest@30.3.0`), singular form failed, plural worked.

## jsdom + structuredClone Polyfill

`jest-environment-jsdom` does NOT expose Node's `structuredClone` global. Production code that depends on `structuredClone` (cloning configs, deep-cloning state) will throw `TypeError: structuredClone is not a function` under jsdom unless the test environment polyfills it.

**Wrong (silently diverges from production):**

```ts
if (typeof globalThis.structuredClone === 'undefined') {
  globalThis.structuredClone = <T>(value: T): T =>
    JSON.parse(JSON.stringify(value))
}
```

JSON round-trip drops `Date`, `Map`, `Set`, `undefined`, typed arrays, functions, `Symbol`. Tests pass for plain-object configs but the day a caller passes a `Date` in production, behavior diverges silently.

**Right (matches the real Node global):**

```ts
if (typeof globalThis.structuredClone === 'undefined') {
  // eslint-disable-next-line @typescript-eslint/no-require-imports
  const v8 = require('node:v8')
  globalThis.structuredClone = <T>(value: T): T =>
    v8.deserialize(v8.serialize(value))
}
```

`v8.serialize`/`deserialize` is true structural clone. Place in `jest.setup.ts` (loaded via `setupFilesAfterEnv` in `jest.config.ts`).

**Why this matters even when current callers only pass plain objects:** a future test that passes a `Date` from a fixture, or a state object that grew a `Map`, will fail-pass (test green, prod broken). The cost of `v8.serialize` over `JSON.parse(JSON.stringify())` is negligible.

Source: 2026-04-29 [your-org]-app-preview PR #14, commits `89a5641` (initial JSON polyfill) and `090405c` (v8 swap after [engineering-toolkit] review).
