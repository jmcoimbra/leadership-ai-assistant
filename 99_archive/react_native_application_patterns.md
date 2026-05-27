# React Native — Application Patterns

**Purpose:** Enforceable patterns, API signatures, platform differences, anti-patterns. No narrative.
**Flags:** `[2019]` = dated pattern; modern equivalent noted inline.

---

## Ch 1: Getting Started with React Native

- React Native renders native UI components, not WebViews. Bridge translates JS calls to native APIs.
- Three threads: JS thread (business logic), native bridge (serialized JSON), native UI thread (rendering).
- JS thread runs on JavaScriptCore (JSC) engine, not V8.
- Entry point: `AppRegistry.registerComponent(appKey, () => RootComponent)` — must be called once per app.
- Project structure: `index.js` (entry), `android/`, `ios/`, `node_modules/`. Component files go in `/app` or `/src` by convention.
- JSX compiles via Babel to `React.createElement()` calls. No browser DOM — maps to native views.
- [2019] `React.createClass()` deprecated. Use ES6 class syntax or functional components.
- [2019] Class components were primary pattern. Prefer functional components + hooks for new code.
- Component types: stateful (class or hooks), stateless/functional, pure components.
- `StyleSheet.create()` validates style properties at compile time. Prefer over inline objects for performance.
- Hot reloading preserves app state during code edits. Live reloading restarts app fully. Prefer hot reloading.
- Developer menu: Shake device (physical) or Cmd+D (iOS simulator) / Cmd+M (Android emulator).

---

## Ch 2: Understanding React

- State: mutable, internal to component. Mutate only via `setState()`. Direct mutation does not trigger re-render.
- Props: immutable from component's perspective. Set by parent. Read via `this.props` (class) or function args (functional).
- `setState()` is asynchronous. If next state depends on current state, use functional form: `setState(prevState => ({ count: prevState.count + 1 }))`.
- [2019] Full lifecycle for class components:
  - `constructor(props)` — initialize state, bind methods. Call `super(props)` first.
  - `static getDerivedStateFromProps(props, state)` — return partial state or null. Replaces deprecated `componentWillReceiveProps`.
  - `render()` — must be pure, no side effects.
  - `componentDidMount()` — fire network requests, set up subscriptions.
  - `shouldComponentUpdate(nextProps, nextState)` — return false to skip re-render. Performance optimization.
  - `componentDidUpdate(prevProps, prevState)` — respond to prop/state changes. Guard against infinite loops.
  - `componentWillUnmount()` — clean up subscriptions, timers, listeners.
- [2019] `componentWillMount`, `componentWillReceiveProps`, `componentWillUpdate` are deprecated (UNSAFE_* prefixed). Do not use.
- Modern equivalent: `useEffect` hook replaces `componentDidMount`, `componentDidUpdate`, `componentWillUnmount`.
- Props validation: PropTypes package (runtime warnings in dev). TypeScript preferred for static analysis.
- Pure components (`React.PureComponent`) implement `shouldComponentUpdate` with shallow comparison. Use when props/state are flat.
- Keys on list items must be stable, unique strings. Using array index as key causes reconciliation bugs when list order changes.
- Virtual DOM diffing: React reconciles component tree, computes minimal native operations. Diff algorithm is O(n) with heuristics.

---

## Ch 3: Building Your First React Native App

- `TextInput` controlled component pattern — always bind `value` and `onChangeText`:
  ```js
  <TextInput
    value={this.state.inputValue}
    onChangeText={text => this.setState({ inputValue: text })}
  />
  ```
- `TextInput` without `value` is uncontrolled — state is internal to native. Avoid in most cases.
- `TouchableHighlight` wraps a single child. `underlayColor` sets the color shown on press.
  ```js
  <TouchableHighlight onPress={this.handlePress} underlayColor="#ccc">
    <View><Text>Press me</Text></View>
  </TouchableHighlight>
  ```
