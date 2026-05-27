# React Patterns

**Purpose:** Raw chapter-by-chapter extraction of enforceable patterns. Narrative discarded. Modern React 18 patterns documented.

---

## Ch 1: Why React?

- React is a UI library only — not a framework. No opinion on routing, data fetching, or server comms.
- Two APIs: React Component API (what to render) + React DOM (how to render to browser).
- Virtual DOM: React diffs new JSX against what's already in the DOM and patches only the delta. Never rebuild entire DOM structure on state change.
- Render target is abstract — same React component code targets web (ReactDOM), mobile (React Native), server (renderToString). Never write platform-specific assumptions into shared components.
- React 18 key changes: (1) automatic state batching anywhere, not just in event handlers; (2) `startTransition()` for priority-based state updates.
- Use `ReactDOM.createRoot()` (not legacy `ReactDOM.render()`) to enable React 18 batching.

---

## Ch 2: Rendering with JSX

- HTML tags in JSX must be lowercase. Custom components must be capitalized. Mixing these up causes compile errors.
- Unknown HTML attributes log warnings at runtime. Validate your prop names.
- Use `{expression}` braces for any JavaScript value — variables, function calls, ternaries, arrays.
- Map collections to JSX elements using `.map()`. Each element in the resulting array requires a unique `key` prop.
- `key` prop must be stable and unique within the list. Do not use array index as key when list order can change.
- Use `<>...</>` fragments (or `<React.Fragment>`) instead of wrapper `<div>` elements when you only need to group siblings. Prevents unnecessary DOM nodes.
- `{this.props.children}` renders nested JSX passed between component tags. Required to make container components work.
- Namespace components with dot notation (`<MyComponent.First />`) when organizing related sub-components under a parent. Assign as class properties: `MyComponent.First = First`.
- JSX compiles to JavaScript — browsers have no native JSX support. Transpilation (Babel/Metro) is mandatory.

---

## Ch 3: Component Properties, State, and Context

- **State** = internal dynamic data of a component. Changes trigger re-render.
- **Props** = external data passed in at render time. Immutable within the component. Never mutate props directly.
- Always initialize state with all required properties. Accessing undefined state keys causes runtime errors.
- State must always be a plain object with named properties. Never set an array or primitive as the top-level state.
- `setState(object)` performs a shallow merge. Only keys provided are updated; others are preserved.
- `setState(fn)` — pass a function `(currentState) => newState` when the next state depends on the current state. Use spread operator to merge: `{ ...state, updatedKey: newValue }`.
- **Stateless functional components**: no state, no lifecycle methods. Accept props, return JSX. Prefer for pure display logic.
- **Container component pattern**: separate data-fetching/state management from UI rendering. Container passes data as props to a stateless child. This makes the child reusable across multiple containers.
- **Context**: for data that is global to many components (e.g., logged-in user, theme). Creates Provider + Consumer pairs.
- `React.createContext(defaultValue)` returns `{ Provider, Consumer }`.
- Wrap the component tree with `<MyContext.Provider value={...}>`. Any descendant can consume with `useContext(MyContext)` or `<MyContext.Consumer>`.
- Use Context when prop drilling through 3+ levels. Do not use Context for frequently-changing data that would cause excessive re-renders.
- `defaultProps` sets fallback values for props when not passed by the parent: `MyComponent.defaultProps = { loading: "loading..." }`.

---

## Ch 4: Getting Started with Hooks

- `useState(initialValue)` returns `[value, setter]`. Call once per state value. Do not combine multiple state values into one `useState` object unless they always change together.
- Setter function from `useState` triggers re-render. Never mutate state directly.
- `useEffect(fn, deps)` runs after render. Used for side effects: API calls, subscriptions, timers.
- `useEffect` with no deps array runs after every render — avoid for API calls.
- `useEffect` with empty deps array `[]` runs only on mount. This is the equivalent of `componentDidMount`.
- `useEffect` with specific deps `[value]` runs when those deps change.
- Return a cleanup function from `useEffect` to cancel subscriptions, pending requests, or timers on unmount. This prevents state updates on unmounted components.
- Pattern for cancellable API calls: use Bluebird or AbortController. Return cleanup from `useEffect` that cancels the pending operation.
- `useContext(MyContext)` reads the current context value within a functional component. No Consumer wrapper needed.
- Context + `useEffect` pattern for shared data: create a `XxxProvider` component that fetches data in `useEffect`, stores in state, and renders `<XxxContext.Provider value={state}>`.
- `useReducer(reducer, initialState)` returns `[state, dispatch]`. Use for complex state with multiple sub-values or when next state depends on previous state in non-trivial ways.
- Reducer signature: `(state, action) => newState`. Must be pure — no side effects. Returns new state object.
- Dispatch actions as plain objects: `dispatch({ type: 'ACTION_NAME', payload: value })`.
- Combine `useReducer` + `useContext` for scalable state management without Redux. Reducer handles state logic; Context distributes it.

---

## Ch 5: Event Handling, the React Way

