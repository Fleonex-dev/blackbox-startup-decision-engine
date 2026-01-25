import json
from core.state import EngineState
from core.context import ExecutionContext

def business_evaluator(state: EngineState, context: ExecutionContext) -> EngineState:
    
    with open("prompts/business.txt", "r") as f:
        system_prompt = f.read()

    user_prompt = f"""
    Evaluate the following B2B startup idea for its business potential:
    {json.dumps(state['brief'], indent=2)}
    
    Provide your evaluation in the following JSON format:
    {{
        "component": "business",
        "status": "approved" or "rejected",
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