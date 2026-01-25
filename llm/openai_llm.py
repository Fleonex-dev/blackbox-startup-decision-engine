from openai import OpenAI
from llm.base import LLMClient


class OpenAILLM(LLMClient):
    def __init__(self, model: str = "gpt-40-mini", max_tokens: int = 500):
        self.client = OpenAI()
        self.model = model
        self.max_tokens = max_tokens

    def generate(self, system: str, user: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            max_tokens=self.max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content