- Declare event handlers as JSX attributes (`onClick`, `onChange`, `onBlur`, etc.). See https://reactjs.org/docs/events.html for full list.
- Event handlers are declared in JSX, not imperatively attached to DOM nodes. React uses a single document-level listener internally.
- For class components, bind handler context in constructor: `this.onClick = this.onClick.bind(this)`. Or use arrow function class properties: `onClick = () => {...}` (auto-binds).
- Pass arguments to handlers via `.bind(null, arg)` in JSX: `onClick={this.handler.bind(null, item.id)}`.
- Higher-order handler pattern — avoids `.bind()` inline: `onClick = (name) => () => { /* uses name */ }`. Call it in JSX: `onClick={this.onClick("fieldName")}`.
- Inline arrow function handlers are fine for simple cases: `onClick={(e) => console.log(e)}`. Avoid for complex logic — extract to named method.
- React uses `SyntheticEvent` objects that wrap native events. They normalize browser inconsistencies.
- SyntheticEvents are pooled and reused for performance. Properties are cleared after the handler runs. **Never access `event` properties asynchronously** — they will be null/undefined in the callback.
- Anti-pattern: storing event reference or its properties in a variable for use in an async callback. Fix: extract the needed value synchronously before the async call.

---

## Ch 6: Crafting Reusable Components

- Monolithic components cannot be shared between features, are hard to test, and couple concerns.
- Split component at JSX boundaries: identify the smallest meaningful units. Headers, list items, and action controls are each separate component candidates.
- Treat state as immutable. Build new arrays/objects when updating state: `[...state.items, newItem]`, `items.filter(...)`, spread with override `{ ...item, display: '' }`.
- When removing items from state: use `.filter()` to build a new array. Never `splice` or mutate in place.
- When toggling item properties: copy the array, find the index, build a new object at that index using spread.
- **Render props pattern**: a component that accepts a `render` prop (function) and calls it to produce JSX. Enables reuse of stateful logic without inheritance. The pattern: `<DataFetcher render={(data) => <MyUI data={data} />} />`.
- Refactor class components to functional with hooks: extract state with `useState`, side effects with `useEffect`, and pass only what's needed as props.
- **Feature components** encapsulate a specific app feature including its state. **Utility components** are generic and reusable across features. Keep both types in your codebase — don't force feature components to be generic.
- Container component renders the tree; the leaf components render data only.
- Deeply nested component trees that pass props through many levels are a sign of prop drilling. Introduce Context or lift state.

---

## Ch 7: The React Component Life Cycle

- **Lifecycle flow (mount):** `getDerivedStateFromProps` → `render` → `componentDidMount`
- **Lifecycle flow (update):** `getDerivedStateFromProps` → `shouldComponentUpdate` → `render` → `getSnapshotBeforeUpdate` → `componentDidUpdate`
- **Lifecycle flow (unmount):** `componentWillUnmount`
- `componentDidMount`: fetch data here. The component is in the DOM; API calls and subscriptions go here. Calling `setState` here triggers a second render but happens before the browser paints — acceptable for data loading.
- Fetching data in `componentDidMount` vs. before `render` makes no practical difference to users since both are async.
- `getDerivedStateFromProps(props, state)`: static method (no `this`). Returns partial state object or null. Called on every render. Use only when state must be derived from props — a rare case.
- `shouldComponentUpdate(nextProps, nextState)`: return `false` to skip re-render. Use for performance optimization in components that render large lists or expensive content.
- `getSnapshotBeforeUpdate(prevProps, prevState)`: captures DOM state (e.g., scroll position) before update is applied. Synchronous — no async here.
- `componentWillUnmount`: cancel subscriptions, timers, and pending requests. Failure to do this causes "setState on unmounted component" warnings and memory leaks.
- **Error boundaries**: class components implementing `componentDidCatch(error, info)` and `static getDerivedStateFromError(error)`. They catch errors in the component tree below them. Functional components cannot be error boundaries (as of React 18). Wrap feature boundaries with error boundary components.

---

## Ch 8: Validating Component Properties

- Install `prop-types` package: `npm install prop-types`. Not built into React.
- Declare `MyComponent.propTypes = { propName: PropTypes.type }` after component definition (or as static class property).
- PropTypes validation runs in development mode only. Zero cost in production.
- Basic validators: `PropTypes.string`, `PropTypes.number`, `PropTypes.bool`, `PropTypes.func`, `PropTypes.array`, `PropTypes.object`.
- Append `.isRequired` to make a prop mandatory: `PropTypes.string.isRequired`.
- `PropTypes.any` accepts any value. Use as placeholder while developing, then narrow to the correct type.
- `PropTypes.node`: anything renderable (string, element, array of elements).
- `PropTypes.element`: a React element only (JSX, not a string).
- `PropTypes.instanceOf(Class)`: validates value is an instance of a specific class.
- `PropTypes.oneOf([value1, value2])`: validates value is one of specific literal values.
- `PropTypes.oneOfType([PropTypes.string, PropTypes.number])`: union type.
- `PropTypes.arrayOf(PropTypes.instanceOf(MyClass))`: array of specific type.
- `PropTypes.shape({ name: PropTypes.string, age: PropTypes.number })`: object with specific shape. Does not require all properties to be present (non-strict).
- Custom validators: `(props, propName, componentName) => null | new Error(message)`. Return `null` for valid, return `Error` for invalid. These can iterate collections and perform complex checks.
- Every component should have a `propTypes` spec. Even if using TypeScript, PropTypes serves as runtime documentation.

