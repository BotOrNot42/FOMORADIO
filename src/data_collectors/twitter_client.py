"""
Twitter Client for FOMO
"""

from typing import Tuple, List, Dict
import tweepy
from .collector import BaseCollector


class TwitterClient(BaseCollector):
    """
    Collector Wrapper for the Twitter
    """
    source: str = "twitter"
    client: tweepy.Client = None

    def __init__(self, bearer_token: str):
        """
        Initializes a new instance of the class
        :param bearer_token: The API Token from the Twitter Developer Portal.
        :return: None
        """
        self.client = tweepy.Client(bearer_token=bearer_token)
        super().__init__()

    def fetch(self) -> Tuple[List[Dict], str, str]:
        """
        Method to fetch the tweets from Twitter
        """
