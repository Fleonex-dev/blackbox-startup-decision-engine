import uuid

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

    # Write run snapshot.
    write_shadow_log(final_state)

    print("\n=== FINAL STATE ===")
    print(final_state)
    print("===================\n")


if __name__ == "__main__":
    run_once()