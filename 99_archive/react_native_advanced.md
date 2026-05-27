# React Native — Advanced Patterns

**Purpose:** Raw chapter-by-chapter extraction of enforceable patterns. Narrative discarded. Dated patterns flagged with [2022]. Modern equivalents noted where significant.

---

## Ch 1: What Is React Native?

### Architecture: Old Bridge (default as of 2022)
- JS thread ↔ Native thread communication via serialized JSON over asynchronous bridge
- Three threads: JS thread (business logic), native/UI thread (rendering), shadow thread (Yoga layout)
- Bridge is the bottleneck: serialization cost on every cross-thread call
- All JS executes on a single thread — blocking JS blocks the entire UI

### Architecture: New (JSI + Fabric + TurboModules) [2022 — partially shipped]
- JSI (JavaScript Interface): C++ layer allowing direct JS ↔ native calls without serialization
- Fabric: new renderer replacing UIManager; synchronous rendering, supports concurrent React features
- TurboModules: lazy-loaded native modules via JSI; replaces NativeModules registry
- CodeGen: generates type-safe native bindings from TypeScript/Flow specs at build time
- Migration: Fabric + TurboModules are opt-in; full new arch requires explicit enablement per platform
- **Decision rule:** New arch = required for Concurrent Mode features; not stable for all libraries as of 2022

### Yoga Layout Engine
- Implements Flexbox subset; maps RN style props to native platform layout primitives
- Default flex direction in RN is `column` (not `row` as in CSS web)
- Cross-platform layout: same Yoga code runs on iOS, Android, Web

### Hermes JS Engine
- AOT bytecode compilation (vs JSC/V8 JIT)
- Android TTI: -53% vs JSC; app size: -46%; memory: -26%
- iOS: available from RN 0.64; Android: default from RN 0.60.4 [verify current default]
- Activation Android: `enableHermes: true` in `android/app/build.gradle`
- Activation iOS: `hermes_enabled => true` in Podfile + `pod install` + clean build
- Hermes does NOT support all ES2015+ features (e.g., Proxy) — verify before adding libraries

### Expo Workflow Decision Matrix
- **Managed workflow:** Expo SDK controls native layer; no `android/` or `ios/` dirs
  - Use when: rapid prototyping, no custom native modules, team lacks native expertise
  - Constraint: limited to Expo SDK API surface; native modules outside SDK require ejecting
- **Bare workflow:** Full React Native project + Expo utilities
  - Use when: custom native code required, third-party native modules, advanced CI/CD
  - `expo init --template bare-minimum`
- **Eject:** One-way operation from managed → bare; cannot reverse
- Expo Go: development client for managed; bare workflow requires custom dev client build

### React Native vs React Web
- No DOM: no `<div>`, `<span>`, `<p>` — use `<View>`, `<Text>`, `<Image>`
- All layout via Flexbox (Yoga) — no CSS Grid, no floats
- Styles are JS objects, not CSS strings
- No browser APIs: no `localStorage`, `document`, `window` in native targets
- Platform-specific file extensions: `.ios.tsx`, `.android.tsx` for platform splits

---

## Ch 2: Understanding the Essentials of JavaScript and TypeScript

### Object Reference Pitfalls
- Objects and arrays are passed by reference in JS — mutations propagate silently
- **Rule:** Never mutate state objects directly; always clone before modification
- Shallow clone: `{ ...obj }` or `Object.assign({}, obj)` — does NOT deep-clone nested objects
- Deep clone: `JSON.parse(JSON.stringify(obj))` — loses functions, Date objects, undefined values
- For nested state: use Immer (via Redux Toolkit) or manual deep spread
- Array mutation traps: `push()`, `pop()`, `splice()`, `sort()` mutate in place — use `[...arr, newItem]`, `arr.filter()`, `arr.map()`

### Async Patterns
- Callback hell: avoid; use Promises or async/await
- async/await: syntactic sugar over Promises; `await` only valid inside `async` function
- **Rule:** Always wrap `await` in try/catch or attach `.catch()` — unhandled rejections crash
- Promise.all: runs concurrent async ops; fails fast if any rejects — use Promise.allSettled for partial results
- useEffect + async: cannot pass async function directly; wrap in IIFE or inner async function:
  ```js
  useEffect(() => {
    const fetchData = async () => { ... };
    fetchData();
  }, []);
  ```

