"""
Functions for interacting with the Twitter API using the tweepy library
"""
import datetime
from statistics import median

import tweepy
from tweepy import models
from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound

from trendr.config import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
from trendr.exceptions import ConnectorException
from trendr.extensions import db
from trendr.models.tweet_model import Tweet


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
    tweet = Tweet.query\
        .filter(Tweet.text.ilike(f'%{asset_identifier}%'))\
        .order_by(desc(Tweet.tweeted_at))\
        .limit(1).all()
    if tweet:
        return tweet[0].tweet_id
    return None


def db_datetime(time_string: str) -> datetime.datetime:
    """
    Takes a datetime from twitter and converts it to a form that can be stored in the database

    :param time_string: The string representing the time to convert
    :return: The db datetime representation
    """
    datetime_object = datetime.datetime.strptime(time_string, '%a %b %d %H:%M:%S %z %Y')
    return datetime_object


def fetch_and_store_tweets(asset_identifier: str):
    """
    Fetches all tweets containing an asset identifier that are newer than the latest tweet and stores them in the
    database

    :param asset_identifier: The identifier for the asset (AAPL, BTC), not a database id
    """
    latest_tweet_id = get_latest_tweet_id(asset_identifier)

    api = auth_to_api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    new_tweets = api.search_tweets(
        q=asset_identifier,
        lang="en",
        result_type="mixed",
        since_id=latest_tweet_id,
        count=100,
    )

    for new_tweet in new_tweets:
        tweet_data = new_tweet._json
        tweeter_data = tweet_data["user"]

        try:
            Tweet.query.filter_by(tweet_id=tweet_data["id"]).one()
            continue  # The tweet already exists so skip adding this one
        except NoResultFound:
            pass

        tweet = Tweet(
            tweet_id=tweet_data["id"],
            text=tweet_data["text"],
            tweeted_at=db_datetime(tweet_data["created_at"]),
            likes=tweet_data["favorite_count"],
            retweets=tweet_data["retweet_count"],
            tweeter_num_followers=tweeter_data["followers_count"],
            tweeter_num_following=tweeter_data["friends_count"],
            tweeter_created_at=db_datetime(tweeter_data["created_at"]),
            tweeter_verified=tweeter_data["verified"]
        )
        db.session.add(tweet)

    db.session.commit()


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


def get_tweets_mentioning_asset(asset_identifier: str) -> [Tweet]:
    """
    Queries the database for tweets containing an asset_identifier in the text field

    :param asset_identifier: The identifier for the asset (AAPL, BTC), not a database id
    :return: A list of Tweet database rows
    """
    # Update the database with recent tweets then return results from the database
    fetch_and_store_tweets(asset_identifier)
    return Tweet.query.filter(Tweet.text.ilike(f'%{asset_identifier}%')).all()


def twitter_accounts_mentioning_asset_summary(asset_identifier: str):
    """
    Queries Twitter for up to 300 tweets that mention an asset_identifier (AAPL, BTC) within the last 7 days, then
    checks meta data about the posters of those tweets.

    :param asset_identifier: The identifier for the asset (AAPL, BTC), not a database id
    :param api: An optional tweepy.API object, if one is not provided it will be created
    :return: a Python dictionary with relevant stats
    """
    # Update the database with recent tweets then return results from the database
    fetch_and_store_tweets(asset_identifier)
    tweets = Tweet.query.filter(Tweet.text.ilike(f'%{asset_identifier}%')).all()

    followers_count_list = []
    following_count_list = []
    verified_count = 0
    accounts_age_list = []

    for tweet in tweets:
        followers_count_list.append(tweet.tweeter_num_followers)
        following_count_list.append(tweet.tweeter_num_following)
        accounts_age_list.append(abs(datetime.datetime.now() - tweet.tweeter_created_at).days)
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