---

## Ch 9: Handling Navigation with Routes

- Use `react-router-dom` for web routing. Current API (v6): `<BrowserRouter>`, `<Routes>`, `<Route path="" element={<Component />} />`.
- Wrap the app in `<BrowserRouter>` (or alias `Router`) at the root.
- Nest routes within `<Routes>`. Each `<Route>` maps a `path` to an `element`.
- Routes are matched exclusively in v6 — no need for `exact` prop.
- Decouple route declarations: let each feature module export its routes. Import and compose them in the top-level `App` component.
- Dynamic segments: `path="/articles/:id"`. Access via `useParams()` hook: `const { id } = useParams()`.
- Query parameters: access via `useSearchParams()`.
- Programmatic navigation: `const navigate = useNavigate(); navigate('/path')`.
- Link components: `<Link to="/path">Label</Link>`. Never use `<a href>` for internal navigation — it causes full page reloads.
- `<NavLink>` adds active styling when the current URL matches. Use `className` or `style` props with a function: `({ isActive }) => isActive ? 'active' : ''`.
- Nested routes: child route's `path` is relative to parent. Parent renders `<Outlet />` where children render.
- Redirect: use `<Navigate to="/path" replace />` component or `navigate('/path', { replace: true })`.

---

## Ch 10: Code Splitting Using Lazy Components and Suspense

- `React.lazy(() => import('./Component'))` creates a lazy component. The `import()` call creates a separate bundle via webpack/Metro.
- Lazy components must be wrapped in `<Suspense fallback={<LoadingUI />}>`. The fallback renders while the bundle is downloading.
- Place `<Suspense>` at the boundary where you want the loading state — typically wrapping a route or page.
- `Suspense` can wrap multiple lazy components. It shows the fallback until all of them are ready.
- Anti-pattern: lazy-loading small components. Reserve code splitting for page-level components and large feature bundles that many users never load.
- Dynamic import pattern (manual, without `lazy()`):
  ```js
  useEffect(() => {
    import('./HeavyModule').then(module => setState(() => module.default));
  }, []);
  ```
  The `lazy()` API is cleaner — prefer it.
- Route-level splitting is the highest-impact use case: each page/screen is a separate bundle downloaded on demand.

---

## Ch 11: Server-Side React Components

- React can render to a string on a Node.js server: `renderToString(<App />)`.
- Server rendering: faster initial load (no JS parse + execute before content appears), better SEO, fewer API round trips (data fetched server-side before HTML is sent).
- Framework: use **Next.js** for server-side rendering. It handles routing, data fetching (getServerSideProps, getStaticProps), and hydration.
- **Hydration**: after server-rendered HTML arrives in browser, React attaches event handlers without re-rendering — calls `hydrateRoot()` instead of `createRoot()`.
- Isomorphic components: components that run identically on server and browser. Avoid browser-only APIs (`window`, `document`) at module top level — guard with `typeof window !== 'undefined'`.
- Next.js `getServerSideProps`: runs on each request. Returns `props` to the page component. Use for data that changes per request.
- Next.js `getStaticProps`: runs at build time. Returns `props`. Use for data that rarely changes.
- Data transformation code (API response shaping) should be shared between server and client.

---

## Ch 12: User Interface Framework Components

- Material-UI (MUI) is the primary React component library covered. Install: `npm install @mui/material @emotion/react @emotion/styled`.
- `<Container maxWidth="sm|md|lg|xl">` controls max horizontal width of content. Content stops growing at the specified breakpoint.
- `<Grid container>` / `<Grid item>` builds responsive layouts. `spacing` prop adds gap between items. Item width: `xs={12} sm={6} md={4}` (12-column grid).
- `<Typography variant="h1|h2|body1|body2|caption|...">` renders semantic text with consistent styling.
- `<AppBar>` + `<Toolbar>` builds nav headers. `<Drawer>` builds side nav.
- `<TextField>`, `<Select>`, `<Checkbox>`, `<Switch>`, `<Slider>` for form inputs. All have `label`, `value`, `onChange` props.
- `<Button variant="contained|outlined|text">` for actions.
- Theme: create with `createTheme({ palette: { primary: {...} } })`. Wrap app with `<ThemeProvider theme={theme}>`.
- Override default styles via `sx` prop (inline sx object) or `styled()` API.

---

## Ch 13: High-Performance State Updates

