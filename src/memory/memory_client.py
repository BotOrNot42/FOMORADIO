"""
Memory for the LLMs
"""
from typing import Dict, List
from mem0 import Memory


class MemoryClient:
    """
    Memory for the agents to get a feeling of déjà vu
    """

    memory: Memory = None

    def __init__(self, config: Dict):
        """
        Initialize the memory from the config
        :param config: Configurations for the mem0 memory library
        """
        self.memory = Memory.from_config(config)

    def set(self, content, user_id, agent, metadata) -> Dict:
        """
        Function to add the memory
        :param content: Content to store in the memory
        :param user_id: ID for the user irrespective of the source agent
        :param agent: Name of the source where the data is collected from
        :param metadata: Extra data about the content
        :return: Memory fragments as dictionary
        """
        return self.memory.add(
            content, user_id=user_id, agent_id=agent, metadata=metadata
        )

    def get(self, query, user_id, agent):
        """
        Function to retrieve the related memories
        ordered by the relevance score
        :param query: Query to fetch the memories
        :param user_id: ID of the user whose memories belong to
        :param agent: Source of the user collected from
        :return: List of memory fragments
        """
        return self.memory.search(query, user_id=user_id, agent_id=agent)

    @staticmethod
    def memory_to_content(memories) -> List:
        """
        Helper function to convert memory to contents
        :param memories: List of memories
        :return: List of contents
        """
        content = []
        for each_memory in memories:
            content.append(
                {
                    "content": each_memory.get("memory"),
                    "primary_key": each_memory.get("user_id"),
                    "source": each_memory.get("agent_id"),
                    "metadata": each_memory.get("metadata"),
                }
            )
        return content

    @staticmethod
    def content_to_memory(contents) -> List:
        """
        Helper function to convert contents to memories
        :param contents: List of contents
        :return: List of memories
        """
        memories = []
        for each_content in contents:
            memories.append(
                {
                    "memory": each_content.get("content"),
                    "user_id": each_content.get("user"),
                    "agent_id": each_content.get("source"),
                    "metadata": each_content.get("metadata"),
                }
            )
        return memories

    def load_memory(self, memories: List) -> None:
        """
        Helper Function to bulk load memories from content
        :param memories: Memories to load
        :return: None
        """
        for each_memory in memories:
            self.set(
                each_memory.get("memory"),
                each_memory.get("user_id"),
                each_memory.get("source"),
                each_memory.get("metadata"),
            )
