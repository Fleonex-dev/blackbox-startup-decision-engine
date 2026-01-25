import os
import json
from llm.base import LLMClient
from llm.openai_llm import OpenAILLM
from llm.mock_llm import MockLLM

"""Factory to select the LLM implementation.

Selection is controlled via the LLM_PROVIDER environment variable. Default is
'mock' to keep local runs deterministic and fast.
"""

def get_llm() -> LLMClient:
    """Return LLM implementation based on LLM_PROVIDER env var."""
    provider = os.getenv("LLM_PROVIDER", "mock")
    if provider == "mock":
        return MockLLM()
    elif provider == "openai":
        return OpenAILLM()
    
    raise ValueError(f"Unsupported LLM provider: {provider}")