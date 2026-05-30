# Decision Frameworks — Operational Knowledge
> Author: Christian, B., & Griffiths, T. (2016). *Algorithms to Live By* | Source: `99_archive/algorithmic_thinking.md` | Owner: [Brain Owner] | Pillar: Pillar 4 (AI Execution) + Pillar 5 (Play Big) | Last Updated: 2026-05-15

Decision-quality frameworks from computer science applied to leadership work. Two sections: (A) coaching vocabulary for 1:1s and management practice, (B) self-application heuristics for own scheduling, prediction, and team-policy design.

Cross-loaded by `weekly-review`, `devils-advocate`, `management-lens`, `meeting-prep`, `decision-protocol`, `product-diagnostic`. Not a standalone skill. Frameworks compound into existing skills.

**Layer separation.** `decision-protocol` is the agent's runtime behavior when surfacing decisions in a session (Confusion Protocol, Completeness Scoring). `product-diagnostic` is the initiative-discovery gate (six forcing questions). This file is the doctrinal source they cite. The skill is the behavior; this file is the principle.

## A. Coaching Vocabulary

### Process vs Outcome ("Computational Stoicism")

Even the optimal decision algorithm fails sometimes. The 37% Rule fails 63% of the time *at the optimum*. UCB still has regret — just minimal regret.

**Coaching prompts:**
- "Did you follow the optimal process? Outcomes can be exogenous."
- "What would change about your decision if the outcome had gone the other way?"
- "Is the criticism about the bet, or about how the dice rolled?"

**Anti-pattern to watch:** Reports blaming themselves for non-clairvoyance. Or, conversely, claiming credit for a good outcome from a sloppy process.

### Procrastination as Wrong-Metric Optimization

Pre-crastination experiments show people grab the closer bucket and carry it the full distance — "hastening subgoal completion." App badges force unweighted SPT (sum of tasks done), causing easy-tasks-first behavior even when impact-per-task differs by 10x.

**Coaching prompts:**
- "Are you optimizing for # of tasks done, or for total impact delivered?"
- "What metric does your tooling default-show you? Is that the metric you actually care about?"
- "If you used the 2x rule (only prioritize a task that takes 2x as long if it's 2x as important), what gets bumped?"

**Anti-pattern:** Calling reports "lazy" or "scattered" when they're following an optimal algorithm for the wrong metric.

### Priority Inversion → Priority Inheritance

When report A blocks on report B for a hotfix, the fix is **priority inheritance**: B's review *temporarily* inherits hotfix priority. Stacking the hotfix queue without elevating B does nothing.

**Coaching prompts:**
- "Who's blocked on whom right now?"
- "What's the lowest-priority work currently sitting on a high-priority resource?"
- "If we elevate the blocker for one day, does the bottleneck clear?"

**Mars Pathfinder origin** worth knowing for credibility. JPL diagnosed and patched the rover from 309 million miles away.

### Marshmallow Trust Signal

Walter Mischel's marshmallow test isn't pure willpower. Kids with unreliable adult experimenters ate the marshmallow earlier — they had a power-law prior on adult disappearance time. Self-control is calibrated to environment trust.

**Coaching read:**
- Reports who stop bringing problems may have learned that adults disappear when problems land. Check for prior priority-inversion of attention.
- Reports who push back hard on commitments may have a power-law prior on management follow-through.

**Anti-pattern:** Reading low engagement as character flaw rather than rational response to history.

### Single Elimination Silver-Medal Lie

In an NCAA-style bracket, only the gold is determined. Silver-medal "second-best" is the team that happened to lose the final — not the actual second-best.

**Coaching application:**
- Don't update talent judgment on a single signal event (one bad PR, one tough customer call). Use Comparison Counting Sort: cumulative season data.
- Robust > efficient when noise is high. Junior engineers, early-career performers — judge them on the regular season, not one game.

### Win-Stay, Lose-Shift Anti-Pattern

Switching arms after a single failure is too rash. "Imagine going to a restaurant a hundred times, each time having a wonderful meal. Would one disappointment be enough to give up on it?"

**Coaching application:**
- Don't penalize good options too strongly for one disappointment. (Veteran engineer's one bad sprint, partner's one missed deadline.)
- Use UCB framing: an option's plausible upper bound matters more than recent point estimate.

## B. Self-Application Heuristics

### Pick Metric Before Strategy

Single-machine total time is order-invariant. Order only matters once you pick which metric to minimize:

