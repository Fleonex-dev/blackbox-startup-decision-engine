from core.state import EngineState

"""Arbiter that produces the final build/kill decision.

The arbiter expects three evaluator results to be present on state and
applies a deterministic rule to set final_decision.
"""

def final_arbiter(state: EngineState) -> EngineState:
    """Apply the final decision rule.

    Inputs:
    - state: EngineState containing market_eval, business_eval, technical_eval

    Output:
    - same EngineState with 'final_decision' set to "BUILD" or "KILL"

    Assumptions:
    - Each eval dict contains a 'status' key with values matching Status enum.
    - Caller ensures evaluators have run before invoking the arbiter.
    """
    # If all evals PASS set BUILD, otherwise set KILL.
    market = state["market_eval"]
    business = state["business_eval"]
    technical = state["technical_eval"]

    if(
        market["status"] == "PASS" and
        business["status"] == "PASS" and
        technical["status"] == "PASS"
    ):
        state["final_decision"] = "BUILD"
    else:
        state["final_decision"] = "KILL"

    return state