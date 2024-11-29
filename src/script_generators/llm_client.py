"""
OpenAI Client for generating the script
"""
from typing import Any, Dict, Callable
from openai import OpenAI


class LLMClient:
    provider: str = None
    model: str = None

    def __init__(self, llm_config: Dict):
        self.provider = llm_config.get("provider")
        self.model = llm_config.get("model")

    def initialize_client(self) -> Any:
        client = OpenAI
        interact = self.interact_openai
        if self.provider == "openai":
            client = OpenAI
            interact = self.interact_openai
        return client, interact

    @staticmethod
    def interact_openai(llm_client: Callable, prompt: str):
        with llm_client() as client:
            messages = [
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": "Provide me the script for the show"
                }
            ]
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                timeout=60)
            choice = completion.choices[0] if len(completion.choices) > 0 else None
            return choice.message.content

    def interact(self, prompt: str):
        llm_client, interact = self.initialize_client()
        return interact(llm_client, prompt)
