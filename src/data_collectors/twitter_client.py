"""
Twitter Client for FOMO
"""
import random
from typing import Tuple, List, Dict
from datetime import datetime, timedelta
import tweepy
from .collector import BaseCollector


class TwitterClient(BaseCollector):
    """
    Collector Wrapper for the Twitter
    """
    source: str = "twitter"
    client: tweepy.Client = None
    host_twitter_handle: str = None
    influencers: List = None

    def __init__(self, bearer_token: str, host_handle: str, influencers: List):
        """
        Initializes a new instance of the class
        :param bearer_token: The API Token from the Twitter Developer Portal.
        :return: None
        """
        self.client = tweepy.Client(bearer_token=bearer_token)
        self.host_twitter_handle = host_handle
        if influencers:
            self.influencers = influencers
        else:
            self.influencers = list(host_handle)
        super().__init__()

    def fetch_tweets(self, query: str) -> List[Dict]:
        """
        Fetches the query in the recent tweets like last 15 minutes and
        returns all the tweets matching them with public metrics.
        :param query: Query to search for
        :return: List of tweets
        """
        start_time = datetime.now()
        end_time = datetime.now() - timedelta(seconds=15)
        response = self.client.search_recent_tweets(
            query=query,
            max_results=15,
            tweet_fields=[
                "author_id", "created_at", "id", "text", "public_metrics",
                "entities", "geo", "lang", "source"
            ],
            start_time=start_time,
            end_time=end_time
        )
        tweets = response.data
        return [i.data for i in tweets] if tweets and len(tweets) > 0 else []

    def get_latest_mentions(self) -> List[Dict]:
        """
        Fetches tweets in which the host is mentioned
        for the last 15 minutes
        """
        query = f"@{self.host_twitter_handle} -is:retweet"
        return self.fetch_tweets(query)

    def get_tweets_from_influencer(self) -> List[Dict]:
        """
        Fetches tweets from the influencers mentioned
        for the last 15 minutes
        """
        query = " OR ".join([f"from:{username}" for username in self.influencers])
        return self.fetch_tweets(query)

    def fetch(self) -> Tuple[List[Dict], str, str]:
        """
        Method to fetch the tweets from Twitter
        """
        pick = [self.get_latest_mentions, self.get_tweets_from_influencer]
        func = random.choice(pick)
        return func()
