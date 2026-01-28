import json
from core.state import EngineState
from core.context import ExecutionContext
from core.prompts import load_prompt

"""Market evaluator agent.

Calls the market-oriented system prompt and returns a partial state patch
containing 'market_eval'. Agents parse raw LLM output into structured data.
"""

def market_evaluator(state: EngineState, context: ExecutionContext) -> EngineState:
    """Evaluate market potential and return {'market_eval': eval_result}.

    Inputs:
    - state: EngineState with 'brief' present
    - context: ExecutionContext with llm

    Output:
    - dict with 'market_eval' key mapping to parsed EvalResult

    Assumptions:
    - 'brief' exists on state when called.
    - LLM returns valid JSON matching the expected EvalResult schema.
    """
    # Call the market prompt and return {'market_eval': ...}.
    system_prompt = load_prompt("market_eval.txt")

    user_prompt = f"""
    Evaluate the following B2B startup idea for its market potential:
    {json.dumps(state['brief'], indent=2)}
    
    Provide your evaluation in the following JSON format:
    {{
        "component": "market",
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
        "market_eval": eval_result
    }