"""
Functions for interacting with the Twitter API using the tweepy library
"""
import datetime
from datetime import date
from time import strptime
from statistics import median

import tweepy
from tweepy import models

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
        raise ConnectorException(
            "Could not authenticate to Twitter because the necessary secrets were not available."
        )


def get_tweet_by_id(
    tweet_id: int, api: tweepy.API = None
) -> tweepy.models.Status:
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
) -> tweepy.models.SearchResults:
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
    return api.search_tweets(q=asset_identifier, lang="en", result_type="popular", since_id=since_id)


def get_mixed_tweets_mentioning_asset(
        asset_identifier: str, since_id: str = None, api: tweepy.API = None
) -> tweepy.models.SearchResults:
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
    return api.search_tweets(q=asset_identifier, lang="en", result_type="mixed", since_id=since_id, count=300)


def account_age_days(month: int, year: int):
    """
    Gets the month and date, and returns the difference in days from the current date.

    :param month: Integer identifier of the month to
    :param year: Integer identifier of the year
    returns integer with the difference of days from today.
    """
    start_date = date(year, month, 1)
    return abs(datetime.datetime.now().date() - start_date).days


def twitter_accounts_mentioning_asset_summary(asset_identifier: str, api: tweepy.API = None):
    """
    Queries Twitter for up to 300 tweets that mention an asset_identifier (AAPL, BTC) within the last 7 days, then
    checks meat data about the posters of those tweets.

    :param asset_identifier: The identifier for the asset (AAPL, BTC), not a database id
    :param api: An optional tweepy.API object, if one is not provided it will be created
    :return: a Python dictionary with relevant stats
    """
    results = get_mixed_tweets_mentioning_asset(asset_identifier=asset_identifier, api=api)
    followers_count_list = []
    following_count_list = []
    verified_count = 0
    accounts_age_list = []

    for i in range(len(results)):
        followers_count_list.append(results[i]._json['user']['followers_count'])
        following_count_list.append(results[i]._json['user']['friends_count'])
        created_at = results[i]._json['user']['created_at'].split(' ')
        month = strptime(created_at[1],'%b').tm_mon
        year = int(created_at[5])
        accounts_age_list.append(account_age_days(month, year))
        if results[i]._json['user']['verified']:
            verified_count += 1

    follower_stats = {
        'median': median(followers_count_list),
        'min': min(followers_count_list),
        'max': max(followers_count_list)
    }
    following_stats = {
        'median': median(following_count_list),
        'min': min(following_count_list),
        'max': max(following_count_list)
    }
    accounts_age_stats = {
        'median': median(accounts_age_list),
        'min': min(accounts_age_list),
        'max': max(accounts_age_list)
    }

    return {
        'follower_stats': follower_stats,
        'following_stats': following_stats,
        'accounts_age_stats': accounts_age_stats,
        'verified_count': verified_count
    }
