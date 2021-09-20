import datetime
import tweepy

from trendr.config import (
    TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
)


def auth_to_api(consumer_key, consumer_secret, access_token, access_token_secret):
    """
    Authenticates to the Twitter API so that we can query it

    :param consumer_key: The consumer key for the Twitter developer account
    :param consumer_secret: The consumer secret for the Twitter developer account
    :param access_token: A Twitter access token
    :param access_token_secret: A Twitter access token secret
    :return: tweepy.API
    """
    # TODO: May want to wrap this in a try except and catch tweepy exceptions
    if consumer_key and consumer_secret and access_token and access_token_secret:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)
    else:
        # TODO: we probably want to develop our own exception classes
        raise Exception("Could not authenticate to Twitter because the necessary secrets were not available.")


def get_tweets_mentioning_asset(asset_identifier: str, start_time: datetime, end_time: datetime):
    """
    Queries Twitter for tweets that mention an asset_identifier (AAPL, BTC) within a time range

    :param asset_identifier: The identifier for the asset (AAPL, BTC), not a database id
    :param start_time: The datetime to start querying
    :param end_time: The datetime to finish querying
    :return: [dict]
    """
    api = auth_to_api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    return api.search(q=asset_identifier)  # TODO: add time range logic


def get_tweet_by_id(tweet_id: str):
    """
    Gets all the information available for given tweet

    :param tweet_id: The Twitter id for the tweet
    :return: dict
    """
    api = auth_to_api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    return api.get_status(tweet_id)
