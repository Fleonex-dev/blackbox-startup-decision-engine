import os
from llm.base import LLMClient
from llm.openai_llm import OpenAILLM

def get_llm() -> LLMClient:

    provider = os.getenv("LLM_PROVIDER", "mock")
    if provider == "mock":
        return MockLLM()
    elif provider == "openai":
        return OpenAILLM()
    
    raise ValueError(f"Unsupported LLM provider: {provider}")

class MockLLM(LLMClient):
    def generate(self, system: str, user: str) -> str:
       
       if "market" in system.lower():
           # Mock market evaluation response
           return '''{
               "component": "market",
               "status": "approved",
               "confidence": 0.9,
               "reason": "The market shows strong demand for B2B solutions."
           }'''
       elif "technical" in system.lower():
           # Mock technical evaluation response
           return '''{
               "component": "technical",
               "status": "approved",
               "confidence": 0.85,
               "reason": "The technology is feasible with current resources."
           }'''
       elif "business" in system.lower():
           # Mock business evaluation response
           return '''{
               "component": "business",
               "status": "approved",
               "confidence": 0.8,
               "reason": "The business model is sustainable and scalable."
           }'''
       else:
           return "{}"    