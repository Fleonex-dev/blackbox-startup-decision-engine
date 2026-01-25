import json
from core.state import EngineState
from core.context import ExecutionContext

"""Business evaluator agent.

Evaluates business viability and returns a partial state patch with
'business_eval'.
"""

def business_evaluator(state: EngineState, context: ExecutionContext) -> EngineState:
    """Evaluate business potential and return {'business_eval': eval_result}.

    Inputs:
    - state: EngineState containing 'brief'
    - context: ExecutionContext with llm

    Output:
    - dict with 'business_eval' key mapping to parsed EvalResult

    Assumptions:
    - The LLM returns well-formed JSON that matches the expected schema.
    """
    # Call the business prompt and return {'business_eval': ...}.
    with open("prompts/business.txt", "r") as f:
        system_prompt = f.read()

    user_prompt = f"""
    Evaluate the following B2B startup idea for its business potential:
    {json.dumps(state['brief'], indent=2)}
    
    Provide your evaluation in the following JSON format:
    {{
        "component": "business",
        "status": "PASS" or "KILL",
        "confidence": float between 0 and 1,
        "reason": "detailed explanation"
    }}
    """

    raw_output = context.llm.generate(
        system=system_prompt,
        user=user_prompt
    )

    eval_result = json.loads(raw_output)

    return {
        "business_eval": eval_result
    }