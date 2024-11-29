"""
News Client for FOMO
"""

from typing import Tuple, List, Dict, Any
from .collector import BaseCollector


class NewsClient(BaseCollector):
    """
    Collector Wrapper for the News
    """

    source: str = "news"
    client: Any = None

    def fetch(self) -> Tuple[List[Dict], str, str, str]:
        """
        TODO: Fetching Logic of News Messages
        """
