import os
import json
from llm.base import LLMClient
from llm.openai_llm import OpenAILLM
from llm.mock_llm import MockLLM

def get_llm() -> LLMClient:

    provider = os.getenv("LLM_PROVIDER", "mock")
    if provider == "mock":
        return MockLLM()
    elif provider == "openai":
        return OpenAILLM()
    
    raise ValueError(f"Unsupported LLM provider: {provider}")