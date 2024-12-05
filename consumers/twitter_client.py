"""
Twitter Consumer Client for FOMO
"""
from typing import Tuple, Union
import time
import tweepy


class TwitterException(Exception):
    """
    Twitter Related Exceptions are handled here :)
    """


class TwitterConsumerClient:
    """
    Consumer Wrapper for the Twitter
    """
    source: str = "twitter"
    client: tweepy.Client = None
    api_client: tweepy.API = None
    max_retries: int = 3
    retry_delay: int = 5

    def __init__(
        self, api_key: str, api_secret: str, access_token: str, access_token_secret: str
    ):
        """
        Initializes a new instance of the class
        :param api_key: API Key of the Twitter App from Twitter Developer Portal
        :param api_secret: API Secret of the Twitter App from Twitter Developer Portal
        :param access_token: Access Token of the user after successful OAuth
        :param access_token_secret: Access Token Secret of the user after
        successful OAuth
        :return: None
        """
        auth = tweepy.OAuth1UserHandler(
            api_key, api_secret, access_token, access_token_secret
        )
        self.client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )
        self.api_client = tweepy.API(auth)

    def post_tweet(self, tweet_content: str) -> Tuple[bool, Union[str, None]]:
        """
        Helper Method to post tweets in Twitter without media
        :param tweet_content: Tweet content to be posted
        :return: Boolean with necessary error if there are any
        """
        try:
            self.client.create_tweet(text=tweet_content)
            return True, None
        except TwitterException as exception:
            return False, str(exception)

    def post_tweet_with_media(
        self, tweet_content: str, path: str
    ) -> Tuple[bool, Union[str, None]]:
        """
        Helper Method to post tweets in Twitter with media
        :param tweet_content: Tweet content to be posted
        :param path: Path of the media file
        :return: Boolean with necessary error if there are any
        """
        try:
            is_uploaded, detail = self.upload_media(path)
            if is_uploaded:
                self.client.create_tweet(text=tweet_content, media_ids=[detail])
                return True, None
            raise TwitterException(detail)
        except TwitterException as exception:
            return False, str(exception)

    def upload_media(self, media_path: str):
        """
        Helper Method to upload media files to twitter
        :param media_path: Path of the media file
        :return: Boolean with necessary error if there are any
        """
        try:
            media = self.api_client.media_upload(
                filename=media_path, media_category="tweet_video"
            )
            # Wait for media processing to complete with retry logic
            retries = 0
            while retries < self.max_retries:
                if hasattr(media, "processing_info"):
                    processing_info = media.processing_info
                    if processing_info["state"] == "succeeded":
                        return True, media.media_id
                    if processing_info["state"] == "failed":
                        raise TwitterException("Media Upload Failed")
                    time.sleep(self.retry_delay)
                    retries += 1
                else:
                    break
            if (
                retries == self.max_retries
                and hasattr(media, "processing_info")
                and media.processing_info["state"] != "succeeded"
            ):
                return True, media.media_id
            raise TwitterException("Media Upload Failed")
        except TwitterException as exception:
            return False, str(exception)
