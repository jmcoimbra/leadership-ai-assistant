# Engineering Management Practice

Operational frameworks extracted per chapter. Two lenses: (A) coaching vocabulary for direct reports, (B) management practice for [Brain Owner].

---

## Part A: Coaching Vocabulary (Ch 1-3)

Frameworks for coaching direct reports based on where they ARE on the IC → Lead → Senior path.

### Ch 1 — Management 101 (IC Lens)

**What good management looks like from the IC side:**
- Manager provides: 1:1s, feedback, career growth guidance, training resources, promotion advocacy
- 1:1s serve two purposes: (1) human connection/trust, (2) private space to discuss concerns
- 1:1s are NOT status meetings. ICs own the 1:1 agenda. Manager brings topics if IC does not
- Feedback must be timely (not batched to performance reviews), public for praise, private for correction
- Manager shows how daily work connects to company goals (mundane work → source of pride when purpose is visible)

**Coaching signals for IC-level reports:**
- Do they bring topics to 1:1s or wait passively? (Ownership signal)
- Do they seek feedback proactively or avoid it? (Growth signal)
- Do they advocate for themselves (promotion, projects, concerns) or expect you to read their mind? (Agency signal)
- Are they building a network inside the company? (Career awareness signal)
- Do they take feedback graciously, including feedback they disagree with? (Maturity signal)

**Anti-pattern: benign neglect.** ICs who seem fine with being left alone may be disengaged, not self-sufficient. Check.

### Ch 2 — Mentoring (Mentor/Mentee Lens)

**Mentoring as first management act:**
- Three core skills: listen carefully, clearly communicate, calibrate your response
- Listening = beyond words. Watch for body language, unsaid concerns, discomfort asking questions
- Communication = state expectations explicitly. "I expect you to research before asking" must be said, not assumed
- Calibration = adjust check-in frequency based on the person's demonstrated autonomy. Some need daily, others weekly

**Good mentoring patterns:**
- Best mentoring evolves naturally in context of larger work (pair on problems, not abstract advice)
- Senior mentoring junior: senior gets better code/fewer reviews, junior gets instruction and context. Both win
- Intern mentoring: (1) prepare for arrival, (2) have a project ready, (3) plan an end-of-tenure presentation

**Anti-pattern: the Alpha Geek.**
- Driven to always have the right answer, be the smartest, solve the hardest problems
- Values intelligence above all. Can not handle dissent. Threatened by anyone who might upstage them
- Tries to create excellence culture but creates fear culture instead
- Watch for this in senior reports who mentor juniors. Alpha geek behavior kills team psychological safety

**Coaching signals:**
- When a senior report mentors a junior, does the junior grow? Or do they become dependent / intimidated?
- Does the senior share credit or hoard it?
- Can the senior explain complex things clearly to non-experts? (Communication maturity)

### Ch 3 — Tech Lead (Leadership Without Authority Lens)

**Tech Lead role definition (Rent the Runway):**
- Not a point on the ladder but a set of responsibilities any senior engineer may take on
- Expected to provide mentorship and guidance even without direct management authority
- Learning to be a strong technical project manager: delegating effectively without micromanaging
- Focus on whole team's productivity, not personal technical output
- Making independent decisions and partnering effectively with product/business

**Three roles of a Tech Lead:**
1. **Systems architect / business analyst:** Identify critical systems, translate business requirements into software, provide structure for estimates
2. **Project planner:** Break work into deliverables, identify parallel vs sequential work, gather input from experts, identify priorities
3. **Software developer / team leader:** Write code, communicate challenges, delegate, know when to do it yourself vs hand off

**The One Weird Trick:** Willingness to step away from code and figure out how to balance technical commitments with what the whole team needs. Stop relying entirely on old skills, start learning new ones (project management, communication, prioritization)

**Project Management (from the tech lead perspective):**
1. Break down the work (big pieces → smaller pieces → tickets)
2. Push through details and unknowns (the tedious part that matters)
3. Run the project and adjust the plan as you go
4. Use planning insights to manage requirement changes
5. Revisit details as you approach completion. Run a premortem

