# Prompt Engineering Techniques

> Owner: [Brain Owner] | Pillar: Pillar 4 (AI Execution)
> Measurable Outcome: 5+ prompt engineering patterns applied to brain skills by 2026-05-15
> Escalation Trigger: If no skill patches applied within 30 days, flag in weekly review

Lens: AI Systems — (A) brain skill patterns, (B) team adoption playbook.

---

## Part A: Brain Skill Patterns

### Ch 1 — Five Principles of Prompting

Core framework applicable to every skill and prompt in the brain:

| Principle | Definition | Brain Application |
|-----------|-----------|-------------------|
| Give Direction | Role assignment, task specification, context framing | YAML frontmatter `description:` + first paragraph of skill. Some skills lack explicit role definition |
| Specify Format | Explicit output structure (JSON, YAML, lists, tables) | Evaluator rubric tables, Output Summary templates. Currently prose-based, not structured |
| Provide Examples | Few-shot prompting (1-3 representative outputs) | No brain skill currently includes output examples. Gap |
| Evaluate Quality | Rubrics, A/B testing, labeled comparison | Evaluator Pass exists on 3 skills but uses basic 5-point prose scale |
| Divide Labor | Break complex tasks into subtasks with clear handoffs | meeting-ingest has steps but lacks explicit per-step gates |

Key insight: "1-3 examples optimal; >3 increases reliability but reduces creativity." For brain skills, 1 example per output format is the minimum viable few-shot.

Anti-pattern: **Blind prompting** — adding instructions to a prompt without testing whether they change the output. Every skill change must be tested against representative inputs.

### Ch 3 — Standard Practices for Structured Output

**Generating lists:** Uncontrolled list generation produces variable-length, inconsistently formatted output. Fix: specify count, format (bullet/numbered), filtering criteria, and "only return X, never include any commentary."

**Structured data extraction:** Three tiers of increasing reliability:
1. Hierarchical lists (regex-parseable but fragile)
2. JSON (explicit schema + "Only return valid JSON" + "Never include backtick symbols")
3. YAML (better for prompts: no escape characters, supports comments, human-readable)

**YAML schema validation pattern:**
- Provide the schema in the prompt
- Provide the user query as YAML
- Ask LLM to return filtered YAML matching schema, or "No Items" if no match
- Validate response programmatically with custom exceptions per edge case (InvalidResponse, InvalidItemType, InvalidItemKeys, InvalidItemName, InvalidItemQuantity, InvalidItemUnit)
- LLM acts as a **reasoning engine** for control flow decisions

Brain application: MCP tool outputs (GitHub, Notion, Slack) should be schema-validated before use. Currently no skill validates MCP responses.

**Audience adaptation:** "Explain it like I'm Five" technique. Useful for: meeting-prep summaries for non-technical stakeholders, Dev Support merchant-facing responses.

**Diverse format generation:** LLMs can generate Mermaid diagrams, CSV, code, conversations, scripts. Format specification in the prompt directly controls output structure.

### Ch 4 — Advanced Techniques (LangChain Patterns)

**Prompt templates:** Variables in prompts (SystemMessage for role/instructions, HumanMessage for task). Brain equivalent: YAML frontmatter variables and contextual triggers.

**LCEL chaining:** `prompt | model | output_parser` — the pipe operator chains components where output of one feeds input of next. Brain equivalent: multi-step skill execution.

**Output parsers (ranked by flexibility):**
1. Pydantic/JSON parser — define BaseModel with typed fields, parser validates and structures. Most flexible
2. Structured output parser — multiple fields
3. List parser — comma-separated items
4. Auto-fixing parser — wraps another parser, uses LLM to fix failures
5. Retry parser — retries from previous failure
6. XML parser — XML-based responses

Brain application: evaluator rubrics should use Pydantic-style structured criteria, not prose. Example upgrade:
- Current: "Every finding references specific code" (prose)
- Upgraded: "Finding has: file_path (present/absent) + line_number (present/absent) + code_snippet (present/absent). Score = count of 3" (structured)

**LangChain Evals:**
- `labeled_pairwise_string` evaluator: compares two outputs using GPT-4, gives reasoning and score
- Use cases: compare outputs from two different prompts, compare model versions
- Can identify positive/negative examples for fine-tuning datasets
- Brain application: when evaluator pass produces ambiguous score (3/5), compare current output vs known-good output for same input type

**Batch processing:** `.batch()` over `.invoke()` for parallelization. `RunnableConfig(max_concurrency=5)` for rate limiting. Brain equivalent: parallel agent dispatch in pr-sweep.

### Ch 5 — Vector Databases & RAG

**Embeddings:** Vector representations of text. Dense vectors (all dimensions nonzero, 384-1536 dims) vs sparse vectors (most dims zero, 100K+ dims). Contextual: "bank" has different embeddings in "river bank" vs "financial bank."

**RAG pipeline (4 steps):**
1. Break documents into chunks
2. Index chunks in vector database
3. Search by vector for similar records
4. Insert records into prompt as context

**Chunking strategy trade-off:** Smaller chunks = more specific location in vector space = better similarity matching. Larger chunks = more context but regression toward mean (loses semantic specificity). RecursiveCharacterTextSplitter: split on paragraphs first, then sentences, then words. chunk_size and chunk_overlap parameters.

