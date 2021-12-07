import datetime
import bisect
from trendr.models.reddit_model import RedditComment, RedditSubmission
from trendr.models.tweet_model import Tweet

hours_time_delta_scores = {
    datetime.timedelta(hours=0): 10,
    datetime.timedelta(hours=1): 9,
    datetime.timedelta(hours=2): 8,
    datetime.timedelta(hours=4): 7,
    datetime.timedelta(hours=10): 6,
    datetime.timedelta(hours=25): 4,
    datetime.timedelta(hours=120): 2,
    datetime.timedelta(hours=96): 3,
}


def get_time_score(
    time: datetime.datetime = None, delta: datetime.timedelta = None
) -> int:
    if time:
        now = datetime.datetime.now()
        delta = now - time

    # find where it fits into hours_time_delta_scores
    keys = list(hours_time_delta_scores.keys())
    bi_res = bisect.bisect(keys, delta)
    # avoid out of bounds
    if bi_res == len(keys):
        bi_res -= 1
    return hours_time_delta_scores[keys[bi_res]]


def assign_score_tweet(tweet: Tweet):
    """
    Calculate and assign tweet score. DOES NOT COMMIT TRANSACTION

    :param tweet: tweet object to calculate score for
    """

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

    score = (
        retweet_score * 2 + likes_score + tweet.subjectivity * 1.3
    ) * tweet.polarity
    tweet.sentiment_score = score


def assign_score_reddit_submission(submission: RedditSubmission):
    """
    Calculate and assign tweet score. DOES NOT COMMIT TRANSACTION

    :param tweet: tweet object to calculate score for
    """
    subscribers_score = 1
    if submission.subreddit.subscribers:
        if submission.subreddit.subscribers > 1000000:
            subscribers_score = 10
        elif submission.subreddit.subscribers > 500000:
            subscribers_score = 8
        elif submission.subreddit.subscribers > 100000:
            subscribers_score = 7
        elif submission.subreddit.subscribers > 30000:
            subscribers_score = 6
        elif submission.subreddit.subscribers > 10000:
            subscribers_score = 5
        elif submission.subreddit.subscribers > 5000:
            subscribers_score = 3
        elif submission.subreddit.subscribers > 1000:
            subscribers_score = 2
        else:
            subscribers_score = 1


    comments_count = len(submission.comments)

    if submission.polarity is None:
        score = None
    else:
        score = (
            (comments_count * 3 + subscribers_score)
            * submission.polarity
            * submission.score
        )

    submission.sentiment_score = score


def assign_score_reddit_comment(comment: RedditComment):
    # TODO: incorporate comment calculation into post calculation.
    #   for example, if a popular post has a popular comment, give it
    #   a high weight as well, but do not consider comments seperately

    subscribers_score = 1

    if comment.subreddit.subscribers:
        if comment.subreddit.subscribers > 1000000:
            subscribers_score = 10
        elif comment.subreddit.subscribers > 500000:
            subscribers_score = 8
        elif comment.subreddit.subscribers > 100000:
            subscribers_score = 7
        elif comment.subreddit.subscribers > 30000:
            subscribers_score = 6
        elif comment.subreddit.subscribers > 10000:
            subscribers_score = 5
        elif comment.subreddit.subscribers > 5000:
            subscribers_score = 3
        elif comment.subreddit.subscribers > 1000:
            subscribers_score = 2
        else:
            subscribers_score = 1

    score = subscribers_score * comment.polarity * comment.score
    comment.sentiment_score = score