### TypeScript Enforcement Rules
- **Never use `any`** — defeats type safety; use `unknown` if type is truly unknown, then narrow
- Use `interface` for object shapes that may be extended; `type` for unions, intersections, primitives
- Strict mode: enable `"strict": true` in tsconfig — catches null/undefined errors at compile time
- `as` type assertion: only when you have 100% certainty; document why
- Generic types: prefer over `any` for reusable utilities
- `readonly` modifier: apply to props that must not mutate
- Non-null assertion (`!`): avoid; handle null explicitly

### Functional Programming Patterns
- Pure functions: same input → same output, no side effects — required for reducers
- Immutability: required for React state (reference equality checks in hooks, memoization)
- Higher-order functions: `map`, `filter`, `reduce` preferred over imperative loops
- Closures: variables captured at definition time — stale closure bug in useEffect is the most common RN pitfall

---

## Ch 3: Hello React Native

### Project File Structure (bare RN)
```
/android          — Android native project
/ios              — iOS native project
/src              — all JS/TS source
  /components     — reusable UI components
  /screens        — screen-level components
  /navigation     — navigator definitions
  /hooks          — custom hooks
  /utils          — pure utility functions
  /services       — API clients, storage wrappers
  /store          — global state (Zustand/Redux slices)
  /assets         — images, fonts, icons
App.tsx           — entry point
index.js          — registers AppRegistry
```

### React Hooks Rules (enforced by eslint-plugin-react-hooks)
- Never call hooks inside conditionals, loops, or nested functions
- Never call hooks from regular JS functions — only from React function components or custom hooks
- Custom hook naming: must start with `use` prefix
- `useState`: initial value evaluated once; for expensive init use `useState(() => expensiveCalc())`
- `useEffect` cleanup: return cleanup function to prevent memory leaks (subscriptions, timers, event listeners)
- `useCallback`: memoize callback references passed as props to prevent child re-renders
- `useMemo`: memoize expensive computed values; do not over-apply (has its own overhead)
- `useRef`: access DOM/native node OR persist mutable value across renders without triggering re-render

### Stale Closure in useEffect — Critical Anti-Pattern
```js
// BUG: stale closure — count never increments beyond 1
useEffect(() => {
  const id = setInterval(() => {
    setCount(count + 1); // 'count' is captured at 0
  }, 1000);
  return () => clearInterval(id);
}, []); // empty deps

// FIX: use functional updater form
useEffect(() => {
  const id = setInterval(() => {
    setCount(prev => prev + 1); // always fresh
  }, 1000);
  return () => clearInterval(id);
}, []);
```
- **Rule:** If a value from outer scope is used inside useEffect, it must be in the dependency array OR use functional updater form

### Component Lifecycle via Hooks
- Mount: `useEffect(() => { ... }, [])` — runs once after first render
- Update: `useEffect(() => { ... }, [dep])` — runs when dep changes
- Unmount: cleanup function returned from useEffect
- `componentDidMount` → `useEffect(fn, [])`
- `componentDidUpdate` → `useEffect(fn, [deps])`
- `componentWillUnmount` → `return () => cleanup()` inside useEffect

### Class Components [2022 — avoid in new code]
- Still valid but React team recommends function components + hooks for all new code
- Error boundaries: only available as class components (no hook equivalent as of 2022)
- **Rule:** New components = function components only. Migrate class components when touching them.

---

## Ch 4: Styling, Storage, and Navigation in React Native

### StyleSheet Rules
- `StyleSheet.create({})`: validates style properties at dev time, flattens at runtime for perf
- **Rule:** Always use `StyleSheet.create()` over inline style objects — inline creates new object reference per render, breaking memoization
- Inline styles: only acceptable for truly dynamic values (e.g., `{{ width: dynamicValue }}`)
- styled-components: valid for complex component libraries; adds JS bundle overhead
- No CSS cascade — styles are flat, no inheritance except `<Text>` inside `<Text>`
- Platform-specific styles:
  ```js
  import { Platform, StyleSheet } from 'react-native';
  const styles = StyleSheet.create({
    shadow: Platform.select({
      ios: { shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.25 },
      android: { elevation: 4 },
    }),
  });
  ```
- `Platform.OS`: `'ios'` | `'android'` | `'web'`

### Local Storage Decision Matrix
| Need | Solution | Notes |
|------|----------|-------|
| Simple key-value | MMKV | 30x faster than AsyncStorage; synchronous reads |
| Simple key-value | AsyncStorage | Deprecated from RN core; use `@react-native-async-storage/async-storage` |
| Structured relational data | SQLite (`react-native-sqlite-storage`) | Full SQL queries |
| File system | `react-native-fs` | Read/write arbitrary files |
| Secrets / tokens | `expo-secure-store` or `react-native-keychain` | Uses iOS Keychain / Android Keystore |
| Sensitive but non-credential | `react-native-sensitive-info` | Fingerprint-locked on Android |

