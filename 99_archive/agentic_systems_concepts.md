# Agentic Systems — Concepts

> Ingested: 2026-03-20 | Owner: [Brain Owner] | Pillar: Pillar 4 (Embrace AI at every level)

Per-chapter key concepts distilled to enforceable patterns. Frameworks and anti-patterns only.

## Chapter 1: Introduction to Agents

- Agency exists on a spectrum. True agents demonstrate real decision making, not deterministic scripts. Key test: does it make decisions or follow a script?
- Seven agent types: business-task, conversational, research, analytics, developer, domain-specific, browser-using. Plus voice and video agents emerging.
- Pretraining revolution: single API call to hosted model replaces months of data collection + training. Lowers barrier to building AI applications by orders of magnitude.
- Sync → async shift: agents operate asynchronously, managing multiple tasks in parallel. Transforms humans from task executors to task managers.
- Decision tree for when to use agents: fixed input + deterministic output → code. Finite branches + error handling → workflow. Q&A over corpus → RAG/chatbot. Unstructured inputs + multistep planning + learning → autonomous agent.
- Table 1-2 (Workflows vs Agents): input structure, explainability, latency, adaptability differ. Agents trade explainability and latency for adaptability.
- Model selection: start with leading general-purpose model (OpenAI/Anthropic). Optimize later with smaller models for cost. Future is multimodel.
- Five principles: scalability, modularity, continuous learning, resilience, future-proofing.

## Chapter 2: Designing Agent Systems

- Start with a narrow, well-scoped problem. "Cancel order" not "handle all support."
- Core components: model + tools + memory + orchestration (Figure 2-1).
- Model selection dimensions: task complexity, modality, openness, cost/latency. Large models for open-ended reasoning, small models for repetitive well-defined tasks. Hybrid routing emerging.
- Tools: local (rule-based), API-based (external services), MCP-based (context injection). Modular design: each tool = self-contained, replaceable module.
- Memory: short-term (rolling context window) vs long-term (databases, knowledge graphs, fine-tuned models). Must differentiate relevant from irrelevant, forget outdated.
- Orchestration: composes, schedules, supervises tool sequences. Incrementally builds plans, adapts based on results.
- Design trade-offs: speed vs accuracy, scalability vs cost, reliability vs flexibility.
- Scoping trap: too narrow = limited impact, too broad = drowning in edge cases, too vague = unmeasurable.

## Chapter 3: UX Design for Agentic Systems

- Interaction modalities: text, graphical, speech, video. Match to use case.
- Sync vs async: async enables proactive agent behavior (drafts ready before user asks).
- Context retention across sessions enables personalization.
- Communicating capabilities: set expectations about what the agent can and cannot do.
- Trust: built through transparency, consistency, and graceful failure handling.
- Key UX principles: progressive disclosure, feedback loops, human override always available.

## Chapter 4: Tool Use

- Three-tier architecture: local tools, API-based tools, plug-in/MCP tools.
- Tool metadata drives LLM selection accuracy. Poor descriptions = misfires.
- Naming convention: verb_noun ("get_stock_price" not "stock"). Descriptions: 1-2 sentences max.
- Standard selection: linear scan, O(n), works for <10 tools. Semantic selection: embedding-based lookup, scales to 100+ but risks collision on similar descriptions.
- Standardized response envelope: `{"status": "success|error", "data": <result>, "error_message": <string>}`.
- Anti-patterns: vague/overlapping tool descriptions, unhandled exceptions from tools (must catch and return as output), over-scoped tools handling multiple unrelated operations.
- Automated tool development: code generation, imitation learning, tool learning from rewards.

## Chapter 5: Orchestration

- Agent archetype spectrum (ordered by complexity): Reflex → ReAct → Planner-Executor → Query-Decomposition → Reflection → Deep Research.
- Reflex: stimulus-response, zero reasoning, 10-100ms. Use for lookup-only.
- ReAct: thought-action-observation loop. Flexible, exploration-friendly. Default for most tasks.
- Planner-Executor: explicit plan phase → execution phase. For predictable workflows with fixed decomposition.
- Deep Research: multi-stage adaptive planning, most capable and costly. For open-ended investigation.
- Tool selection: standard (<15 tools), semantic (15+ with description engineering), hierarchical (two-tier LLM routing, adds latency but scales cleanly).
- Tool topologies: single, parallel, sequential execution. Chains, trees, graphs for complex decomposition.
- Planning strategies: incremental execution, zero-shot, few-shot, ReAct.
- Anti-pattern: using Deep Research for simple factual lookups.
- Orchestration state machine: explicit states (initialized, planning, executing, reflecting, done, error) with transitions. Enables observability.

## Chapter 6: Knowledge and Memory