- **React 18 automatic batching**: multiple `setState` calls in any context (event handlers, `setTimeout`, promises, async/await) are batched into one re-render. Zero code changes needed — just use `createRoot()`.
- Pre-React 18: batching only worked inside synchronous event handlers. Async callbacks caused individual re-renders per `setState` call.
- Migration to automatic batching: replace `ReactDOM.render()` with `ReactDOM.createRoot(el).render(<App />)`.
- To **opt out** of batching for a specific update (rare): wrap in `ReactDOM.flushSync(() => setState(...))`.
- **`startTransition(fn)`**: marks state updates inside `fn` as lower priority. React will defer them in favor of urgent updates (e.g., user input responsiveness).
- `useTransition()` hook returns `[isPending, startTransition]`. `isPending` is `true` while the transition is running. Use it to show a loading indicator.
- Use `startTransition` for: list filtering/sorting with large datasets, tab switches that render expensive content, navigation that renders a new route.
- Do NOT use `startTransition` for: text input state, immediate user feedback, critical error states.
- Pattern for high-performance filtering:
  ```js
  const [filter, setFilter] = useState('');
  const [items, setItems] = useState([]);
  const [isPending, startTransition] = useTransition();
  function onChange(e) {
    setFilter(e.target.value); // urgent — updates input immediately
    startTransition(() => {
      setItems(bigList.filter(item => item.name.includes(e.target.value)));
    });
  }
  ```

---

## Ch 14: Why React Native?

- React Native goal: "learn once, write anywhere" — NOT "write once, run anywhere."
- iOS and Android are fundamentally different. Do not attempt a single codebase that ignores platform-specific UX patterns.
- RN renders native platform widgets (not HTML). `<View>` maps to `UIView` (iOS) and `android.view.View` (Android).
- JS code runs in JavaScriptCore (legacy) or Hermes (recommended from RN 0.64+). Hermes reduces startup time, memory usage, and APK size.
- Bridge (legacy arch): async JSON messages between JS thread and Native thread. Risk of bottleneck on heavy scroll or animation.
- New architecture (JSI + Fabric + TurboModules): JS calls native methods directly via C++ HostObject. Eliminates bridge serialization overhead.
- React Native is not a mobile web wrapper. It calls actual native UI APIs.

---

## Ch 15: React Native Under the Hood

- **Threads in RN**: JS Thread (business logic, components, hooks, API calls), Native Thread (native UI rendering + native modules), Shadow Thread (layout calculation via Yoga engine).
- All component code, state, hooks, and REST calls run on the JS thread.
- Styling is CSS-in-JS: plain objects with camelCase properties. Yoga engine calculates layout.
- Metro bundler: packages JS into a single bundle. Transpiles JSX. TypeScript supported via Babel out of the box.
- Core components: `View`, `Text`, `Image`, `TextInput`, `ScrollView`, `FlatList`, `SectionList`, `Button`, `Pressable`, `Switch`.
- `Pressable` (RN 0.63+): preferred over `TouchableOpacity` / `TouchableHighlight`. More precise touch control.
- **JS libraries usable in RN**: anything without DOM or Node.js APIs. Lodash, Axios, Redux, MobX, Moment, etc. all work.
- **Cannot use**: libraries that depend on `document`, `window`, or Node.js built-ins.
- Error handling: `setJSExceptionHandler` and `setNativeExceptionHandler` from `react-native-exception-handler` for global crash handling.
- OTA updates: replace the JS bundle without App Store review using CodePush (Microsoft). Only JS-layer changes qualify; native code changes require store submission.
- Package discovery: https://reactnative.directory/

---

## Ch 16: Kick-Starting React Native Projects

- Two CLI options: **React Native CLI** (full native access, requires Xcode/Android Studio) vs. **Expo CLI** (managed workflow, no native access needed, faster start).
- Expo CLI setup: `npm install -g expo-cli` → `expo init my-project`.
- Expo Go app: scan QR code to run app on physical device during development. No build step required.
- Expo Snack: browser-based playground for RN — useful for isolated component testing.
- Expo Managed workflow: Expo handles native build; you cannot link custom native modules directly.
- Expo Bare workflow: access to native code; more like React Native CLI.
- Start dev server: `npm start` (runs Metro). Access at `exp://[ip]:19000`.
- For production builds: use EAS Build (Expo Application Services) for cloud builds and store submission.

---

## Ch 17: Building Responsive Layouts with Flexbox

- RN styles are JavaScript objects. Create with `StyleSheet.create({})`. Names are camelCase: `backgroundColor`, `justifyContent`.
- `StyleSheet.create()` validates styles in development and provides performance optimization in production.
- Apply styles with `style={styles.name}` or `style={[styles.one, styles.two]}` (array merges).
- Platform-specific styles: `Platform.select({ ios: {...}, android: {...} })`. Spread into the style object.
- Android status bar height: `StatusBar.currentHeight`. iOS: `paddingTop: 20` (or use `SafeAreaView`).
- Flexbox defaults in RN differ from web: `flexDirection` defaults to `'column'` (not `'row'`). `flex: 1` fills available space.
- Key Flexbox properties:
  - `flexDirection`: `'row'` | `'column'` | `'row-reverse'` | `'column-reverse'`
  - `justifyContent`: main axis alignment — `'flex-start'` | `'center'` | `'flex-end'` | `'space-between'` | `'space-around'`
  - `alignItems`: cross-axis alignment — `'flex-start'` | `'center'` | `'flex-end'` | `'stretch'`
  - `flex`: numeric weight for distributing space. `flex: 1` on a container fills parent.
  - `flexWrap`: `'wrap'` | `'nowrap'`
