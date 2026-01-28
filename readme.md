# Blackbox Engine

A stateless, deterministic evaluation engine that orchestrates domain-specific agents via multi-agent evaluation and applies fixed aggregation rules to produce structured decisions.

## Problem Statement

When evaluating complex, multi-dimensional decisions (startup ideas, technical proposals, design reviews), manual review is serial and subjective. Running multiple independent evaluators in parallel and combining their outputs deterministically allows:

- Parallel assessment across orthogonal dimensions (market, business, technical)
- Reproducible decision logic auditable by inspection
- Decoupling of decision rules from LLM outputs

This engine provides the scaffolding for that pattern.

## What This Is / What This Is Not

**Is:**

- A stateless orchestration layer for multi-agent workflows
- A framework for plugging in domain-specific evaluators
- Deterministic (given the same inputs and LLM, produces identical results)
- Designed for evaluation tasks that decompose into independent parallel assessments
- Currently deployed to evaluate early-stage B2B startup ideas

**Is not:**

- A general-purpose LLM orchestration platform (no built-in retries, rate limiting, cost controls, or concurrency management)
- A persistent system (no database, no state durability across restarts)
- An optimization or tuning system (no statistical learning, no parameter adaptation across runs)
- An autonomous agent framework (agents follow fixed evaluation logic, not free exploration)
- A user-facing product (no UI, no auth, no multi-tenancy)
- A research framework (no hypothesis testing infrastructure, no logging designed for analysis)

## Core Concepts

### Engine Model

The engine treats evaluation as a directed acyclic graph (DAG):

1. **Generator**: Produces initial structured input (e.g., startup brief)
2. **Evaluators** (parallel): Each independently assesses the input on a specific dimension, producing a partial state update
3. **Arbiter**: Applies fixed aggregation rules to evaluator outputs, producing a final decision

Each node receives the full engine state and returns a dict of keys to merge back into state. The graph runtime manages orchestration.

### State

`EngineState` is the canonical data structure passed through the graph. It contains:

- `run_id`: Unique identifier for this evaluation
- `brief`: Generated input (e.g., startup concept)
- `market_eval`: EvalResult from market dimension
- `business_eval`: EvalResult from business dimension
- `technical_eval`: EvalResult from technical dimension
- `final_decision`: Arbiter output ("BUILD" or "KILL")

`EvalResult` is the typed output of each evaluator:

```python
{
    "component": str,        # Evaluator name (e.g., "market")
    "status": "PASS" | "KILL",
    "confidence": float,     # [0, 1]
    "reason": str           # Explanation
}
```

### Arbitration

The arbiter applies a simple, fixed rule: **all evaluators must return "PASS" for the final decision to be "BUILD"; any "KILL" result sets the final decision to "KILL".**

This is rejection-first: conservative, auditable, and biases toward caution.

### Determinism and Statelessness

Each run is fully described by `EngineState`. Given identical inputs and the same LLM implementation (mock or real with fixed random seed), the engine produces identical outputs. No run depends on previous runs or external state.

This enables:

- Reproducible evaluation (same brief always produces same decision)
- Hermetic testing (no flaky integration)
- Debugging by rerunning with the same state

## Architecture Overview

### Modules and Responsibilities

| Module | Responsibility |
|--------|---|
| `main.py` | Entry point; composes initial state, instantiates context, invokes graph, persists shadow log |
| `graph.py` | Builds and compiles the StateGraph with nodes and edges |
| `core/state.py` | TypedDict definitions for `EngineState` and `EvalResult` |
| `core/context.py` | `ExecutionContext` container passed to agents (holds LLM, optional retriever/tools/config) |
| `core/logger.py` | File-based shadow logging (writes per-run JSON snapshot to `logs/`) |
| `agents/*` | Domain-specific evaluators and generator; implement `(state, context) -> dict` |
| `llm/base.py` | `LLMClient` interface (minimal: `generate(system: str, user: str) -> str`) |
| `llm/factory.py` | Selects LLM implementation via `LLM_PROVIDER` env var |
| `llm/mock_llm.py` | Deterministic mock for local dev and tests |
| `llm/openai_llm.py` | OpenAI API client |

### Separation of Concerns

- **Core**: State management, graph orchestration, logging. Domain-agnostic.
- **Domain**: Evaluator prompts, parsing logic, evaluation criteria. Replaceable.
- **LLM**: Client implementations. Pluggable via factory pattern.

## Execution Flow

