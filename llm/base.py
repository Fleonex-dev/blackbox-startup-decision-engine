from abc import ABC, abstractmethod

"""LLM client interface.

Defines the minimal contract agents rely on: synchronous generation of text
given system and user prompts. Implementations must return the raw string
model output (parsing/validation happens in agents).
"""

class LLMClient(ABC):
    # Minimal LLM client interface; returns string output.
    @abstractmethod
    def generate(self, system: str, user: str) -> str:
        pass
