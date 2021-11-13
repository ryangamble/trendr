from typing import Union
import sys
from datetime import datetime
import pandas as pd
import numpy as np
from statistics import mean
from trendr.models.reddit_model import RedditComment, RedditSubmission, Subreddit
from trendr.models.tweet_model import Tweet


def aggregate_sentiment_simple_mean(
    socials, search_type:int
):
    """
    Gets a selection of socials posts, and returns a list with the moving average
    for each day since the first post and until the latest post.

    :param socials: social post list of types Tweet, RedditSubmission, or RedditComment.
    :param search_type: integer identifier for the type of list passed to the
                        1 is Tweet, 2 is RedditSubmission, 3 is RedditComment.
    :return: a float list of moving average for each day since the first post.
    """
    averages = []
    days_MA = 3
    if search_type == 1:
        return get_tweets_moving_average(days_MA, socials)
        # res =  get_tweets_moving_average(days_MA, socials)
        # return 3 * res[len(socials) - 1]
    elif search_type == 2:
        return get_reddit_post_moving_average(days_MA, socials)
        # res = get_reddit_post_moving_average(days_MA, socials)
        # return 4 * res[len(socials) - 1]
    else:
        return get_reddit_comment_moving_average(days_MA, socials)
        # res = get_reddit_comment_moving_average(days_MA, socials)
        # return 1.5 * res[len(socials) - 1]

    # return mean([s.polarity for s in socials])
    # return mean([x for s in averages])


'''
A hard-coded dictionary that gives a score for the time_delta weight, based
on how many hours passed since the post was created.
'''
hours_time_delta_scores = {
    0:10, 1:9, 2:8, 3:8, 4:7, 5:7, 6:7, 7:7, 8:7, 9:7, 10:6, 11:6, 12:6, 13:6, 14:6
}
for i in range(14, 25):
    hours_time_delta_scores[i] = 6



def time_delta_hours(date: datetime) -> int:
    """
    Gets a datetime, and returns time delta from now in hours.

    :param date: datetime
    :return: difference of days from today.
    """
    now  = datetime.now()                         # Now
    duration = now - date                         # built-in functions
    duration_in_s = duration.total_seconds()      # Total number of seconds between dates
    hours = divmod(duration_in_s, 3600)[0]
    return hours

def time_delta_days(date: datetime) -> int:
    """
    Gets a datetime, and returns time delta from now in days.

    :param date: datetime
    :return: difference of days from today.
    """
    now  = datetime.now()                         # Now
    duration = now - date                         # built-in functions
    duration_in_s = duration.total_seconds()      # Total number of seconds between dates
    days  = duration.days
    return days


def tweet_score(tweet: Tweet, old_score: bool=False) -> float:
    """
    Gets a Tweet, and returns a score for how impactful it is on the sentiment

    :param tweet: Tweet
    :return: a float value representing the effectiveness (includes the directions- Postitve/negative)
    """

    time_score = 5 # weight of time in the total score. the newer a post, the higher the weight
    time_delta = time_delta_hours(tweet.tweeted_at)
    if old_score:  # If the tweet is part of a list(for calculating an old moving average)
        time_score = 6
    elif time_delta > 120:
        time_score = 2
    elif time_delta > 96:
        time_score = 3
    elif time_delta > 24:
        time_score = 4
    else:
        time_score = hours_time_delta_scores[time_delta]

    retweet_score = 0 # more retweets equal higher weighr. However, it's not a linear correlation
    if tweet.retweets > 100000:
        retweet_score = 100
    elif tweet.retweets > 50000:
        retweet_score = 75
    elif tweet.retweets > 10000:
        retweet_score = 40
    elif tweet.retweets > 5000:
        retweet_score = 30
    elif tweet.retweets > 3000:
        retweet_score = 25
    elif tweet.retweets > 1000:
        retweet_score = 20
    elif tweet.retweets > 500:
        retweet_score = 15
    elif tweet.retweets > 300:
        retweet_score = 12
    elif tweet.retweets > 100:
        retweet_score = 9
    elif tweet.retweets > 80:
        retweet_score = 7
    elif tweet.retweets > 50:
        retweet_score = 6
    elif tweet.retweets > 30:
        retweet_score = 4
    elif tweet.retweets > 10:
        retweet_score = 3
    elif tweet.retweets > 5:
        retweet_score = 2
    elif tweet.retweets > 1:
        retweet_score = 1
    else:
        retweet_score = 0

    likes_score = 0 # more likes equal higher weighr. However, it's not a linear correlation
    if tweet.likes > 100000:
        likes_score = 100
    elif tweet.likes > 50000:
        likes_score = 75
    elif tweet.likes > 10000:
        likes_score = 40
    elif tweet.likes > 5000:
        likes_score = 30
    elif tweet.likes > 3000:
        likes_score = 25
    elif tweet.likes > 1000:
        likes_score = 20
    elif tweet.likes > 500:
        likes_score = 15
    elif tweet.likes > 300:
        likes_score = 12
    elif tweet.likes > 100:
        likes_score = 9
    elif tweet.likes > 80:
        likes_score = 7
    elif tweet.likes > 50:
        likes_score = 6
    elif tweet.likes > 30:
        likes_score = 4
    elif tweet.likes > 10:
        likes_score = 3
    elif tweet.likes > 5:
        likes_score = 2
    elif tweet.likes > 1:
        likes_score = 1
    else:
        likes_score = 0

    # formula for getting the score. Some factors are more important. Based on observation.
    score = (retweet_score * 2 + likes_score + tweet.subjectivity * 1.3) * tweet.polarity * time_score
    # print(score)
    return score