- No CSS cascading in RN. Each component's style is isolated — no inherited text color/size from parent unless explicitly passed.
- `Styled Components` library works with RN: `import styled from 'styled-components/native'`.

---

## Ch 18: Navigating Between Screens

- Use `@react-navigation/native` as the primary navigation library.
- Install: `npm install @react-navigation/native` + `expo install react-native-screens react-native-safe-area-context`.
- Wrap the app in `<NavigationContainer>`.
- Stack navigator: `npm install @react-navigation/native-stack`. Creates `Stack.Navigator` + `Stack.Screen`.
  ```js
  const Stack = createNativeStackNavigator();
  <NavigationContainer>
    <Stack.Navigator>
      <Stack.Screen name="Home" component={Home} />
      <Stack.Screen name="Settings" component={Settings} />
    </Stack.Navigator>
  </NavigationContainer>
  ```
- Navigate programmatically: `navigation.navigate('ScreenName')`. The `navigation` prop is injected into screen components automatically.
- Pass params to screens: `navigation.navigate('Details', { itemId: 42 })`. Access: `route.params.itemId`.
- Customize header: `navigation.setOptions({ title: 'New Title' })` or via `Stack.Screen options={{ title: '...' }}`.
- Tab navigation: `@react-navigation/bottom-tabs`. `createBottomTabNavigator()`. Each tab is a screen.
- Drawer navigation: `@react-navigation/drawer`. `createDrawerNavigator()`. Open/close via `navigation.openDrawer()` / `navigation.closeDrawer()`.
- Nested navigators: wrap a Stack inside a Tab, or a Tab inside a Drawer.
- Navigate back: `navigation.goBack()`.

---

## Ch 19: Rendering Item Lists

- Use `FlatList` for any scrollable list of items. Never use raw `ScrollView` with `.map()` for long lists — it renders all items at once.
- `FlatList` virtualizes rendering — only renders items visible on screen.
- Required props: `data` (array of objects with `key` string property) + `renderItem` (function receiving `{ item }` destructured).
- If data objects lack a `key` property, provide `keyExtractor={(item) => item.id.toString()}`.
- Give the `FlatList` container `flex: 1` for proper scroll behavior. Without explicit height, scroll breaks.
- `onEndReached` prop: fires when user scrolls near the bottom. Use for infinite scroll / pagination.
- `onRefresh` + `refreshing` props: implements pull-to-refresh. `refreshing` is a boolean state; `onRefresh` triggers fetch.
- `SectionList` for sectioned lists (e.g., alphabetical groups). Props: `sections` (array of `{ title, data }`) + `renderItem` + `renderSectionHeader`.
- Sort/filter data in the component rendering the list — transform the data array before passing to `FlatList`. Do not build multiple FlatList components for different states.
- Fetch data in `useEffect` with `[]` dependency. Show `ActivityIndicator` while loading. Show error message if fetch fails.

---

## Ch 20: Showing Progress

- `ActivityIndicator`: platform-native spinner. Props: `size="small|large"`, `color`.
- Show `ActivityIndicator` during: API fetches, file uploads, background processing.
- `ProgressBar` (Android-specific native component) for determinate progress. For cross-platform: use a custom `View` with width calculated from percentage.
- Always communicate progress to the user. Never block the UI without feedback.
- Navigation indicator pattern: show `ActivityIndicator` in the navigation header while a screen's data is loading. Use `navigation.setOptions({ headerRight: () => <ActivityIndicator /> })`.
- Step progress (wizard pattern): track step index in state, render a visual progress bar using step count / total steps.

---

## Ch 21: Geolocation and Maps

- Install: `expo install expo-location`.
- Request permissions before accessing location: `Location.requestForegroundPermissionsAsync()`.
- Get current position: `Location.getCurrentPositionAsync()`. Returns `{ coords: { latitude, longitude, altitude, accuracy } }`.
- Watch position changes: `Location.watchPositionAsync(options, callback)`. Returns a subscription object — call `.remove()` on unmount.
- Reverse geocoding (coords → address): call Google Maps Geocoding API or `Location.reverseGeocodeAsync({ latitude, longitude })`.
- Maps: `react-native-maps` — install via Expo: `expo install react-native-maps`.
- `<MapView>` component. Required props: `style` (must have explicit width/height), `initialRegion` `{ latitude, longitude, latitudeDelta, longitudeDelta }`.
- Add markers: `<Marker coordinate={{ latitude, longitude }} title="Label" description="Details" />`.
- `latitudeDelta` / `longitudeDelta`: zoom level. Smaller values = closer zoom. ~0.01 ≈ city-block level.
- Always test on physical device or simulator with location simulation — browser doesn't provide real GPS.

