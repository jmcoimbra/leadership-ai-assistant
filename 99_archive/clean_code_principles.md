# Clean Code Principles

**Purpose:** Raw chapter-by-chapter extraction of enforceable rules. Narrative and Java-specific syntax discarded. Universal principles retained.

## Ch 1: Clean Code
- Bad code brought companies down. Code rot is real and compounding.
- Law: Later equals never.
- Total cost of owning a mess: productivity approaches zero asymptotically as mess grows.
- The Grand Redesign in the Sky: rewrite races take years and often fail.
- Boy Scout Rule: Leave the campground cleaner than you found it.
- Clean code definitions: reads like well-written prose, does what you expect, written by someone who cares, has no duplication and uses tiny expressive abstractions.

## Ch 2: Meaningful Names
- Intention-revealing: name answers why it exists, what it does, how it is used.
- Avoid disinformation: `accountList` only if actually a List. Names that vary subtly are traps.
- Meaningful distinctions: no number-series (`a1`, `a2`), no noise words (`ProductInfo` vs `ProductData`).
- Pronounceable: `generationTimestamp` not `genymdhms`.
- Searchable: name length proportional to scope size. Single-letter only in short methods.
- No encodings: no Hungarian, no `m_` prefix, no `I` interface prefix.
- Class names = nouns. Method names = verbs.
- One word per concept across the codebase. Don't pun (same word, different operations).
- Solution domain names OK (CS terms). Problem domain names when no CS term fits.
- Add meaningful context (`addrFirstName`, `addrState`) but don't add gratuitous context (`GSDAccountAddress`).

## Ch 3: Functions
- Small. 4-10 lines. Rarely exceed 20.
- Do one thing. If you can extract another function with a non-restating name, it does more than one thing.
- One level of abstraction per function. Don't mix high and low.
- Stepdown rule: read top-to-bottom. Each function at the next abstraction level down.
- Switch statements: tolerate only in polymorphic factories. Hidden behind abstract interfaces.
- Arguments: 0 best, 1 fine, 2 acceptable, 3 suspect, >3 extract to object.
- Common monadic forms: asking about arg (`isReady(file)`), transforming arg (`fileOpen(name) → InputStream`), event (`passwordAttemptFailed(attempts)`).
- No flag arguments. Boolean param = function does two things. Split.
- Dyadic: `assertEquals(expected, actual)` forces ordering memory. Use named methods or objects.
- No side effects. `checkPassword` initializing session = temporal coupling hidden as side effect.
- Output arguments: confusing. Change state of the owning object instead.
- Command-Query Separation: do or answer, never both.
- Prefer exceptions over return codes. Extract try/catch bodies.
- Error handling is one thing. Function that handles errors should do nothing else.
- DRY: duplication is the root of all evil in software.
- Structured programming (Dijkstra: one entry, one exit) matters less in tiny functions.

## Ch 4: Comments
- Comments compensate for failure to express in code. Always a failure.
- Good: legal, informative, intent explanation, clarification, warning, TODO, amplification, Javadoc for public APIs.
- Bad: mumbling, redundant, misleading, mandated, journal/changelog, noise, position markers, closing brace, attribution/byline, commented-out code, HTML in comments, nonlocal information, too much info, inobvious connection, function header (good name instead).
- "Truth can only be found in one place: the code."

## Ch 5: Formatting
- Formatting = communication. Communication = professional's first order of business.
- Vertical: file size 200-500 lines. Newspaper metaphor (name=headline, synopsis at top, detail increases down).
- Vertical openness: blank lines between concepts.
- Vertical density: tightly related lines close together.
- Vertical distance: variables declared near first use. Instance variables at class top. Dependent functions: caller above callee, close together. Conceptual affinity groups functions.
- Horizontal: under 120 characters. No right-scrolling.
- Horizontal openness: spaces around operators, no space between function name and parenthesis.
- Indentation: never collapse. Even for short if/while.
- Team rules: individual preferences yield to team conventions.

## Ch 6: Objects and Data Structures
- Data abstraction: expose abstract interfaces, not concrete implementation.
- Data/Object anti-symmetry: objects hide data + expose behavior; data structures expose data + have no behavior.
- Procedural: easy to add functions, hard to add types. OO: easy to add types, hard to add functions.
- Law of Demeter: method f of class C calls methods only on: C itself, objects created by f, objects passed to f, instance variables of C. No train wrecks.
- Data Transfer Objects (DTOs): pure data structures. Active Records with business methods = hybrid (bad).

