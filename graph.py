from langgraph.graph import StateGraph, END
from core.state import EngineState
from core.context import ExecutionContext

from agents.workflow_gate import workflow_gate
from agents.market_eval import market_evaluator
from agents.business_eval import business_evaluator
from agents.technical_eval import technical_evaluator
from agents.arbiter import final_arbiter

"""Graph construction for the evaluation pipeline.

The StateGraph composes nodes that receive the EngineState and return a
partial state patch. The runtime merges patches to form the new EngineState.
Keep node implementations free of orchestration concerns — they should only
perform state transformation for their responsibility.
"""

def build_graph(ctx: ExecutionContext):
    """Build and compile the evaluation state graph.

    Inputs:
    - ctx: ExecutionContext provided to agent nodes.

    Output:
    - A compiled graph ready for invocation.

    Structure:
    Start -> Workflow Gate -> (Conditional)
         -> PASS -> [Market, Business, Technical] -> Arbiter -> End
         -> KILL -> End
    """
    # Create state graph.
    graph = StateGraph(EngineState)

    # Add nodes
    graph.add_node("workflow_gate", lambda state: workflow_gate(state, ctx))
    graph.add_node("broadcast", lambda state: state) # Dummy node for fan-out
    graph.add_node("market_eval", lambda state: market_evaluator(state, ctx))
    graph.add_node("business_eval", lambda state: business_evaluator(state, ctx))
    graph.add_node("technical_eval", lambda state: technical_evaluator(state, ctx))
    graph.add_node("arbiter", final_arbiter)

    # Define Conditional Logic
    def route_after_gate(state: EngineState):
        result = state.get("workflow_gate_result", {})
        decision = result.get("decision")
        
        if decision == "KILL":
            return "end"
        return "continue"

    # Set up edges
    graph.set_entry_point("workflow_gate")
    
    graph.add_conditional_edges(
        "workflow_gate",
        route_after_gate,
        {
            "end": END,
            "continue": "broadcast"
        }
    )

    # Fan-out from broadcast
    graph.add_edge("broadcast", "market_eval")
    graph.add_edge("broadcast", "business_eval")
    graph.add_edge("broadcast", "technical_eval")

    # Fan-in to arbiter
    graph.add_edge("market_eval", "arbiter")
    graph.add_edge("business_eval", "arbiter")
    graph.add_edge("technical_eval", "arbiter")
    
    graph.set_finish_point("arbiter")

    return graph.compile()