- **Rule:** Never store auth tokens in AsyncStorage — use Keychain/Keystore only
- **Rule:** Never store API keys in the app bundle — they are extractable; use a backend proxy
- MMKV: synchronous reads are safe in React Native (unlike web); avoids async waterfall for startup data

### react-navigation Setup Patterns
- Install: `@react-navigation/native` + required navigators + `react-native-screens` + `react-native-safe-area-context`
- Wrap app in `<NavigationContainer>`
- Stack Navigator: `@react-navigation/native-stack` (uses native primitives) vs `@react-navigation/stack` (JS implementation — more customizable, heavier)
- **Rule:** Use `native-stack` by default; fall back to JS stack only for custom header animations
- Tab Navigator: `@react-navigation/bottom-tabs`
- Passing params: `navigation.navigate('Screen', { id: 123 })` → receive via `route.params.id`
- Type-safe navigation:
  ```ts
  type RootStackParamList = {
    Home: undefined;
    Profile: { userId: string };
  };
  ```
- Deep linking: configure `linking` prop on `NavigationContainer`
- Navigation ref: `createNavigationContainerRef()` for navigation outside components

---

## Ch 5: Managing States and Connecting Backends

### State Management Decision Rules
- Component-local state (`useState`): UI state that doesn't cross component boundaries
- Context API: shared state for low-frequency updates (theme, locale, auth user)
  - **Anti-pattern:** Context for high-frequency updates (search input, animation values) — causes all consumers to re-render on every change
  - Mitigation: split contexts by update frequency; memoize with `useMemo` + `useCallback`
- Zustand: global state for medium-frequency updates; minimal boilerplate
- Redux Toolkit: global state for complex business logic with many action types and side effects

### Zustand Patterns
```ts
import create from 'zustand';

interface CounterState {
  count: number;
  increment: () => void;
}

const useCounterStore = create<CounterState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}));

// Selector — only re-renders when count changes
const count = useCounterStore((state) => state.count);
```
- **Rule:** Always use selectors in Zustand — `useStore(state => state.specificField)` not `useStore()` (subscribes to entire store)
- Zustand persist: `zustand/middleware` `persist` middleware wraps store for AsyncStorage/MMKV persistence

### Redux Toolkit Patterns
- `createSlice`: combines actions + reducer in one declaration
- `createAsyncThunk`: handles async operations with pending/fulfilled/rejected states
- `RTK Query`: data fetching + caching; generates hooks from endpoint definitions
- **Rule:** Use RTK Query for server state — avoids manual loading/error state management
- `immer` is built into RTK — mutate state directly inside `createSlice` reducers (immutability handled automatically)

### API Security Rules
- **Never hardcode API keys in source** — extractable from binary
- Environment variables via `.env` + `react-native-config` or `babel-plugin-transform-inline-environment-variables`
- **Rule:** `.env` files must be in `.gitignore` — never commit
- Sensitive keys (payment, auth) must live server-side; app calls your backend, backend calls third-party
- Certificate pinning: `react-native-ssl-pinning` for high-security API calls; adds maintenance overhead (cert rotation)

### Backend Connection Patterns
- REST: `fetch` (built-in) or `axios`; axios provides interceptors, request cancellation, automatic JSON parsing
- GraphQL: `@apollo/client` — normalized cache, optimistic updates, subscriptions
- WebSockets: React Native supports `WebSocket` global natively
- **Rule:** Always handle network errors explicitly — RN does not throw by default on non-2xx responses with `fetch`
  ```js
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  ```

---

## Ch 6: Working with Animations

### Animated API (Core RN)
- `Animated.Value`: mutable animated value; never read `.value` directly in render
- `Animated.timing`: time-based animation
- `Animated.spring`: physics-based with `tension` and `friction` params
- `Animated.decay`: friction-based deceleration
- `useNativeDriver: true`: runs animation entirely on native thread — **required for 60fps**
  - Supported props: `opacity`, `transform` (translate, scale, rotate) only
  - NOT supported: `width`, `height`, `backgroundColor`, `padding`, `margin`
- Interpolation:
  ```js
  const opacity = animValue.interpolate({
    inputRange: [0, 1],
    outputRange: [0, 1],
    extrapolate: 'clamp', // prevents values outside outputRange
  });
  ```
