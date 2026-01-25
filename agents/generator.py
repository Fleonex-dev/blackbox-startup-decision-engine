import json
from core.state import EngineState
from core.context import ExecutionContext

"""Generator agent.

Responsible for producing the startup brief. The agent writes the 'brief'
key into the provided state and returns the mutated state (partial patch).
"""

def idea_generator(state: EngineState, context: ExecutionContext) -> EngineState:
    """Generate a startup brief and attach it to state.

    Inputs:
    - state: current EngineState (may be mutated)
    - context: ExecutionContext providing an LLM client

    Output:
    - the same EngineState instance with 'brief' populated

    Assumptions/Invariant:
    - LLM returns valid JSON with the expected fields. Caller is responsible for
      handling parse errors or schema validation if needed.
    """
    # Generate a single B2B startup brief and store it on state.
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