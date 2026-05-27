# Algorithmic Thinking for Decisions
> Source: Christian, B., & Griffiths, T. (2016). *Algorithms to Live By: The Computer Science of Human Decisions*. Henry Holt and Co. | Owner: [Brain Owner] | Pillar: Pillar 4 (AI Execution) + Pillar 5 (Play Big) | Last Updated: 2026-05-08

Distilled doctrine from 11 chapters + Conclusion. Each section: framework + when it applies + [Your Company]-specific application. No narrative.

## Ch 1 — Optimal Stopping

**Core problem:** When to stop looking and commit.

**Algorithms:**
- **37% Rule (Look-Then-Leap)** — no-information case. Look at first 37% noncommittally, then leap on first option that beats everything seen. Optimal success rate: 37%. Failure rate at optimum: 63%. Failure rate is intrinsic, not a process flaw.
- **Threshold Rule** — full-information case. With percentile data, no look phase needed. Set threshold based on remaining options. Success rate jumps to 58%.
- **House-selling variant** — set threshold from cost-of-waiting analysis, never lower. Past offers are sunk cost.
- **Burglar problem** — stop after roughly (success_rate / failure_rate) attempts. 90% success → stop after 9.
- **No optimal stopping rule exists** for "triple-or-nothing" — average gains rise forever but eventual loss is certain. Some problems are better avoided than solved.

**People stop early.** ~80% of subjects leap before the 37% mark. Time costs explain it: in real life, every search has a clock cost.

## Ch 2 — Explore/Exploit

**Core problem:** New thing or known-good thing. Multi-armed bandit.

**Algorithms:**
- **Win-Stay, Lose-Shift (Robbins)** — heuristic, beats chance. Loses on long horizons because lose-shift is too rash.
- **Gittins Index** — optimal under geometric discounting. Untested option (0-0) has index 0.7029 — *higher than a 7-of-10 winner*. Exploration bonus is mathematically real.
- **Upper Confidence Bound (UCB)** — "optimism in the face of uncertainty." Pick the option with the highest plausible upper-bound. Easier to compute than Gittins, no discount assumption.
- **Regret-Minimization Framework** — project to age 80, minimize regret of "didn't try."
- **Restless bandit (world changes):** never fully stop exploring. Intractable in general.

**Interval makes the strategy.** Short interval → exploit. Long interval → explore. Hollywood sequels = signal of end-of-interval. Childhood = exploration license; senior = exploit license.

**Regret minimum is logarithmic** — best you can do; first decade's mistakes equal next century's combined.

## Ch 3 — Sorting

**Core problem:** When and how to make order.

**Algorithms:**
- **Bubble Sort / Insertion Sort** — O(n²). Don't.
- **Mergesort** — O(n log n). Optimal for comparison-based. Parallelizable.
- **Bucket Sort** — O(n) when distribution is known. Knowledge of material beats algorithm.
- **Comparison Counting Sort (Round-Robin)** — O(n²) but **most robust to noise**. Each item compared to all others.

**Diseconomies of scale.** Sorting 100 books takes longer than sorting two batches of 50. Smaller, more frequent batches always win.

**"Sort is prophylaxis for search."** Only sort if you'll search. "Sorting something you'll never search is a complete waste; searching something you never sorted is merely inefficient."

**Single Elimination — silver medal is a lie.** Only the gold is determined; second-best could be anyone the gold beat. NCAA tournament's 12% chance of crowning the actual best team (with 70% game certainty over 6 rounds).

**Race vs fight.** Cardinal numbers (measurable performance) avoid pairwise comparison. Money/GDP/Fortune 500 = scaling devices. Pecking orders are violence preempting violence; debeaking chickens worsens chaos.

## Ch 4 — Caching

**Core problem:** What to keep close, what to evict.

**Algorithms:**
- **Bélády's Algorithm** — clairvoyant optimal: evict whichever item we'll need furthest in the future. Impossible.
- **LRU (Least Recently Used)** — closest to clairvoyant in practice. "Best guide to the future is a mirror image of the past."
- **FIFO** — worse than LRU. Don't use Stewart's "how long have I had it" — use "when did I last use it."
- **Random Eviction** — surprisingly not bad; just having a cache is most of the win.

**Memory hierarchy.** Small/fast → large/slow. Multi-tier caching is multiplicatively better than single-cache.

**Geographic caching.** Akamai/CDN: proximity is itself a cache layer. Amazon anticipatory shipping = pre-populate regional caches. Place tools/info near point-of-use.