- `Animated.event`: maps gesture/scroll events directly to Animated.Value without JS thread
  ```js
  onScroll={Animated.event(
    [{ nativeEvent: { contentOffset: { y: scrollY } } }],
    { useNativeDriver: true }
  )}
  ```
- Composition: `Animated.sequence`, `Animated.parallel`, `Animated.stagger`, `Animated.loop`
- `Animated.add`, `Animated.multiply`, `Animated.divide`, `Animated.modulo`: derived values

### Reanimated 2 (react-native-reanimated) — Preferred for Complex Animations
- Worklets: functions that run on the UI thread (marked with `'worklet'` directive)
- `useSharedValue(initialValue)`: mutable value accessible from both JS and UI thread
- `useAnimatedStyle(fn)`: derives styles from shared values; re-runs worklet on UI thread
- `useAnimatedScrollHandler`: handles scroll events on UI thread
- `withTiming`, `withSpring`, `withDecay`: animation functions for shared values
- `runOnJS(fn)(args)`: call JS-thread function from worklet (for state updates, navigation)
- `runOnUI(workletFn)(args)`: call UI-thread worklet from JS thread

```ts
import { useSharedValue, useAnimatedStyle, withTiming } from 'react-native-reanimated';

const opacity = useSharedValue(0);
const animatedStyle = useAnimatedStyle(() => ({
  opacity: withTiming(opacity.value, { duration: 300 }),
}));
// trigger: opacity.value = 1;
```

- **Rule:** Prefer Reanimated 2 over Animated API for interactions requiring gesture-driven or high-frequency animations — avoids JS thread bottleneck entirely
- Reanimated 2 requires Hermes enabled for full functionality

### Lottie Animations
- Library: `lottie-react-native`
- Source: JSON animation files exported from After Effects via Bodymovin plugin
- `progress` prop: Animated.Value (0–1) controls playback position — enables gesture-driven scrubbing
- `autoPlay + loop` props for fire-and-forget animations
- **Rule:** Validate Lottie JSON file size — complex animations can be 100KB+; impacts bundle size
- Lottie renders natively on iOS/Android — no JS thread cost during playback

---

## Ch 7: Handling Gestures in React Native

### Pressable (preferred over TouchableOpacity/TouchableHighlight) [2022]
- `Pressable`: new, recommended; supports `onPressIn`, `onPressOut`, `onLongPress`
- Style callback receives `{ pressed }` state:
  ```jsx
  <Pressable style={({ pressed }) => [styles.btn, pressed && styles.btnPressed]}>
  ```
- `hitSlop`: expand touch area beyond visual bounds (accessibility requirement: min 44x44pt)
- `android_ripple`: native ripple effect on Android
- **Rule:** Minimum 44x44pt touch target — use `hitSlop` if component is visually smaller

### Gesture Responder System (Internal)
- Negotiation protocol: `onStartShouldSetResponder`, `onMoveShouldSetResponder`
- Parent can override: `onStartShouldSetResponderCapture` (capture phase)
- **Anti-pattern:** Nested scrollable containers with conflicting gesture responders — Android and iOS resolve differently
- `ScrollView.scrollEnabled = false` to temporarily disable scroll during custom gesture

### PanResponder [2022 — use RNGH 2.0 instead for new code]
- `PanResponder.create({})` wraps gesture responder system
- `onPanResponderMove`: `(evt, gestureState)` — `gestureState.dx`, `gestureState.dy` are cumulative offsets
- Spread onto `Animated.View` via `{...panResponder.panHandlers}`

### React Native Gesture Handler 2.0 (RNGH)
- Runs gesture recognition on native thread — eliminates JS thread latency
- Declarative gesture composition: `Gesture.Pan()`, `Gesture.Tap()`, `Gesture.Pinch()`, etc.
- `Gesture.Simultaneous(pan, pinch)`: multiple gestures active at once
- `Gesture.Exclusive(tap, doubleTap)`: only one active; priority by order
- `GestureDetector`: wraps component with gesture handlers
- **Rule:** Wrap app root in `<GestureHandlerRootView style={{ flex: 1 }}>` — required for RNGH 2.0
- Install: `react-native-gesture-handler` — requires additional native setup (MainActivity.java for Android)
- Works with Reanimated 2 via shared values — full UI thread pipeline

---

## Ch 8: JavaScript Engines and Hermes

### Hermes Benchmark Data (Android, vs JSC)
| Metric | Improvement |
|--------|-------------|
| TTI (Time to Interactive) | -53% |
| App download size | -46% |
| Memory usage | -26% |

