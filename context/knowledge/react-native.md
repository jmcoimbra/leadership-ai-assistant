# React Native Patterns

**Added:** 2026-04-02
**Last Updated:** 2026-04-18

## Repo Routing (Read First)

- `[your-org]-mobile-app` = **active** RN app. Default branch `master`. All branded merchant apps ship from here. Current release baseline: `release-v48.0.0` (RN 0.77.3, Firebase 23.8.4, Sentry 7.8.0, Datadog 3.0.0, LaunchDarkly 7.2.0), shipped 2026-04-17.
- `[your-org]-mobile` = **legacy**. Last push 2025-10-27. Do not patch. Not wired into the current release pipeline.
- Any RN / mobile / signing-key / Play Console question routes to `[your-org]-mobile-app` unless explicitly archival.
- Compliance tracks (16 KB page size, iOS SDK 26, Android developer verification): see `ios-deploy-patterns.md`.
**Sources:**

Distilled for understanding [your-org]-mobile-app codebase and mobile development context. Dated patterns flagged with year; modern equivalents noted.

## Architecture & Bridge

- React Native renders real native views (UIView on iOS, android.view.View on Android). Not a WebView/hybrid.
- [2018] **Old bridge:** JS thread and native thread communicate via async serialized JSON messages. Batched for performance. All data crossing the bridge is serialized/deserialized.
- [Modern] **New Architecture (RN 0.68+):** JSI (JavaScript Interface) replaces the bridge with direct JS-to-C++ function calls. No serialization overhead. Three pillars:
  - **JSI:** Shared C++ layer. JS can hold references to C++ host objects directly.
  - **TurboModules:** Lazy-loaded native modules. Only initialized when first accessed (vs old bridge loading all at startup).
  - **Fabric:** New rendering system. Synchronous layout computation. Concurrent features support.
- **Hermes:** Default JS engine since RN 0.70 (replaces JavaScriptCore on Android). Bytecode precompilation for faster startup. Built-in debugger.
  - Benchmarks (Android): TTI -53%, app size -46%, memory -26% vs JavaScriptCore.
  - Hermes compiles JS to bytecode at build time (not runtime). `.hbc` files in APK/IPA.
- **Metro bundler:** Transforms JSX, resolves platform extensions (`.ios.js`/`.android.js`), tree-shakes, serves hot module replacement in dev. Config: `metro.config.js`.
- Entry point: `AppRegistry.registerComponent('AppName', () => App)`.

## Core Components & Layout

- `<View>` = container (like `<div>`). All layout and visual nesting.
- `<Text>` = text display. Raw strings MUST be inside `<Text>`. Nested `<Text>` inherits parent styles.
- `<Image>` requires explicit dimensions. Local: `require('./img.png')`. Remote: `{uri: 'https://...'}`.
- `<ScrollView>` renders ALL children. Only for small bounded content.
- `<FlatList>` for large lists. Virtualizes off-screen items. Required props: `data`, `renderItem`, `keyExtractor`.
  - **`extraData` prop required for external state.** FlatList is a PureComponent; won't re-render when state outside `data` prop changes.
  - Pull-to-refresh: `onRefresh` callback + `refreshing` boolean prop. [React and React Native 4e]
- `<SectionList>` for grouped data with headers. Required: `sections`, `renderItem`, `renderSectionHeader`.
- **StyleSheet.create():** Always use. Not inline objects. Enables validation, deduplication, and bridge optimization.
- Styles are JS objects with camelCase: `backgroundColor`, `fontSize`, `borderWidth`. No CSS cascade, no CSS classes.
- Multiple styles via array: `style={[styles.base, styles.active]}`. Last value wins on conflict.
- **Flexbox defaults differ from web:** `flexDirection: 'column'` (web default is `row`). `alignItems: 'stretch'`.
- `flex: 1` fills available space. `justifyContent` for main axis. `alignItems` for cross axis.
- **Responsive design:** `Dimensions.get('window')` for static, `useWindowDimensions()` hook for reactive. `PixelRatio` for density-aware sizing.
- **Platform shadow divergence:** iOS uses `shadowColor`/`shadowOffset`/`shadowOpacity`/`shadowRadius`. Android uses `elevation` (single prop).

