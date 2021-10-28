"""
Integration tests for the Twitter connector module
"""

import pytest
import tweepy
from tweepy import models

import trendr.exceptions
from trendr.config import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
from trendr.connectors import twitter_connector


# Positive tests

@pytest.fixture
def twitter_api() -> tweepy.API:
    """
    Creates a tweepy.API object to be used by
    """
    yield twitter_connector.auth_to_api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)


def test_get_tweet_by_id_positive(twitter_api: tweepy.API):
    """
    Tests that if you attempt to get a tweet by id, then you get that tweet back
    """
    tweets = twitter_connector.get_tweets_mentioning_asset("and", api=twitter_api)
    tweet_id = tweets[0].__getattribute__("id")
    tweet = twitter_connector.get_tweet_by_id(tweet_id, api=twitter_api)
    assert tweet
    assert isinstance(tweet, tweepy.models.Status)
    assert tweet.__getattribute__("id") == tweet_id


def test_get_tweets_mentioning_asset_positive(twitter_api: tweepy.API):
    """
    Tests that if you attempt to get tweets with a search string, then you get some results back
    """
    search_term = "apple"
    tweets = twitter_connector.get_tweets_mentioning_asset(search_term, api=twitter_api)
    assert tweets
    assert isinstance(tweets, tweepy.models.SearchResults)
    assert tweets.__getattribute__("count") >= 1
    # Tweets are returned when attributes other than text contain the search term such as tweet.entities.urls so we
    # can't always assert the search term will be in the tweet text


# Negative tests


def test_get_tweet_by_id_invalid_id(twitter_api: tweepy.API):
    """
    Tests that when you try to retrieve a tweet that doesn't exist, you get a TweepError
    """
    tweet_id = -1
    with pytest.raises(tweepy.errors.TweepyException):
        twitter_connector.get_tweet_by_id(tweet_id, api=twitter_api)


def test_get_tweet_by_id_unauthenticated():
    """
    Tests that when you try to authenticate to the Twitter API without a key and secret, you get a ConnectorException
    """
    tweet_id = -1
    with pytest.raises(trendr.exceptions.ConnectorException):
        twitter_connector.get_tweet_by_id(tweet_id, api=twitter_connector.auth_to_api("", ""))