**Noguchi Filing System.** Always insert at left, search from left. Equivalent to LRU on a horizontal box. **Optimal for self-organizing lists** (Sleator-Tarjan 1985: never more than 2x clairvoyant).

**A pile of papers is a self-organizing optimal LRU.** Top of pile = front of LRU. Stop apologizing for the pile.

**Forgetting curve = optimal tuning.** Anderson + Schooler: word-frequency-over-time in NYT headlines mirrors Ebbinghaus's forgetting curve. The brain is optimally tuned to the world. **"Cognitive decline" is mostly larger search space, not deterioration.** "Cache miss," not "brain fart."

## Ch 5 — Scheduling

**Core problem:** Order of single-machine tasks.

**Hardest insight first:** With one machine and the same task set, total time is identical regardless of order. **Pick your metric before your strategy.**

**Algorithms by metric:**
- **Earliest Due Date (EDD)** — minimizes max lateness. Optimal for "no customer waits too long."
- **Moore's Algorithm** — minimizes # of late tasks. Drop the biggest item that goes late.
- **Shortest Processing Time (SPT)** — minimizes sum of completion times. "Get stuff done." Reduces list length fastest.
- **Weighted SPT** — divide importance by duration; work highest density first. **Closest thing to a Swiss Army knife in scheduling theory.** Heuristic: "Only prioritize a task that takes 2x as long if it's 2x as important."
- **Debt avalanche** (highest interest) vs **snowball** (smallest balance) = weighted vs unweighted SPT.

**Procrastination is wrong-metric optimization.** Pre-crastination experiment: people grab the closer bucket and carry it the full distance, "hastening subgoal completion." App badges force unweighted SPT — turn them off.

**Priority inversion (Mars Pathfinder).** Low-priority task holding a resource needed by high-priority task. Fix: **priority inheritance** — block-er momentarily inherits the priority of the block-ee.

**Precedence constraints make most problems intractable** (84% of scheduling problems are intractable; only 9% have efficient solutions).

**Preemption + uncertainty.** Even without knowing arrival times, preemptive EDD and preemptive Weighted SPT are still optimal. **Clairvoyance is sometimes a burden.** "Replace 'plan' with 'guess' and take it easy."

**Context switch cost is real.** Thrashing: full-tilt with zero throughput. It's a cliff edge, not gradual. Symptoms: panic-by-hyperactivity, unable to even list what you should be doing.

**Cures for thrashing:**
- Get more memory (rare luxury for humans)
- Learn to say no (refuse new work that would exceed working set)
- Work dumber (random/visual task order beats prioritization in thrashing state)
- Interrupt coalescing — batch interruptions

**Responsiveness vs throughput.** Minimum slice rule (pomodoro/timeboxing) — refuse to subdivide attention below the slice. **"Be no more responsive than required."** Office hours, weekly meetings = interrupt coalescing as a feature.

## Ch 6 — Bayes's Rule

**Core problem:** Predict from small data.

**Algorithms:**
- **Laplace's Law:** (w+1)/(n+2) — works on a single data point. Universal small-data predictor.
- **Bayes's Rule:** posterior ∝ prior × likelihood. Multiply preexisting belief by observed evidence.
- **Copernican Principle:** Bayes with uninformative prior. Predict total duration = 2 × current age. Worked for the Berlin Wall (8 years observed → 8 more), German tank production (245 estimated, 246 actual).

**Three prediction rules per distribution:**

| Distribution | Rule | Predict |
|---|---|---|
| Power-law (wealth, city size, movie grosses, hold times) | Multiplicative | constant × current value |
| Normal (life span, height, runtime) | Average | distribution mean |
| Erlang (radioactive decay, politician tenure) | Additive | constant + current — memoryless |

**Surprise pattern.**
- Power-law: surprise grows the longer you wait. Empires only seem stable until they collapse.
- Normal: surprise is high when early, low when late.
- Erlang: never surprised. Five-more-minutes is correct.

**"Small data is big data in disguise."** Good predictions require good priors. Mismatch = bad prediction.

**Stephen Jay Gould's cancer.** Median 8 months sounds like a normal-distribution death sentence. Actual distribution had a long right tail (power-law). He lived 20 more years.

**Marshmallow test.** Not pure willpower — also priors. Kids with unreliable adult experimenters ate the marshmallow earlier (Multiplicative Rule on power-law of wait time). Self-control is calibrated to environment trust.