| Metric | Algorithm | When to use |
|---|---|---|
| Max lateness (worst customer wait) | Earliest Due Date | SLO-style commitments |
| # of late tasks | Moore's Algorithm (drop biggest item that goes late) | When throughput matters more than perfection |
| Sum of completion times | Shortest Processing Time | "Get the to-do list shorter, fast" |
| **Sum of weighted completion times** | **Weighted SPT** (importance ÷ duration, descending) | **Default. Closest thing to a Swiss Army knife.** |

**Heuristic:** "Only prioritize a task that takes 2x as long if it's 2x as important."

### Three Prediction Rules per Distribution

Identify the distribution before forecasting cycle time, MTTR, promotion timeline, deal close, recovery from incident.

| Distribution | Examples | Rule | Predict |
|---|---|---|---|
| **Power-law** | Wealth, city size, movie grosses, hold times, viral spread, cycle time of stuck tickets | Multiplicative | constant × current value (longer waits = longer expected total) |
| **Normal** | Life span, height, runtime of typical movie, standard sprint cycle | Average | distribution mean (early surprises early; late events overdue) |
| **Erlang** | Radioactive decay, politician tenure, gambling, debugging-stuck-on-hard-bug | Additive | constant + current — memoryless. "Five more minutes" is correct. |

**Stephen Jay Gould's cancer:** the median was 8 months, but distribution was right-skewed power-law. He lived 20 years.

**Application:** Most engineering work is power-law. Multiplicative Rule. If a ticket has been open for 3 weeks, expect 3+ more weeks, not "should close any day now."

### Optimal Stopping Defaults

| Situation | Algorithm |
|---|---|
| No data on candidate quality | 37% Rule (Look-Then-Leap). 63% failure rate at optimum is intrinsic. |
| Have percentile data (rubric, market comp) | Threshold Rule. Reject below; hire above. No look phase. |
| Selling a house / closing a deal | Set threshold from cost-of-waiting; never lower it. Past offers are sunk cost. |
| Quitting while ahead | Burglar problem. Stop after roughly (success_rate / failure_rate) attempts. |
| Triple-or-nothing games (no optimal stop rule) | Refuse. Some problems are better avoided than solved. |

### Caching: LRU + Multi-Tier

- **Eviction:** Least Recently Used beats FIFO and Random in real-world workloads.
- **Don't fight the pile.** A horizontal pile or a Noguchi Filing System (always insert at left) is provably within 2x of clairvoyant optimal for self-organizing lists.
- **Geographic caching:** Place tools/info near point of use. Anticipatory pre-fetch beats on-demand search.
- **"Cognitive decline" reframe:** "Brain fart" is a cache miss. The retrieval gets harder as the cache gets fuller. Coaching language for senior engineers feeling slower.

### Thrashing Detection + Cure

**Symptoms:**
- Panic-by-hyperactivity. Can't even list what you should be doing.
- "I just need to write down everything I'm supposed to be doing, but I don't have time."
- Productivity falls off a cliff edge, not gradually.

**Cures (in order):**
1. Get more memory (rare luxury — protected calendar blocks).
2. Learn to say no. Refuse new work that exceeds working set.
3. Work dumber. Random-order processing beats prioritization-thinking when in thrash. Pick whatever is on top.
4. Interrupt coalescing. Batch all interruptions into office hours / weekly meetings. Already encoded as a Hard Constraint.

### Overfitting + Early Stopping

- **More factors ≠ better predictions.** A 9-factor model fits 8 data points perfectly *and* gyrates wildly with tiny noise.
- **Sketch with a Sharpie, not a ballpoint.** For early-stage strategy and uncertain forecasts, broad strokes win.
- **Cross-validate every KPI** against an orthogonal qualitative signal. Standardized tests + occasional oral exams. Cycle time + skip-level themes.
- **"The company will build whatever the CEO decides to measure."** Pick metrics carefully; they overfit.
- **Training scars:** Repetitive drills produce overfitting to drill conditions. Cross-train with novel-scenario tabletops.

### Relaxation for Stuck Problems

Three ways to make intractable problems tractable:

1. **Constraint Relaxation.** "What if you couldn't fail?" / "What if we had 2x headcount?" Use the answer as a *bound*, not a fantasy.
2. **Continuous Relaxation.** Turn binary into gradient (full/none → fractional or probabilistic). Round at the end.
3. **Lagrangian Relaxation.** "Or else what?" Replace hard rules with costs. "We never miss sprint commits" → "Each missed commit costs Y planning time."

### Randomness as a Tool

