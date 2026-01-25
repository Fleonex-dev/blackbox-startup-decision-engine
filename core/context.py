from typing import Optional, Dict, Any
from llm.base import LLMClient

class ExecutionContext:
    def __init__(
        self,
        llm: LLMClient,
        retriever: Optional[Any] = None,
        tools: Optional[Dict[str, Any]] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        self.llm = llm
        self.retriever = retriever
        self.tools = tools or {}
        self.config = config or {}