**"Protect your priors."** Media skews — gun violence on news rose 600% as murder rate dropped 20%. Snake bites and lightning strikes are over-reported. Counterintuitive: "turn off the news."

## Ch 7 — Overfitting

**Core problem:** When more data / more thought is worse.

**Insight:** A 9-factor model fits 8 data points perfectly *and* gyrates wildly with tiny noise. A 1- or 2-factor model fits worse but generalizes better. **Overfitting is idolatry of data** — worshiping the proxy metric instead of the underlying goal.

**Detection: Cross-Validation.** Hold out data. Test against a *different* metric. Standardized tests + occasional oral exams. KPIs + customer interviews.

**Combat: Penalize complexity.**
- **Lasso (Tibshirani 1996):** add penalty proportional to factor weights, drive most to zero.
- **Occam's Razor.** Among equally good models, simplest wins.
- **Heuristics regularize naturally** — limited time, energy, and memory force simplification.
- **Markowitz's own retirement = 50/50 stocks/bonds.** Even Nobel-laureate optimization expert refused to apply his own model when he didn't trust the inputs enough.

**Early Stopping.** "Sketch with a Sharpie, not a ballpoint." Big strokes early. Don't drill down before you understand the shape. **The more uncertainty you have, the earlier you should stop thinking.**

**Training scars.** Police instinctively pocket spent brass mid-firefight (firing-range etiquette). FBI agents reflexively holster after 2 shots regardless of threat. **Repetitive drill produces overfitting to drill conditions.**

**Steve Jobs / Sam Altman:** "The company will build whatever the CEO decides to measure." Every metric overfits. KPIs without cross-validation become the work product itself.

**Tradition as evolutionary regularization.** "Jump toward the bandwagon, by all means — but not necessarily on it."

## Ch 8 — Relaxation

**Core problem:** Most discrete optimization is intractable. The traveling salesman problem has been unsolved for 80+ years.

**Three relaxations:**

1. **Constraint Relaxation** — drop a constraint, solve the easier problem, port back. Minimum spanning tree as bound on TSP. **"What would you do if you couldn't fail?"** = Constraint Relaxation. Gives bounds (lower for fantasy, upper for reality).
2. **Continuous Relaxation** — fractional / probabilistic versions of discrete choices. Send "0.4 of an invitation" → flip coin to decide. For fire-truck placement, get within 2x of optimal in linear time.
3. **Lagrangian Relaxation** — turn impossible constraints into penalties. **"Or else what?"** Brian's mother: "Technically, you don't have to do anything. There are consequences." Sports scheduling lives on Lagrangian relaxation.

**"Relaxation = consciously driven wishful thinking."** With bounds. With reconciliation paths back to reality.

## Ch 9 — Randomness

**Core problem:** When sampling beats reasoning.

**Algorithms:**
- **Monte Carlo Method** (Ulam, Los Alamos) — sample beats exhaustive analysis when problem space is too large. Solitaire winnability, nuclear physics, polynomial identity testing.
- **Miller-Rabin primality test** — randomized; arbitrarily small error rate. Underlies modern cryptography.
- **Bloom filter** — trade certainty for time + space. **The 3rd dimension of CS tradeoffs is error probability.**
- **Hill Climbing** — get stuck at local maxima. Lobster-trap kills.
- **Random Restart (Shotgun Hill Climbing)** — re-roll from random points. Best for code-breaking and high-multimodal landscapes.
- **Metropolis Algorithm** — sometimes accept worse moves, with probability inverse to how much worse.
- **Simulated Annealing** — front-load randomness (high temperature), cool down over time. Always rapidly converges *and* escapes local maxima.

**Three rules from the Dice Man cautionary tale:**
1. Always act on good ideas (hill climb).
2. Probability of acting on a bad idea ~ inversely proportional to how bad it is.
3. Front-load randomness; anneal over time.

**Sampling > selected anecdotes.** GiveDirectly publishes random recipient interviews verbatim, not curated success stories.

**Creativity as variation + selection** (Campbell, William James). Brian Eno's Oblique Strategies = jitter cards to escape local maxima.

## Ch 10 — Networking

**Core problem:** Communicate over unreliable channels with unknown peers.