- Source: Meta internal benchmarks cited in book

### Hermes Activation
**Android:**
```groovy
// android/app/build.gradle
project.ext.react = [
  enableHermes: true,
]
```
Clean build required: `cd android && ./gradlew clean`

**iOS (RN 0.64+):**
```ruby
# ios/Podfile
use_react_native!(
  :path => config[:reactNativePath],
  :hermes_enabled => true
)
```
Then: `cd ios && pod install` + clean build in Xcode

### Hermes Limitations
- No Proxy object support — some libraries rely on Proxy (verify before adopting)
- No JIT — workloads with heavy runtime code generation may be slower than JSC
- Bytecode format is Hermes-specific — cannot run Hermes bytecode on other engines
- Profiling: Chrome DevTools works with Hermes via metro debugger; `hermes-profile-transformer` for flamegraphs

### JSC (JavaScriptCore) [default before Hermes]
- JIT compilation — better for CPU-intensive sustained workloads
- Ships on iOS (system library); bundled on Android (adds 3–12MB)
- V8 via `react-native-v8`: not officially supported; community maintained

### Engine Selection Rule
- **Default choice:** Hermes — better TTI and memory for typical RN apps
- Only reconsider if: profiling shows Hermes slower for specific workload, or library requires Proxy

---

## Ch 9: Essential Tools for Improving React Native Development

