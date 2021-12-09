"""
Integration tests for the Twitter connector module
"""

import pytest
import tweepy
from tweepy import models

import trendr.exceptions
from trendr.connectors import twitter_connector
from trendr.models.tweet_model import Tweet


# Positive tests


def test_get_tweet_by_id_positive(client, db):
    """
    Tests that if you attempt to get a tweet by id, then you get that tweet back
    """
    tweet_id = 1464764077666881542
    expected_tweet_text = "Just checked, and AAPL’s at $156.81. (It dropped $5.13.)"
    db_tweet_ids = twitter_connector.get_tweet_by_id(tweet_id)
    assert db_tweet_ids == [1]
    tweet = Tweet.query.filter_by(id=db_tweet_ids[0]).first()
    assert isinstance(tweet, Tweet)
    assert tweet.tweet_id == tweet_id
    assert tweet.text == expected_tweet_text


def test_get_tweets_mentioning_asset_positive(client, db):
    """
    Tests that if you attempt to get tweets with a search string, then you get some results back
    """
    search_term = "apple"
    db_tweet_ids = twitter_connector.get_tweets_mentioning_asset(search_term)
    assert isinstance(db_tweet_ids, list)
    assert len(db_tweet_ids) >= 1
    # Tweets are returned when attributes other than text contain the search term such as tweet.entities.urls so we
    # can't always assert the search term will be in the tweet text


# Negative tests


def test_get_tweet_by_id_invalid_id():
    """
    Tests that when you try to retrieve a tweet that doesn't exist, you get a TweepError
    """
    tweet_id = -1
    with pytest.raises(tweepy.errors.TweepyException):
        twitter_connector.get_tweet_by_id(tweet_id)


def test_get_tweet_by_id_unauthenticated():
    """
    Tests that when you try to authenticate to the Twitter API without a key and secret, you get a ConnectorException
    """
    tweet_id = -1
    with pytest.raises(trendr.exceptions.ConnectorException):
        twitter_connector.get_tweet_by_id(
            tweet_id, api=twitter_connector.auth_to_api("", "")
        )
