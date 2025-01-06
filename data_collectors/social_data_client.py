"""
Social Data Client for FOMO
"""
import time
import requests
import urllib.parse
from typing import Tuple, List, Dict, Any
from .collector import BaseCollector


class SocialDataClient(BaseCollector):
    """
    Collector Wrapper for the Social Data apps
    """

    source: str = "social-data"
    # Data fetching interval is kept for past 4 hours
    time_interval: int = 14400
    headers = {
        'Accept': 'application/json'
    }
    influencer: str = None
    fetch_type: str = None
    timestamp_key: str = "tweet_created_at"
    content_key: str = "full_text"
    user_key: str = "user_id"


    def __init__(self, api_key: str, influencer: str, fetch_type: str="Latest"):
        """
        Initializes a new instance of the class
        :param api_key: Social Data API Key
        :param influencer: X User/Project handle
        :param fetch_type: Latest / Top strategy to fetch the data
        :return: None
        """
        if not influencer:
            raise Exception("Influencer handle is needed to fetch the data")
        if not api_key:
            raise Exception("Social Data API Key is needed")
        self.headers["Authorization"] = f"Bearer {api_key}"
        self.influencer = influencer
        self.fetch_type = fetch_type
        super().__init__()

    def fetch_tweets(self, query: str):
        all_tweets = []
        cursor = None
        while True:
            url = (
                f'https://api.socialdata.tools/twitter/search?query={query}&type={self.fetch_type}'
            )
            if cursor:
                url += f"&cursor={cursor}"
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                if "tweets" in data:
                    tweets = data["tweets"]
                    all_tweets.extend(tweets)
                else:
                    break
                cursor = data.get("cursor")
                if not cursor:
                    break
            except requests.exceptions.RequestException as _:
                break
        return all_tweets

    def fetch_user_details(self) -> Dict:
        """
        Fetch User Details from twitter using Social Data
        :return: Influencer details as a dictionary
        """
        url = f"https://api.socialdata.tools/twitter/user/{self.influencer}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_tweets_from_handle(self) -> List[Dict[str, Any]]:
        """
        Fetch User Posted Tweets from Twitter using Social Data
        :return: List of all the tweets posted by the given influencer
        """
        current_time = int(time.time())
        since_time = current_time - self.time_interval
        query = (f"from:{self.influencer} -filter:replies "
                 f"since_time:{since_time} until_time:{current_time}")
        encoded_query = urllib.parse.quote(query)
        return self.fetch_tweets(encoded_query)

    def fetch_reply_tweets_from_handle(self) -> List[Dict[str, Any]]:
        """
        Fetch User Replied Tweets from Twitter using Social Data
        :return: List of all the tweets replied by the given influencer
        """
        current_time = int(time.time())
        since_time = current_time - self.time_interval
        query = (f"from:{self.influencer} filter:replies "
                 f"since_time:{since_time} until_time:{current_time}")
        encoded_query = urllib.parse.quote(query)
        return self.fetch_tweets(encoded_query)

    def fetch_retweeted_tweets_from_handle(self) -> List[Dict[str, Any]]:
        """
        Fetch User Replied Re-tweets from Twitter using Social Data
        :return: List of all the re-tweets posted by the given influencer
        """
        current_time = int(time.time())
        since_time = current_time - self.time_interval
        query = (f"from:{self.influencer} filter:nativeretweets "
                 f"since_time:{since_time} until_time:{current_time}")
        encoded_query = urllib.parse.quote(query)
        return self.fetch_tweets(encoded_query)

    def fetch(self) -> Tuple[List[Dict], str, str, str]:
        tweets = []
        tweets.extend(self.fetch_tweets_from_handle())
        tweets.extend(self.fetch_reply_tweets_from_handle())
        tweets.extend(self.fetch_retweeted_tweets_from_handle())
        for each_tweet in tweets:
            each_tweet["user_id"] = each_tweet["user"]["id"]
            del each_tweet["user"]
            del each_tweet["entities"]
        return tweets, self.timestamp_key, self.content_key, self.user_key