- `TouchableOpacity` reduces opacity on press. Use when no underlay color is needed.
- `TouchableWithoutFeedback` provides no visual feedback. Use only when building custom feedback.
- [2019] `TouchableNativeFeedback` Android-only ripple effect. Modern: `Pressable` replaces all Touchable variants.
- Developer menu shortcuts:
  - Reload: `R+R` (Android), `Cmd+R` (iOS simulator)
  - Toggle inspector: `Cmd+I` (iOS), Menu → Toggle Inspector (Android)
  - Show perf monitor: available via developer menu
- `console.log()` output visible in Metro bundler terminal and Chrome DevTools remote debugger.
- Chrome remote debugging: Developer menu → Debug JS Remotely. Opens `http://localhost:8081/debugger-ui`.

---

## Ch 4: Introduction to Styling

- All style properties use camelCase (no hyphens). Values are JS strings or numbers.
- Dimensions are unitless numbers (density-independent pixels). No `px`, `em`, `%` (except for some flexbox values).
- `StyleSheet.create({ name: {...} })` returns an object with integer IDs — more efficient than plain objects.
- Inline styles: `<View style={{ backgroundColor: 'red' }}>` — creates new object on every render. Avoid in loops/lists.
- Array styles: `<View style={[styles.base, styles.override, { marginTop: 10 }]}>` — later styles win. Falsy values ignored.
- Color formats: `'red'` (named), `'#fff'` / `'#ffffff'` (hex), `'rgb(r,g,b)'`, `'rgba(r,g,b,a)'`.
- Border properties: `borderWidth`, `borderColor`, `borderRadius`, `borderTopWidth`, `borderBottomLeftRadius`, etc.
- Text-specific styles (only valid on `Text` component): `fontFamily`, `fontSize`, `fontWeight`, `fontStyle`, `lineHeight`, `letterSpacing`, `textAlign`, `textDecorationLine`, `color`.
- View-specific: `backgroundColor`, `opacity`, `overflow` (`'visible'` | `'hidden'`).
- `overflow: 'hidden'` clips children. Required for `borderRadius` to clip child content on Android.

---

## Ch 5: Styling in Depth

- `Platform.OS` returns `'ios'` or `'android'`. Use for conditional logic.
- `Platform.select({ ios: value, android: value, default: value })` — returns platform-specific value.
- Platform-specific files: `Component.ios.js` and `Component.android.js` — React Native picks correct file at bundle time. No runtime check needed.
- iOS shadow props (View): `shadowColor`, `shadowOffset: {width, height}`, `shadowOpacity`, `shadowRadius`. iOS only.
- Android elevation: `elevation: N` (integer). Creates shadow + affects z-index stacking. Android only.
- [2019] `ShadowPropTypesIOS` imported from React Native. Modern: these props work on iOS View directly.
- Transforms (all cross-platform on View/Text/Image):
  ```js
  transform: [
    { translateX: 50 },
    { translateY: 100 },
    { rotateX: '45deg' },
    { rotateY: '45deg' },
    { rotateZ: '45deg' },   // same as rotate
    { rotate: '45deg' },
    { scaleX: 2 },
    { scaleY: 2 },
    { scale: 2 },
    { skewX: '10deg' },
    { skewY: '10deg' },
    { perspective: 1000 },  // required for rotateX/Y to appear 3D
  ]
  ```
- Transform order matters — transforms are applied right-to-left in the array.
- Flexbox default axis: `flexDirection: 'column'` (not row like CSS web default).
- `flex: N` distributes remaining space proportionally among siblings.
- `justifyContent`: `'flex-start'` | `'flex-end'` | `'center'` | `'space-between'` | `'space-around'` | `'space-evenly'`. Along main axis.
- `alignItems`: `'flex-start'` | `'flex-end'` | `'center'` | `'stretch'` | `'baseline'`. Along cross axis.
- `alignSelf` overrides `alignItems` per child.
- `flexWrap: 'wrap'` enables multi-line flex containers.
- `position: 'absolute'` removes element from flow. Positioned relative to nearest positioned ancestor.
- `zIndex` controls stacking order within the same parent.

---

## Ch 6: Navigation

