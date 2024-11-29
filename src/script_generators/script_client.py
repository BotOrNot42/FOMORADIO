"""
Generates Script for the Show
"""
from pytz import UTC
from typing import List, Dict
from datetime import datetime
from src.memory import MemoryClient
from src.config.prompt import script_generation_prompt


class ScriptClient:
    """
    Script Generator based on the memories of the RJ
    """
    users: List[str] = None
    current_host: Dict = None
    next_host: str = None
    show_details: Dict = None

    def __init__(self, users: List[str], show_details: Dict, current_host: Dict, next_host: str):
        self.users = users
        self.current_host = current_host
        self.next_host = next_host
        self.show_details = show_details

    def extract_memories(self):
        memories = []
        for each_user in self.users:
            memories.extend(self.current_host['memory'].get(
                "List the latest tweets from this user for the past 15 minutes",
                user_id=each_user
            ))
        return MemoryClient.memory_to_content(memories)

    def generate_prompt(self):
        contents = self.extract_memories()
        return script_generation_prompt.format(
            show_name=self.show_details.get("show_name"),
            radio_name=self.show_details.get("aired_on"),
            host=self.current_host,
            host_name=self.current_host.get("host_name"),
            current_utc_time=datetime.now(UTC).strftime("%I:%M %p UTC"),
            alternate_host_name=self.next_host,
            formatted_content=contents
        )