---

## Ch 22: Collecting User Input

- `TextInput`: key props: `value`, `onChangeText`, `placeholder`, `secureTextEntry`, `returnKeyType`, `keyboardType`, `autoCapitalize`, `autoCorrect`, `multiline`.
- `onChangeText` receives the string value directly (not an event object like web React).
- `onSubmitEditing` fires when the user presses the return/submit key.
- `onFocus` / `onBlur` for keyboard show/hide and field focus tracking.
- `keyboardType` options: `'default'`, `'email-address'`, `'numeric'`, `'phone-pad'`, `'url'`.
- Date/time input: no native cross-platform picker in RN core. Use `@react-native-community/datetimepicker` or a third-party modal picker.
- Selection list: `Picker` was removed from RN core. Use `@react-native-picker/picker`.
- Toggle: `Switch` component. Props: `value` (bool), `onValueChange`. No `onChange`.
- Checkbox: no native cross-platform checkbox. Use `Switch` or implement with `Pressable` + visual state.
- Keyboard avoidance: wrap form in `KeyboardAvoidingView behavior="padding|height"` so the keyboard doesn't cover inputs.
- `ScrollView` inside a form lets user scroll to inputs when keyboard is open.

---

## Ch 23: Displaying Modal Screens

- Distinguish three categories of user-facing information:
  - **Alert**: critical, user must acknowledge. Use native `Alert.alert(title, message, buttons)`.
  - **Confirmation**: user must confirm before proceeding. Use `Alert.alert` with OK + Cancel buttons.
  - **Notification**: informational, dismisses automatically. Use a custom component with a timer.
- `Alert.alert(title, message, [{ text, onPress, style }])`: native OS dialog. Cannot be styled. Use for errors and destructive confirmations.
- `Modal` component: `<Modal visible={bool} animationType="slide|fade|none" transparent={bool}>`. Requires explicit close button — there is no automatic dismiss.
- Activity modal pattern: show `Modal` with `ActivityIndicator` during background operations to prevent user interaction.
- Passive notifications: custom `Animated.View` that slides in, waits, then slides out. Implement with `Animated.timing()` or React Native Reanimated.
- Do not overuse `Alert` — it blocks interaction. Use passive notifications for non-critical messages.

---

## Ch 24: Responding to User Gestures

- `ScrollView`: handles scrolling with momentum, bounce, and velocity. Requires explicit height/flex.
- `ScrollView` is for arbitrary content. `FlatList` is for lists. Do not put a FlatList inside a ScrollView.
- `TouchableOpacity`: reduces opacity on press. Most common touchable wrapper. Use instead of raw `View` with `onPress`.
- `TouchableHighlight`: changes background color on press. Useful for list items.
- `Pressable` (preferred, RN 0.63+): `onPress`, `onPressIn`, `onPressOut`, `onLongPress`. Supports `hitSlop` for expanding touch target. `style` prop accepts function: `({ pressed }) => pressed ? pressedStyle : defaultStyle`.
- `onLongPress` delay is configurable: `delayLongPress={500}`.
- Swipeable list items: use `react-native-gesture-handler` and `Swipeable` component for left/right swipe actions. Do not roll your own swipe gesture from scratch.
- Gesture responder system: low-level API for custom gestures. Almost never needed — use library components instead.

---

## Ch 25: Using Animations

- **Animated API** (built-in): runs on JS thread with async bridge communication. Causes minimum 1 frame (~16ms) delay. Acceptable for simple animations, problematic for complex or gesture-driven ones.
- **React Native Reanimated** (preferred): runs animation logic on the UI thread via worklets. Zero JS-bridge overhead. Install: `expo install react-native-reanimated`.
- After installing Reanimated, add Babel plugin to `babel.config.js`:
  ```js
  plugins: ['react-native-reanimated/plugin']
  ```
  Then restart with: `expo start --clear`.
- Reanimated core APIs:
  - `useSharedValue(initial)`: stateful value that lives on UI thread. Triggers animation when changed.
  - `useAnimatedStyle(() => ({ ... }))`: creates animated style from shared values.
  - `withTiming(value, config)`: smooth linear/easing animation to target.
  - `withSpring(value, config)`: spring-based animation.
  - `withDecay(config)`: deceleration animation (for fling gestures).
  - `useDerivedValue(() => derivation)`: computed value based on other shared values.
- Layout animations (enter/exit): wrap component in `<Animated.View entering={SlideInLeft} exiting={SlideOutRight}>`. Predefined animations: `FadeIn`, `FadeOut`, `SlideInLeft`, `SlideOutRight`, `BounceIn`, `ZoomIn`, etc.
- Worklet functions: mark with `"worklet"` directive at top of function body to run synchronously on UI thread.
- Anti-pattern: using Animated API for gesture-linked animations (e.g., drag-to-scroll). Use Reanimated + `react-native-gesture-handler` instead.

