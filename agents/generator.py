import json
from core.state import EngineState
from core.context import ExecutionContext

def idea_generator(state: EngineState, context: ExecutionContext) -> EngineState:

    with open("prompts/generator.txt", "r") as f:
        system_prompt = f.read()

    user_prompt = "Generate one B2B startup idea"

    raw_output = context.llm.generate(
        system=system_prompt,
        user=user_prompt
    )

    brief = json.loads(raw_output)
    state["brief"] = brief
    return state