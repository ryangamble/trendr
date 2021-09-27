"""
Functions for interacting with the Twitter API using the tweepy library
"""

import tweepy

from trendr.config import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
from trendr.exceptions import ConnectorException


def auth_to_api(consumer_key: str, consumer_secret: str) -> tweepy.API:
    """
    Authenticates to the Twitter API so that we can query it

    :param consumer_key: The consumer key for the Twitter developer account
    :param consumer_secret: The consumer secret for the Twitter developer account
    :return: A tweepy API object
    """
    if consumer_key and consumer_secret:
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        return tweepy.API(auth)
    else:
        raise ConnectorException("Could not authenticate to Twitter because the necessary secrets were not available.")


def get_tweet_by_id(tweet_id: int, api: tweepy.API = None) -> tweepy.Status:
    """
    Gets all the information available for given tweet.

    :param tweet_id: The Twitter id for the tweet
    :param api: An optional tweepy.API object, if one is not provided it will be created
    :return: A tweepy.Status object
    """
    if not api:
        api = auth_to_api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    return api.get_status(tweet_id)


def get_tweets_mentioning_asset(
        asset_identifier: str, since_id: str = None, api: tweepy.API = None
) -> tweepy.SearchResults:
    """
    Queries Twitter for tweets that mention an asset_identifier (AAPL, BTC) within the last 7 days, starting at the
    tweet with the id since_id if one is provided.

    :param asset_identifier: The identifier for the asset (AAPL, BTC), not a database id
    :param since_id: The id of the oldest tweet to start searching from
    :param api: An optional tweepy.API object, if one is not provided it will be created
    :return: A tweepy.SearchResults object
    """
    if not api:
        api = auth_to_api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    return api.search(q=asset_identifier, since_id=since_id)
