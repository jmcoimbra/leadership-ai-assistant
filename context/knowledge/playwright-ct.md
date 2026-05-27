# Playwright Component Testing (CT)

**Owner:** [Brain Owner]
**Pillar:** Pillar 4 (AI Execution)
**Last Updated:** 2026-03-06

## What It Is

Playwright CT is a testing mode within the Playwright framework for testing individual UI components in a real browser without a running application. Same Playwright core, different entry point.

- **Package:** `@playwright/experimental-ct-react` (also `-vue`, `-svelte`)
- **Status:** Experimental (API may evolve, but actively maintained and production-usable)

## How It Differs from Playwright E2E

| Aspect | E2E (`@playwright/test`) | CT (`@playwright/experimental-ct-*`) |
|--------|--------------------------|---------------------------------------|
| Entry point | `page.goto(url)` | `mount(<Component />)` |
| Requires running app | Yes | No (Vite bundles the component) |
| Scope | Full user flows across pages | Single component in isolation |
| API after mount | Same (locators, assertions, traces) | Same |
| Browser engines | Chromium, Firefox, WebKit | Chromium, Firefox, WebKit |

Everything after the entry point is identical: locators, clicks, assertions, trace viewer, CI integration.

## When to Use

| Tool | Best for |
|------|----------|
| **Playwright CT** | Component tests needing real browser behavior (CSS, a11y, visual regression) |
| **Vitest / Jest + Testing Library** | Fast unit tests where JSDOM is sufficient |
| **Playwright E2E** | Full user flows across multiple pages |

## Example

```ts
import { test, expect } from '@playwright/experimental-ct-react';
import { Button } from './Button';

test('button fires onClick', async ({ mount }) => {
  let clicked = false;
  const component = await mount(
    <Button onClick={() => (clicked = true)}>Click me</Button>
  );
  await component.click();
  expect(clicked).toBe(true);
});
```

## Key Advantages Over JSDOM-Based Testing

- Real browser rendering (CSS, layout, browser APIs behave as in production)
- No dev server startup required (Vite handles bundling)
- Same debugging tools as E2E (trace viewer, screenshots, video)
- Cross-browser testing out of the box
