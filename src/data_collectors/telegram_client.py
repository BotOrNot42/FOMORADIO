"""
Telegram Client for FOMO
"""

from typing import Tuple, List, Dict
import telethon
from .collector import BaseCollector


class TelegramClient(BaseCollector):
    """
    Collector Wrapper for the Telegram
    """
    source: str = "telegram"
    client: telethon.TelegramClient = None
    bearer_token: str = None

    def __init__(self, session_name: str, api_id: int, api_hash: str) -> None:
        """
        Initializes a new instance of the class
        :param session_name: The name of the session, which is used to store
        client data locally.
        :param api_id: The API ID obtained from the Telegram Developer Portal.
        :param api_hash: The API hash associated with the provided API ID.
        :return: None
        """
        self.client = telethon.TelegramClient(session_name, api_id, api_hash)
        super().__init__()

    def fetch(self) -> Tuple[List[Dict], str, str, str]:
        """
        TODO: Fetching Logic of Telegram Messages
        """
