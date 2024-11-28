"""
Text Client for FOMO
"""

from typing import Tuple, List, Dict, Any
from .collector import BaseCollector


class TextClient(BaseCollector):
    """
    Collector Wrapper for the Text related apps
    """
    source: str = "text"
    client: Any = None

    def fetch(self) -> Tuple[List[Dict], str, str, str]:
        """
        TODO: Fetching Logic of Text Messages
        """
