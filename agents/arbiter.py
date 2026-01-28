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
    # Sort priorities: KILL > INSUFFICIENT_INFO > PASS
    evals = [state.get("market_eval"), state.get("business_eval"), state.get("technical_eval")]
    
    # Filter out Nones (in case some didn't run, though graph should ensure they do if we reach here)
    valid_evals = [e for e in evals if e is not None]

    statuses = [e["status"] for e in valid_evals]
    
    if "KILL" in statuses:
        state["final_decision"] = "KILL"
    elif "INSUFFICIENT_INFO" in statuses:
        state["final_decision"] = "INSUFFICIENT_INFO"
    elif all(s == "PASS" for s in statuses) and len(valid_evals) == 3:
        state["final_decision"] = "BUILD"
    else:
        # Fallback if something is missing or weird
        state["final_decision"] = "KILL"


    return state