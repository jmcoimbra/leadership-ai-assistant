# LaunchDarkly Patterns

**Owner:** [Brain Owner]
**Pillar:** Pillar 4 (AI Execution)
**Added:** 2026-05-12
**Last Updated:** 2026-05-12
**Source:** [your-org]-[your-product-ui] App Preview Boilerplate (JULI-96) session, 2026-05-11 / 2026-05-12. Captured 6+ rounds of LD UI back-and-forth before targeting rules matched.

## Context kind=user, not kind=merchant

The [your-product-ui] LD SDK initializer at `[your-org]-[your-product-ui]/src/components/FlagsProvider.tsx:107-111` calls `asyncWithLDProvider({ user: { key: 'merchant-${merchant.id}' } })`. The `user:` argument arrives at LD as a single context with `kind: 'user'`. There is no `merchant` context kind sent by the [your-product-ui] SDK today.

Targeting rules in the LD UI must use `kind=user`. The UI's add-target widget remembers the last-used Kind across flags and silently defaults to whichever was used last. If a previous flag set Kind to `merchant`, a new flag's targeting rows inherit `merchant` and silently never fire. No error surfaces.

**Validation:** open the flag in LD UI, Release, Live events, filter by flag key. When the staging dashboard impersonates a flagged merchant, the event should show `kind=user, key=merchant-{id}, value=true`. If it shows `false` despite a matching key, the rule is keyed on the wrong kind.

Source: 2026-05-11 JULI-99 LD config. Targeting rules for NBC (merchant-1059) and Salt & Straw (merchant-1095) initially shipped with `kind=merchant` on all 4 rows across staging + sandbox. Caught only after a screenshot zoom showed the Kind column.

## Safe production posture: toggle ON, default false, no rules

For a flag staged before any merchant pilots:

| Env | Toggle | Default rule | Targeting rules |
|---|---|---|---|
| Production | ON | `false` | None |
| Staging | ON | `false` | `kind=user, key in {pilot_ids...} → true` |
| Sandbox | ON | `false` | `kind=user, key in {sandbox_pilot_ids...} → true` |

**Toggle ON + default false:** rules evaluate, fallback returns false. Lets you add targeting rules later without remembering to flip the toggle first.

**Toggle OFF:** short-circuits all rules and serves the off-variation to everyone, bypassing the default rule. Adding rules has no effect until the toggle is flipped.

Same observable behavior today (everyone sees false), different operational shape. Default to ON-with-default-false for new flags so the production flip is "add a rule" not "flip the toggle AND add a rule."

**Pitfall caught 2026-05-11:** the LD UI's flag creation flow can land the default rule on `true` for some templates. A production flag with `toggle ON + default true + no rules` means EVERY merchant in prod gets the variation. Always edit the default rule to `false` before saving production config. Screenshot the prod Targeting tab before walking away.

## Per-environment merchant IDs

Staging and sandbox often have different merchant IDs for the same brand. Even when one ID happens to match (e.g. NBC = 1059 in all 3 envs in our session), do not assume.

| Source | Method |
|---|---|
| Production | Looker query against `merchants` explore (`SELECT id, name FROM merchants WHERE name ILIKE '%nbc%'`) or prod replica |
| Staging | Log into staging dashboard, impersonate, copy `merchant.id` from URL or React DevTools Redux state |
| Sandbox | Same flow on sandbox dashboard |

Looker reads Snowflake which mirrors production only. There is no Looker shortcut for staging / sandbox IDs.

## Impersonation works automatically

When a [Your Company] admin impersonates a merchant, `useCurrentMerchant()` (`[your-org]-[your-product-ui]/src/hooks/useCurrentMerchant.ts`) returns the impersonated merchant. The LD context key becomes `merchant-{impersonated_id}` and targeting rules follow the impersonated merchant. No extra plumbing needed.

Validation: impersonate a flagged merchant in staging, navigate to a flag-gated page, confirm the gated render. Switch to a non-flagged merchant, refresh, confirm fallback behavior.

## Tag conventions

Recommended tags on every new LD flag:

- Product area: `mx-dashboard`, `cms`, `ordering`, `loyalty`, etc.
- Feature: short kebab-case name matching the flag key prefix.
- Jira link: lowercase ticket-key without prefix (`juli-96`, `bugs-4025`).
- Temporality: use the LD-native `Temporary` toggle rather than a tag.

Tag filtering in LD UI scales better than flag-key search when the project has 50+ flags.

## SDK kind taxonomy reference

If we ever want to send a separate `merchant` context (e.g. for brand-level rules), the SDK call shape changes to multi-context:

```ts
asyncWithLDProvider({
  context: {
    kind: 'multi',
    user: { key: 'user-...' },
    merchant: { key: 'merchant-...' },
  },
})
```

Today's `user: { key }` shorthand maps to single-context `kind=user`. Migrating to multi-context requires editing every existing LD rule that depends on the current `user` key shape. Treat as a deliberate cross-team migration, not a quick refactor.
