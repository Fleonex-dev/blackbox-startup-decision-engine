from core.state import EngineState

def final_arbiter(state: EngineState) -> EngineState:

    market = state["market_eval"]
    business = state["business_eval"]
    technical = state["technical_eval"]

    if(
        market["status"] == "approved" and
        business["status"] == "approved" and
        technical["status"] == "approved"
    ):
        state["final_decision"] = "BUILD"
    else:
        state["final_decision"] = "KILL"

    return state