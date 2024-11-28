"""
Web Scrapper Client for FOMO
"""

from typing import Tuple, List, Dict, Any
from .collector import BaseCollector


class ScrapperClient(BaseCollector):
    """
    Collector Wrapper for the Web Scrapper
    """
    source: str = "scrapper"
    client: Any = None

    def fetch(self) -> Tuple[List[Dict], str, str]:
        """
        TODO: Fetching Logic of Web Scrapping Messages
        """
