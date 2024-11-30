"""
Text to Speech modules for Fomo
"""
from typing import Any, Dict, Callable
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings


class TTSClient:
    """
    Wrapper for the TTS Model Clients
    client libraries. Currently, supports: ElevenLabs
    TODO: Support more models like Amazon Polly, OpenAI TTS
    """

    provider: str = None
    model: str = None
    api_key: str = None

    def __init__(self, tts_config: Dict, api_key: str):
        """
        Initialize the provider and voice model to use from the configurations
        """
        self.provider = tts_config.get("provider")
        self.model = tts_config.get("model")
        self.api_key = api_key

    def initialize_client(self) -> Any:
        """
        Initializing the client using the provider's client library and
        desired model to use
        """
        client = ElevenLabs
        interact = self.interact_elevenlabs
        if self.provider == "elevenlabs":
            client = ElevenLabs
            interact = self.interact_elevenlabs
        return client, interact

    def interact_elevenlabs(self, tts_client: Callable, script: str, voice_id: str) -> str:
        """
        Helper Function to interact with the Eleven Labs Audio Models
        :param tts_client: Defines the provider's TTS client functions
        :param script: Script to be converted
        :param voice_id: Voice ID for the RJ
        :return: Generated Audio Response from the voice model
        """
        client = tts_client(api_key=self.api_key)
        voice_settings = VoiceSettings(
            stability=0.2,
            similarity_boost=0.8
        )
        return client.generate(
            text=script,
            voice=voice_id,
            model=self.model,
            voice_settings=voice_settings
        )