**FAISS:** Facebook AI Similarity Search. Local vector store. IndexFlatL2 for brute-force L2 distance search.

**TF-IDF:** Term Frequency-Inverse Document Frequency. Statistical measure for small document sets. Lighter than embedding models. Brain application: could be used for knowledge file similarity matching.

**Context injection + grounding:** After vector search, inject results into prompt with system message: "Please answer using only the context provided. If you don't know, say I don't know." This prevents hallucination by grounding responses in retrieved data.

Brain application: knowledge-dependent skills should validate that retrieved knowledge was actually used in the output. Currently no skill does this.

### Ch 6 — Autonomous Agents

**Chain-of-Thought (CoT):** Adding "step-by-step" or "think through this step by step" triggers reasoning chains. Breaks complex problems into sequential sub-steps the model can verify.

**ReAct framework:** Observe → Think → Act → Repeat → Final Answer. The agent loops through observation (tool output), thinking (reasoning about what to do next), and acting (calling a tool or producing output). Terminates when it has enough information for a Final Answer.

**Agent architecture (6 components):**
1. Inputs — what the agent receives
2. Goal/reward function — what success looks like
3. Available actions — tools the agent can use
4. Memory — what the agent remembers across steps
5. Planning — how the agent decides what to do next
6. Retrieval — how the agent accesses external knowledge

**Function calling:** Alternative to ReAct. Model outputs structured function calls (name + arguments) instead of free-text reasoning. More deterministic, less flexible.

**Agent types:** OpenAI Functions, OpenAI Tools, XML Agent, JSON Chat Agent, Structured Chat, ReAct, Self-Ask with Search. Each optimized for different use cases.

**OnlyStoreAIMemory:** Custom memory class that only stores AI-generated messages, not user messages or tool outputs. Prevents memory bloat from large tool responses. Brain application: memory/ system already does this via selective writing rules.

**Prewarm/Internal Retrieval:** Before generating output, ask the LLM to recall best practices for the specific task. Then use that recalled context alongside the actual data. Combines with few-shot: prewarm generates examples on demand rather than hardcoding.

Brain application: Before writing a PR review, ask "What are the 3 most common review pitfalls for [language/framework]?" Then include that as grounding context for the actual review.

**Self-consistency:** Generate multiple outputs (N=3), evaluate each against criteria, select the best. Increases reliability for high-variance tasks at the cost of latency.

Brain application: slack-triage urgency classification. For messages classified as HIGH, re-classify independently. If disagreement, default to HIGH (fail-safe).

### Ch 10 — Building AI-Powered Applications

**Prompt chaining (5-step blog pipeline):**
1. Topic Research — gather background information
2. Interview — generate Q&A based on research
3. Outline — structure the content
4. Generation — write the full content
5. Style — match target writing style

Each step has explicit input, output, and success criteria. The output of step N becomes the input of step N+1. If any step fails, the pipeline stops.

Brain application: meeting-ingest has 8 steps but only 2 have explicit gates. weekly-review has 11 steps. Both need per-step success criteria.

**Meta-prompting:** One AI writes the prompt for another AI. Use case: optimizing prompt wording by having a "prompt engineer" model refine the instructions.

Brain application: `/create-skill` could use meta-prompting — have the AI draft the skill prompt, then have a second pass evaluate the prompt quality.

**Prompt optimization:**
- A/B testing: run two prompt variants against same inputs, compare outputs
- Embedding distance: measure similarity between generated output and target style using cosine distance
- DSPy framework: automated prompt optimization through compilation

**Writing style matching:** Collect examples of target style. Generate embeddings for target examples. Generate candidate outputs. Compare embedding distances. Select output closest to target style.

Brain application: voice-profile.md already captures [Brain Owner]'s style. Could use embedding similarity to score draft messages against known [Brain Owner] messages.

**Blind prompting anti-pattern (critical):** Adding instructions to a prompt without testing whether they actually change the output. The #1 prompt engineering mistake. Every prompt change must be evaluated against representative inputs before deployment.

---

## Part B: Team Adoption Playbook

| Team | Pattern | Application | CWR Stage |
|------|---------|-------------|-----------|
| QA | Few-shot test case generation | Provide 1-3 example test cases per test type to LLM. Format: input scenario → expected behavior → assertion | Walk |
| QA | Schema-validated test output | Define JSON schema for test results (test_name, status, evidence, severity). Validate LLM output against schema | Walk |
| QA | Evaluator rubric for test completeness | Structured criteria: coverage percentage, edge case count, assertion specificity score | Crawl |
| [Mobile Team] | Prompt chaining for code generation | Research → Design → Generate → Review pipeline with per-step gates | Walk |
| [Mobile Team] | Prewarm retrieval before code review | Recall best practices for the PR's language/framework before generating findings | Crawl |
| [Mobile Team] | Output parser for structured PR feedback | Define feedback schema: file, line, severity, category, suggestion. Parse LLM review into this schema | Crawl |
| Dev Support | Structured output for ticket classification | JSON schema: type (bug/question/config), urgency (high/medium/low), team (QA/[Mobile Team]/CS), confidence_score | Crawl |
| Dev Support | Audience adaptation for merchant responses | "Explain it like I'm a restaurant manager" technique for non-technical merchant communications | Walk |
| Dev Support | YAML schema validation for config checks | Provide merchant config schema, ask LLM to validate incoming config data against it | Crawl |
