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
        raise ConnectorException("Could not authenticate to Twitter because the necessary secrets were not available.")


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
    return api.search_tweets(q=asset_identifier, lang="en", result_type="mixed", since_id=since_id, count= 300)


def account_age_days(month: int, year: int):
    '''
    Gets the month and date, and returns the difference in days from the current date.

    :param month: Integer identifier of the month to
    :param year: Integer identifier of the year
    returns integer with the difference of days from today.
    '''
    date1 = date(year, month, 1)
    return abs(datetime.datetime.now().date() - date1).days

def twitter_accounts_mentioning_asset_summary(
        asset_identifier: str, since_id: str = None, api: tweepy.API = None):

    """
    Queries Twitter for up to 300 tweets that mention an asset_identifier (AAPL, BTC) within the last 7 days, then
    checks meat data about the posters of those tweets.

    :param asset_identifier: The identifier for the asset (AAPL, BTC), not a database id
    :param api: An optional tweepy.API object, if one is not provided it will be created
    :return: a Python dictionary with relevant stats
    """
    results = get_mixed_tweets_mentioning_asset(asset_identifier = asset_identifier, api = tweep)
    followersCountList = []
    followingCountList = []
    verifiedCount = 0
    accoutnsAge_list = []
    for i in range(len(results)):
        followersCountList.append(results[i]._json['user']['followers_count'])
        followingCountList.append(results[i]._json['user']['friends_count'])
        created_at = results[i]._json['user']['created_at'].split(' ')
        month = strptime(created_at[1],'%b').tm_mon
        year = int(created_at[5])
        accoutnsAge_list.append(account_age_days(month, year))
        if results[i]._json['user']['verified']:
            verifiedCount += 1
    followorsStats = {'median': median(followersCountList), 'min': min(followersCountList), 'max': max(followersCountList)}
    followingStats = {'median': median(followingCountList), 'min': min(followingCountList), 'max': max(followingCountList)}
    AccountsAgeStats = {'median': median(accoutnsAge_list), 'min': min(accoutnsAge_list), 'max': max(accoutnsAge_list)}
    return {'followorsStats': followorsStats,'followingStats': followingStats , 'AccountsAgeStats' : AccountsAgeStats,
            'verifiedCount' :verifiedCount }

tweep=auth_to_api(consumer_key= 'Z9O6ST99noLo6n4e1B5Gi1EL6', consumer_secret ='8XT3XvL6pWlX5pOnBxZGTOEPuxUXHRlg8ezIa0Hx1Kq9TlJc6c')
res = twitter_accounts_mentioning_asset_summary('btc', api = tweep)
print(res)