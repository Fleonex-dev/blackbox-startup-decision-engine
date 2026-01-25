from langgraph.graph import StateGraph
from core.state import EngineState
from core.context import ExecutionContext

from agents.generator import idea_generator
from agents.market_eval import market_evaluator
from agents.business_eval import business_evaluator
from agents.technical_eval import technical_evaluator
from agents.arbiter import final_arbiter

def build_graph(ctx: ExecutionContext):


    graph = StateGraph(EngineState)

    graph.add_node("generator", lambda state: idea_generator(state, ctx))

    graph.add_node("market_eval", lambda state: market_evaluator(state, ctx))
    graph.add_node("business_eval", lambda state: business_evaluator(state, ctx))
    graph.add_node("technical_eval", lambda state: technical_evaluator(state, ctx))

    graph.add_node("arbiter", final_arbiter)

    graph.set_entry_point("generator")

    graph.add_edge("generator", "market_eval")
    graph.add_edge("generator", "business_eval")
    graph.add_edge("generator", "technical_eval")

    graph.add_edge("market_eval", "arbiter")
    graph.add_edge("business_eval", "arbiter")
    graph.add_edge("technical_eval", "arbiter")

    graph.set_finish_point("arbiter")

    return graph.compile()