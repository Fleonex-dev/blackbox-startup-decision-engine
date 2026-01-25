import uuid
import json

from core.state import EngineState
from core.context import ExecutionContext
from core.logger import write_shadow_log
from llm.factory import get_llm
from graph import build_graph

"""Orchestrator for a single evaluation run.

Responsibilities:
- Compose initial EngineState.
- Instantiate ExecutionContext and LLM.
- Build and execute the state graph.
- Persist a shadow log and print the final state.

Assumptions:
- Agents return partial state patches that the graph runtime merges into the EngineState.
- This module performs orchestration only; decision/business logic lives in agents/.
"""

def format_final_state(state: EngineState) -> str:
    """Produce a display-only JSON string representing final state.

    Responsibility:
    - Create a deterministic, human-friendly representation of final state
      for console output without mutating the provided state.

    Inputs:
    - state: EngineState (read-only for this function)

    Outputs:
    - JSON string with a consistent layout:
      { run_id, brief, evaluations: {market,business,technical}, final_decision }

    Important:
    - Uses json.dumps(..., default=str) to safely serialize enums or unexpected
      objects for display. This does not change the underlying state.
    """
    display_view = {
        "run_id": state.get("run_id"),
        "brief": state.get("brief"),
        "evaluations": {
            "market": state.get("market_eval"),
            "business": state.get("business_eval"),
            "technical": state.get("technical_eval"),
        },
        "final_decision": state.get("final_decision")
    }
    # Pretty-print for readability; do not mutate state.
    return json.dumps(display_view, indent=2, ensure_ascii=False, default=str)

def run_once():
    """Run one evaluation pass.

    Inputs: None
    Outputs: prints final state and writes a JSON snapshot via write_shadow_log.
    Assumptions:
    - run_id must be unique per run.
    - The graph.invoke call will return the merged EngineState.
    """
    # Prepare initial run state.
    state: EngineState = {
        # NOTE: current f-string contains a literal; if you want an 8-char hex slice,
        # change to: uuid.uuid4().hex[:8]
        "run_id": f"run_{uuid.uuid4()}.hex[:8]",
        "brief": None,
        "market_eval": None,
        "business_eval": None,
        "technical_eval": None,
        "final_decision": None
    }

    llm = get_llm()
    ctx = ExecutionContext(llm=llm)

    # Build and execute the state graph.
    graph = build_graph(ctx)
    
    final_state = graph.invoke(state)

    # Persist a shadow log for debugging/observability.
    write_shadow_log(final_state)

    # Print a structured, readable view of the final state to stdout.
    print("\n=== FINAL STATE ===")
    print(format_final_state(final_state))
    print("===================\n")


if __name__ == "__main__":
    run_once()