### TypeScript Configuration (tsconfig.json)
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "esModuleInterop": true,
    "jsx": "react-native"
  }
}
```
- **Rule:** `strict: true` is non-negotiable — catches null/undefined bugs at compile time
- `noUnusedLocals` + `noUnusedParameters`: enforces dead code cleanup

### ESLint Setup
- Base: `@react-native-community/eslint-config`
- Required plugins: `eslint-plugin-react-hooks` (enforces hooks rules), `eslint-plugin-react-native`
- Import ordering: `eslint-plugin-import` with `order` rule — enforces consistent import grouping
- `.eslintrc.js` over `.eslintrc.json` — allows comments
- **Rule:** ESLint must run in CI — failing lint fails the build

### Prettier Setup
- Integrates with ESLint via `eslint-config-prettier` (disables conflicting ESLint formatting rules)
- `eslint-plugin-prettier` reports Prettier diffs as ESLint errors
- `.prettierrc`:
  ```json
  {
    "singleQuote": true,
    "trailingComma": "all",
    "printWidth": 100,
    "semi": true
  }
  ```
- **Rule:** `prettier --check` must run in CI before lint/test

### Boilerplate Evaluation Criteria
When selecting a starter template or boilerplate, validate:
1. Actively maintained (commits within 90 days)
2. TypeScript enabled by default
3. Navigation included (react-navigation)
4. State management included or documented decision
5. Testing setup included (Jest + RNTL)
6. Absolute imports configured (no `../../..` import chains)
7. ESLint + Prettier configured

### UI Library Selection Criteria
- Component coverage: does it cover all needed primitives?
- Theming: supports design tokens / theme overrides?
- Accessibility: ARIA roles, focus management, screen reader support?
- Maintenance: last release date, GitHub issues response time
- **React Native Paper**: Material Design; good accessibility; themeable
- **NativeBase**: cross-platform; utility-style props; heavier bundle
- **Rule:** Evaluate bundle size impact before adopting any UI library — use `react-native-bundle-visualizer`

### Absolute Imports Configuration
```json
// tsconfig.json (paths)
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@components/*": ["src/components/*"],
      "@screens/*": ["src/screens/*"],
      "@hooks/*": ["src/hooks/*"]
    }
  }
}
```
Also requires `babel-plugin-module-resolver` in `babel.config.js`:
```js
plugins: [
  ['module-resolver', {
    root: ['./src'],
    alias: { '@components': './src/components' }
  }]
]
```

### Flipper [2022]
- Desktop debugging tool for RN; plugin ecosystem (network inspector, layout inspector, Redux DevTools)
- Network plugin: inspect HTTP requests without proxy setup
- React DevTools: integrated component tree + hooks inspector
- **Note [2022]:** Meta deprecated Flipper as default RN debugger post-0.73; check current debugging toolchain

---

## Ch 10: Structuring Large-Scale, Multi-Platform Projects

### 4-File Component Split Pattern
Every non-trivial component is split into:
```
/components/Button/
  index.tsx         — exports; may contain logic/hooks
  Button.view.tsx   — pure presentational JSX only; no business logic
  Button.styles.tsx — StyleSheet definitions only
  Button.types.tsx  — TypeScript interfaces for props and internal types
```
- **Rule:** `.view.tsx` files must be pure — no hooks except `useStyles`, no API calls, no state
- **Rule:** `.styles.tsx` exports only `StyleSheet.create({})` result and any dynamic style functions
- Benefit: testability (view is snapshot-testable without mocking logic), readability, parallel development

### Feature-Grouped Project Architecture
```
/src
  /features
    /auth
      /components
      /screens
      /hooks
      /store
      /services
    /profile
      /components
      /screens
      ...
  /shared
    /components   — app-wide reusable components
    /hooks        — app-wide hooks
    /utils        — pure utilities
    /services     — global API clients
  /navigation     — root navigator + type definitions
```
- **Rule:** Feature modules must not import from other feature modules directly — go through `shared/` or navigation params
- Barrel files (`index.ts`): expose public API of each feature; internal structure is hidden

### react-native-web for Web Target
- Library: `react-native-web` + Webpack
- Aliases in Webpack config:
  ```js
  resolve: {
    alias: {
      'react-native': 'react-native-web',
    },
    extensions: ['.web.tsx', '.web.ts', '.web.js', '.tsx', '.ts', '.js'],
  }
  ```
- Platform file resolution order: `.web.tsx` → `.tsx` (platform-specific files override automatically)
- **Rule:** Test web build in CI — RN web-incompatible APIs (`PanResponder`, some Animated features) fail silently at runtime
- Unsupported: all native modules without web implementations

### Yarn Workspaces Monorepo
```
/packages
  /mobile         — React Native app
  /web            — react-native-web app
  /shared         — shared components, utilities, types
/package.json     — workspace root with `workspaces: ["packages/*"]`
```
- Hoists shared dependencies to root `node_modules`
- `nohoist`: packages requiring native linking must be nohoisted
  ```json
  "nohoist": ["**/react-native", "**/react-native/**"]
  ```
- Build shared package changes propagate to consumers without publish

### react-native-builder-bob (Library Creation)
- Scaffolds native module or component library with correct project structure
- Outputs: CJS, ESM, TypeScript declarations
- Peer dependency model: `react` and `react-native` are peerDependencies, not dependencies
- **Rule:** Library code must not include `StyleSheet.create()` references to device-specific values — consumers own their styles

---

## Ch 11: Creating and Automating Workflows

### Git Branching Strategy
- Feature branch workflow: `feature/<ticket-id>-description`
- **Rule:** Never commit directly to `main`/`master` — all changes via PR
- Branch protection rules on `main`: require PR review, require status checks to pass
- Commit message convention: `<type>(<scope>): <description>` (Conventional Commits)
  - Types: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`, `perf`
- Squash merge: keeps main history linear; preserve individual commits for complex features

### GitHub Actions CI Pattern
```yaml
name: CI
on:
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '16'
          cache: 'yarn'
      - run: yarn install --frozen-lockfile
      - run: yarn prettier --check .
      - run: yarn lint
      - run: yarn test --ci --coverage
```
- `--frozen-lockfile`: prevents lockfile drift in CI
- `cache: 'yarn'`: caches `node_modules` by lockfile hash — saves 1-3 minutes per run
- `--ci` flag on Jest: fails on snapshot updates (prevents accidental snapshot commits)

### CI Caching Strategy
- Cache key: hash of lockfile (`${{ hashFiles('**/yarn.lock') }}`)
- Restore keys: fallback to most recent cache if exact match misses
- Cache invalidation: automatic when lockfile changes
- Native dependency caching (CocoaPods):
  ```yaml
  - uses: actions/cache@v3
    with:
      path: ios/Pods
      key: ${{ runner.os }}-pods-${{ hashFiles('**/Podfile.lock') }}
  ```
- Gradle caching: `~/.gradle/caches` and `~/.gradle/wrapper`

### Parallelization Pattern
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [checkout, setup-node, yarn lint]
  test:
    runs-on: ubuntu-latest
    steps: [checkout, setup-node, yarn test]
  type-check:
    runs-on: ubuntu-latest
    steps: [checkout, setup-node, yarn tsc --noEmit]