1. **Initialization** (`main.py::run_once`): Create initial `EngineState` with unique `run_id`, instantiate `ExecutionContext` with selected LLM, build graph.

2. **Generation** (`agents/generator.py`): LLM produces a structured brief (e.g., startup concept). Returns `{"brief": ...}`.

3. **Parallel Evaluation**: Three evaluators run in parallel:
   - Market evaluator: Assesses market size, timing, TAM. Returns `{"market_eval": EvalResult}`.
   - Business evaluator: Assesses business model, monetization, defensibility. Returns `{"business_eval": EvalResult}`.
   - Technical evaluator: Assesses technical feasibility, architecture, risk. Returns `{"technical_eval": EvalResult}`.

   Each evaluator independently reads the brief and applies domain-specific logic.

4. **Arbitration** (`agents/arbiter.py`): Reads all three eval results, applies fixed rule (all PASS → BUILD, any KILL → KILL). Returns `{"final_decision": "BUILD" | "KILL"}`.

5. **Logging** (`core/logger.py`): Full final state written as JSON to `logs/{run_id}_{timestamp}.json`.

6. **Output** (`main.py`): Final state printed to stdout.

## Design Principles & Invariants

### Contracts

- Each agent function accepts `(state: EngineState, context: ExecutionContext)` and returns a dict of keys to merge into state.
- LLM outputs are not validated by the engine; agents must parse and validate before returning.
- `EngineState` keys are explicitly defined; new keys should not be added without updating the TypedDict.
- Status values must match the `Status` enum: "PASS" or "KILL".

### Philosophy

- **Statelessness first**: No run-to-run state; each evaluation is self-contained.
- **Explicit over implicit**: Contracts are documented in docstrings; magic is avoided.
- **Rejection-first arbitration**: Conservative bias toward KILL reduces downstream costs.
- **LLM as a component**: Treated as an external dependency, not the source of truth. Outputs must be parsed and validated.
- **Auditability**: Logs and decision rules are simple enough to inspect and understand without tooling.

### Constraints

- Evaluators run in parallel; they cannot depend on each other's results.
- Graph topology is fixed (not dynamically generated).
- No inter-run state or learning; each run is isolated.
- No cost controls, retries, or rate limiting in the engine (delegate to LLM layer or orchestrator).

## Current Capabilities

### Implemented

- Multi-agent evaluation of B2B startup ideas across market, business, and technical dimensions
- Deterministic arbitration rule and shadow logging
- Pluggable LLM backends (mock and OpenAI)
- Reproducible execution with mock LLM
- Per-run JSON logs for debugging

### Stable

- Core engine (graph orchestration, state merging, arbitration rule)
- TypedDict contract for EngineState and EvalResult
- LLMClient interface

### Experimental / Subject to Change

- Evaluator prompts and parsing logic (domain-specific; may be refactored as use cases expand)
- Shadow logging format (currently simple JSON; may add structured fields for analytics)

## Extensibility

### Adding a New Evaluator

1. Create `agents/new_eval.py` with function `new_evaluator(state: EngineState, context: ExecutionContext) -> dict`.
2. Load your prompt from `prompts/new.txt`.
3. Call `context.llm.generate(system, user)` and parse the result.
4. Return `{"new_eval": EvalResult}` (update EngineState TypedDict to include this key).
5. Add node and edges in `graph.py`.

### Adding a New LLM Backend

1. Create `llm/new_llm.py` with class `NewLLM(LLMClient)` implementing `generate(system: str, user: str) -> str`.
2. Update `llm/factory.py` to instantiate your backend when `LLM_PROVIDER=new_llm`.
3. Optionally add environment variable configuration for API keys or endpoints.

### Adding a New Domain (e.g., Feature Review Instead of Startup Evaluation)

1. Replace `agents/generator.py` to accept and parse the domain input (e.g., feature spec instead of startup brief).
2. Rewrite or replace evaluators in `agents/*` to assess domain-specific criteria.
3. Update `core/state.py` EngineState if new dimensions are needed (e.g., add `security_eval`, `performance_eval`).
4. Optionally adjust the arbitration rule in `agents/arbiter.py` if the domain requires different logic.
5. Update prompts in `prompts/*`.

## Operational Notes

### Observability

**Logging**: Each run produces a JSON file in `logs/` containing the full final state. Search logs by `run_id` or timestamp for debugging.

**Console Output**: Final decision and structured state are printed to stdout for immediate feedback.