---

## Ch 26: Controlling Image Display

- `Image` component: `source` prop accepts either `{ uri: 'https://...' }` for network images or `require('./path/image.png')` for local images.
- `require()` returns a number. PropType for source: `PropTypes.oneOfType([PropTypes.shape({ uri: PropTypes.string }), PropTypes.number])`.
- `resizeMode` prop: `'cover'` (fill, may crop) | `'contain'` (fit, may letterbox) | `'stretch'` (distort to fill) | `'center'` (no resize).
- Always set explicit `width` and `height` on Image. Without them, the image may not render.
- Lazy image loading / placeholder: use `onLoadStart` and `onLoad` callbacks to show a placeholder `ActivityIndicator` while the image loads.
- `@expo/vector-icons`: icon library bundled with Expo. `import { Ionicons } from '@expo/vector-icons'`. Render: `<Ionicons name="icon-name" size={24} color="black" />`. Browse icons at https://icons.expo.fyi.
- For SVG: `react-native-svg` library. Wrap SVG paths in `<Svg>` component from the library.
- Network images require HTTPS on iOS (App Transport Security). Either configure exception or use HTTPS.

---

## Ch 27: Going Offline

- Detect network state: `@react-native-community/netinfo`. Install: `expo install @react-native-community/netinfo`.
- Pattern:
  ```js
  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsConnected(state.isConnected);
    });
    return () => unsubscribe();
  }, []);
  ```
- `state.type` values: `'wifi'`, `'cellular'`, `'none'`, `'unknown'`.
- Local storage: `@react-native-async-storage/async-storage`. Install: `expo install @react-native-async-storage/async-storage`.
- `AsyncStorage` API: `setItem(key, value)`, `getItem(key)`, `removeItem(key)`, `clear()`, `getAllKeys()`, `multiGet(keys)`. All return Promises.
- AsyncStorage stores strings only. Serialize objects: `JSON.stringify` before `setItem`, `JSON.parse` after `getItem`.
- Sync pattern: store pending mutations locally when offline. On reconnect (detected via NetInfo), replay them against the server and clear local queue.
- `multiGet` / `multiSet` for batch operations — more efficient than individual calls.
- AsyncStorage is not encrypted. Do not store tokens, passwords, or PII in AsyncStorage without additional encryption.

---

## Ch 28: Selecting Native UI Components Using NativeBase

- NativeBase: cross-platform UI library for RN. Requires font loading at startup via `useFonts()` hook.
- Wrap app in `<NativeBaseProvider theme={theme}>`. This is the equivalent of MUI's `ThemeProvider`.
- Font loading pattern:
  ```js
  const [fontsLoaded] = useFonts({ Roboto_500Medium, Roboto_400Regular, ...Ionicons.font });
  if (!fontsLoaded) return <AppLoading />;
  ```
- Layout components: `Box` (generic View equivalent), `HStack` (horizontal flex row), `VStack` (vertical flex column), `Stack`, `Center`, `Flex`.
- `safeAreaTop` prop on `Box` handles iOS notch/status bar automatically.
- Typography: `<Text>` with `fontSize`, `fontWeight`, `color` props.
- Form components: `Input`, `Select`, `Checkbox`, `Switch`, `Slider`, `TextArea`.
- Navigation components: build with `HStack` + NativeBase `Box` components. NativeBase does not provide a Navigator — use `@react-navigation/*` for screen navigation.
- Theming: `extendTheme({ colors: {...}, fonts: {...} })`. Custom theme values override defaults.
- `Container` component pattern: one top-level component that wraps NativeBaseProvider + StatusBar + header, accepts `title` and `children` props. All screens import this Container.

---

## Ch 29: Handling Application State

- **Unidirectional data flow**: state flows from parent to child via props. Child components cannot directly modify parent state.
- Prop drilling problem: passing props through many intermediate components that don't use them. Solved with Context.
- **Context architecture**:
  1. `const MyContext = createContext(defaultValue)` — creates context
  2. `<MyContext.Provider value={stateAndActions}>` — wraps the subtree
  3. `useContext(MyContext)` — reads context in any descendant
- Combine `createContext` + `useReducer` for scalable state:
  ```js
  const [state, dispatch] = useReducer(reducer, initialState);
  return <MyContext.Provider value={{ state, dispatch }}>{children}</MyContext.Provider>;
  ```
- Reducer function: `(state, action) => newState`. Must be pure. All state transformations happen here.
- Action pattern: `dispatch({ type: 'FETCH_SUCCESS', payload: data })`. Reducer switches on `action.type`.
- Create one Context per domain slice (articles, users, auth). Aggregate in an `AppContext` wrapper:
  ```js
  const AppContext = ({ children }) => (
    <ArticlesProvider>
      <AuthProvider>{children}</AuthProvider>
    </ArticlesProvider>
  );
  ```
