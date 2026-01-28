import json
import asyncio
from typing import List, Dict
import os
import uuid
import sys
import os

# Add project root to path so we can import core/agents/etc
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set provider to mock if not set, or OpenAI if keys are present
# os.environ["LLM_PROVIDER"] = "openai" # User must set this if they want real evaluation
# If running with mock, we expect random/fixed results.

from core.context import ExecutionContext
from graph import build_graph
from core.state import EngineState, Status

def load_calibration_set():
    with open("tests/calibration_set.json", "r") as f:
        return json.load(f)

def run_evaluation(brief: Dict):
    run_id = f"test_{uuid.uuid4().hex[:8]}"
    state: EngineState = {
        "run_id": run_id,
        "brief": brief,
        "workflow_gate_result": None,
        "market_eval": None,
        "business_eval": None,
        "technical_eval": None,
        "final_decision": None,
        "judgment_status": None
    }
    
    # Setup context (Mock or OpenAI based on env)
    from llm.factory import get_llm
    llm = get_llm()
    ctx = ExecutionContext(llm=llm) 
    graph = build_graph(ctx)
    
    final_state = graph.invoke(state)
    return final_state

def verify():
    test_cases = load_calibration_set()
    results = []
    
    print(f"Running {len(test_cases)} calibration tests...")
    
    for case in test_cases:
        expected = case["expected_verdict"]
        brief = case["brief"]
        print(f"\nEvaluating: {brief['concept_hook']} (Expected: {expected})")
        
        final_state = run_evaluation(brief)
        decision = final_state.get("final_decision")
        gate_result = final_state.get("workflow_gate_result")
        
        print(f"  -> Gate Result: {gate_result.get('decision') if gate_result else 'SKIPPED'}")
        print(f"  -> Final Decision: {decision}")
        
        success = (decision == expected)
        results.append(success)
        
        if not success:
            print(f"  [FAILURE] Expected {expected} but got {decision}")
            if decision == "KILL":
                # Show who killed it
                if gate_result and gate_result.get("decision") == "KILL":
                    print(f"  Reason: Gate Killed - {gate_result.get('reason')}")
                else:
                    evals = [
                        ("Market", final_state.get("market_eval")),
                        ("Business", final_state.get("business_eval")),
                        ("Tech", final_state.get("technical_eval"))
                    ]
                    for name, res in evals:
                        if res and res.get("status") == "KILL":
                            print(f"  Reason: {name} Killed - {res.get('reason')}")
    
    pass_rate = sum(results) / len(results)
    print(f"\nSensitivity: {pass_rate:.1%} Correctness")

if __name__ == "__main__":
    verify()
