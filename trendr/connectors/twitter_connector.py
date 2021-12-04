"""
Functions for interacting with the Twitter API using the tweepy library
"""
import datetime
from statistics import median

import tweepy
from tweepy import models
from sqlalchemy import desc

from trendr.config import (
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
    TWITTER_BEARER_TOKEN,
)
from trendr.exceptions import ConnectorException
from trendr.models.tweet_model import Tweet
from trendr.controllers.social_controller.utils import store_in_db


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
        raise ConnectorException(
            "Could not authenticate to Twitter because the necessary secrets were not available."
        )


def get_latest_tweet_id(asset_identifier: str) -> int or None:
    """
    Returns the id of the latest tweet stored in the database for a given identifier

    :param asset_identifier: The identifier for the asset (AAPL, BTC), not a database id
    :return: A tweet id
    """
    tweet = (
        Tweet.query.filter(Tweet.text.ilike(f"%{asset_identifier}%"))
        .order_by(desc(Tweet.tweeted_at))
        .limit(1)
        .all()
    )
    if tweet:
        return tweet[0].tweet_id
    return None


@store_in_db()
def get_tweet_by_id(tweet_id: int, api: tweepy.API = None) -> tweepy.models.Status:
    """
    Gets all the information available for given tweet.

    :param tweet_id: The Twitter id for the tweet
    :param api: An optional tweepy.API object, if one is not provided it will be created
    :return: A tweepy.Status object
    """
    if not api:
        api = auth_to_api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    return api.get_status(tweet_id)


@store_in_db()
def get_tweets_mentioning_asset(
    asset_identifier: str, api: tweepy.API = None
) -> tweepy.models.SearchResults:
    """
    Queries Twitter for tweets that mention an asset_identifier (AAPL, BTC) within the last 7 days, starting at the
    latest tweet we have already stored
    :param asset_identifier: The identifier for the asset (AAPL, BTC), not a database id
    :param api: An optional tweepy.API object, if one is not provided it will be created
    :return: A tweepy.SearchResults object
    """
    latest_tweet_id = get_latest_tweet_id(asset_identifier)
    if not api:
        api = auth_to_api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)

    # 100 is the allowed max
    return api.search_tweets(
        q=asset_identifier,
        lang="en",
        result_type="mixed",
        since_id=latest_tweet_id,
        count=100,
    )


def get_stored_tweet_by_id(tweet_id: int) -> Tweet or None:
    """
    Gets all stored information available for given tweet.

    :param tweet_id: The Twitter id for the tweet
    :return: A Tweet model object
    """
    get_tweet_by_id(tweet_id)
    return Tweet.query.filter_by(tweet_id=tweet_id).one()


def get_stored_tweets_mentioning_asset(asset_identifier: str) -> [Tweet]:
    """
    Gets all tweets from the database that contain the asset_identifier

    :param asset_identifier: The identifier for the asset (AAPL, BTC), not a database id
    :return: A list of Tweet model objects
    """
    # TODO: If this starts returning too many results we may want to provide a limit
    get_tweets_mentioning_asset(asset_identifier)
    return Tweet.query.filter(Tweet.text.ilike(f"%{asset_identifier}%")).all()


def twitter_accounts_mentioning_asset_summary(asset_identifier: str) -> dict:
    """
    Queries Twitter for up to 300 tweets that mention an asset_identifier (AAPL, BTC) within the last 7 days, then
    checks meta data about the posters of those tweets.

    :param asset_identifier: The identifier for the asset (AAPL, BTC), not a database id
    :return: a Python dictionary with relevant stats
    """
    tweets = get_stored_tweets_mentioning_asset(asset_identifier)

    followers_count_list = []
    following_count_list = []
    verified_count = 0
    accounts_age_list = []

    for tweet in tweets:
        followers_count_list.append(tweet.tweeter_num_followers)
        following_count_list.append(tweet.tweeter_num_following)
        accounts_age_list.append(
            abs(datetime.datetime.now() - tweet.tweeter_created_at).days
        )
        if tweet.tweeter_verified:
            verified_count += 1

    if followers_count_list:
        follower_stats = {
            "median": median(followers_count_list),
            "min": min(followers_count_list),
            "max": max(followers_count_list),
        }
    else:
        follower_stats = {"median": 0, "min": 0, "max": 0}
    if following_count_list:
        following_stats = {
            "median": median(following_count_list),
            "min": min(following_count_list),
            "max": max(following_count_list),
        }
    else:
        following_stats = {"median": 0, "min": 0, "max": 0}
    if accounts_age_list:
        accounts_age_stats = {
            "median": median(accounts_age_list),
            "min": min(accounts_age_list),
            "max": max(accounts_age_list),
        }
    else:
        accounts_age_stats = {"median": 0, "min": 0, "max": 0}

    return {
        "follower_stats": follower_stats,
        "following_stats": following_stats,
        "accounts_age_stats": accounts_age_stats,
        "verified_count": verified_count,
    }


def tweet_count_mentioning_asset(asset_identifier: str, client: tweepy.Client = None):
    """
    Queries Twitter for the count of tweets mentioning the asset.

    :param asset_identifier: The name of the asset (AAPL, BTC, Bitcoin, etc.)
    :param client: An optional tweepy.Client object, if one is not provided it will be created
    :return: a Python list with the count data(start, end, tweet_count) for each hour for the previous 7 days.
    """
    if not client:
        client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

    results = client.get_recent_tweets_count(
        query=asset_identifier,
    )[0]
    return results