- [2019] React Navigation v2 APIs. Modern: React Navigation v6+ has different import paths and API shapes. Flag all APIs below.
- [2019] `createStackNavigator(routeConfig, stackConfig)` — returns a component. Stack config: `headerMode`, `initialRouteName`, `navigationOptions`.
  ```js
  const Navigator = createStackNavigator({
    Home: { screen: HomeComponent },
    Detail: { screen: DetailComponent },
  }, { initialRouteName: 'Home' });
  ```
- [2019] `createBottomTabNavigator(routeConfig, tabConfig)` — tab bar at bottom. Config: `tabBarOptions`, `initialRouteName`.
- [2019] `createDrawerNavigator(routeConfig, drawerConfig)` — side drawer. Config: `drawerWidth`, `contentComponent`, `drawerPosition`.
- Navigation prop injected into screen components: `this.props.navigation`.
  - `navigation.navigate('RouteName', { paramKey: value })` — go to route, pass params.
  - `navigation.goBack()` — pop stack.
  - `navigation.getParam('paramKey', defaultValue)` — read params.
  - `navigation.setParams({ key: value })` — update current screen params (triggers re-render).
- `navigationOptions` static property on screen component — configures header:
  ```js
  static navigationOptions = ({ navigation }) => ({
    title: navigation.getParam('title', 'Default'),
    headerRight: <Button onPress={...} />,
  });
  ```
- `screenProps` passed to all screens in navigator — use for shared data (e.g., theme, auth).
- Nested navigators: outer navigator wraps inner. `navigation.navigate` resolves to nearest matching route.
- AsyncStorage pattern for persisting navigation state:
  ```js
  AsyncStorage.setItem('key', JSON.stringify(state));
  AsyncStorage.getItem('key').then(state => JSON.parse(state));
  ```

---

## Ch 7: Animations

- `Animated.Value` holds animated scalar. `Animated.ValueXY` holds {x, y} pair.
  ```js
  animatedValue = new Animated.Value(0);
  ```
- `Animated.timing(value, config)` — interpolate to target over duration:
  ```js
  Animated.timing(this.animatedValue, {
    toValue: 1,
    duration: 500,
    easing: Easing.linear,
    useNativeDriver: true,
  }).start(({ finished }) => { /* callback */ });
  ```
- `Animated.spring(value, config)` — spring physics: `toValue`, `friction`, `tension`, `stiffness`, `damping`.
- `Animated.decay(value, config)` — decelerate from `velocity` with `deceleration` factor.
- `Animated.loop(animation, { iterations: N })` — repeat N times. `-1` for infinite.
- Parallel/sequence/stagger:
  ```js
  Animated.parallel([anim1, anim2]).start();
  Animated.sequence([anim1, anim2]).start();       // wait for each to finish
  Animated.stagger(200, [anim1, anim2]).start();   // 200ms delay between starts
  ```
- `animatedValue.interpolate({ inputRange: [0, 1], outputRange: ['0deg', '360deg'] })` — map value to new range. Output can be strings (colors, degrees).
- `useNativeDriver: true` — runs animation entirely on native thread. Avoids JS thread blocking. Restriction: only works with transform and opacity properties.
- `Animated.createAnimatedComponent(Component)` — makes any component animatable. Pre-built: `Animated.View`, `Animated.Text`, `Animated.Image`, `Animated.ScrollView`.
- Reset animation: `animatedValue.setValue(0)` — synchronously resets without triggering animation.
- [2019] `Animated.event` with `useNativeDriver` for scroll/pan tracking — complex. Modern: `useAnimatedStyle` (Reanimated 2) preferred for complex animations.

---

## Ch 8: Redux Data Architecture

- Redux principles: single store, state is read-only, changes via pure reducer functions.
- Store setup:
  ```js
  import { createStore, combineReducers } from 'redux';
  const rootReducer = combineReducers({ books: booksReducer, user: userReducer });
  const store = createStore(rootReducer);
  ```
- Provider wraps app root:
  ```js
  import { Provider } from 'react-redux';
  <Provider store={store}><App /></Provider>
  ```
- Connect pattern [2019]:
  ```js
  import { connect } from 'react-redux';
  const mapStateToProps = state => ({ books: state.books });
  const mapDispatchToProps = dispatch => ({
    addBook: book => dispatch({ type: 'ADD_BOOK', book }),
  });
  export default connect(mapStateToProps, mapDispatchToProps)(BookList);
  ```
