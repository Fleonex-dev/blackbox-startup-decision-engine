import os
from llm.base import LLMClient

def get_llm() -> LLMClient:

    provider = os.getenv("LLM_PROVIDER", "mock")
    if provider == "mock":
        return MockLLM()
    
    raise ValueError(f"Unsupported LLM provider: {provider}")

class MockLLM(LLMClient):
    def generate(self, system: str, user: str) -> str:
        return "{}"
    