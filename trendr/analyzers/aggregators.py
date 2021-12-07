from typing import List, Tuple
import datetime
from trendr.models.search_model import Search
from trendr.models.sentiment_model import SentimentDataPoint
from trendr.models.reddit_model import RedditComment, RedditSubmission
from trendr.models.tweet_model import Tweet
from trendr.analyzers.posts_weight import get_time_score
from trendr.extensions import db


def create_datapoints(
    search_id: int,
    start_ts: int,
    end_ts: int,
    increment: datetime.timedelta = datetime.timedelta(hours=1),
    top: int = 3,
) -> List[int]:
    """
    Create datapoints for a certain time range and get their ids

    :param search_id: id of search to assign this datapoint to
    :param start: first time to generate datapoint for
    :param end:last time to generate datapoint for, defaults to datetime.now(), defaults to datetime.now()
    :param increment: time increment or how often data points should be generated, defaults to datetime.timedelta(hours=1)
    :return: list of SentimentDataPoint ids
    """
    start = datetime.datetime.fromtimestamp(start_ts)
    start = start.replace(second=0, microsecond=0, minute=0)
    end = datetime.datetime.fromtimestamp(end_ts)

    if end < start:
        return []

    created = []
    existing = []
    curr = start
    while curr < end:
        is_new, dat_pt = create_data_point(time=curr, search_id=search_id, top=top)
        if is_new:
            created.append(dat_pt)
        else:
            existing.append(dat_pt)
        curr += increment

    db.session.add_all(created)
    db.session.commit()

    return [c.id for c in created] + [e.id for e in existing]


def create_data_point(
    time: datetime.datetime, search_id: int, top: int
) -> Tuple[bool, SentimentDataPoint]:
    """
    Create SentimentDataPoint populated with all relevant fields

    :param time: time to create datapoint for
    :param search_id: id of the calling search
    :param top: number of top social posts to record
    :return: new data point
    """
    search = Search.query.filter_by(id=search_id).one()
    existing = SentimentDataPoint.query.filter_by(
        asset_id=search.asset_id, datetime=time
    ).first()
    if existing:
        return False, existing
    tweets, reddit_submissions, reddit_comments = get_affecting_socials(
        time, asset_id=search.asset_id
    )

    tweet_scores = [t.sentiment_score for t in tweets]
    if tweet_scores:
        twitter_avg = sum(tweet_scores) / len(tweet_scores)
    else:
        twitter_avg = None

    # sort list of tweet indicies by their corresponding scores
    tweets_ind_by_importance = sorted(range(len(tweets)), key=lambda x: tweet_scores[x])
    important_tweets = [tweets[i] for i in tweets_ind_by_importance[-top:]]

    reddit_submission_scores = [rs.sentiment_score for rs in reddit_submissions]
    reddit_avg = sum(reddit_submission_scores)
    # sort list of reddit_submission indicies by their corresponding scores
    reddit_submissions_ind_by_importance = sorted(
        range(len(reddit_submissions)), key=lambda x: reddit_submission_scores[x]
    )
    important_submissions = [
        reddit_submissions[i] for i in reddit_submissions_ind_by_importance[-top:]
    ]

    reddit_comment_scores = [rc.sentiment_score for rc in reddit_comments]
    reddit_avg += sum(reddit_comment_scores)
    # sort list of reddit_submission indicies by their corresponding scores
    reddit_comments_ind_by_importance = sorted(
        range(len(reddit_comments)), key=lambda x: reddit_comment_scores[x]
    )
    important_comments = [
        reddit_comments[i] for i in reddit_comments_ind_by_importance[-top:]
    ]
    if reddit_submission_scores or reddit_comment_scores:
        reddit_avg /= len(reddit_submission_scores) + len(reddit_comment_scores)
    else:
        reddit_avg = None

    dp = SentimentDataPoint(
        datetime=time,
        twitter_sentiment=twitter_avg,
        reddit_sentiment=reddit_avg,
        search=search,
        asset=search.asset,
    )
    dp.tweets.extend(important_tweets)
    dp.reddit_submissions.extend(important_submissions)
    dp.reddit_comments.extend(important_comments)

    return True, dp


def get_affecting_socials(
    time: datetime.datetime, asset_id: int
) -> Tuple[List[Tweet], List[RedditSubmission], List[RedditComment]]:
    """
    Get important posts for the given time (time - time-5d)

    :param time: datetime we are trying to analyze sentiment for
    :param asset_id: asset we are analyzing sentiment for
    :return: all the social posts that can affect the sentiment score for that time
    """
    max_time = time
    min_time = time - datetime.timedelta(days=14)

    tweets = Tweet.query.filter(
        Tweet.assets.any(id=asset_id),
        Tweet.tweeted_at <= max_time,
        Tweet.tweeted_at >= min_time,
    ).all()
    reddit_submissions = RedditSubmission.query.filter(
        RedditSubmission.assets.any(id=asset_id),
        RedditSubmission.polarity != None,
        RedditSubmission.posted_at <= max_time,
        RedditSubmission.posted_at >= min_time,
    ).all()
    reddit_comments = RedditComment.query.filter(
        RedditComment.assets.any(id=asset_id),
        RedditComment.polarity != None,
        RedditComment.posted_at <= max_time,
        RedditComment.posted_at >= min_time,
    ).all()
    return (tweets, reddit_submissions, reddit_comments)