**Stone of Triumph:** Tech lead role comes with heavy burden, little extra pay, and is often a temporary title. It is the hardest transition because scope increases dramatically without formal authority or training

**Decision Point: IC vs Manager track.** If you are not ready for management responsibilities, do not take them. Nothing wrong with staying deep in technology. Good managers watch for and protect talented people from being pushed into leadership too early

**Coaching signals for senior/lead-track reports:**
- Are they willing to step away from code for the team's benefit? Or do they retreat into technical rabbit holes?
- Can they break down a project and delegate pieces, or do they try to do everything themselves?
- Do they communicate status and risks proactively? Or only when asked?
- Can they influence peers without authority? Sell a technical direction?
- Do they protect the team's focus time (meeting load, interruptions)?

---

## Part B: Management Practice (Ch 4-9)

Frameworks for [Brain Owner]'s own management execution.

### Ch 4 — Managing People

**New hire management cadence:**
- More attention in first 90 days. Frequent check-ins → taper as trust builds
- Create a 30/60/90 day plan. Use it as conversation anchor, not as a test

**1:1 styles spectrum:**
- Todo list (tactical, risks missing signals)
- Catch-up (human connection, risks lack of structure)
- Feedback (direct, risks being one-directional)
- Progress report (useful for senior reports, boring for ICs)
- Best: mix based on what the person needs at the moment