## Touch & Gestures

- [2018] `<TouchableHighlight>`, `<TouchableOpacity>`, `<TouchableWithoutFeedback>`.
- [Modern] **`<Pressable>`** replaces all Touchable variants. Supports `onPressIn`, `onPressOut`, `onLongPress`, `style` as function of pressed state.
- `<Button>` for simplest cases (platform-styled, limited customization).
- **PanResponder** for custom gestures (drag, swipe, pinch):
  - Claim protocol: `onStartShouldSetPanResponder`, `onMoveShouldSetPanResponder` return true/false.
  - `gestureState` provides: `dx`, `dy` (distance), `vx`, `vy` (velocity), `numberActiveTouches`.
  - Parent/child gesture negotiation via grant/release system.
- [Modern] **React Native Gesture Handler:** `Gesture.Pan()`, `Gesture.Pinch()`, `Gesture.Simultaneous()` for composition. Runs on native thread. Pair with Reanimated 2 for 60fps custom gestures. [React and React Native 4e]

## Animations

- **Animated API (built-in):**
  - `Animated.Value` for single values, `Animated.ValueXY` for 2D.
  - `Animated.timing()` (duration-based), `Animated.spring()` (physics), `Animated.decay()` (momentum).
  - Composition: `Animated.parallel()`, `Animated.sequence()`, `Animated.stagger()`.
  - `useNativeDriver: true` offloads to native thread. **Limited to transform and opacity only.** Layout props (width, height, top, left) must run on JS thread. [Professional React Native, React Native in Action]
  - Interpolation: `animatedValue.interpolate({inputRange: [0, 1], outputRange: ['0deg', '360deg']})`.

- [Modern] **Reanimated 2:**
  - Worklet-based: animations run on UI thread via `'worklet'` directive. 60fps guaranteed.
  - `useSharedValue(initial)`: value shared between JS and UI threads.
  - `useAnimatedStyle(() => ({...}))`: style computed on UI thread.
  - `withTiming(target, config)`, `withSpring(target, config)`, `withSequence(...)`, `withRepeat(...)`.
  - **Layout animations:** `entering={FadeIn}`, `exiting={FadeOut}` props on `Animated.View` for automatic enter/exit transitions. [React and React Native 4e]
  -

- **Lottie:** `lottie-react-native` for After Effects JSON animations. `<LottieView source={require('./anim.json')} autoPlay loop />`.

## Platform APIs

- **AsyncStorage** [2018: `react-native` core. Modern: `@react-native-async-storage/async-storage`]:
  - Key-value string storage. `setItem(key, value)`, `getItem(key)`. Always async (returns Promise).
  - For complex data: `JSON.stringify()` on write, `JSON.parse()` on read.
- **Geolocation** [2018: `navigator.geolocation` polyfill. Modern: `@react-native-community/geolocation`]:
  - `getCurrentPosition(success, error, options)`, `watchPosition()`, `clearWatch(id)`.
- **CameraRoll** [2018: core. Modern: `@react-native-camera-roll/camera-roll`].
- **Network:** `fetch(url)` same as web. `XMLHttpRequest` polyfill available. `FormData` for multipart uploads.
  - **`fetch()` only rejects on network failure.** HTTP 4xx/5xx resolve successfully. Always check `response.ok` or `response.status`. This is the #1 networking bug pattern. [React Native in Action, Professional React Native]
- **GraphQL/Apollo Client:** `ApolloProvider` wrmobile-team app, `useQuery(QUERY)` for reads, `useMutation(MUTATION)` for writes. `InMemoryCache` for client-side caching. `refetchQueries` after mutations. [React and React Native 4e]
- **Offline sync:** `@react-native-community/netinfo` for connectivity detection. Queue mutations while offline, replay on reconnect. [React and React Native 4e]
- **Permissions:** iOS: `Info.plist` usage description strings. Android: `AndroidManifest.xml` permission declarations. [Modern: `react-native-permissions` library for unified API.]
- **AppState:** `active`, `background`, `inactive`. `AppState.addEventListener('change', handler)` for lifecycle monitoring.
- **Keyboard:** `Keyboard.dismiss()`. `<KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>`. iOS uses padding, Android uses height.
- **BackHandler (Android only):** `BackHandler.addEventListener('hardwareBackPress', handler)`. Return `true` to prevent default back. Essential for modals, custom navigation.
- **PermissionsAndroid:** `PermissionsAndroid.request(permission)` returns `GRANTED`/`DENIED`/`NEVER_ASK_AGAIN`. Runtime permission flow required for Android 6+.
- Pattern: core APIs extracted to community packages after RN 0.60. Check `@react-native-community/*` and `@react-native-*` scopes.

