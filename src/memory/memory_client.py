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
        self.memory = Memory.from_config(config)

    def set(self, content, user_id, agent_id, metadata):
        return self.memory.add(content, user_id=user_id, agent_id=agent_id, metadata=metadata)

    def get(self, query, user_id, agent_id):
        return self.memory.search(query, user_id=user_id, agent_id=agent_id)

    @staticmethod
    def memory_to_content(memories):
        content = []
        for each_memory in memories:
            content.append({
                "content": each_memory.get("memory"),
                "primary_key": each_memory.get("user_id"),
                "metadata": each_memory.get("metadata")
            })
        return content

    @staticmethod
    def content_to_memory(contents):
        memories = []
        for each_content in contents:
            memories.append({
                "memory": each_content.get("content"),
                "user_id": each_content.get("user"),
                "agent_id": each_content.get("source"),
                "metadata": each_content.get("metadata")
            })
        return memories

    def load_memory(self, memories: List):
        for each_memory in memories:
            self.set(
                each_memory.get("memory"),
                each_memory.get("user_id"),
                each_memory.get('source'),
                each_memory.get("metadata")
            )
