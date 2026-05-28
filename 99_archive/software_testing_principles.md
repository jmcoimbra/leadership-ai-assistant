# Software Testing Principles
> Source: Myers, G. J., Sandler, C., & Badgett, T. (2011). *The Art of Software Testing*, 3rd ed. Wiley. | Owner: [Brain Owner] | Pillar: Pillar 4 (AI Execution) | Last Updated: 2026-05-08

Distilled doctrine from 11 chapters. Knowledge file landed at `99_archive/software_testing_principles.md` under the testing category. Cross-link to existing `testing-infrastructure.md`. Reinforces QE-as-enabler Hard Constraint with primary-source authority.

## Ch 2 — The Psychology and Economics of Software Testing

**Core thesis:** Define testing as "the process of executing a program with the intent of finding errors." NOT "demonstrating absence of errors." The definition is psychological, not semantic. People work toward the goal they are given. Goal "find errors" produces high-yield test data; goal "show it works" produces low-yield data.

**A "successful" test case finds an error.** Same inversion as the medical analogy: a lab test is successful when it locates the disease, not when it returns clean.

**Exhaustive testing is impossible.** Black-box exhaustive (every input combination) → infinite. White-box exhaustive (every path) → ~10^14 paths in a 20-statement loop program. Neither is feasible. Therefore the question becomes: **what subset of test cases has the highest probability of finding the most errors?**

### The 10 Vital Testing Principles

1. **A necessary part of a test case is a definition of the expected output or result.** Without it, "the eye sees what it wants to see" and you accept plausible-but-wrong output as correct.
2. **A programmer should avoid attempting to test his or her own program.** The constructive mindset (designing) cannot easily flip to the destructive mindset (testing). Author also carries forward any misunderstanding of the spec.
3. **A programming organization should not test its own programs.** Schedule pressure and cost objectives are easy to measure; reliability is hard. The org will optimize for what it can measure, against testing.
4. **Any testing process should include a thorough inspection of the results of each test.** Errors found in later tests were often missed in earlier results.
5. **Test cases must be written for invalid and unexpected input conditions, as well as valid and expected.** Invalid-input cases tend to have higher error-detection yield than valid-input cases.
6. **Examining a program to see if it does not do what it is supposed to do is only half the battle.** The other half is checking for unwanted side effects (extra paychecks, overwritten records).
7. **Avoid throwaway test cases unless the program is truly throwaway.** Save and rerun them as regression tests.
8. **Do not plan a testing effort under the tacit assumption that no errors will be found.** This mistake is the root of underestimated test schedules and resources.
9. **The probability of more errors in a section of a program is proportional to the number of errors already found in that section.** Errors cluster. Focus additional testing effort on error-prone modules.
10. **Testing is an extremely creative and intellectually challenging task.** Testing a large program often requires more creativity than designing it.

## Ch 3 — Program Inspections, Walkthroughs, and Reviews

**Core thesis:** Human (noncomputer) testing finds 30-70% of logic-design and coding errors before computer testing begins. Inspections and walkthroughs work because they apply Principle 2 (someone else reads the code).

**Inspection team (4 people):**
- Moderator (quality-control engineer; not the author; runs the session, records errors, ensures correction)
- Programmer (the author)
- Designer (if different from programmer)
- Test specialist

**Inspection agenda:**
1. Programmer narrates the code statement-by-statement. Reading aloud is itself a remarkable error-detection technique. Author often finds many errors during own narration.
2. Program is analyzed against a checklist of historically common error categories.

**Inspection rules:**
- 90-120 minutes per session is optimal. Mentally taxing.
- ~150 statements per hour. Larger programs = multiple inspections.
- Goal is to FIND errors, not FIX them. Author corrects after.
- Confidential. Not used for performance management of the author. If managers use results to evaluate competence, the inspection becomes adversarial.
- The error-prone-section identification is itself a side benefit: tells you where to focus computer-based testing.