## Storage

- **AsyncStorage** (`@react-native-async-storage/async-storage`): Key-value string store. Non-sensitive data. Simple but slow for large datasets.
- **MMKV** (`react-native-mmkv`): 30x faster than AsyncStorage via JSI. Same key-value API. Use for performance-critical or frequent read/write.
- **SQLite** (`react-native-sqlite-storage`): Full SQL queries. Use for complex data relationships, offline-first with sync.
- **Secure Store** (`expo-secure-store` or `react-native-keychain`): Keychain (iOS) / Keystore (Android). Sensitive data only (tokens, credentials).
- **Decision matrix:** Simple key-value → MMKV. Complex queries → SQLite. Sensitive → Secure Store. Legacy → AsyncStorage.

## Native Modules

- **iOS (Objective-C):**
  - Class conforming to `<RCTBridgeModule>` protocol.
  - `RCT_EXPORT_MODULE()` macro registers the module.
  - `RCT_EXPORT_METHOD(methodName:(NSString *)arg)` exposes methods to JS.
  - `RCT_EXPORT_VIEW_PROPERTY(propName, type)` for native UI component props.

- **Android (Java):**
  - Class extending `ReactContextBaseJavaModule`.
  - `@ReactMethod` annotation on public methods.
  - Register in `ReactPackage.createNativeModules()`.
  - `@ReactProp(name = "propName")` for native UI component props.

- **Native UI Components:**
  - iOS: Subclass `RCTViewManager`, override `-(UIView *)view`.
  - Android: Extend `SimpleViewManager<View>`, override `createViewInstance()`.

- [Modern] **TurboModules:** TypeScript spec file generates native bindings via codegen. Synchronous calls via JSI. Lazy initialization. C++ shared modules for cross-platform native code.

- Auto-linking (RN 0.60+): no manual `react-native link` needed. `pod install` for iOS, Gradle auto-detects for Android.

## Platform-Specific Code

- **File extensions:** `.ios.js` / `.android.js` (also `.ios.tsx` / `.android.tsx`). Metro bundler resolves automatically. Same import path: `import Foo from './Foo'` resolves to `Foo.ios.js` on iOS.
- **Platform module:**
  - `Platform.OS`: returns `'ios'` or `'android'`.
  - `Platform.Version`: OS version number (iOS: string like `'16.0'`, Android: API level number).
  - `Platform.select({ios: value, android: value, default: value})`: inline branching.
- [2018] Platform-specific components (`TabBarIOS`, `ToolbarAndroid`, `DatePickerIOS`, `ProgressBarAndroid`) all removed in modern RN. Use react-navigation tabs, community date pickers.
- [2018] `index.ios.js` / `index.android.js` entry points. [Modern: single `index.js` entry point.]

## Navigation

- [2018] **react-navigation v1/v2:** Factory functions `StackNavigator()`, `TabNavigator()`, `DrawerNavigator()`.
- [Modern] **react-navigation v6/v7:**
  - `<NavigationContainer>` wrmobile-team app.
  - `createNativeStackNavigator()`, `createBottomTabNavigator()`, `createDrawerNavigator()`.
  - Hook-based: `useNavigation()`, `useRoute()`, `useFocusEffect()`.
  - Typed routes with TypeScript (`RootStackParamList`).
  - Deep linking via `linking` prop on NavigationContainer.
- **Navigation patterns (unchanged):**
  - Stack: push/pop screens. Back button pops.
  - Tabs: bottom/top bar. Each tab can contain its own stack.
  - Drawer: side menu. Often wrmobile-team a tab navigator.
  - Nested navigators: Stack-in-Tab, Drawer-wrapping-Tabs common patterns.
