"""
Twitter Client for FOMO
"""
import tweepy
from .collector import BaseCollector

class TwitterClient(BaseCollector):

    source: str = "twitter"
    bearer_token: str = None

    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token
        super().__init__()

    def fetch(self):
        client = tweepy.Client(bearer_token=bearer_token)