**Tracing**: Currently minimal. To add detailed tracing (e.g., intermediate LLM calls, parsing errors), hook into agent functions or the graph runtime.

### Determinism and Reproducibility

- **Mock LLM**: Returns fixed JSON. Runs are fully deterministic.
- **OpenAI LLM**: Same brief + same model/temperature produces identical results (given OpenAI doesn't change model weights).
- **Re-running**: Save the `brief` from a previous run's log, inject it into a fresh run, and the arbiter will make the same decision.

### Failure Modes

| Failure | Cause | Impact | Mitigation |
|---------|-------|--------|-----------|
| LLM API unavailable | Network/service outage | Run halts, exception raised | Retry logic at orchestrator level; use mock LLM for dev |
| Invalid JSON from LLM | Model returning non-JSON or unexpected schema | Agent parse fails, run halts | Validate schema at agent; add error handling; use mock LLM to test |
| Missing `brief` when evaluator runs | Generator didn't populate state | Evaluator gets None, likely crashes | Graph ordering ensures generator runs first; add asserts |
| All evaluators KILL, but rule expects all PASS | Domain evaluation agrees idea is bad | Final decision is KILL (correct) | This is by design; rule is rejection-first |

### Debugging

1. Check the shadow log (run_id from console output).
2. Re-run with `LLM_PROVIDER=mock` to isolate LLM issues.
3. Add print statements or logging in agents to trace LLM calls.
4. Manually inspect the `brief` in the log to understand why evaluators voted KILL.

## How to Run Locally

### Prerequisites

- Python 3.10+
- `virtualenv` or `conda`

### Quickstart

```bash
# Clone and navigate to the project
git clone <repo>
cd blackbox-engine

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run with mock LLM (deterministic, no API keys needed)
export LLM_PROVIDER=mock
python main.py

# Or use OpenAI (requires OPENAI_API_KEY in environment)
export LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-...
python main.py
```

### Running Tests

```bash
pytest -v

# Run a specific test
pytest tests/test_arbiter.py -v

# Run with coverage
pytest --cov=core --cov=agents tests/
```

### Output

- **Console**: Prints final state as formatted JSON.
- **Logs**: A `.json` file is written to `logs/` for each run.

## Project Status

**Version**: Pre-release  
**Stability**: Core engine and TypedDict contracts are stable. Evaluator logic, prompts, and shadow log format may change.  
**Maturity**: Functional prototype suitable for evaluation and iteration within a team. Not production-hardened (no async, no concurrency controls, no persistence, no comprehensive error handling).

### Known Limitations

- No schema validation of evaluator outputs (agents must validate manually)
- No cost tracking or rate limiting
- No retry logic or exponential backoff
- Shadow logs are not indexed or queryable (plain JSON files)
- No support for dynamic graph topology or conditional edges
- LLM calls are synchronous (blocks until response)

## Contributing

This project is maintained as an internal tool. External contributions are not currently accepted. Issues and suggestions from internal stakeholders are welcome.

---

## Observability / shadow logging 🔍 📣

- Each run writes a JSON snapshot to `logs/` (run_id, timestamp, brief,
  market_eval, business_eval, technical_eval, final_decision).
- Shadow logs are intended for audit and debugging; they are file-based and
  not atomic. Replace with an atomic writer or central store when needed.
- Console output includes a formatted, read-only view of the final state.

---

## Extensibility 🧩 🧪

- Add new domains: implement an agent that returns a partial state patch and
  wire it into `graph.py`.
- Add new LLM backends: implement `LLMClient.generate(system: str, user: str) -> str`
  and register in `llm/factory.py`.
- Policy changes: keep arbiter deterministic; for complex policies, add a
  separate policy node that produces a final patch.
- Validation: add pydantic models in agents to validate LLM outputs before
  merging into state.

---

## Project status 📈

- v0.1 — intentionally scoped:
  - Core orchestration and graph execution in place.
  - Deterministic mock LLM for local runs, basic OpenAI adapter available.
  - File-based shadow logging and unit tests for core rules.
- Next steps for production readiness:
  - Add schema validation and stronger LLM wrappers (retry, rate limit).
  - Introduce atomic logging or an audit store.
  - Add integration tests covering live LLM paths in a controlled environment.

---

## Operational notes 📝

- Preserve EngineState and EvalResult shapes; many components rely on them.
- Treat evaluators as untrusted inputs: validate and sanitize before merge.
- The system deliberately biases toward rejection to contain cost and risk.

---