- Screen params: `navigation.navigate('Screen', {id: 123})`. Access via `route.params.id`.

## State Management

- [2018] **Redux with `connect` HOC:**
  - `<Provider store={store}>` wrmobile-team app.
  - `connect(mapStateToProps, mapDispatchToProps)(Component)` binds store to component.
  - Action types as string constants. Action creators return `{type, payload}`.
  - Reducers: pure functions `(state, action) => newState`. Immutable updates via spread.
  - `combineReducers()` for modular state slices.

- [Modern] **Redux Toolkit (RTK):**
  - `createSlice()` replaces manual action types + creators + reducer.
  - `configureStore()` replaces `createStore()`.
  - `useSelector(state => state.slice.field)` replaces `mapStateToProps`.
  - `useDispatch()` replaces `mapDispatchToProps`.
  - RTK Query for API caching.

- [Modern] **Context + useReducer:**
  - Redux-like without external deps. `createContext` + `useContext` + `useReducer`.
  - Split contexts by domain (AuthContext, ThemeContext, DataContext). Compose providers.
  - Good for moderate complexity apps. No devtools, no middleware. [React and React Native 4e]

- [Modern] **Zustand:**
  - Minimal API: `create((set) => ({count: 0, increment: () => set(state => ({count: state.count + 1}))}))`.
  - No providers needed. Selectors for render optimization: `useStore(state => state.count)`.
  - Recommended for most apps. Simpler than Redux, more capable than Context.

- **Decision matrix:** Simple local state → `useState`. Moderate shared state → Context+useReducer or Zustand. Complex with middleware/devtools → Redux Toolkit. Server state → TanStack Query.

- **Persistence pattern:** AsyncStorage/MMKV middleware. Serialize state on change, hydrate on app start. `redux-persist` for Redux. Zustand has built-in `persist` middleware.

## React 18 Features (applicable to RN)

- **Automatic batching:** Multiple `setState` calls in event handlers, timeouts, promises are batched into a single re-render. Previously only batched in React event handlers. [React and React Native 4e]
- **`startTransition`:** Mark non-urgent state updates. UI stays responsive during heavy renders. Wrap in `startTransition(() => setState(newValue))`.
- **Suspense:** `<Suspense fallback={<Loading />}>` for async component boundaries. Data fetching integration with compatible libraries.

## Testing

- **Jest + react-native-testing-library (RNTL):** Unit and component tests. Query by `getByText`, `getByTestId`, `getByRole`. `fireEvent.press()`, `fireEvent.changeText()`. `waitFor()` for async assertions.
- **Detox (E2E):** `element(by.id('submit-btn'))`, `expect(element(by.id('list'))).toBeVisible()`, `element(by.id('input')).typeText('hello')`. Gray-box testing: knows when app is idle.
- **Appium + AWS Device Farm:** Real-device cloud testing. Cross-platform test scripts. Slower but catches device-specific bugs.
- **Storybook React Native:** Component development in isolation. Visual regression testing. `.stories.tsx` files alongside components.
- **Snmobile-teamhot testing:** `expect(tree).toMatchSnmobile-teamhot()`. Detects unintended UI regressions. [React and React Native 4e]

## Large-Scale Project Structure

- **Feature-grouped architecture:** `src/features/<name>/` containing components, screens, hooks, services, types. Co-locate related code.
- **4-file component split:** `index.ts` (barrel export), `View.tsx` (JSX), `styles.ts` (StyleSheet), `types.ts` (interfaces). Scales beyond 100+ components.
- **Barrel exports:** `index.ts` re-exports public API. Absolute imports via `tsconfig.json` paths: `import { Button } from '@/components'`.
- **Monorepo:** Yarn workspaces for shared packages. `react-native-web` for web target from same codebase.
- **TypeScript strict mode:** Mandatory for large projects. Interface > type for component props. `as const` for immutable objects. Discriminated unions for state machines.

## CI/CD

