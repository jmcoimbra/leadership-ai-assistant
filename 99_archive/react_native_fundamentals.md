# React Native Fundamentals

**Purpose:** Raw chapter-by-chapter extraction of enforceable patterns. Narrative discarded. Dated patterns flagged with [2018]. Modern equivalents noted where significant.

## Ch 1: What Is React Native?

- React Native renders to real native views, not WebView. Not a hybrid framework.
- Bridge architecture [2018]: JS thread sends serialized JSON messages to native thread over async bridge. Native thread renders platform UI components.
- "Learn once, write anywhere" -- not "write once, run anywhere." Platform-specific code is expected.
- React Native uses the same React component model as web React. Virtual DOM diffing applies.
- Risk factors acknowledged: dependency on Facebook, platform update lag, native fallback sometimes required.
- Ecosystem: npm for JS packages, Xcode for iOS builds, Android Studio for Android builds.

## Ch 2: Working with React Native

- Components: class-based `extends Component` with `render()` method [2018 -- now functional components + hooks].
- JSX compiles to `React.createElement()` calls. Same as web React.
- Props flow down, state is local. `setState()` triggers re-render [2018 -- now `useState` hook].
- Lifecycle methods: `componentDidMount`, `componentWillUnmount` [2018 -- now `useEffect` hook].
- `AppRegistry.registerComponent()` is the entry point for the app.
- Create React Native App (CRNA) for quick setup [2018 -- now `npx react-native init` or Expo CLI].

## Ch 3: Building Your First Application

- `<View>` = container (like `<div>`). `<Text>` = text display (required -- cannot render raw strings outside `<Text>`).
- `<Image>` requires explicit dimensions. Source: `require('./image.png')` for local, `{uri: 'https://...'}` for remote.
- StyleSheet.create() is mandatory pattern. Not inline style objects. Enables optimization and validation.
- Styles are JS objects with camelCase properties: `backgroundColor`, `fontSize`, `borderWidth`.
- No CSS cascade. No CSS classes. Styles are scoped to the component where applied.
- Multiple styles via array: `style={[styles.base, styles.active]}`. Last one wins on conflicts.

## Ch 4: Components, Styles, and Layout