- Modern equivalent: `useSelector` and `useDispatch` hooks replace `connect`.
- Reducer pattern — must be pure, no mutation:
  ```js
  function booksReducer(state = [], action) {
    switch (action.type) {
      case 'ADD_BOOK':
        return [...state, action.book];
      case 'REMOVE_BOOK':
        return state.filter((_, index) => index !== action.index);
      default:
        return state;
    }
  }
  ```
- Immutable array deletion: `state.filter((_, i) => i !== indexToRemove)`. Never `splice`.
- Immutable object update: `{ ...state, key: newValue }`. Never `state.key = value`.
- Context API is the Provider/Consumer mechanism Redux Provider uses internally. Can use Context directly for simpler shared state.
- Action creators: pure functions returning action objects. Keeps dispatch calls clean.
- [2019] `redux-thunk` for async actions. Modern: RTK Query or `createAsyncThunk` (Redux Toolkit) preferred.

---

## Ch 9: Cross-Platform APIs

- **Alert:**
  ```js
  Alert.alert(title, message, [
    { text: 'Cancel', onPress: () => {}, style: 'cancel' },
    { text: 'OK', onPress: () => {} },
  ]);
  ```
  - Button styles: `'default'` | `'cancel'` | `'destructive'`. iOS only — Android ignores style.
  - Android supports max 3 buttons. iOS: unlimited via scroll list.

- **AppState:**
  ```js
  AppState.currentState   // 'active' | 'background' | 'inactive' (iOS only)
  AppState.addEventListener('change', handler);
  AppState.removeEventListener('change', handler);  // [2019] — use returned subscription.remove() in modern RN
  ```
  - `'inactive'` fires on iOS during phone calls, notification center open.

- **AsyncStorage:** [2019] `AsyncStorage` removed from React Native core. Use `@react-native-async-storage/async-storage`.
  ```js
  await AsyncStorage.setItem('key', 'value');
  const value = await AsyncStorage.getItem('key');
  await AsyncStorage.removeItem('key');
  await AsyncStorage.mergeItem('key', JSON.stringify({ newField: 'value' }));
  await AsyncStorage.clear();
  const keys = await AsyncStorage.getAllKeys();
  const pairs = await AsyncStorage.multiGet(['key1', 'key2']);  // returns [[key, value], ...]
  await AsyncStorage.multiSet([['key1', 'val1'], ['key2', 'val2']]);
  await AsyncStorage.multiRemove(['key1', 'key2']);
  ```
  - Values must be strings. Use `JSON.stringify`/`JSON.parse` for objects.

- **Clipboard:** [2019] Removed from React Native core. Use `@react-native-clipboard/clipboard`.
  ```js
  await Clipboard.setString('text');
  const text = await Clipboard.getString();
  ```

- **Dimensions:**
  ```js
  const { width, height } = Dimensions.get('window');
  const { width, height } = Dimensions.get('screen');  // includes status bar on Android
  ```
  - Subscribe to changes: `Dimensions.addEventListener('change', handler)`. Required for orientation support.
  - Modern: `useWindowDimensions()` hook re-renders component on size change.

- **Geolocation:** [2019] Removed from React Native core. Use `@react-native-community/geolocation` or `expo-location`.
  ```js
  navigator.geolocation.getCurrentPosition(
    position => { /* position.coords.latitude/longitude/accuracy */ },
    error => { /* error.code, error.message */ },
    { enableHighAccuracy: true, timeout: 20000, maximumAge: 1000 }
  );
  const watchId = navigator.geolocation.watchPosition(successCb, errorCb, options);
  navigator.geolocation.clearWatch(watchId);
  ```
  - Must request permission before calling on iOS. Add `NSLocationWhenInUseUsageDescription` to Info.plist.