- **iOS deploy automation:** `ios-deploy ios beta`, `ios-deploy android beta`. Match for iOS cert management. Automates build, signing, store upload.
- **GitHub Actions:** Lint + type-check + test on PR. iOS deploy automation deploy on main merge.
- **Husky:** Pre-commit hooks for lint-staged. ESLint + Prettier enforced before commits.
- [[your-org]-mobile-app: See `context/knowledge/ios-deploy-patterns.md` for [Your Company]-specific iOS deploy automation setup.]

## Debugging

- **Developer menu:** Shake device, or Cmd+D (iOS sim), Cmd+M (Android emu).
- **Console:** `console.log()`, `console.warn()` (yellow box), `console.error()` (red screen in dev).
- [2018] Chrome DevTools remote debugging (JS runs in Chrome V8). [Modern: Hermes debugger via Chrome DevTools directly. JS runs in Hermes on device.]
- **React DevTools:** Component tree inspection, props/state, search. `npx react-devtools`.
- **Red Screen of Death:** Unhandled JS exceptions (dev only). Shows stack trace.
- **Yellow Box / LogBox:** Warnings in dev. [Modern: LogBox replaces YellowBox. `LogBox.ignoreLogs(['pattern'])` to suppress.]
- **iOS native debugging:** Xcode console, Instruments profiler, native breakpoints.
- **Android native debugging:** `adb logcat *:S ReactNative:V ReactNativeJS:V`.
- **Performance rule:** Always profile on production builds. Dev mode adds 2-5x overhead (type checking, warnings, bridge logging).
- [2018] Flipper was recommended 2019-2023, now deprecated. React Native DevTools (built-in) replacing it.

## Deployment

- **iOS:** Xcode Archive -> App Store Connect -> TestFlight (beta) -> App Review (1 day to 2 weeks) -> Release.
- **Android:** Keystore signing -> `./gradlew assembleRelease` -> Play Console -> Internal/Closed Testing -> Review -> Release.
- Asset checklist: app icons (all required sizes/resolutions per device), launch screens, promotional screenshots.
- Post-release: mobile versions have longer lifespan than web. Many users don't auto-update. Every version counts.
- **Expo deployment [Modern]:** EAS Build for cloud builds. EAS Submit for store submission. OTA updates via `expo-updates` (JS-only changes without store review).
- [[your-org]-mobile-app: iOS deploy automation automates build + deploy. See `context/knowledge/ios-deploy-patterns.md`.]

## Component Libraries

- **NativeBase:** `Box`, `Button`, `Input`, `VStack`/`HStack`, `useTheme`. Theme customization via `extendTheme()`. Design tokens for consistency. Cross-platform (iOS, Android, web). [React and React Native 4e]

## Critical Delta: 2018 vs Modern React Native

| 2018 Pattern | Modern Equivalent | Impact |
|-------------|-------------------|--------|
| Class components + lifecycle methods | Functional components + hooks (`useState`, `useEffect`, `useRef`, `useMemo`, `useCallback`) | Fundamental paradigm shift |
| Old bridge (async serialized JSON) | New Architecture: JSI + TurboModules + Fabric | Performance, synchronous native calls |
| JavaScriptCore engine | Hermes (default since RN 0.70) | Faster startup, smaller bundle, built-in debugger |
| Core APIs in `react-native` package | Community packages (`@react-native-async-storage/*`, `@react-native-community/*`) | Import paths changed |
| `TouchableHighlight`/`TouchableOpacity` | `Pressable` | API consolidation |
| react-navigation v1/v2 (factory functions) | react-navigation v6/v7 (component + hooks API) | Completely different API surface |
| Redux `connect` HOC | Redux Toolkit + `useSelector`/`useDispatch` hooks | Less boilerplate, hook-based |
| `index.ios.js`/`index.android.js` | Single `index.js` entry point | Simplified entry |
| `react-native link` for native deps | Auto-linking (RN 0.60+) | No manual linking |
| Expo eject (one-way) | Expo Dev Builds + EAS | No ejection needed for most native code |
| Chrome remote JS debugging | Hermes debugger (on-device) | More accurate debugging |
| YellowBox | LogBox | Better warning management |
| Flipper (2019-2023) | React Native DevTools (built-in) | Simplified tooling |
