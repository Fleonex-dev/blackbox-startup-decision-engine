from typing import Optional, Dict, Any
from llm.base import LLMClient

"""Execution context passed to agent functions.

Contains runtime dependencies such as the LLM client and optional helper
components (retriever, tools, config). Agents depend on this lightweight
container to avoid global state.
"""

class ExecutionContext:
    # Container for runtime dependencies used by agents.
    def __init__(
        self,
        llm: LLMClient,
        retriever: Optional[Any] = None,
        tools: Optional[Dict[str, Any]] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        self.llm = llm
        self.retriever = retriever
        # Use empty dicts to avoid None checks in agents.
        self.tools = tools or {}
        self.config = config or {}