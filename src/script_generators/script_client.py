"""
Generates Script for the Show
"""
from typing import List, Dict
from src.memory import MemoryClient
from src.config.prompt import SCRIPT_GENERATION_PROMPT


class ScriptClient:
    """
    Script Generator based on the memories of the RJ
    """

    users: List[str] = None
    current_host: Dict = None
    next_host: str = None
    show_details: Dict = None

    def __init__(
        self, users: List[str], show_details: Dict, current_host: Dict, next_host: str
    ):
        self.users = users
        self.current_host = current_host
        self.next_host = next_host
        self.show_details = show_details

    def extract_memories(self, agent: str) -> List:
        """
        Helper function to extract the related memories from the memory.
        :param agent: Source of the memory collected from
        :return: List of contents
        """
        memories = []
        for each_user in self.users:
            memories.extend(
                self.current_host["memory"].get(
                    "List the latest tweets from this user for the past 15 minutes",
                    user_id=each_user,
                    agent=agent,
                )
            )
        return MemoryClient.memory_to_content(memories)

    def generate_prompt(self, agent: str, current_time: str) -> str:
        """
        Generate the prompt used for creating the script for the show
        :param agent: Source of the collected data to fed to the script generation
        :param current_time: Current time of the show
        :return: Prompt to create the show script
        """
        contents = self.extract_memories(agent)
        return SCRIPT_GENERATION_PROMPT.format(
            show_name=self.show_details.get("name"),
            show_motive=self.show_details.get("description"),
            radio_name=self.show_details.get("aired_on"),
            host=self.current_host,
            host_name=self.current_host.get("host_name"),
            current_utc_time=current_time,
            alternate_host_name=self.next_host,
            formatted_content=contents,
        )