def get_tweets_moving_average(days: int, tweetsList:[Tweet]) -> [float]:
    """
    Gets a list of Tweets, and returns a a list for the sentiment moving average, where each
    each index represents a day. The first index is the date of the first post.

    :param tweet: List of tweets Tweet
    :return: a list of floats represning the moving average in each day.
    """

    if len(tweetsList) < 1:
        return [0]
    elif len(tweetsList) == 1:
        return [tweet_score(tweetsList[0])] # return the score of individual tweet

    maxDays = 0 # number of days that we will calculate the moving average.
                # it starts at the oldest post we receive.
    for tweet in tweetsList:
        time_delta = time_delta_days(tweet.tweeted_at)
        if time_delta > maxDays:
            maxDays = time_delta

    tweetDaysDict = {} # dictionary for each day since the first post
                        # we will place each post's score in its day
    for i in range(maxDays + 1):
        tweetDaysDict[i] = []

    for tweet in tweetsList:
        time_delta = time_delta_days(tweet.tweeted_at)
        if time_delta < 0:
            continue
        tweetDaysDict[time_delta].append(tweet_score(tweet, old_score=True))

    daysAvg = []
    for day in tweetDaysDict:
        avg = np.average(tweetDaysDict[day])
        daysAvg.append(avg)

    #calculate moving average
    movingAvg = pd.Series(daysAvg).rolling(window=days).mean().iloc[days-1:].values
    for i in range(len(movingAvg)):
        if i == 0 and np.isnan(movingAvg[i]):
            movingAvg[0] = movingAvg[1]
        elif i == len(movingAvg) - 1 and np.isnan(movingAvg[i]):
            movingAvg[i] = movingAvg[i - 1]
        elif np.isnan(movingAvg[i]):
            avg = (movingAvg[i - 1] + movingAvg[i + 1]) / 2
            movingAvg[i] = avg
        if np.isnan(movingAvg[i]):
            movingAvg[i] = mean

    return movingAvg


def reddit_post_score(post: RedditSubmission, old_score: bool=False) -> float:
     """
    Gets a RedditSubmission, and returns a score for how impactful it is on the sentiment

    :param post: RedditSubmission
    :return: a float value representing the effectiveness (includes the directions- Postitve/negative)
    """

    time_score = 5
    time_delta = time_delta_hours(post.posted_at)
    if old_score:
        time_score = 6
    elif time_delta > 120:
        time_score = 2
    elif time_delta > 96:
        time_score = 3
    elif time_delta > 24:
        time_score = 4
    else:
        time_score = hours_time_delta_scores[time_delta]

    subscribers_score = 1
    if post.subreddit.subscribers > 1000000:
        subscribers_score = 10
    elif post.subreddit.subscribers > 500000:
        subscribers_score = 8
    elif post.subreddit.subscribers > 100000:
        subscribers_score = 7
    elif post.subreddit.subscribers > 30000:
        subscribers_score = 6
    elif post.subreddit.subscribers > 10000:
        subscribers_score = 5
    elif post.subreddit.subscribers > 5000:
        subscribers_score = 3
    elif post.subreddit.subscribers > 1000:
        subscribers_score = 2
    else:
        subscribers_score = 1

    comments_count = len(post.comments)
    score = (comments_count * 3 + subscribers_score) * post.sentiment_score * post.score * time_score
    return score

