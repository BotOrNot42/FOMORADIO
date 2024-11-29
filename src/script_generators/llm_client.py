"""
OpenAI Client for generating the script
"""
from typing import Any, Dict, Callable
from openai import OpenAI


class LLMClient:
    """
    LLM Wrapper for the models and their respective
    client libraries. Currently, supports: OpenAI
    TODO: Support more models like GROK, Azure AI, Google VertexAI
    """

    provider: str = None
    model: str = None

    def __init__(self, llm_config: Dict):
        """
        Initialize the provider and llm model to use from the configurations
        """
        self.provider = llm_config.get("provider")
        self.model = llm_config.get("model")

    def initialize_client(self) -> Any:
        """
        Initializing the client using the provider's client library and
        desired model to use
        """
        client = OpenAI
        interact = self.interact_openai
        if self.provider == "openai":
            client = OpenAI
            interact = self.interact_openai
        return client, interact

    @staticmethod
    def interact_openai(llm_client: Callable, prompt: str) -> str:
        """
        Helper Function to interact with the OpenAI LLMs
        :param llm_client: Defines the provider's client functions
        :param prompt: Prompt to query the model with
        :return: Generated response from the model
        """
        with llm_client() as client:
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Provide me the script for the show"},
            ]
            completion = client.chat.completions.create(
                model="gpt-4o-mini", messages=messages, timeout=60
            )
            choice = completion.choices[0] if len(completion.choices) > 0 else None
            return choice.message.content

    def interact(self, prompt: str) -> str:
        """
        Interacts with the LLM Provider and model to generate the response
        :param prompt: Prompt for the LLM Model
        :return: Generated response
        """
        llm_client, interact = self.initialize_client()
        return interact(llm_client, prompt)