- **Bloom filter / Monte Carlo:** Trade certainty for time + space. "Good enough at scale" > perfect at small scale.
- **Hill climbing alone gets stuck.** Add jitter (small random walks), Random Restart (re-roll from scratch), or Metropolis (sometimes accept worse).
- **Simulated Annealing:** Front-load randomness, cool down over time. Match temperature to project phase. Heat up early-quarter ideation; cool toward execution.
- **Three rules** (from the Dice Man cautionary tale):
  1. Always act on good ideas.
  2. Probability of acting on a bad idea ~ inversely proportional to how bad it is.
  3. Front-load randomness; anneal over time.

### Networking: Backoff + AIMD

- **Exponential Backoff** > "three strikes you're out." Doubling wait times on failure. Never give up entirely.
- **HOPE program (Hawaii probation)**: small immediate accountability + exponential ramp. 50% reduction in re-arrest, 72% in drug use. Beats rare-large penalties.
- **AIMD as career architecture.** Sawtooth promotion (some up, some back) is more resilient than monotonic up-or-out. Counter to Peter Principle's stagnation.
- **Bufferbloat:** "We're not always connected; we're always buffered." Tail Drop > infinite buffering. Auto-reject at overload.
- **Latency > bandwidth for interactive use.** Incident comms favor fast-and-noisy over clear-but-delayed.

### Game Theory + Mechanism Design

- **Avoid leveling wars.** Play one level above opponent in negotiation; don't recurse three levels deep.
- **Find dominant strategies.** When honesty is dominant (Vickrey auction, well-designed performance review), you don't need to recurse.
- **Mechanism Design over coaching.** Bad team equilibria (race-to-bottom on hours, weekend Slack) require rule changes, not exhortation. The Godfather worsens defection's payoff to fix the equilibrium.
- **Information cascade.** Actions ≠ beliefs. Approvals chain without independent analysis. Counter: capture explicit dissent, require independent review before reading prior reviewers' notes.
- **Vacation policy:** Floor (mandatory minimum) > ceiling (unlimited). The unlimited policy creates a race to zero.
- **Compulsory floors > carrot bonuses.** The Evernote $1k vacation bonus didn't change the game.

**Composes with `product-diagnostic`.** Q1 red flags ("[Your CDO] likes it / [Your CTO] is supportive / survey said 4.2/5") are Information Cascade in operational form: public-data exceeding private-data, leadership endorsement mistaken for demand. When the diagnostic verdict is "this is a behavior problem, not a build problem," the fork to follow is Mechanism Design (rule change) rather than another initiative.

### Computational Kindness

Minimize the labor of thought you impose on others. Verification is easier than search.

- **State preferences first.** "Personally I lean toward X, what do you think?" beats "I'm flexible, you decide."
- **Reduce options offered, don't maximize.** Two restaurants > ten.
- **Cognitive subsidy in design.** Bus-arrival display > "next bus eventually." Helix parking lot > lane grid. Internal dashboards show next-state, not raw data requiring inference.
- **Blocking > spinning.** Restaurant policy: take name + call when ready. Don't make people hover.
- **Skip-level prep:** offer 2-3 specific topics, not "what's on your mind."

**Operationalized by `decision-protocol`.** The Confusion Protocol pattern (STOP, name in one sentence, present 2-3 options, state the read) IS Computational Kindness for AI-to-human option presentation. The "My read" line is the agent applying "state preferences first." The 2-3 cap is the agent applying "reduce options, don't maximize." Completeness X/10 is cognitive subsidy: pre-computing the coverage tradeoff so the user verifies instead of searches.

## Persona-Anchored Product Consultation

When asked to answer open questions in a product doc (RFC, scope proposal, MVP spec), anchor every answer to the actual end-user persona before evaluating the doc's recommendations. If the doc cites a benchmark (e.g., shadcn-studio, Stripe Dashboard, Linear) whose audience differs from the product's audience, expect defaults to flip on UX-affordance questions (visibility, undo, confirmation, error tolerance).

**Test:** for each recommendation, ask "does this default assume the benchmark's user or the product's user?" If the answer is the benchmark's user, re-derive.

**Heuristic flips for non-tech end users vs developer-audience benchmarks:**
- Silent confirmation becomes small non-blocking toast
- Ship-in-editor-without-consumer becomes hide-until-consumer-exists
- Per-group reset only becomes also-ship-a-global-reset
- AAA tiers, OKLCH-editable, power-user affordances become display-only readouts with hex-canonical inputs

Source: 2026-05-15 JULI-139 MVP scope consult. 3 of 12 doc recommendations flipped under non-tech merchant persona (Q4 Destructive token visibility, Q7 Apply toast, Q8 global reset). The doc benchmarked shadcn-studio (dev audience); the product is [your-product-ui] (marketer audience).

## Source

Re-derive depth from the private books database when configured. Raw distillation: `99_archive/algorithmic_thinking.md`.
