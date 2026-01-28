import json
from core.state import EngineState, Status
from core.context import ExecutionContext

"""Workflow Reality Gate Agent.

This agent acts as the first "bouncer" in the pipeline. It evaluates whether the
proposed idea addresses a real, recurring, and unavoidable workflow problem.

It does NOT assess market size or business viability. It only asks:
"Is this a real problem that happens frequently?"
"""

def workflow_gate(state: EngineState, context: ExecutionContext) -> EngineState:
    """Evaluate if the brief describes a valid workflow problem."""
    
    brief = state.get("brief")
    if not brief:
        # Should not happen if brief is provided manually, but handle safety.
        return state

    # Load prompt
    with open("prompts/workflow_gate.txt", "r") as f:
        system_prompt = f.read()

    # Format brief for the LLM
    brief_str = json.dumps(brief, indent=2)
    user_prompt = f"Analyze this startup brief for Workflow Reality:\n\n{brief_str}"

    # Call LLM
    raw_output = context.llm.generate(
        system=system_prompt,
        user=user_prompt
    )

    # Parse output
    try:
        result = json.loads(raw_output)
        decision = result.get("decision") # "PASS" or "KILL"
        reason = result.get("reason")
        confidence = result.get("confidence")
        
        # Store result in state
        state["workflow_gate_result"] = {
            "decision": decision,
            "reason": reason,
            "confidence": confidence
        }
        
        # If the gate kills it, we can set judgment_status immediately
        if decision == "KILL":
            state["judgment_status"] = Status.KILL
            state["final_decision"] = "KILL" # Sync for now
            
    except json.JSONDecodeError:
        # Fallback for parse error
        state["workflow_gate_result"] = {
            "decision": "KILL",
            "reason": "Agent output parsing failed",
            "confidence": 0.0
        }
        state["judgment_status"] = Status.KILL

    return state
