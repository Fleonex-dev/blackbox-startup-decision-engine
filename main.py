import uuid

from core.state import EngineState
from core.context import ExecutionContext
from llm.factory import get_llm
from graph import build_graph

def run_once():
    state: EngineState = {
        "run_id": f"run_{uuid.uuid4()}.hex[:8]",
        "brief": None,
        "market_eval": None,
        "business_eval": None,
        "technical_eval": None,
        "final_decision": None
    }

    llm = get_llm()
    ctx = ExecutionContext(llm=llm)

    graph = build_graph(ctx)
    
    final_state = graph.invoke(state)

    print("\n=== FINAL STATE ===")
    print(final_state)
    print("===================\n")


if __name__ == "__main__":
    run_once()