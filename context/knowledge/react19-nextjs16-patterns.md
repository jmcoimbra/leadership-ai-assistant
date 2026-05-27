# React 19 + Next.js 16 + Tailwind v4 Patterns

> Owner: [Brain Owner] | Pillar: Pillar 4 (AI Execution) | Last Updated: 2026-03-30
> Measurable Outcome: Zero React 19 lint regressions in [your-org]-app-preview. Baseline: 4 (this session)
> Escalation Trigger: Same lint error encountered twice across sessions

---

## React 19 Strict Lint Rules

### `react-hooks/refs` — No ref access during render

React 19 forbids reading or writing `ref.current` during the render phase. This includes the common "sync ref to latest prop" pattern.

```tsx
// FAILS: react-hooks/refs
const onDoneRef = useRef(onDone)
onDoneRef.current = onDone  // ← Cannot update ref during render

// FIX: useCallback with empty deps (stable identity)
const stableOnDone = useCallback(onDone, [])
```

For `useSyncExternalStore`, the `getSnapshot` function can read localStorage (it's not a ref), so it works. Use this for any value that needs to survive hydration mismatch.

### `react-hooks/set-state-in-effect` — No setState in effects for initialization

```tsx
// FAILS: react-hooks/set-state-in-effect
useEffect(() => { setPref(getStoredPreference()) }, [])

// FIX: useSyncExternalStore
const pref = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot)
```

### `forwardRef` deprecated

React 19 passes `ref` as a regular prop. `forwardRef` still works but adds wrapper complexity and triggers strict mode warnings.

```tsx
// OLD (React 18)
export const Foo = forwardRef<FooRef, FooProps>(function Foo(props, ref) { ... })

// NEW (React 19)
export function Foo({ ref, ...props }: FooProps & { ref?: Ref<FooRef> }) {
  useImperativeHandle(ref, () => ({ focus: () => inputRef.current?.focus() }))
}
```

## Next.js 16 App Router Script Handling

### `<script dangerouslySetInnerHTML>` triggers console error in App Router

React 19 warns: "Scripts inside React components are never executed when rendering on the client." The script DOES execute via SSR, but the console error is noisy and indicates incorrect usage.

```tsx
// FAILS (React 19 console error)
<script dangerouslySetInnerHTML={{ __html: themeScript }} />

// FIX: next/script with beforeInteractive
import Script from 'next/script'
<Script id="theme-script" strategy="beforeInteractive" dangerouslySetInnerHTML={{ __html: themeScript }} />
```

Verified: `beforeInteractive` renders an identical synchronous inline `<script>` in SSR HTML output. No FOUC. Confirmed via curl against production build (2026-03-29). Add `suppressHydrationWarning` on `<html>` for server/client class mismatch.

**Note:** This is App Router specific. Pages Router may behave differently.

### Build-time env var for version (hydration mismatch prevention)

Direct `import packageJson from '../../package.json'` in components can cause hydration mismatch if server/client bundles resolve different versions during overlapping deployments.

```ts
// next.config.ts — expose at build time
import packageJson from './package.json'
if (!packageJson.version) {
  throw new Error('package.json version is missing')
}
const nextConfig: NextConfig = {
  env: { NEXT_PUBLIC_APP_VERSION: packageJson.version },
}

// Component — read from env
const version = process.env.NEXT_PUBLIC_APP_VERSION || 'dev'
```

This ensures server and client both use the same build-time constant. Add a build-time assertion to fail fast if version is missing.

## Tailwind v4 Dark Mode

### `@theme` vs `@theme inline`

`@theme inline` bakes literal hex values into utility classes. CSS variable overrides in `.dark {}` have no effect because utilities reference hex literals, not `var()`.

```css
/* BROKEN: dark mode variables ignored */
@theme inline {
  --color-background: #f8f9fa;
}

/* CORRECT: utilities emit var(--color-background) */
@theme {
  --color-background: #f8f9fa;
}
```

### Class-based dark mode directive

Tailwind v4 requires explicit custom variant for class-based dark mode:

```css
@custom-variant dark (&:where(.dark, .dark *));
```

Without this, `dark:` prefixed utilities have no effect.

### Dark mode variable overrides

Define light values in `@theme {}`, override in `.dark {}`:

```css
@theme {
  --color-background: #f8f9fa;
  --color-surface: #ffffff;
}
.dark {
  --color-background: #0d1117;
  --color-surface: #161b22;
}
body { background: var(--color-background); }
```

## FOUC Prevention (Dark Mode)

### Cookie-based server rendering

Eliminate hydration mismatch by syncing theme preference via cookie:

1. Inline script reads localStorage, sets cookie + `.dark` class
2. `layout.tsx` reads cookie server-side via `cookies()` from `next/headers`
3. Server renders correct `className` on `<html>` — no mismatch

Cookie flags: `SameSite=Lax` (no `Secure` for localhost dev compatibility).

### Double requestAnimationFrame

Single rAF can fire before first paint is committed on fast loads. Double rAF is reliable:

```js
requestAnimationFrame(function(){
  requestAnimationFrame(function(){
    document.documentElement.classList.add('theme-ready')
  })
});
```

`theme-ready` class enables CSS transitions only after first paint, preventing color flash.

## Silent Failure Checklist (Dark Mode)

When adding dark mode to an existing app, audit every component for:

1. **Form elements** (`<select>`, `<input>`, dialog inputs) — browser defaults white background. Add `bg-surface text-foreground`
2. **Status text** (`text-red-600`, `text-amber-600`) — low contrast on dark backgrounds. Add `dark:text-red-400`, `dark:text-amber-400`
3. **Hardcoded Tailwind colors** (any `zinc-*`, `gray-*`, `blue-*` without `dark:` variant) — replace with semantic tokens
4. **Hover states** (`hover:text-red-700`) — gets darker on dark backgrounds. Add `dark:hover:text-red-300`
5. **Cookie flags** — `Secure` flag prevents cookie on localhost HTTP. Omit for dev tools

## Parent-Child Control via `useImperativeHandle`

When a parent component needs to trigger actions on a child (e.g., replay button outside a phone simulator), use `forwardRef` + `useImperativeHandle`:

```tsx
// Child: expose specific actions
export interface AppPreviewHandle {
  replayOnboarding: () => void
  hasOnboarding: boolean
}
export const AppPreview = forwardRef(function AppPreview(
  { appConfig, onOnboardingChange }: Props,
  ref: Ref<AppPreviewHandle>
) {
  useImperativeHandle(ref, () => ({
    replayOnboarding: () => updateOnboarding(true),
    hasOnboarding,
  }))
})

// Parent: call via ref
const previewRef = useRef<AppPreviewHandle>(null)
<AppPreview ref={previewRef} onOnboardingChange={setPlaying} />
<button onClick={() => previewRef.current?.replayOnboarding()} disabled={playing}>
  Replay
</button>
```

Use callback props (`onOnboardingChange`) to sync child state back to parent for UI updates (disabled state, etc.).

**Standalone HTML export parity:** When a React app has both a web app entry and a standalone HTML export (esbuild IIFE), every UI change to the phone preview must be mirrored in the export's entry point (`preview-entry.tsx`). Use inline styles in the export (no Tailwind available).

## Cloudflare Bot Management ([Your Company] staging/sandbox)

[Your Company] staging/sandbox API endpoints are behind Cloudflare Bot Management. Client-side `fetch` triggers:
- HTTP 307 redirect → 403 Forbidden
- Response header: `cf-mitigated: challenge`
- This is NOT basic auth — it's Cloudflare challenge injection

No client-side workaround exists. If a tool needs staging/sandbox data, it must go through a server-side proxy or be production-only. Document the limitation in an ADR rather than building broken fallbacks.

## NextAuth v5 (beta.30) on Next.js 16

### Critical: Server action signIn only

Client-side `signIn()` from `next-auth/react` does NOT create session cookies on Next.js 16. Only server action `signIn()` from the auth config works:

```tsx
// BROKEN: client-side signIn (no session cookie set)
import { signIn } from 'next-auth/react'
<button onClick={() => signIn('google')}>Sign in</button>

// WORKS: server action signIn
import { signIn } from '@/auth'
<form action={async () => { 'use server'; await signIn('google', { redirectTo: '/' }) }}>
  <button type="submit">Sign in</button>
</form>
```

### No middleware for auth

Next.js 16 deprecated `middleware.ts`. The `authorized` callback in NextAuth config breaks the OAuth callback flow. Use layout-based route groups instead:

- `src/app/(protected)/layout.tsx` — calls `auth()`, redirects to `/auth/signin` if no session
- `src/app/(public)/` — sign-in and error pages, no auth check
- API routes: call `auth()` inline and return 401 if no session

### AUTH_URL is mandatory in production

Without `AUTH_URL`, NextAuth falls back to the container's internal address (`0.0.0.0:3000`). OAuth callbacks redirect there instead of the public domain.

When using docker-compose with explicit env vars, `AUTH_URL` must be listed in the `environment` section. Adding it to `.env` alone is not enough if docker-compose cherry-picks which vars to forward.

### AUTH_SECRET format

Use hex (64 chars), not base64. Base64 with `+`/`=` characters causes `JWTSessionError: no matching decryption secret`. Generate with: `openssl rand -hex 32`.

### Google OAuth: Internal vs External

For internal tools (e.g., [Your Company] employees only):
- Set User type to **Internal** on the Google OAuth consent screen
- Skips Google verification entirely
- All Google Workspace org users can sign in immediately
- **External + Production** requires privacy policy URL, TOS URL, authorized domains, and Google verification

### redirect_uri_mismatch: 2-sided check

`redirect_uri_mismatch` and "fast fix without redeploy" almost never coexist. The error has TWO independent checks; both must pass:

1. **Google-side allowlist** — does the URI exactly match an entry in the OAuth client's Authorized redirect URIs?
2. **App-side handler** — does the app actually serve a route at that path?

Whitelisting a path the app does not serve makes Google accept the redirect and send the user to a 404. NextAuth only mounts at `<basePath>/api/auth/callback/<provider>`. Adding any other path to Google's allowlist is a 404 trap.

The only legitimate no-deploy fixes are: (a) the path you whitelist is one the app already serves, OR (b) a reverse-proxy rewrite. Everything else requires a code change deploy.

Source: 2026-04-29 [your-org]-app-preview — basePath inference bug emitted `/app-preview/callback/google` instead of `/app-preview/api/auth/callback/google`. Whitelisted the broken URI as a "fast fix"; Google accepted, app 404'd. Removed the entry; only the basePath code fix (commit `18e54a4` on `[your-github-handle]/desired-count-no-ignore`) actually unblocks.

### NextAuth v5 basePath inference (Next.js basePath gotcha)

When `next.config.ts` sets `basePath: '/app-preview'` and `AUTH_URL` points at the path-rooted host (`https://admin.example.com/app-preview`), NextAuth v5's `setEnvDefaults` assigns the URL pathname to `config.basePath` and never appends `/api/auth`. The generated `redirect_uri` lands as `<host>/app-preview/callback/google` (missing `/api/auth/`). Set `basePath` explicitly in the NextAuth config:

```ts
export const { handlers, signIn, signOut, auth } = NextAuth({
  basePath: '/app-preview/api/auth',  // <next-config-basePath>/api/auth
  ...
})
```

Source: 2026-04-29 [your-org]-app-preview commit `18e54a4`.

## TypeScript Type-Narrowing Safety (saved-JSON round-trip)

When dropping a required field from an interface that flows through a JSON file then `JSON.parse` then `as` cast (e.g. user-saved configs, API responses), verify the runtime parser before changing the type. TS does not validate at parse time. Extra fields survive `JSON.parse` and `as` casts silently. The risk runs the OTHER direction: removing a field that an existing reader, serializer, or consumer still depends on.

**Verification checklist before narrowing a type:**
1. Grep the codebase for every reader of `<field>` (`grep -rn "\.<field>" src/`).
2. For each reader, confirm it has been updated or proves to be dead code.
3. If a `parseConfigFile`-style function exists, confirm it does NOT enforce shape. Most use a structural sanity check + `as`, which preserves extra fields. Then old saved files load cleanly, and the narrower type causes no breakage.
4. Confirm any serializer (`exportConfig`, `JSON.stringify(config)`) round-trips the in-memory object. Extra fields survive, which is the desired behavior for backward compat.
5. Check generated bundles (`.gitignore`d files like `src/generated/preview-bundle.ts`). They refresh on next `yarn generate` and are not a finding.

If all five hold, dropping the field is safe at the type level without breaking saved-config compat. If any reader still consumes `<field>` at runtime, fix that first before narrowing.

Source: 2026-04-29 [your-org]-app-preview PR #10. Removed `placement: string` from `NavigationTabStyle`. Ran the checklist: only ConfigEditor.tsx and AppPreview.tsx read it (both updated), `parseConfigFile` (`src/lib/config-state.ts:107`) does sanity-check + cast (preserves extras), `exportConfig` shallow-copies. Clean narrowing, zero backward-compat break.

## Cross-References

- `[your-org]-techstack.md` — Canonical stack (React, Next.js, Tailwind are ADOPT)
- `clean-code.md` — Smell G5 (duplication) applies to repeated `dark:` variant patterns; use semantic tokens instead
- `[your-org]-services.md` — Cloudflare zone settings, AWS account topology