- Context window = working memory. Fixed token budget. Must choose what goes in.
- Three memory approaches: (1) rolling context window (FIFO, lossy), (2) keyword-based (BM25, no ML needed), (3) semantic memory + RAG (embeddings + vector store + retrieval).
- RAG pipeline: documents → chunking → embedding → vector store → query embedding → similarity search → reranking → context injection.
- GraphRAG: knowledge graph with entities and relationships. For multi-hop queries that flat RAG cannot answer.
- Working memory: whiteboards, note-taking patterns for agents to track state across steps.
- Anti-patterns: embedding entire documents without chunking, storing raw chat history without summarization, mixing embedding models, skipping reranking step.
- Keyword memory (BM25) when vocabulary is stable/precise. Semantic RAG when language varies or meaning > keywords.

## Chapter 7: Learning from Experience

- Nonparametric learning: experiences as examples (few-shot), exploration/exploitation balance, reflection.
- Parametric learning: fine-tuning large models (expensive, domain adaptation), fine-tuning small models (efficient, task-specific), transfer learning.
- Reflection: agent reviews its own outputs, identifies errors, self-corrects. Expensive but high-stakes.
- Exploration vs exploitation: balance trying new approaches vs using known-good ones.
- Key: agents must genuinely improve over time, not just overfit or memorize.

## Chapter 8: From One Agent to Many

- Progression principle: start single-agent, add multiagent only when single-agent fails (<90% accuracy or latency exceeds SLA).
- Single-agent ceiling: ~15-20 tools before selection accuracy degrades.
- Decomposition strategy: partition tools by domain/responsibility. Example: 16 tools → 3 specialist agents + 1 manager.
- Coordination patterns: democratic, manager/hierarchical, actor-critic, automated design.
- Manager pattern: supervisor routes requests to specialists, collects results, synthesizes. Enables parallel execution.
- Shared response interface: all agents return identical format. Simplifies aggregation.
- Anti-patterns: >5 agents (coordination overhead compounds), overlapping toolsets (selection ambiguity), no shared response format, synchronous chaining (latency adds linearly).
- Agent specialization by charter: define domain, tool ownership (exclusive preferred), responsibility boundaries.

## Chapter 9: Validation and Measurement

- "An untested agent is an untrusted agent."
- Measurement is the keystone. Define clear objectives, select metrics, systematic evaluation.
- Semantic similarity measures (BERTScore, BLEU, ROUGE) over exact-match for LLM outputs.
- Evaluation sets: input state + expected outcome. Living specification, not static test suite.
- Integrate evaluation into development lifecycle. Automate. Trigger on every merge.
- Human-in-the-loop: automated evaluation rarely tells the whole story.
- Component evaluation (unit tests): tools (deterministic for identical inputs, regression on modification), planning (tool recall, tool precision, parameter accuracy), memory (retrieval accuracy, relevance, staleness), learning (generalization, adaptability).
- Integration testing: end-to-end scenarios, consistency, hallucination detection.
- Evaluation set scaling: mine from production logs, generate with LLMs (adversarial prompting, counterfactual editing), refine with human review.

## Chapter 10: Monitoring in Production

- Causes of failures: model drift, tool failures, data distribution shifts, prompt degradation.
- Agent metrics: system health (latency, error rates, throughput), automated evaluation (accuracy, tool usage), human evaluation (sampling + review), user feedback.
- Distribution shifts: detect when input patterns change vs what the agent was built for.
- Monitoring at scale: analytics dashboards, alerting on metric thresholds, structured logging of agent decisions and tool calls.
- Key: monitor not just whether the system is up, but whether it is making good decisions.

## Chapter 11: Improvement Loops

- Three interconnected techniques: feedback pipelines, experimentation, continuous learning.
- Feedback pipelines: observe failures → cluster patterns → root cause analysis → prioritize fixes. Automated (DSPy, Trace, APO) + human review.
- Automated prompt optimization: initial prompt → target model → evaluation model → scores → optimization model → refined prompt. Loop.
- Root cause analysis: workflow tracing → fault localization → pattern recognition → impact assessment. RCA surfaces organizational blind spots, not just technical bugs.
- Experimentation: shadow deployments, A/B testing, Bayesian Bandits, adaptive experiments, gating.
- Continuous learning: in-context learning (immediate), offline retraining (periodic), online reinforcement (continuous).
- Key insight: improvement is organizational, not just technical. Requires alignment across engineering, data science, product, UX.

## Chapter 12: Protecting Agentic Systems

- Unique risks: prompt injection, data poisoning, tool misuse, unauthorized actions.
- Securing LLMs: model selection (prefer well-audited models), input/output validation, red teaming, fine-tuning for safety.
- Data protection: privacy (minimize data exposure), provenance (track data lineage).
- Securing agents: safeguards (guardrails on actions), external protections (rate limiting, sandboxing), internal protections (permission scoping, audit logging).
- Governance and compliance: audit trails, access controls, regulatory alignment.

## Chapter 13: Human-Agent Collaboration

- Ethical principles: human oversight, transparency, fairness, explainability, privacy.
- Building trust: consistent behavior, graceful failure, clear capability boundaries.
- Addressing bias: audit training data, test for demographic disparities, feedback loops for bias detection.
- Accountability: clear ownership of agent decisions, regulatory compliance (EU AI Act, etc.).
- Human-agent integration: agents augment (not replace) human capability. Shift from executor to manager/supervisor.