- State mutations outside Context/reducer are anti-patterns. Never mutate data in event handlers, API callbacks, or outside reducers.
- Web vs. mobile state shape will differ — do not force identical Context shape across platforms. Share architecture patterns, not identical structures.
- Context limitations at scale: too many Context updates cause broad re-renders. At scale, consider Zustand, Jotai, or Redux Toolkit.

---

## Ch 30: Why GraphQL?

- GraphQL: query language where the client specifies the exact data shape it needs. Server returns only those fields.
- Apollo Client: JS library that manages GraphQL data fetching, caching, and state. Provides `useQuery`, `useMutation`, `useSubscription` hooks.
- GraphQL terminology:
  - **Query**: read operation — fetch data
  - **Mutation**: write operation — create, update, delete
  - **Subscription**: real-time stream (WebSocket-based)
  - **Fragment**: reusable piece of a query
  - **Schema**: server-side contract — defines types, queries, mutations
- Apollo Client handles caching via `InMemoryCache`. Normalized cache deduplicates results by type + ID.
- Advantage over Context: no manual reducers/actions for data fetching. Apollo handles optimistic updates, cache invalidation, and re-fetch policies.
- Disadvantage vs. Context: learning curve, heavier dependency, some immutability constraints are verbose.
- GraphQL server must be set up separately. Apollo Client is the frontend adapter only.
- Both web and native apps can share the same GraphQL backend schema. Write the schema once; query from both platforms.

---

## Ch 31: Building a GraphQL React App

- Bootstrap Apollo Client:
  ```js
  import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';
  const client = new ApolloClient({
    cache: new InMemoryCache(),
    uri: 'http://localhost:4000/graphql',
  });
  root.render(<ApolloProvider client={client}><App /></ApolloProvider>);
  ```
- For React Native with Expo: use local network IP instead of `localhost` — Expo cannot resolve `localhost` on device.
- Define queries with `gql` template literal tag:
  ```js
  import { gql } from '@apollo/client';
  export const GET_USER = gql`
    query GetUser($userId: String) {
      user(id: $userId) {
        id totalCount completedCount
        todos { id text complete }
      }
    }
  `;
  ```
- Fetch data with `useQuery`:
  ```js
  const { loading, error, data } = useQuery(GET_USER, { variables: { userId: 'me' } });
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage />;
  ```
- Mutate data with `useMutation`:
  ```js
  const [addTodo] = useMutation(ADD_TODO, { refetchQueries: [GET_USER] });
  ```
- `refetchQueries`: list of queries to re-run after a mutation completes. Ensures cache stays fresh.
- `InMemoryCache` automatically normalizes results by `__typename` + `id`. Components subscribed to the same data auto-update when cache changes.
- Schema type system: `!` suffix = required field. Types: `ID!`, `String!`, `Boolean`, `Int`, `[Todo]!`.
- Mutation type defines all write operations with their input params and return type:
  ```graphql
  type Mutation {
    addTodo(text: String): [Todo]
    changeTodoStatus(id: Int!, complete: Boolean): [Todo]
  }
  ```
- Web and native React Native apps can share the same GraphQL schema. Apollo Client API is identical on both platforms.

---

## Cross-Cutting Patterns

### State Management Decision Matrix
| Complexity | Solution |
|---|---|
| Local UI state (toggle, form field) | `useState` |
| Local side effects (API fetch, timer) | `useEffect` |
| Complex state with multiple sub-values | `useReducer` |
| Global shared data (user, theme, config) | `Context + useReducer` |
| Server data with caching + sync | Apollo Client + GraphQL |
| High-frequency updates across many components | Zustand / Jotai (not covered, but flagged) |

### React Native vs. Web Component Mapping
| Web | React Native |
|---|---|
| `div` | `View` |
| `span`, `p`, `h1`-`h6` | `Text` (no semantic differentiation) |
| `img` | `Image` |
| `input` | `TextInput` |
| `button` | `Pressable` / `TouchableOpacity` |
| `ul` + `li` with scroll | `FlatList` |
| `a href` | `navigation.navigate()` |
| CSS classes | `StyleSheet.create({})` |
| `:hover` | `onPressIn` / `Pressable` pressed state |
| `position: fixed` | Not available — use modal or absolute positioning |

### Deprecated Patterns to Avoid
- `TouchableNativeFeedback`, `TouchableHighlight`, `TouchableOpacity` → use `Pressable`.
- Class components → use functional components + hooks.
- `componentWillMount`, `componentWillUpdate`, `componentWillReceiveProps` → removed in React 18.
- `AsyncStorage` from `react-native` directly → use `@react-native-async-storage/async-storage`.
- `Picker` from `react-native` → use `@react-native-picker/picker`.
- `ReactDOM.render()` → use `ReactDOM.createRoot().render()`.
- Animated API for gesture-linked animations → use React Native Reanimated.
- Bridge-heavy native interactions → plan for JSI/Fabric new architecture migration.
