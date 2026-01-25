# Blackbox Engine — adversarial evaluation engine

A stateless, multi-agent adversarial decision framework. The current concrete
instantiation evaluates B2B startup ideas across market, business, and
technical dimensions; the core engine is domain-agnostic and supports other
adversarial review workflows.

---

## What is this?

- Core: a compact engine that runs independent evaluators in parallel and
  aggregates their verdicts via deterministic arbitration.
- Current use case: automated triage of early-stage B2B ideas (generator +
  market, business, technical evaluators + deterministic arbiter).
- Outputs: a reproducible decision (BUILD or KILL) and a per-run shadow log.

---

## Core engine vs domain evaluators

- Core engine (domain-agnostic):
  - Stateless orchestration of state patches returned by nodes.
  - Graph-based execution: entry → parallel evaluators → arbiter.
  - Pluggable LLM backends via a minimal LLMClient interface.
  - Deterministic aggregation rules and shadow logging.

- Domain-specific evaluators:
  - Implement (state, context) → partial state patch.
  - Contain domain rules and prompts; return structured JSON.
  - Can be replaced, extended, or disabled without changing core logic.

---

## High-level architecture 🧠

- main.py: runner — build context, run compiled StateGraph, persist shadow log.
- graph.py: graph construction — nodes and edges, entry/finish points.
- agents/*: domain evaluators and generator (produce partial state patches).
- llm/*: LLM adapters implementing generate(system, user) -> str.
- core/*: types (EngineState, EvalResult), ExecutionContext, file-based logger.

Flow: generator → evaluators (parallel) → arbiter → final_decision → shadow log.

---

## Design principles & invariants

- Explicit contracts:
  - EngineState keys: run_id, brief, market_eval, business_eval,
    technical_eval, final_decision.
  - EvalResult: { component, status, confidence, reason }.
  - Status values are the literals "PASS" or "KILL".
- Deterministic arbitration: arbiter applies a simple, auditable rule.
- Fail-fast / rejection-first: a single evaluator KILL biases final decision
  toward KILL to limit cost and downstream effort.
- LLMs are components: injected, replaceable, and treated as external
  dependencies; outputs must be validated by callers.
- Statelessness: each run is independent and fully described by EngineState.

---

## What this intentionally does NOT do

- Not a full LLM orchestration platform (no built-in retries, backoff,
  or comprehensive cost controls in adapters).
- No persistent database, no UI, no auth, no long-running orchestration.
- Not an autonomous optimizer or learning system — no stateful tuning or
  adaptation across runs.
- No schema validation beyond current json.loads parsing in agents (add
  pydantic for production as needed).

---

## How to run locally ⚙️

Prereqs:
- Python 3.10+, virtualenv, project dependencies (requirements.txt).

Quickstart:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# default: deterministic mock LLM
export LLM_PROVIDER=mock
python main.py

# or use OpenAI (configure SDK credentials)
export LLM_PROVIDER=openai
python main.py
```

Run tests:

```bash
pytest -q
```

---

## Observability / shadow logging

- Each run writes a JSON snapshot to `logs/` (run_id, timestamp, brief,
  market_eval, business_eval, technical_eval, final_decision).
- Shadow logs are intended for audit and debugging; they are file-based and
  not atomic. Replace with an atomic writer or central store when needed.
- Console output includes a formatted, read-only view of the final state.

---

## Extensibility 🧩

- Add new domains: implement an agent that returns a partial state patch and
  wire it into `graph.py`.
- Add new LLM backends: implement `LLMClient.generate(system: str, user: str) -> str`
  and register in `llm/factory.py`.
- Policy changes: keep arbiter deterministic; for complex policies, add a
  separate policy node that produces a final patch.
- Validation: add pydantic models in agents to validate LLM outputs before
  merging into state.

---

## Project status

- v0.1 — intentionally scoped:
  - Core orchestration and graph execution in place.
  - Deterministic mock LLM for local runs, basic OpenAI adapter available.
  - File-based shadow logging and unit tests for core rules.
- Next steps for production readiness:
  - Add schema validation and stronger LLM wrappers (retry, rate limit).
  - Introduce atomic logging or an audit store.
  - Add integration tests covering live LLM paths in a controlled environment.

---

## Operational notes

- Preserve EngineState and EvalResult shapes; many components rely on them.
- Treat evaluators as untrusted inputs: validate and sanitize before merge.
- The system deliberately biases toward rejection to contain cost and risk.

---
