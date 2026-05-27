# WireMock & Service Virtualization Patterns

**Added:** 2026-03-27
**Last Updated:** 2026-03-27
**Source:** Stability Tiger Team Kickoff, WireMock docs, codebase analysis

> Patterns for WireMock-based E2E testing at [Your Company]. For CircleCI orb patterns, see `[your-org]-services.md`. For tech stack classification, see `[your-org]-techstack.md`.

## Tool Overview

- **WireMock OSS:** Apache 2.0, free. Docker image: `wiremock/wiremock:latest`
- **gRPC Extension:** `wiremock/wiremock-grpc-extension` (required for [Your Company] — services use gruf on port 50051)
- **Testcontainers:** Disposable Docker containers for databases. Used alongside WireMock for full isolation.

## [Your Company] Architecture Decisions (Mar 27, 2026)

| Decision | Rationale |
|----------|-----------|
| App runs native, deps in containers | Ruby/Rails dev not optimized for containerized dev (volume mount perf, gem install, debugging) |
| Extend `[your-org]-services` orb, not new orb | All backend repos already use it. WireMock = optional sidecar like MySQL/Postgres/Redis |
| Contract validation is Phase 1 | [Senior IC] raised mock drift risk (gift card failure: worked in mock, failed in prod with different POS). Nightly validation mitigates |
| Frontend uses Playwright, not Cypress | Cypress dep exists abandoned in [your-org]-ordering-ui. Playwright: faster, Docker-native, multi-browser, better TS support |
| Frontend WireMock mocks internal APIs | Backend WireMock mocks external third-party APIs. Different stub strategies |

## Stub File Structure (per repo)

```
test/
  wiremock/
    mappings/         # REST stub definitions (JSON)
    grpc/             # gRPC stub definitions
    __files/          # Response body files
    proto/            # Proto files (from [your-org]-protorepo)
```

## gRPC Stubbing

WireMock gRPC extension requires `.proto` files. Proto source: `[your-org]-protorepo`.

Options for proto access:
1. Git submodule in each repo (preferred — version-pinned)
2. CI step fetches protos before WireMock starts
3. Custom WireMock Docker image with protos baked in

gRPC stub format matches REST but with service/method URL paths:
- URL pattern: `/com.example.ordering.OrderService/CreateOrder`
- Content-Type: `application/grpc`

## Recording Mode (VCR Migration)

WireMock can proxy real APIs and record traffic as stubs. Useful for converting existing VCR cassettes:
1. Start WireMock with `--record-mappings --proxy-all="https://api.olo.com"`
2. Run existing test suite through WireMock
3. Generates stub files automatically

[your-org]-ordering has 8 VCR cassette directories — prime candidate for conversion.

## Test Migration: Assertion Derivation (VCR → WireMock)

When migrating a VCR cassette test to WireMock, assertion values must be re-derived from the **stub payload**, not transcribed from the prior test's literal values.

The stub is the new source of truth. Any field the stub adds, changes, or omits relative to the original cassette recording shifts downstream computed fields:

| Scenario | Downstream impact |
|----------|-------------------|
| Stub adds a fee/charge the cassette didn't record | `total_fee`, `total` shift. Computed nets (`subtotal_v2 = subtotal - total_discount`) shift |
| Stub applies a discount the cassette didn't | `total_discount` non-zero, `subtotal_v2 < subtotal` |
| Stub uses different item amounts | `item_total`, `subtotal`, all downstream totals shift |
| Stub omits an array the cassette had (e.g., `taxes: []`) | Length and aggregate calculations shift |

**Reviewer mandate:** when suggesting literal assertion values in a PR review for a VCR-to-WireMock migration, open the stub file (`test/wiremock/__files/<provider>/<endpoint>/success.json`) and derive the expected value from it. Never transcribe from the prior test's assertion block — that captures the cassette's reality, not the stub's.

**Inline comment pattern** (author of [your-org]-ordering#3195 demonstrated): reference the stub path + explain the divergence quantitatively. Example:

```ruby
# Assertion values reflect what the WireMock prices stub at
# test/wiremock/__files/toast/prices/success.json returns, which differs
# from the original VCR cassette's recorded payload on three fields:
# the stub applies a $1.00 discount and a $2.99 service charge that
# weren't in the cassette. subtotal_v2 = subtotal - total_discount
# (6.0 - 1.0 = 5.0). The stub is the new source of truth.
```

Source: 2026-04-24 [your-org]-ordering#3195 (TIGER-34 Toast migration). Reviewer suggestion proposed `subtotal_v2: 6.0` transcribed from the old cassette's literal; author corrected to `5.0` by deriving from stub-controlled fields.

## Fault Simulation

Available faults: `CONNECTION_RESET_BY_PEER`, `EMPTY_RESPONSE`, `MALFORMED_RESPONSE_CHUNK`, `RANDOM_DATA_THEN_CLOSE`.
Fixed/random delays via `fixedDelayMilliseconds` or `randomDelay`.

## Contract Validation Pattern

Nightly scheduled pipeline:
1. Replay recorded stubs against real downstream APIs
2. Compare responses to stored expectations
3. On drift: Slack alert to #stability-tiger-team + auto-create Jira ticket
4. Dashboard tracks contract compliance %

Without this, WireMock stubs diverge from real APIs over time. [Senior IC]'s gift card example proves this risk is real.

## CircleCI Integration

**Approach:** Add optional `wiremock: true` parameter to `[your-org]-services` orb `rspec` job.

When enabled:
- Adds WireMock Docker image as sidecar (same pattern as MySQL/Postgres/Redis sidecars)
- Mounts `test/wiremock/mappings/` and `test/wiremock/__files/`
- Exposes REST on :8080, gRPC on :8081
- E2E tests tagged `e2e` run against the mocked services

**Executor note:** Docker executor supports sidecars natively. No need for machine executor for WireMock sidecar.

## Local Development

```yaml
# docker-compose.wiremock.yml (template)
services:
  wiremock:
    image: wiremock/wiremock:latest
    ports:
      - "8080:8080"   # REST + Admin API
      - "8081:8081"   # gRPC
    volumes:
      - ./test/wiremock/mappings:/home/wiremock/mappings
      - ./test/wiremock/__files:/home/wiremock/__files
    command: >
      --verbose --extensions grpc --grpc-port 8081
```

App configured via env var: `WIREMOCK_HOST=localhost:8080`.

## Stateful Behavior

WireMock supports scenarios (state machines) for multi-step flows:
- Order lifecycle: create → poll status → webhook callback
- Uses `scenarioName`, `requiredScenarioState`, `newScenarioState`

## Request Verification

Post-test assertion that WireMock received expected requests:
```
POST http://localhost:8080/__admin/requests/count
{"method": "POST", "url": "/api/v1/orders"}
```

## Relevant Extensions

| Extension | Purpose | Priority |
|-----------|---------|----------|
| wiremock-grpc-extension | gRPC stubbing (gruf services) | Required day 1 |
| Response templating (built-in) | Dynamic responses from request data | Built-in |
| Webhooks extension | Simulate provider webhook callbacks | Evaluate for ordering |

## Target Repos

| Repo | Type | Why First | Key Dependencies |
|------|------|-----------|-----------------|
| [your-org]-ordering | Backend | Most integrations, VCR cassettes, REST+gRPC | OLO, Toast, DoorDash, Square, MySQL, Postgres, Redis |
| [your-org]-ordering-ui | Frontend | Pairs with ordering, Cypress intent exists | [your-org]-api, [your-org]-merchant-api-new |
