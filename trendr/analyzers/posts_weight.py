import sys
from trendr.models import tweet_model
from trendr.models import reddit_model
from datetime import datetime
import pandas as pd
import numpy as np

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

def tweet_score(tweet: tweet_model.Tweet()) -> float:
    time_score = 5
    time_delta = time_delta_hours(tweet.tweeted_at)
    if time_delta > 120:
        time_score = 2
    elif time_delta > 96:
        time_score = 3
    elif time_delta > 24:
        time_score = 4
    else:
        time_score = hours_time_delta_scores[time_delta]

    retweet_score = 0
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

    likes_score = 0
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

    score = (retweet_score * 2 + likes_score + tweet.subjectivity * 0.3) * tweet.polarity * time_score
    print(score)
    return score



def reddit_post_score(post: reddit_model.RedditSubmission()) -> float:
    pass


def get_tweets_moving_average(days: int, tweetsList) -> float:
    if len(tweetsList) < 1:
        return [0]
    elif len(tweetsList) == 1:
        return [tweet_score(tweetsList[0])]


    maxDays = 0
    for tweet in tweetsList:
        time_delta = time_delta_days(tweet.tweeted_at)
        if time_delta > maxDays:
            maxDays = time_delta

    tweetDaysDict = {}
    for i in range(maxDays + 1):
        tweetDaysDict[i] = []

    for tweet in tweetsList:
        time_delta = time_delta_days(tweet.tweeted_at)
        if time_delta < 0:
            continue
        tweetDaysDict[time_delta].append(tweet_score(tweet))

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

    return movingAvg


def get_reddit_post_moving_average(days: int,post: reddit_model.RedditSubmission()) -> float:
    pass

# post = reddit_model.RedditSubmission()
# print(post.comments)
# print(type(post.comments))

# print(post.author)
# print(type(post.author))


# b = datetime(2021, 11, 2, 10, 55, 59, 342380)
# post.posted_at = b
# post.score = 1
# post.sentiment_score = 0.5




# tweet = tweet_model.Tweet()
# tweet.text = "test"
# b = datetime(2021, 11, 2, 10, 55, 59, 342380)
# tweet.tweeted_at = b
# tweet.polarity = 0.8
# tweet.likes = 500
# tweet.retweets = 300
# tweet.subjectivity = 1.0
# print('tweet score:', tweet_score(tweet))

# tweet2 = tweet_model.Tweet()
# tweet2.text = "test"
# b = datetime(2021, 11, 2, 1, 55, 59, 342380)
# tweet2.tweeted_at = b
# tweet2.polarity = 0.5
# tweet2.likes = 50
# tweet2.retweets = 3000
# tweet2.subjectivity = 1.0

# tweet3 = tweet_model.Tweet()
# tweet3.text = "test"
# b = datetime(2021, 11, 1, 1, 55, 59, 342380)
# tweet3.tweeted_at = b
# tweet3.polarity = 0.3
# tweet3.likes = 500
# tweet3.retweets = 30000
# tweet3.subjectivity = 1.0

# print(get_tweets_moving_average(3, [tweet, tweet2, tweet3]))