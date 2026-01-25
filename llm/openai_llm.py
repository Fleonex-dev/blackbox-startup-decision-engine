from openai import OpenAI
from llm.base import LLMClient

"""OpenAI-backed LLM client.

This implementation performs a direct synchronous call to the OpenAI SDK.
It intentionally keeps retries and error handling out of scope; callers should
wrap or replace with a resilient wrapper in production.
"""


class OpenAILLM(LLMClient):
    # OpenAI-backed LLM client; calls the OpenAI chat completions API.
    def __init__(self, model: str = "gpt-40-mini", max_tokens: int = 500):
        self.client = OpenAI()
        self.model = model
        self.max_tokens = max_tokens

    def generate(self, system: str, user: str) -> str:
        """Call the OpenAI chat completions endpoint and return the content string.

        Inputs:
        - system: system prompt
        - user: user prompt

        Output:
        - raw string content from the model response

        Note: no retry/backoff is implemented here.
        """
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