```
- Run independent jobs in parallel — reduces CI wall time by 40-60% for typical RN projects
- `needs: [lint, test]` to gate build jobs on passing checks

### iOS deploy automation
- Ruby-based automation for iOS/Android builds, signing, deployment
- `Fastfile` defines lanes:
  ```ruby
  lane :beta do
    build_app(scheme: "MyApp")
    upload_to_testflight
  end
  ```
- `match`: manages certificates and provisioning profiles in a shared Git repo (encrypted)
- `supply`: uploads Android builds to Play Store
- **Rule:** Never store certificates in the app repo — use `match` with a separate private repo

### Bitrise (CI Platform) [2022]
- Mobile-first CI with pre-built steps for RN, Xcode, Gradle
- Workflow editor: GUI + YAML; prefer YAML for version control
- `bitrise.yml`: checked into repo for reproducibility
- Cache steps: `cache-push` and `cache-pull` around build steps
- Triggers: PR, push to branch, tag push for release builds

### OTA Updates (CodePush / EAS Update)
- **CodePush** (AppCenter): deploy JS bundle updates without App Store review
  - Applies to: JS code and assets only — no native code changes
  - Mandatory vs optional updates: `installMode: CodePush.InstallMode.IMMEDIATE` vs `ON_NEXT_RESTART`
  - **Constraint:** Cannot update native code (new permissions, new native modules) via OTA
  - **Rule:** OTA is not a substitute for proper release process — use for hotfixes and minor updates only
  - Rollback: AppCenter dashboard allows instant rollback to previous bundle
- **EAS Update** (Expo): Expo-native OTA; requires Expo SDK; incompatible with arbitrary bare projects

---

## Ch 12: Automated Testing for React Native Apps

### Testing Pyramid
1. **Unit tests (Jest):** pure functions, reducers, utilities, hooks in isolation
2. **Component tests (RNTL):** component rendering and interaction
3. **E2E tests (Detox):** full app flows on device/simulator

- **Rule:** Unit tests are cheapest — maximize coverage here first
- Target: 70%+ unit/integration coverage before investing in E2E
- E2E tests are expensive to write and maintain — limit to critical user journeys (login, checkout, core feature)

### Jest Unit Test Patterns
```ts
// Pure function test
describe('calculateTotal', () => {
  it('returns sum of items with tax', () => {
    expect(calculateTotal([10, 20], 0.1)).toBe(33);
  });

  it('returns 0 for empty array', () => {
    expect(calculateTotal([], 0.1)).toBe(0);
  });
});
```
- `describe` groups related tests; `it`/`test` are individual assertions
- **Rule:** One assertion per test where possible — multiple failing assertions obscure root cause
- Mock modules: `jest.mock('module-path')` — auto-mocks all exports
- Manual mocks: `__mocks__/module-path.js` — checked into repo for shared mocks
- `jest.spyOn`: mock specific method while preserving rest of module
- Async tests: `async/await` or return Promise; always use `resolves`/`rejects` matchers:
  ```ts
  await expect(fetchUser(1)).resolves.toEqual({ id: 1, name: 'Test' });
  ```

### React Native Testing Library (RNTL) Patterns
```ts
import { render, fireEvent, screen } from '@testing-library/react-native';