**Algorithms:**
- **Packet switching** > circuit switching. Resilience scales with network size. Asynchronous, postcard-style.
- **Triple handshake + ACK numbers** — Byzantine generals problem says perfect coordination is impossible. Three exchanges suffice for "good enough" mutual confirmation.
- **Exponential Backoff** (ALOHAnet → TCP). After failure, double the wait window, retry. Never gives up entirely. **Three strikes you're out is wrong.** HOPE program (Hawaii probation): small-immediate punishments + exponential ramp beat rare-large penalties. 50% reduction in re-arrest, 72% in drug use.
- **AIMD (Additive Increase, Multiplicative Decrease)** — TCP sawtooth. Push to failure, recover by halving. Stable in unknown topologies.
- **Tail Drop** — refuse new packets when buffer fills. *Better* than infinite buffering.

**Bufferbloat:** Modern devices have so much memory that buffers never zero out. Latency explodes while bandwidth is fine. **"We're not always connected; we're always buffered."**

**Backchannel matters.** Distracted listeners destroy stories. Janet Bavelas: narrators told stories worse, especially the climax, when listeners weren't engaging. **Listener feedback is causal, not diagnostic.**

**Latency > bandwidth for interactive use.** Skype prefers a clear-3-seconds-late call over a staticky-now call — and that's wrong. Engineers should treat time as a first-class citizen.

**Peter Principle alternative:** AIMD as career model. Sawtooth promotion (some up, some back). Counter-intuitive but resilience-aware. Vs. up-or-out. Vs. permanent stagnation at incompetence band.

## Ch 11 — Game Theory

**Core problem:** Strategy under recursive simulation of others.

**Algorithms:**
- **Halting problem.** Simulating something as complex as you = unbounded recursion. Don't try.
- **Nash equilibrium** exists for any 2-player game (1951). Finding it is intractable (2008). "If your laptop cannot find it, neither can the market."
- **Dominant strategy** = best response regardless of opponent. Avoids recursion entirely.
- **Prisoner's Dilemma:** dominant strategy (defect) is provably worse for everyone than cooperation. Equilibrium ≠ best outcome.
- **Price of Anarchy:** gap between selfish and coordinated. Selfish routing on the internet = 4/3 (33% worse). PD = infinite.
- **Tragedy of the Commons** = scaled PD. Vacation policy, retail open hours, deforestation, climate change. Verbal truces are unstable.

**Mechanism Design (reverse game theory):** Change the rules, not the strategy. The Godfather worsens defection's payoff → equilibrium becomes cooperation.
- **Compulsory minimum vacation** > the Evernote $1k bonus. The bonus doesn't change the game; the floor does.
- **Religion / regulation as omertà.** Worsen options to improve equilibria.

**Emotion as evolutionary mechanism design.** Anger, love, guilt = involuntary commitment devices. Revenge that hurts you also makes pickpocketing not pay. Love makes leaving not rational, even when "objective optimum" exists. **"Happiness is the lock."**

**Information cascades.** Actions ≠ beliefs. People follow others' actions, dropping their own private information. $23M textbook on Amazon. 2010 flash crash. Real estate bubble. Bidders rationally amplify each other into collective error.

**Vickrey auction (second-price sealed bid).** Honesty is the dominant strategy. Pay what the second-place bidder bid. No shading, no recursion.

**Revelation Principle (Myerson).** Any strategic game can be redesigned so that truth-telling is dominant — *if* the rules optimize for the players. Vickrey is a special case.

## Conclusion — Computational Kindness

**Three meta-lessons:**

1. **Optimal algorithms are transferable** — 37% Rule, LRU, UCB, Weighted SPT.
2. **Process > outcome.** "Computational Stoicism." Best algorithm sometimes yields bad results. The 37% Rule fails 63% of the time *at the optimum*. Don't blame yourself for non-clairvoyance.
3. **Sometimes good enough really is good enough.** Heuristics, approximation, randomization for intractable cases. Choose tractable problems when you have the choice.

**Computational Kindness.** Minimize the labor of thought you impose on others. Verification is easier than search.

- **State your preferences.** "Oh, I'm flexible" passes the cognitive buck. "Personally I lean X, what do you think?" shoulders the load.
- **Reduce options, don't maximize.** Two restaurants > ten.
- **Bus arrival display, not "next bus eventually."** Cognitive subsidy.
- **Helix parking lot, not lane-grid.** First spot wins. No optimization required.
- **Blocking > spinning.** Restaurant: take name and call when ready, don't make people hover. The customers' minds are the CPUs being burned.

**Bias toward simpler solutions, trade off cost-of-error against cost-of-delay, take chances. These aren't concessions when we can't be rational. They're what being rational means.**

