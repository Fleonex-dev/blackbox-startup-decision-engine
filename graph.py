from langgraph.graph import StateGraph
from core.state import EngineState
from core.context import ExecutionContext

from agents.generator import idea_generator
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

    Node contract:
    - Each node accepts the full EngineState and returns a dict with keys to
      merge into the state (partial patch).
    """
    # Create state graph.
    graph = StateGraph(EngineState)

    # Add nodes that call agents with the execution context.
    graph.add_node("generator", lambda state: idea_generator(state, ctx))
    graph.add_node("market_eval", lambda state: market_evaluator(state, ctx))
    graph.add_node("business_eval", lambda state: business_evaluator(state, ctx))
    graph.add_node("technical_eval", lambda state: technical_evaluator(state, ctx))
    graph.add_node("arbiter", final_arbiter)

    # Define entry and finish points and edges.
    graph.set_entry_point("generator")

    graph.add_edge("generator", "market_eval")
    graph.add_edge("generator", "business_eval")
    graph.add_edge("generator", "technical_eval")

    graph.add_edge("market_eval", "arbiter")
    graph.add_edge("business_eval", "arbiter")
    graph.add_edge("technical_eval", "arbiter")

    graph.set_finish_point("arbiter")

    return graph.compile()