def get_reddit_post_moving_average(days: int, posts:[RedditSubmission]) -> [float]:
     """
    Gets a list of RedditSubmission, and returns a a list for the sentiment moving average, where each
    each index represents a day. The first index is the date of the first post.

    :param posts: List of RedditSubmission
    :return: a list of floats represning the moving average in each day.
    """

    if len(posts) < 1:
        return [0]
    elif len(posts) == 1:
        return [reddit_post_score(posts[0])]

    maxDays = 0 # number of days that we will calculate the moving average.
                # it starts at the oldest post we receive.
    for post in posts:
        time_delta = time_delta_days(post.posted_at)
        if time_delta > maxDays:
            maxDays = time_delta

    postDaysDict = {}
    for i in range(maxDays + 1):
        postDaysDict[i] = []

    for post in posts:
        time_delta = time_delta_days(post.posted_at)
        if time_delta < 0:
            continue
        postDaysDict[time_delta].append(reddit_post_score(post, old_score=True))

    daysAvg = []
    for day in postDaysDict:
        avg = np.average(postDaysDict[day])
        daysAvg.append(avg)

    #calculate moving average
    movingAvg = pd.Series(daysAvg).rolling(window=days).mean().iloc[days-1:].values

    for i in range(len(movingAvg)):
        if i == 0 and np.isnan(movingAvg[i]):
            movingAvg[0] = movingAvg[1]
        elif i == len(movingAvg) - 1 and np.isnan(movingAvg[i]):
            movingAvg[i] = movingAvg[i - 1]
        elif np.isnan(movingAvg[i]):
            avg = (movingAvg[i - 1] + movingAvg[i + 1]) / 2
            movingAvg[i] = avg
        if np.isnan(movingAvg[i]):
            mean = np.nanmean(movingAvg, axis=0)
            movingAvg[i] = mean

    return movingAvg


def reddit_comment_score(post: RedditComment, old_score: bool=False) -> float:
     """
    Gets a RedditComment, and returns a score for how impactful it is on the sentiment

    :param post: RedditComment
    :return: a float value representing the effectiveness (includes the directions- Postitve/negative)
    """

    time_score = 5
    time_delta = time_delta_hours(post.posted_at)
    if old_score:
        time_score = 6
    elif time_delta > 120:
        time_score = 2
    elif time_delta > 96:
        time_score = 3
    elif time_delta > 24:
        time_score = 4
    else:
        time_score = hours_time_delta_scores[time_delta]


    subscribers_score = 1 # the weight used for each level of subscribers
    if post.subreddit.subscribers > 1000000:
        subscribers_score = 10
    elif post.subreddit.subscribers > 500000:
        subscribers_score = 8
    elif post.subreddit.subscribers > 100000:
        subscribers_score = 7
    elif post.subreddit.subscribers > 30000:
        subscribers_score = 6
    elif post.subreddit.subscribers > 10000:
        subscribers_score = 5
    elif post.subreddit.subscribers > 5000:
        subscribers_score = 3
    elif post.subreddit.subscribers > 1000:
        subscribers_score = 2
    else:
        subscribers_score = 1

    score = subscribers_score * post.sentiment_score * post.score * time_score
    return score

def get_reddit_comment_moving_average(days: int, posts:[RedditComment]) -> [float]:
     """
    Gets a list of RedditSubmission, and returns a a list for the sentiment moving average, where each
    each index represents a day. The first index is the date of the first post.

    :param posts: List of RedditSubmission
    :return: a list of floats represning the moving average in each day.
    """

    if len(posts) < 1:
        return [0]
    elif len(posts) == 1:
        return [reddit_comment_score(posts[0])]

    maxDays = 0 # number of days that we will calculate the moving average.
                # it starts at the oldest post we receive.
    for post in posts:
        time_delta = time_delta_days(post.posted_at)
        if time_delta > maxDays:
            maxDays = time_delta

    postDaysDict = {}
    for i in range(maxDays + 1):
        postDaysDict[i] = []

    for post in posts:
        time_delta = time_delta_days(post.posted_at)
        if time_delta < 0:
            continue
        postDaysDict[time_delta].append(reddit_comment_score(post, old_score=True))

    daysAvg = []
    for day in postDaysDict:
        avg = np.average(postDaysDict[day])
        daysAvg.append(avg)

    #calculate moving average
    movingAvg = pd.Series(daysAvg).rolling(window=days).mean().iloc[days-1:].values

    for i in range(len(movingAvg)):
        if i == 0 and np.isnan(movingAvg[i]):
            movingAvg[0] = movingAvg[1]
        elif i == len(movingAvg) - 1 and np.isnan(movingAvg[i]):
            movingAvg[i] = movingAvg[i - 1]
        elif np.isnan(movingAvg[i]):
            avg = (movingAvg[i - 1] + movingAvg[i + 1]) / 2
            movingAvg[i] = avg
        if np.isnan(movingAvg[i]):
            mean = np.nanmean(movingAvg, axis=0)
            movingAvg[i] = mean

    return movingAvg