- **Keyboard:**
  ```js
  Keyboard.addListener('keyboardWillShow', handler);   // iOS only
  Keyboard.addListener('keyboardDidShow', handler);    // cross-platform
  Keyboard.addListener('keyboardWillHide', handler);   // iOS only
  Keyboard.addListener('keyboardDidHide', handler);    // cross-platform
  Keyboard.dismiss();
  ```
  - `KeyboardAvoidingView` component wraps content that should move when keyboard appears.

- **NetInfo:** [2019] Removed from React Native core. Use `@react-native-community/netinfo`.
  ```js
  NetInfo.fetch().then(state => { state.isConnected; state.type; });
  const unsubscribe = NetInfo.addEventListener(state => { /* state.isConnected */ });
  unsubscribe();
  ```

- **PanResponder:**
  ```js
  panResponder = PanResponder.create({
    onStartShouldSetPanResponder: () => true,
    onMoveShouldSetPanResponder: () => true,
    onPanResponderGrant: (evt, gestureState) => { /* touch started */ },
    onPanResponderMove: (evt, gestureState) => {
      /* gestureState.dx, gestureState.dy, gestureState.vx, gestureState.vy */
    },
    onPanResponderRelease: (evt, gestureState) => { /* touch ended */ },
    onPanResponderTerminate: (evt, gestureState) => { /* interrupted */ },
  });
  // Apply: <View {...panResponder.panHandlers}>
  ```
  - Modern: `react-native-gesture-handler` preferred. More performant, runs on UI thread.

---

## Ch 10: iOS-Specific Components and APIs

- iOS-specific components only render on iOS. Wrap in `Platform.OS === 'ios'` guard when used in shared files, or use `.ios.js` file extension.
- **DatePickerIOS:** [2019] Deprecated. Use `@react-native-community/datetimepicker`.
  ```js
  <DatePickerIOS
    date={this.state.date}
    onDateChange={date => this.setState({ date })}
    mode="date"          // 'date' | 'time' | 'datetime'
    minimumDate={new Date()}
    maximumDate={new Date(2030, 0, 1)}
    minuteInterval={15}
  />
  ```
- **PickerIOS:** [2019] Deprecated. Use `@react-native-picker/picker`.
  ```js
  <PickerIOS
    selectedValue={this.state.selected}
    onValueChange={value => this.setState({ selected: value })}
  >
    <PickerIOS.Item label="Option 1" value="opt1" />
  </PickerIOS>
  ```
- **ProgressViewIOS:** [2019] Deprecated. Use `@react-native-community/progress-view`.
  ```js
  <ProgressViewIOS progressViewStyle="default" progress={0.5} />
  ```
- **SegmentedControlIOS:** [2019] Deprecated. Use `@react-native-segmented-control/segmented-control`.
  ```js
  <SegmentedControlIOS
    values={['One', 'Two', 'Three']}
    selectedIndex={this.state.selectedIndex}
    onChange={event => this.setState({ selectedIndex: event.nativeEvent.selectedSegmentIndex })}
  />
  ```
- **ActionSheetIOS:**
  ```js
  ActionSheetIOS.showActionSheetWithOptions({
    options: ['Cancel', 'Delete', 'Save'],
    cancelButtonIndex: 0,
    destructiveButtonIndex: 1,
    title: 'What do you want to do?',
  }, buttonIndex => { /* handle buttonIndex */ });
  ```
  - iOS only. No Android equivalent — use Alert with buttons on Android.
- **TabBarIOS:** [2019] Removed from React Native core. Use React Navigation `createBottomTabNavigator` instead.
- Platform detection strategies (in preference order):
  1. Separate files: `Component.ios.js` / `Component.android.js` — cleanest, no runtime check.
  2. `Platform.OS` conditional: use for small differences within a shared component.
  3. `Platform.select()`: for style/config objects with platform-specific values.

---

## Ch 11: Android-Specific Components and APIs

- Android-specific components only render on Android. Wrap in `Platform.OS === 'android'` guard or use `.android.js` extension.
- **DrawerLayoutAndroid:**
  ```js
  <DrawerLayoutAndroid
    ref={ref => { this.drawer = ref; }}
    drawerWidth={300}
    drawerPosition="left"          // 'left' | 'right'
    renderNavigationView={() => <DrawerContent />}
    onDrawerOpen={() => {}}
    onDrawerClose={() => {}}
  >
    <MainContent />
  </DrawerLayoutAndroid>
  // Open/close via ref:
  this.drawer.openDrawer();
  this.drawer.closeDrawer();
  ```
  - [2019] Use `createDrawerNavigator` from React Navigation for cross-platform drawer.

