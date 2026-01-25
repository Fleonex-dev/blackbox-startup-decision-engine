import json
from core.state import EngineState
from core.context import ExecutionContext

def technical_evaluator(state: EngineState, context: ExecutionContext) -> EngineState:

    with open("prompts/technical.txt", "r") as f:
        system_prompt = f.read()

    user_prompt = f"""
    Evaluate the following B2B startup idea for its technical potential:
    {json.dumps(state['brief'], indent=2)}
    
    Provide your evaluation in the following JSON format:
    {{
        "component": "technical",
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
    state["technical_eval"] = eval_result
    return state