## Ch 7: Error Handling
- Exceptions > return codes. Separate error handling from logic.
- Write try-catch-finally first. Defines scope.
- Use unchecked exceptions. Checked exceptions violate OCP.
- Provide context in exception messages: operation + failure type.
- Define exceptions by caller's needs, not source.
- Special Case pattern: instead of checking for special conditions, create objects that handle them.
- Don't return null. Return empty list, throw exception, use Special Case.
- Don't pass null. Forbid by policy.

## Ch 8: Boundaries
- Wrap third-party code. Don't let Map/Hash/HttpClient leak through public APIs.
- Learning tests: explore third-party APIs through tests. Free documentation that detects upgrade breakage.
- Clean boundaries: depend on what you control. Adapter pattern at the boundary.

## Ch 9: Unit Tests
- TDD Three Laws: (1) no production code until failing test, (2) no more test than sufficient to fail, (3) no more production code than sufficient to pass.
- Test code = production code quality. Dirty tests → discarded tests → code rot → bug explosion.
- Tests enable the -ilities: flexibility, maintainability, reusability. Without tests, every change is a possible bug.
- Clean tests = readability. Build-Operate-Check pattern.
- One concept per test. Multiple asserts OK if all testing the same concept.
- F.I.R.S.T.: Fast, Independent, Repeatable, Self-Validating, Timely.

## Ch 10: Classes
- Organization: public static constants → private static variables → private instance variables → public functions → private utilities called by the public function above.
- Classes should be small (by responsibility count, not line count).
- SRP: one reason to change. 25-word description test (no "if", "and", "or", "but").
- Cohesion: every method uses most instance variables. Small number of variables. When cohesion drops: split.
- OCP: open for extension, closed for modification. New feature = new class, not modified existing.
- Encapsulation: private by default. Protected only for test access, as last resort.

## Ch 11: Systems
- Separate construction from use. Don't mix object wiring with runtime logic.
- Separation of Main: main builds objects, passes to app, app only uses.
- Factories: Abstract Factory for deferred construction decisions.
- Dependency Injection: Inversion of Control for dependency management.
- Scale up, not down. YAGNI for architecture. BDUF (Big Design Up Front) is harmful.
- Cross-cutting concerns (persistence, security, transactions): use aspects/decorators.
- Use standards wisely. Standards enable reuse but can slow adoption.
- Systems need domain-specific languages.

## Ch 12: Emergence
- 4 Rules of Simple Design (in priority order):
  1. Runs all the tests
  2. Contains no duplication
  3. Expresses intent of the programmer
  4. Minimizes number of classes and methods
- Tests drive toward SRP and DIP.
- Refactoring: tests give confidence to clean up. Incremental improvement.
- No duplication: TEMPLATE METHOD pattern for subtle duplication.
- Expressiveness: good names, small functions, standard patterns, tests as documentation.
- Minimal classes/methods: pragmatism over dogma. Lowest priority rule.

## Ch 13: Concurrency
- Decoupling what from when. Structural and throughput benefits.
- Myths: concurrency always improves performance (false), design unchanged (false), container handles it (false).
- Truths: overhead exists, bugs non-repeatable, fundamental design changes needed.
- SRP for concurrency: keep concurrent code separate.
- Limit scope of data shared between threads. Encapsulate.
- Use copies: copy data rather than share it.
- Independent threads: partition data into independent subsets.
- Know your library: thread-safe collections, executor framework, nonblocking solutions, producer-consumer.
- Execution models: Producer-Consumer, Readers-Writers, Dining Philosophers.
- Keep synchronized sections small. One lock, one concern.
- Writing correct shutdown is hard. Think about it early.
- Testing: make code pluggable, make it tunable, run more threads than processors, run on all platforms, instrument with jiggling.

## Ch 17: Smells and Heuristics
- C1: Inappropriate Information (metadata in comments)
- C2: Obsolete Comment
- C3: Redundant Comment
- C4: Poorly Written Comment
- C5: Commented-Out Code
- E1: Build Requires More Than One Step
- E2: Tests Require More Than One Step
- F1: Too Many Arguments
- F2: Output Arguments
- F3: Flag Arguments
- F4: Dead Function
- G1-G36: (36 general smells — see knowledge file for full catalog)
- N1-N7: (7 naming smells)
- T1-T9: (9 testing smells)
