import json
from core.state import EngineState
from core.context import ExecutionContext

"""Technical evaluator agent.

Assesses technical feasibility and returns a partial state patch with
'technical_eval'.
"""

def technical_evaluator(state: EngineState, context: ExecutionContext) -> EngineState:
    """Evaluate technical feasibility and return {'technical_eval': eval_result}.

    Inputs:
    - state: EngineState with populated 'brief'
    - context: ExecutionContext with llm

    Output:
    - dict with 'technical_eval' key mapping to parsed EvalResult

    Assumptions:
    - The LLM returns valid JSON using the expected keys and casing.
    """
    # Call the technical prompt and return {'technical_eval': ...}.
    with open("prompts/technical.txt", "r") as f:
        system_prompt = f.read()

    user_prompt = f"""
    Evaluate the following B2B startup idea for its technical potential:
    {json.dumps(state['brief'], indent=2)}
    
    Provide your evaluation in the following JSON format:
    {{
        "component": "technical",
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
        "technical_eval": eval_result
    }