**Error checklist categories (Myers framework):**
- **Data reference:** uninitialized variables, array bounds, dangling pointers, alias names with mismatched attributes, off-by-one indexing
- **Data declaration:** undeclared variables, default attribute confusion, similar-named variables (VOLT vs VOLTS), incorrect length / data type
- **Computation:** mixed-mode arithmetic, overflow / underflow, divide-by-zero, base-2 representation rounding, operator precedence assumptions
- **Comparison:** mixed-type comparisons, "at most / at least / less than or equal" confusion, Boolean / comparison operator mixing (`2<i<10` vs `(2<i)&&(i<10)`), short-circuit evaluation traps
- **Control-flow:** non-terminating loops, off-by-one iteration counts, missing closing brackets, nonexhaustive decisions
- **Input/output:** file open errors, end-of-file handling, format-spec mismatch
- **Other:** see book

## Ch 4 — Test-Case Design

**Core thesis:** The most important single consideration in testing. Random-input testing has the lowest yield. **The strategy is to combine black-box and white-box methods.**

### Black-box techniques (data-driven, spec-based)

- **Equivalence partitioning.** Divide input domain into classes such that a test of any element of a class is representative. Two types: valid equivalence classes and invalid equivalence classes. Heuristics:
  - Range of values → 1 valid + 2 invalid (below range, above range)
  - Number of values → 1 valid + 2 invalid (zero, more than max)
  - Set of input values → 1 valid per element + 1 invalid (something not in set)
  - "Must-be" condition → 1 valid + 1 invalid
  - Process: assign unique number to each class, then write minimum test cases covering all valid classes, then 1 test case per invalid class (don't combine invalid conditions; one masks the other).

- **Boundary value analysis.** Test ON the edges, JUST INSIDE, and JUST OUTSIDE each equivalence class. ALSO test output equivalence-class boundaries, not just input. Heuristics:
  - Range 1-999 → test 0, 1, 999, 1000
  - Range -1.0 to 1.0 → test -1.0, 1.0, -1.001, 1.001
  - Each output condition → same treatment
  - Ordered sets → test first and last elements
  - "Boundaries are subtle. Identification requires thought." Boundary value analysis is one of the most useful test-case design methods, but often used ineffectively because it sounds simple.

- **Cause-effect graphing.** Translate spec into a Boolean digital-logic graph. Cause = distinct input condition. Effect = output condition or system transformation. Annotate with constraints (E exclusive, I inclusive, O one-only, R requires, M masks). Trace into a limited-entry decision table; each column is a test case. Side benefit: pointing out incompleteness and ambiguity in the spec.

- **Error guessing.** Intuitive technique. Enumerate likely errors: empty list, list of one, all-same-values, already-sorted, off-by-one boundaries, zero values forced, unexpected end-of-file. Often complementary to systematic methods.

### White-box techniques (logic-driven, code-based)

| Criterion | What it requires |
|---|---|
| **Statement coverage** | Every statement executed at least once. Weakest. Generally useless. |
| **Decision (branch) coverage** | Each decision takes both true and false outcomes at least once. Better but misses condition errors inside compound decisions. |
| **Condition coverage** | Each condition in a decision takes all outcomes at least once. Doesn't always satisfy decision coverage. |
| **Decision/condition coverage** | Both. Still doesn't catch masking. |
| **Multiple-condition coverage** | Every combination of condition outcomes in each decision. The strongest. Fewer test cases than path coverage but catches more errors than condition coverage. |

### The strategy (combination)

1. If the spec contains combinations of input conditions, start with **cause-effect graphing**.
2. Use **boundary value analysis** for input AND output boundaries.
3. Identify **valid and invalid equivalence classes** for input AND output. Supplement.
4. Use **error guessing** to add more.
5. Examine the program's logic against the test set. If multiple-condition coverage isn't satisfied, add more.

**No methodology guarantees finding all errors.** This is a reasonable compromise, requires hard work.

## Ch 5 — Module (Unit) Testing

**Core thesis:** Test individual modules before testing the whole. Module testing is largely white-box (you have the source), supplemented by black-box from the module's spec.

**Three motivations:**
1. Manage combinatorial complexity by isolating units.
2. Ease debugging — when an error appears, you know which module.
3. Enable parallelism — test multiple modules simultaneously.

**Incremental beats nonincremental.** Nonincremental ("big bang") testing combines everything before testing. Incremental — top-down or bottom-up — adds and tests one module at a time. Advantages of incremental:
- Less effort per test (tests grow gradually)
- Earlier integration error detection
- Easier debugging (the new module is the suspect)
- More opportunities to test interactions

### Top-Down vs Bottom-Up

**Top-down:** Start with the entry module. Replace called modules with stubs. Replace stubs with real modules incrementally.
- **Advantage:** Early skeletal program enables demos, morale, design validation.
- **Disadvantages:** Stub modules are surprisingly complex (must return realistic test data, sometimes multiple versions for multiple test cases). Difficult to feed test data through intervening modules to deeper modules. Difficult to observe outputs from deep modules.

**Bottom-up:** Start with terminal (leaf) modules. Build driver modules. Replace drivers with real callers incrementally.
- **Advantage:** Driver modules are usually easier than stubs. Test conditions easier to create. Output easier to observe.
- **Disadvantage:** No skeletal working program until the last module is added.

**Myers's recommendation:** Bottom-up generally has the edge, but the choice depends on where you expect the most errors (top vs bottom). Available tooling (test tools that eliminate driver need but not stub need) tilts toward bottom-up.

## Ch 6 — Higher-Order Testing

**Core thesis:** Module testing is just the start. Higher-order testing maps to development phases, each catching errors made during a specific translation.

**Software development = chain of translations:** requirements → objectives → external spec → system design → module design → code. Most errors come from translation breakdowns.

**Each test phase has a specific purpose:**
- **Module test:** find discrepancies between a module and its interface spec.
- **Function test:** find discrepancies between the program and the external spec. Usually black-box. Equivalence partitioning, boundary value analysis, cause-effect, error guessing apply directly.
- **System test:** find discrepancies between the program and its **original objectives**. NOT a re-test of features. The hardest test phase. No formal methodology; requires creativity.
- **Acceptance test:** customer's responsibility. Compare the program against contract / use cases.
- **Installation test:** the org that produced the system delivers tests that run after install (verify config, file existence, hardware compatibility).

### 15 Categories of System Test (Myers)

| Category | Description |
|---|---|
| Facility | Each objective is implemented |
| Volume | Abnormally large data |
| Stress | Peak concurrent load over short span |
| Usability | End-user can interact effectively |
| Security | Subvert security measures |
| Performance | Response and throughput meet objectives |
| Storage | Memory and disk managed correctly |
| Configuration | Recommended configurations work |
| Compatibility / Conversion | Backward / forward compatibility |
| Installation | Installation works on all platforms |
| Reliability | Uptime, MTBF |
| Recovery | Recovery facilities work as designed |
| Serviceability / Maintenance | Telemetry for support |
| Documentation | User docs are accurate |
| Procedure | Operational procedures work |

### Test Planning (12-Component Checklist)

1. Objectives. Per phase.
2. Completion criteria. Per phase.
3. Schedules. Per phase.
4. Responsibilities. Designers, writers, executors, verifiers, fixers, arbitrator.
5. Test case libraries and standards.
6. Tools. Acquisition / development plan.
7. Computer time. Per phase.
8. Hardware configuration. Per phase.
9. Integration. Order of integration; scaffolding plan.
10. Tracking procedures. Error-prone-module location, schedule progress, completion-criterion progress.
11. Debugging procedures. Reporting, tracking, fix integration.
12. Regression testing. Plan for who, how, when after each fix or feature.

### Completion Criteria

**Bad criteria:**
- "Stop when scheduled time expires" → trivially satisfied by doing nothing.
- "Stop when all test cases pass" → encourages tests with low error-detection probability.

**Good criteria (combine):**
1. Test-case-design-method completion (e.g., multi-condition coverage + boundary value analysis, all unsuccessful).
2. **Predefined number of errors detected.** Estimate total errors via industry averages (4-8 errors per 100 statements pre-inspection), seeded errors, or two-team comparison. Set targets per phase (e.g., module test = 65% of coding/logic errors found).
3. **Errors-per-unit-time graph.** Plot detection rate. Climbing → don't stop. Plateau or decline → consider phase transition.

### Independent Test Agency

The most extreme application of Principle 3. A separate org (or company) tests so they are not subject to the development org's schedule pressure. Advantages: motivation, healthy competition, removed from management influence, specialized knowledge. The [Your Company] QE function is positioned for this — pairing with engineering, never reporting into engineering.

## Ch 7 — Usability (User) Testing

**Core thesis:** Test that real users can use the product. Distinct from functional correctness. Usability testing predates the broader UX movement and Myers treats it as a system-test category.

**Process:**
- Identify user-facing functions
- Recruit representative users
- Observe (don't intervene)
- Capture errors, hesitations, confusions
- Iterate

## Ch 8 — Debugging

**Core thesis:** Debugging starts after a successful test case. Two steps: locate the error (95% of the work) and fix it. The locating phase is mentally taxing and rarely formally taught.

### Brute-force debugging methods (least preferred)

- **Storage dump.** Static, irrelevant data flood, no methodology. Worst.
- **Scattered print statements.** Better than dump (dynamic, source-related), but hit-or-miss, modifies the program (potentially masking timing or introducing bugs).
- **Automated debugging tools (breakpoints, watch variables).** Tool-assisted version of print debugging. Still hit-or-miss without thinking.

**Brute force ignores thinking.** "Murder mysteries are solved by analysis of clues, not by setting up roadblocks." Recommend brute force only as a supplement, not a substitute, for thought.

### Thinking debugging methods

- **Induction.** From clues to general theory.
  1. Locate pertinent data (what worked, what didn't, what test cases caused it, what test cases didn't)
  2. Organize data (what / where / when / to-what-extent, IS / IS-NOT contradictions)
  3. Devise hypothesis (look for patterns and contradictions)
  4. Prove hypothesis (compare to ALL clues, not just some)
  5. Fix the problem (and regression test)
- **Deduction.** From general suspects to one cause via elimination + refinement.
  1. Enumerate possible causes
  2. Use data to eliminate
  3. Refine the remaining hypothesis
  4. Prove
  5. Fix
- **Backtracking.** Start at the wrong output, work backward through the logic until the state was last correct. Effective for small programs.
- **Debugging by testing.** Slim test cases (one condition each) targeted at the suspected error. Different from "fat" testing test cases.

### Debugging Principles (Error-Repairing)

- **Where there is one bug, likely another nearby.** Errors cluster (Principle 9 again). Examine the vicinity.
- **Fix the error, not just a symptom.** If the proposed fix doesn't explain ALL the clues, you're patching a symptom.
- **The probability of the fix being correct is NOT 100%.** Test the fix. Test for new bugs.
- **The probability of the fix being correct DROPS as the program grows.** In one widely used large program, 1 of every 6 new errors was an error in a prior correction.
- **Beware: a correction can introduce a new error.** Run regression tests after every fix.
- **Error repair = temporarily back into the design phase.** Same rigor (inspection, walkthrough) applies to fixes as to original code.
- **Change the source code, not the object code.** Object-code patches are sloppy and re-emerge on next compile.

### Error Analysis (the underdone but valuable practice)

Periodic post-mortem on detected errors:
- Where was the error made?
- Who made the error? (For education, not punishment.)
- What was done incorrectly?
- How could the error have been prevented?
- Why wasn't the error detected earlier?
- How could the error have been detected earlier?

## Ch 9 — Testing in the Agile Environment

**Core thesis:** Agile and XP elevate testing into a continuous, customer-collaborative activity. Tests are written first; code passes them. Automated testing is mandatory; manual testing is exploratory only.

**Key claims:**
- Customer involvement throughout, not just at acceptance.
- Unit tests written before code (TDD pattern).
- Acceptance tests defined by customer use cases.
- Tests run on every change. Testing is integrated, not a phase.
- Pair programming applies inspection-style review continuously.
- Automation is a hard constraint, not a nice-to-have.

## Ch 10 — Testing Internet Applications (sampled, dated content)

E-commerce architecture, browser compatibility, web-specific challenges (security, latency, SEO). Most of this is dated to 2011 web. Skip for direct ingestion. Useful patterns: test plan should explicitly account for browser / device / network configuration variability.

## Ch 11 — Mobile Application Testing (sampled, dated content)

Mobile-specific challenges (varied hardware, varied networks, battery, sensor, location, store-submission). Dated. Useful patterns: device matrix planning, simulator vs real device coverage, store-rejection failure modes. Already encoded in [Your Company] [Mobile Team] testing infrastructure for [mobile-app-repo].

## Conclusion — The Testing Doctrine

The 10 principles, the test design strategy (cause-effect → boundary → equivalence → error guess → multi-condition coverage), the higher-order test phase mapping, and the debugging discipline together define a coherent QE doctrine. Myers (1979 first edition, 2011 third) remains the primary source for QE-as-enabler thinking. Subsequent books (TDD, Agile testing, BDD) operate downstream of these principles.