**Trust-building questions (from the IC's perspective, flipped for managers):**
- Am I giving this person timely feedback (not batching to reviews)?
- Do I know something personal about them (life outside work)?
- Have I helped them connect their daily work to company purpose?
- Am I their ally for career growth, or just their task assigner?
- Have I helped them navigate a difficult situation recently?

**Micromanager vs Delegator diagnostic:**
- Micromanager: questions every detail, refuses to let people make decisions, takes back delegated work
- Delegator: provides context and autonomy, checks in at appropriate intervals, lets people own outcomes
- Most new managers oscillate. The skill is matching oversight to the person's demonstrated capability

**Delivering feedback:**
- Praise publicly, correct privately
- Timely > perfect. Deliver feedback quickly, even imperfectly
- Ask the person for their self-assessment first. You learn more about their self-awareness
- Continuous feedback prevents surprise performance reviews

### Ch 5 — Managing a Team

**Debugging Dysfunctional Teams checklist:**

| Symptom | Diagnosis | Intervention |
|---------|-----------|-------------|
| Not Shipping | Unclear goals, poor planning, perfectionism, or fear of failure | Set clear milestones with deadlines. Make "good enough" explicit. Celebrate shipping |
| People Drama | Interpersonal conflict, toxic individuals, cliques | Address directly. Do not let it fester. One brilliant jerk can destroy team culture |
| Overwork | Poor boundaries, hero culture, understaffing, or poor prioritization | Model healthy boundaries. Cut scope. Say no to stakeholders. Protect team's time |
| Collaboration failures | Silos, poor communication, lack of shared context | Create shared rituals (standups, retros, demos). Pair across silos |

**Staying Technical (as a manager):**
- You will write less code. Accept it
- Stay technical through: code reviews, architecture discussions, debugging sessions, reading code
- Do not take critical-path coding tasks. You will be interrupted and become the bottleneck
- Pick low-priority, educational tasks if you want to code
- Technical credibility comes from understanding the system, not writing features

**Shield the team from chaos:**
- Filter organizational noise. Your reports do not need to know about every political drama
- Translate business priorities into engineering work. Be the adapter between worlds
- But do not over-shield. Share context that helps people make better decisions

### Ch 6 — Managing Multiple Teams ([Brain Owner]'s exact role)

**Delegation matrix:**

| | Frequent | Infrequent |
|---|---------|-----------|
| **Simple** | Delegate fully. Train once, let them run | Delegate with checklist |
| **Complex** | Delegate with check-ins. Build capability over time | Do yourself or pair with someone to build the skill |

**Time Management via Importance/Urgency:**
- Quadrant 1 (Important + Urgent): crises, deadlines — do now
- Quadrant 2 (Important + Not Urgent): strategy, relationships, development — schedule proactively (this is where CTO growth lives)
- Quadrant 3 (Not Important + Urgent): interruptions, some meetings — delegate or decline
- Quadrant 4 (Not Important + Not Urgent): time wasters — eliminate

**Strategies for Saying No:**
1. **"Yes, and..."** — Accept the request but add your conditions (timeline, scope, resources)
2. **Create policies** — Turn repeated decisions into rules so you do not relitigate each time
3. **"Help me say yes"** — Ask the requester to solve the constraint ("I need X to make this work, can you get me X?")
4. **Appeal to budget** — Frame in terms of what gets dropped: "We can do this if we stop doing Y"

**Warning signs you are failing at this level:**
- You are the bottleneck for every decision
- You do not know what your teams are working on
- You spend all time firefighting and none on strategy
- Your managers are not growing

### Ch 7 — Managing Managers

**Skip-level meetings:**
- Meet with your reports' reports regularly (monthly or quarterly)
- Purpose: verify trust, spot issues managers miss, build organizational context
- Do NOT undermine the middle manager. Reinforce their authority. If someone complains about their manager, coach the manager — do not solve the problem directly

**Manager Accountability:**
- Hold managers to outcomes, not activities
- Managers must demonstrate: team health, delivery, people development, cross-team collaboration
- If a manager is failing, coach them directly. If coaching fails, you own the decision to change the role

**Open-Door Policy Fallacy:**
- "My door is always open" means nothing if people are afraid to walk through it
- Proactive connection > reactive availability. Go to people, do not wait for them to come to you
- Skip-levels are one tool. Walking the floor, attending team demos, informal coffee chats are others

### Ch 8 — The Big Leagues (CTO Trajectory)

**CTO definition:** "The CTO is a strategic technical executive. She is responsible for the technical direction of the company and ensuring that the technical team can execute against the business strategy."

**Four Management Tasks (Andy Grove):**
1. Information gathering
2. Decision making
3. Nudging (influencing behavior through informal channels)
4. Being a role model

**VP Engineering vs CTO:**
- VP Eng: runs the engineering org (people, process, delivery)
- CTO: sets technical direction, represents tech externally, translates business → technology strategy
- At some companies same person. At others, they partner (CTO = strategy, VP Eng = execution)
- CTO must be comfortable with ambiguity, politics, and executive communication

**Setting Strategy:**
- Strategy ≠ plan. Strategy = framework for making decisions
- Must connect company business goals to technical investments
- A good strategy helps the team say no to things that do not advance the business

**Changing Priorities:**
- Priorities will change. Your job is to communicate why, absorb the team's frustration, and help them pivot
- People need to understand the WHY behind the change or they will disengage

**Delivering Bad News:**
- Do not sugarcoat. Be clear and direct
- Own the decision even if you disagree with it personally (unless it is unethical)
- Give people space to react. Do not rush past their emotions

### Ch 9 — Bootstrapping Culture

**Culture as infrastructure:**
- Culture is the unwritten rules that determine how work gets done
- If you do not define it intentionally, it will form on its own — and you may not like the result
- Your behavior as a leader IS the culture. What you tolerate, celebrate, and ignore defines it

**Gall's Law:** "A complex system that works is invariably found to have evolved from a simple system that worked." Do not design elaborate processes from scratch. Start simple, iterate

**Structurelessness trap (Jo Freeman):** The absence of formal structure does not mean no structure — it means invisible, unaccountable structure where influence follows social ties, not merit. Make structure explicit

**Process creation rules:**
- Every process should solve a specific, documented problem
- Kill processes that no longer serve their purpose
- Simple processes > complex ones. If you cannot explain it in 2 minutes, it is too complex

---

## Ch 10 — Conclusion

**Core message:** "You have to be able to manage yourself if you want to be good at managing others."
- Self-awareness is the foundation. Understand your reactions, biases, and triggers
- Conflict mastery: separate ego from facts. Your interpretation is just that — an interpretation
- Curiosity is the meta-skill. "Get curious" about the other perspective in every interpersonal challenge