test('button calls onPress when tapped', () => {
  const onPress = jest.fn();
  render(<Button label="Submit" onPress={onPress} />);

  fireEvent.press(screen.getByText('Submit'));

  expect(onPress).toHaveBeenCalledTimes(1);
});
```
- Query priority: `getByRole` > `getByText` > `getByTestId` — test semantics, not implementation
- `getBy*`: throws if not found; `queryBy*`: returns null; `findBy*`: async with retry
- `screen` object (RNTL v7+): replaces destructuring from `render()` return — prefer `screen.getBy*`
- `userEvent` (RNTL v12+): more realistic event simulation than `fireEvent`
- **Rule:** Avoid `getByTestId` as primary selector — couples tests to implementation details

### testID Convention
- Add `testID` to interactive and key structural elements only
- Naming: `kebab-case`, feature-prefixed: `auth-login-button`, `profile-avatar`
- **Rule:** Do not add testID to every element — creates maintenance burden

### Detox E2E Patterns
```ts
describe('Login flow', () => {
  beforeAll(async () => {
    await device.launchApp({ newInstance: true });
  });

  it('logs in with valid credentials', async () => {
    await element(by.id('auth-email-input')).typeText('user@test.com');
    await element(by.id('auth-password-input')).typeText('password123');
    await element(by.id('auth-login-button')).tap();
    await expect(element(by.id('home-screen'))).toBeVisible();
  });
});
```
- `device.launchApp({ newInstance: true })`: cold start; use `{ delete: true }` to clear app state
- `by.id()`: matches `testID` prop
- `by.text()`: matches visible text
- `waitFor(element).toBeVisible().withTimeout(5000)`: async wait with timeout
- **Rule:** E2E tests must run against a real device build — simulator-only tests miss platform-specific bugs
- Detox config in `package.json` or `.detoxrc.js`: defines device configs (iOS simulator, Android emulator)

### Snapshot Testing
- `toMatchSnapshot()`: captures rendered output; fails on any change
- **Rule:** Snapshot tests are low-value for dynamic components — use for static/presentational components only
- Update snapshots: `jest --updateSnapshot` — must code-review snapshot diffs; never auto-approve
- Inline snapshots: `toMatchInlineSnapshot()` — snapshot stored in test file; easier to review

---

## Ch 13: Tips and Outlook

### OTA Update Constraints (repeat + expand)
- CodePush updates: JS bundle + assets only
- Blocked from OTA: changes to `android/` or `ios/` native code, new native module linking, new permissions in manifests, new capabilities in entitlements
- **Rule:** Any PR touching `android/` or `ios/` requires a full app store release, not OTA
- Apple App Store: OTA updates must not change core app functionality (App Store Review Guidelines 3.3.2)

### Error Monitoring
- **Bugsnag** or **Sentry**: required for production RN apps
- Sentry RN SDK: `@sentry/react-native`
  ```ts
  Sentry.init({
    dsn: 'your-dsn',
    environment: __DEV__ ? 'development' : 'production',
    tracesSampleRate: 0.2, // 20% performance tracing
  });
  ```
- Sourcemaps: upload to Sentry in CI so stack traces map to source, not minified bundle
- **Rule:** Ship with error monitoring from day one — silent crashes in production are unacceptable
- Breadcrumbs: automatically captured (navigation, console.log, network); add custom breadcrumbs for key user actions

### A/B Testing in RN
- Firebase Remote Config: feature flags + A/B test cohort assignment; free tier sufficient for most apps
- LaunchDarkly: more sophisticated flag management; paid
- **Rule:** Feature flag all significant changes before full rollout — enables instant kill switch
- **Anti-pattern:** A/B test logic embedded in components — isolate in a service layer

### Clean Code Rules for RN
- Function length: max 20-30 lines — extract to named helper if longer
- Component length: max 150-200 lines — split into subcomponents if larger
- Prop drilling beyond 2 levels: extract to Context or state management
- Magic numbers: extract to named constants (`const MAX_RETRY_COUNT = 3`)
- Comments: explain WHY, not WHAT — code explains what; intent needs documentation
- **Rule:** Dead code must be deleted, not commented out — version control is the history

### Performance Anti-Patterns
- `FlatList` with `keyExtractor` returning index: prevents proper re-render optimization — use stable IDs
- Anonymous functions in JSX: `onPress={() => handler(id)}` creates new reference per render; use `useCallback` for expensive children
- Large lists without `getItemLayout`: VirtualizedList cannot skip layout calculations — implement for fixed-height items
- `ScrollView` for long lists: renders all items at once — always use `FlatList`/`SectionList` for dynamic content
- Image caching: `Image` component caches on Android; iOS uses NSURLCache; `react-native-fast-image` for consistent cross-platform caching with priority control
- **Rule:** Profile before optimizing — use React DevTools Profiler and Flipper Performance plugin to identify actual bottlenecks

### New Architecture Migration Path [2022 state]
- Enable in `android/gradle.properties`: `newArchEnabled=true`
- Enable in iOS: `RCT_NEW_ARCH_ENABLED=1` in Podfile
- Interop layer: allows old arch libraries to run on new arch without full migration
- **Blocking issues:** Libraries using direct UIManager calls, old TurboModule registration
- Timeline: Meta targeting new arch as default in upcoming RN versions (post-0.71)
- **Rule:** Audit all native dependencies for new arch compatibility before enabling

### Release Checklist Items (Extractable)
- [ ] Hermes enabled on both platforms
- [ ] Error monitoring (Sentry/Bugsnag) configured with sourcemap upload
- [ ] API keys not in app bundle
- [ ] Auth tokens stored in Keychain/Keystore only
- [ ] OTA update strategy defined (CodePush or EAS)
- [ ] E2E tests covering login + core user journey
- [ ] `strict: true` TypeScript enabled
- [ ] ESLint + Prettier running in CI
- [ ] Bundle size analyzed (`react-native-bundle-visualizer`)
- [ ] `FlatList` with stable `keyExtractor` for all lists >20 items
- [ ] `useNativeDriver: true` on all Animated animations using supported props