- Flexbox is the layout system. Default `flexDirection: 'column'` (unlike web's `row`).
- `justifyContent`: main axis alignment. `alignItems`: cross axis alignment. `flex: 1` fills available space.
- `<FlatList>`: performant scrolling list. Requires `data`, `renderItem`, `keyExtractor`. Renders only visible items.
- `<SectionList>`: grouped list with section headers. Requires `sections`, `renderItem`, `renderSectionHeader`.
- `<ScrollView>`: renders all children at once. Only for small, bounded content. `<FlatList>` for large lists.
- Touch handlers: `<Button>` (simplest), `<TouchableHighlight>` (visual feedback), `<TouchableOpacity>` (opacity change) [2018 -- now `<Pressable>` preferred].
- PanResponder: gesture system for drag/swipe. Claim protocol: `onStartShouldSetPanResponder`, `onMoveShouldSetPanResponder`. Returns `gestureState` with `dx`, `dy`, `vx`, `vy`.
- Gesture negotiation: parent and child can both claim touch. PanResponder grant/release system resolves conflicts.

## Ch 5: Platform APIs

- Geolocation: `navigator.geolocation.getCurrentPosition(success, error, options)`. MDN-based polyfill [2018 -- now `@react-native-community/geolocation` community package].
- `watchPosition` for continuous tracking. `clearWatch(watchID)` to stop.
- CameraRoll: `CameraRoll.getPhotos({first: 25})` [2018 -- now `@react-native-camera-roll/camera-roll`].
- AsyncStorage: key-value string storage. `AsyncStorage.setItem(key, value)`, `getItem(key)`. Always async (returns Promise) [2018 -- now `@react-native-async-storage/async-storage`].
- Network: `fetch(url)` -- same API as web. Also `XMLHttpRequest` polyfill. `FormData` for multipart uploads.
- Permissions: iOS requires `Info.plist` entries (NSLocationWhenInUseUsageDescription, NSCameraUsageDescription). Android requires `AndroidManifest.xml` permissions.

## Ch 6: Platform APIs (Deep Dive)

- SmarterWeather app: combines Geolocation + forecast API + photo backgrounds.
- Image upload pattern: FormData with {uri, type, name} object, POST via fetch.
- Error handling for platform APIs: always handle denial/failure cases. Geolocation can timeout, be denied.
- Photo picker integration with camera roll for background selection.

## Ch 7: Modules and Native Code

- **iOS native module:** Objective-C class conforming to `<RCTBridgeModule>`. `RCT_EXPORT_MODULE()` macro registers it. `RCT_EXPORT_METHOD(methodName:(args))` exposes methods to JS.
- **Android native module:** Java class extending `ReactContextBaseJavaModule`. `@ReactMethod` annotation on public methods. Register in `ReactPackage.createNativeModules()`.
- **Native UI components (iOS):** Subclass `RCTViewManager`. Override `-(UIView *)view` to return native view. `RCT_EXPORT_VIEW_PROPERTY` for prop bridging.
- **Native UI components (Android):** Extend `SimpleViewManager<View>`. Override `createViewInstance()`. `@ReactProp` annotation for prop bridging.
- Third-party native modules: `react-native link <package>` for auto-linking [2018 -- auto-linking is now default in RN 0.60+, no manual linking needed].
- `react-native-video` walkthrough: demonstrates wrapping native video player for both platforms.
- Cross-platform native modules: `index.ios.js` / `index.android.js` for platform-specific JS entry [2018 -- now single `index.js` with platform file extensions only where needed].
- [Modern: TurboModules replace the async bridge with synchronous JSI calls. Codegen from TypeScript specs. C++ shared native modules possible.]

## Ch 8: Platform-Specific Code

- **File extensions:** `.ios.js` / `.android.js`. Metro bundler resolves automatically. `MyComponent.ios.js` and `MyComponent.android.js` share the same import: `import MyComponent from './MyComponent'`.
- **Platform module:** `Platform.OS` returns `'ios'` or `'android'`. `Platform.Version` returns OS version number.
- `Platform.select({ios: value, android: value})` for inline platform branching.
- Platform-specific components [2018]: `<TabBarIOS>`, `<ToolbarAndroid>`, `<DatePickerIOS>`, `<ProgressBarAndroid>` [All removed in modern RN. Use cross-platform alternatives from react-navigation or community].
- When to use platform-specific code: different UX conventions (iOS back swipe vs Android back button), platform-specific APIs, performance optimizations.

## Ch 9: Debugging and Developer Tools

- **Developer menu:** Shake device (or Cmd+D iOS sim, Cmd+M Android emu). Options: Reload, Debug JS Remotely, Hot Reloading, Inspector.
- **Chrome DevTools:** "Debug JS Remotely" opens Chrome tab. Full breakpoint debugging, console, network inspection. JS runs in Chrome's V8 during debug [2018 -- now Hermes debugger via Chrome DevTools, no remote debugging needed].
- **React DevTools:** Standalone electron app. Component tree, props/state inspection, search. Install: `npm install -g react-devtools` then `react-devtools`.
- **Red Screen of Death:** Unhandled JS exceptions in development. Shows stack trace. Tap to dismiss. Not shown in production builds.
- **Yellow Box:** Warnings in development. `console.warn()` triggers yellow box. Can be suppressed per-warning.
- **iOS debugging:** Xcode console for native logs. Instruments for profiling. Breakpoints in native code.
- **Android debugging:** `adb logcat *:S ReactNative:V ReactNativeJS:V` for filtered logs.
- **Performance:** Use production builds for profiling. Dev mode adds significant overhead (type checking, warnings).
- [Modern: Flipper was the recommended debugger 2019-2023, now deprecated. React Native DevTools (built-in) replacing it.]

## Ch 10: Navigation and App Structure

- **react-navigation library** [2018: v1/v2 API with factory functions]:
  - `StackNavigator({ScreenName: {screen: Component}})` [2018 -- now `createNativeStackNavigator()`]
  - `TabNavigator({...})` [2018 -- now `createBottomTabNavigator()`]
  - `DrawerNavigator({...})` [2018 -- now `createDrawerNavigator()`]
- Navigation patterns: Stack (push/pop screens), Tabs (bottom/top bar), Drawer (side menu).
- `navigation.navigate('ScreenName', {params})` for screen transitions. `navigation.goBack()` to pop.
- Screen params: `this.props.navigation.state.params` [2018 -- now `route.params` via `useRoute()` hook].
- **Flashcard app architecture:**
  - `components/` -- presentational components
  - `data/` -- data models and storage
  - `styles/` -- shared style constants
- Nested navigators: Stack inside Tab, Drawer wrapping Stack. Compose navigation hierarchies.
- [Modern: react-navigation v6/v7 uses `<NavigationContainer>`, hook-based API (`useNavigation()`, `useRoute()`), typed routes with TypeScript, deep linking configuration.]

## Ch 11: State Management with Redux

- **Problem:** Complex apps need shared state across screens. Props drilling breaks down.
- **Redux architecture:** Single store, actions describe events, reducers return new state. Unidirectional data flow.
- **Action types:** String constants in dedicated file. `const ADD_CARD = 'ADD_CARD'`.
- **Action creators:** Functions returning action objects: `{type: ADD_CARD, payload: {...}}`.
- **Reducers:** Pure functions `(state, action) => newState`. Use spread operator for immutable updates. Never mutate state.
- **Store:** `createStore(rootReducer)`. Single source of truth.
- **React-Redux bindings [2018]:** `<Provider store={store}>` wraps app. `connect(mapStateToProps, mapDispatchToProps)(Component)` [2018 -- now `useSelector()` and `useDispatch()` hooks].
- `mapStateToProps`: derives component props from store state. `mapDispatchToProps`: binds action creators.
- **Persistence:** AsyncStorage + Redux middleware. `LOAD_DATA` action on app start to hydrate store from AsyncStorage.
- `combineReducers({deck: deckReducer, card: cardReducer})` for modular state slices.
- [Modern: Redux Toolkit (`createSlice`, `configureStore`) replaces manual boilerplate. Alternatives: Zustand, Jotai, React Query for server state.]

## Ch 12: Conclusion

- Summary chapter. No enforceable rules.
- Key journey: Hello World -> styled components -> platform APIs -> native modules -> navigation -> state management -> deployment.
- Community resources: Stack Overflow, GitHub issues, reactnative.dev.

## Appendix A: Modern JavaScript Syntax

- `let` (block-scoped, reassignable) and `const` (block-scoped, not reassignable) replace `var`.
- ES6 module syntax: `import X from './module'`, `export default X`. Replaces CommonJS `require`/`module.exports`.
- Destructuring: `const {a, b} = obj` and `import React, {Component} from 'react'`.
- Arrow functions: `(val) => { ... }`. Auto-binds `this` (no `.bind(this)` needed).
- Template literals: `` `Hello ${name}` ``.
- Default parameters: `function greet(name = 'World') {}`.
- Promises: `.then().catch()` chaining replaces callback nesting. Cleaner async flow.

## Appendix B: Deploying Your Application

- **iOS deployment:** Xcode Archive -> App Store Connect -> TestFlight (beta) -> App Review -> Release.
- **Android deployment:** Keystore signing -> `./gradlew assembleRelease` -> Play Console -> Internal/Closed Testing -> Review -> Release.
- Asset checklist: app icons (all required sizes), launch screens, promotional screenshots.
- Review times: 1 day to 2 weeks. Plan for it. Expedited review for critical bugs (use sparingly).
- Post-release: mobile versions have longer lifespan than web deploys. Many users don't auto-update.

## Appendix C: Working with Expo

- Expo: write RN apps without Xcode/Android Studio. Great for learning and prototyping.
- Create React Native App (CRNA) projects are Expo projects [2018].
- **Eject:** One-way migration from Expo to full RN project. Required for: custom native code, third-party modules needing `react-native link`, full build control.
- [Modern: Expo has evolved dramatically. Expo Dev Builds replace eject for most cases. EAS (Expo Application Services) handles builds and submissions. Expo Router for file-based navigation. Expo SDK covers most native APIs without ejecting.]