- **ToolbarAndroid:** [2019] Deprecated. Use React Navigation header or `@react-native-community/toolbar-android`.
  ```js
  <ToolbarAndroid
    title="App Title"
    titleColor="white"
    actions={[
      { title: 'Search', show: 'always', showWithText: true },
      { title: 'Settings', show: 'never' },
    ]}
    onActionSelected={index => { /* index maps to actions array position */ }}
    navIcon={require('./nav-icon.png')}
    onIconClicked={() => {}}
  />
  ```

- **ViewPagerAndroid:** [2019] Removed from React Native core. Use `react-native-pager-view`.
  ```js
  <ViewPagerAndroid initialPage={0} onPageSelected={e => e.nativeEvent.position}>
    <View key="1"><Text>Page 1</Text></View>
    <View key="2"><Text>Page 2</Text></View>
  </ViewPagerAndroid>
  ```

- **DatePickerAndroid:** [2019] Deprecated. Use `@react-native-community/datetimepicker`.
  ```js
  const { action, year, month, day } = await DatePickerAndroid.open({
    date: new Date(),
    minDate: new Date(),
    maxDate: new Date(2030, 0, 1),
    mode: 'default',   // 'default' | 'calendar' | 'spinner'
  });
  if (action !== DatePickerAndroid.dismissedAction) {
    // year, month (0-indexed), day
  }
  ```

- **TimePickerAndroid:** [2019] Deprecated. Use `@react-native-community/datetimepicker`.
  ```js
  const { action, hour, minute } = await TimePickerAndroid.open({
    hour: 14,
    minute: 0,
    is24Hour: false,
    mode: 'default',
  });
  if (action !== TimePickerAndroid.dismissedAction) {
    // hour (0-23), minute (0-59)
  }
  ```

- **ToastAndroid:**
  ```js
  ToastAndroid.show('Message', ToastAndroid.SHORT);   // SHORT | LONG
  ToastAndroid.showWithGravity('Message', ToastAndroid.LONG, ToastAndroid.CENTER);
  // Gravity: TOP | CENTER | BOTTOM
  ```
  - Android only. Use Alert or custom toast library for cross-platform.

- **BackHandler:**
  ```js
  BackHandler.addEventListener('hardwareBackPress', () => {
    // return true to prevent default back behavior
    return true;
  });
  BackHandler.removeEventListener('hardwareBackPress', handler);
  BackHandler.exitApp();
  ```
  - Android only. React Navigation handles this automatically for navigators.

- **PermissionsAndroid:**
  ```js
  const granted = await PermissionsAndroid.request(
    PermissionsAndroid.PERMISSIONS.CAMERA,
    { title: 'Camera Permission', message: 'App needs camera access' }
  );
  if (granted === PermissionsAndroid.RESULTS.GRANTED) { /* proceed */ }
  // RESULTS: GRANTED | DENIED | NEVER_ASK_AGAIN
  ```
  - iOS permissions set in Info.plist, not runtime API (except via expo-permissions or react-native-permissions).

---

## Ch 12: Building a Cross-Platform App

- **FlatList** — virtualizes large lists. Only renders visible items:
  ```js
  <FlatList
    data={this.state.items}
    renderItem={({ item, index }) => <ItemComponent item={item} />}
    keyExtractor={item => item.id.toString()}
    onEndReached={this.loadMore}
    onEndReachedThreshold={0.5}
    ListEmptyComponent={<EmptyState />}
    ListHeaderComponent={<Header />}
    ListFooterComponent={this.state.loading ? <ActivityIndicator /> : null}
    initialNumToRender={10}
    refreshControl={<RefreshControl refreshing={this.state.refreshing} onRefresh={this.refresh} />}
  />
  ```
  - `keyExtractor` required. Must return unique string per item.
  - `SectionList` variant adds section headers: `sections={[{ title, data: [] }]}`, `renderSectionHeader`.

