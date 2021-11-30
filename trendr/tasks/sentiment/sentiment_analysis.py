from typing import Type, Union, List
from trendr.analyzers.text_blob import pattern_analyzer
from trendr.analyzers.posts_weight import (
    assign_score_tweet,
    assign_score_reddit_submission,
    assign_score_reddit_comment,
)
from trendr.extensions import celery, db
from trendr.models.reddit_model import RedditSubmission, RedditComment
from trendr.models.tweet_model import Tweet
from trendr.models.search_model import SearchType


@celery.task
def analyze_by_ids(ids: List[int], social_type: SearchType):
    print(ids, social_type)
    if social_type == SearchType.TWITTER:
        tweet_analysis_by_ids.apply(ids)
    elif social_type == SearchType.REDDIT_SUBMISSION:
        reddit_submission_analysis_by_ids.apply(ids)
    elif social_type == SearchType.REDDIT_COMMENT:
        reddit_comment_analysis_by_ids.apply(ids)
    return ids


@celery.task
def tweet_analysis():
    print("Running tweet analysis")
    tweets_to_analyze = Tweet.query.filter_by(polarity=None).all()
    print(f"Tweets to analyze: {tweets_to_analyze}")
    for tweet in tweets_to_analyze:
        polarity, subjectivity = pattern_analyzer(tweet.text)
        tweet.polarity = polarity
        tweet.subjectivity = subjectivity
        assign_score_tweet(tweet)
    db.session.commit()


@celery.task
def tweet_analysis_by_ids(*ids: int):
    print("Running tweet analysis")
    tweets_to_analyze = Tweet.query.filter(Tweet.id.in_(ids)).all()
    print(f"Tweets to analyze: {tweets_to_analyze}")
    for tweet in tweets_to_analyze:
        polarity, subjectivity = pattern_analyzer(tweet.text)
        tweet.polarity = polarity
        tweet.subjectivity = subjectivity
        assign_score_tweet(tweet)
    db.session.commit()
    return ids


@celery.task
def reddit_submission_analysis():
    print("Running reddit submission analysis")
    submissions_to_analyze = RedditSubmission.query.filter_by(polarity=None).all()
    print(f"Reddit submissions to analyze: {submissions_to_analyze}")
    for submission in submissions_to_analyze:
        polarity, subjectivity = pattern_analyzer(submission.text)
        submission.polarity = polarity
        submission.subjectivity = subjectivity
        assign_score_reddit_submission(submission)
    db.session.commit()


@celery.task
def reddit_submission_analysis_by_ids(*ids: int):
    print("Running reddit submission analysis")
    submissions_to_analyze = RedditSubmission.query.filter(
        RedditSubmission.id.in_(ids)
    ).all()
    print(f"Reddit submissions to analyze: {submissions_to_analyze}")
    for submission in submissions_to_analyze:
        polarity, subjectivity = pattern_analyzer(submission.text)
        submission.polarity = polarity
        submission.subjectivity = subjectivity
        assign_score_reddit_submission(submission)
    db.session.commit()
    return ids


@celery.task
def reddit_comment_analysis():
    print("Running reddit comment analysis")
    comments_to_analyze = RedditComment.query.filter_by(polarity=None).all()
    print(f"Reddit comments to analyze: {comments_to_analyze}")
    for comment in comments_to_analyze:
        polarity, subjectivity = pattern_analyzer(comment.text)
        comment.polarity = polarity
        comment.subjectivity = subjectivity
        assign_score_reddit_comment(comment)
    db.session.commit()


@celery.task
def reddit_comment_analysis_by_ids(*ids: int):
    print("Running reddit comment analysis")
    comments_to_analyze = RedditComment.query.filter(RedditComment.id.in_(ids)).all()
    print(f"Reddit comments to analyze: {comments_to_analyze}")
    for comment in comments_to_analyze:
        polarity, subjectivity = pattern_analyzer(comment.text)
        comment.polarity = polarity
        comment.subjectivity = subjectivity
        assign_score_reddit_comment(comment)
    db.session.commit()
    return ids