- **Fetch API:**
  ```js
  fetch('https://api.example.com/endpoint', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ key: 'value' }),
  })
    .then(response => response.json())
    .then(data => this.setState({ data }))
    .catch(error => console.error(error));
  ```
  - Fetch returns Response object. Must call `.json()`, `.text()`, or `.blob()` to read body.
  - Network requests require permissions on Android: `android.permission.INTERNET` (auto-granted for normal network).

- **Modal:**
  ```js
  <Modal
    visible={this.state.showModal}
    animationType="slide"      // 'none' | 'slide' | 'fade'
    transparent={false}
    onRequestClose={() => this.setState({ showModal: false })}  // Android back button
  >
    <ModalContent />
  </Modal>
  ```
  - `onRequestClose` required on Android (hardware back button).

- **ActivityIndicator:**
  ```js
  <ActivityIndicator size="large" color="#0000ff" animating={true} />
  ```
  - `size`: `'small'` | `'large'` | number (Android only for number).

- **Picker:** [2019] Removed from React Native core. Use `@react-native-picker/picker`.
  ```js
  <Picker
    selectedValue={this.state.value}
    onValueChange={(value, index) => this.setState({ value })}
    mode="dropdown"    // Android: 'dialog' | 'dropdown'. iOS: wheel.
  >
    <Picker.Item label="Option 1" value="opt1" />
  </Picker>
  ```

- Container vs. Presentational component pattern [2019]:
  - Container: connected to store/data, passes props to presentational.
  - Presentational: pure UI, no business logic, all props from parent.
  - Modern: hooks dissolve this distinction. `useSelector`/`useDispatch` in any component.

- `navigationOptions` with function form to access navigation prop:
  ```js
  static navigationOptions = ({ navigation }) => ({
    headerTitle: navigation.getParam('title'),
    headerRight: <Button title="Save" onPress={navigation.getParam('onSave')} />,
  });
  // Pass callback via setParams in componentDidMount:
  this.props.navigation.setParams({ onSave: this.handleSave });
  ```

---

## Appendix: Installation

- iOS development requires macOS. Linux/Windows cannot build iOS.
- Required for iOS: Xcode (App Store), Node.js, Watchman, react-native-cli.
- Required for Android on Mac: Node.js, Watchman, Android Studio, react-native-cli.
- Required for Android on Windows: Node.js, Python2, Android Studio, react-native-cli, Watchman (alpha).
- Required for Android on Linux: Node.js, Android Studio, react-native-cli, Watchman.
- [2019] `npm install -g react-native-cli` + `react-native init ProjectName` is the old pattern.
- Modern: `npx react-native@latest init ProjectName` (no global install needed). Or use Expo: `npx create-expo-app ProjectName`.
- Run iOS: `npx react-native run-ios` or open `.xcodeproj` in Xcode.
- Run Android: `npx react-native run-android` (requires Android emulator running or device connected).

---

## Cross-Cutting Patterns

- **Never mutate state directly.** Always `setState` (class) or setter from `useState`.
- **Always provide `keyExtractor`** on FlatList/SectionList. Stable keys prevent reconciliation bugs.
- **`useNativeDriver: true`** on all animations where possible (transform + opacity only).
- **Platform-specific files** (`.ios.js`/`.android.js`) preferred over `Platform.OS` conditionals for large divergences.
- **All APIs marked [2019]** that reference direct imports from `'react-native'` have been extracted to community packages. Check `@react-native-community/` and `@react-native-*` scopes.
- **Class components** throughout the book are [2019] pattern. All class lifecycle methods map to hooks: `componentDidMount` → `useEffect(fn, [])`, `componentDidUpdate` → `useEffect(fn, [deps])`, `componentWillUnmount` → `useEffect` cleanup return.
- **`connect()` from react-redux** is [2019] pattern. Use `useSelector`/`useDispatch` hooks.
- **AsyncStorage, Clipboard, Geolocation, NetInfo** were all in React Native core in 2019. All are now community packages.
