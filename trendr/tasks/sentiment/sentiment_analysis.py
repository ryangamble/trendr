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


@celery.task
def analyze_by_ids_chunk(ids: List[int], social_type: SearchType, n: int):
    # Synchronously calling subtasks is probably the only thing you are
    #   supposed to never do with celery, and beacuse of this it is not possible
    #   to chunk results unless we switch to a celery fork
    print(ids, social_type)
    if social_type == SearchType.TWITTER:
        task = tweet_analysis_by_ids.chunks(ids, n).apply_async()
    elif social_type == SearchType.REDDIT_SUBMISSION:
        task = reddit_submission_analysis_by_ids.chunks(ids, n).apply_async()
    elif social_type == SearchType.REDDIT_COMMENT:
        task = reddit_comment_analysis_by_ids.chunks(ids, n).apply_async()
    task.get(1000)


@celery.task
def tweet_analysis():
    print("Running tweet analysis")
    tweets_to_analyze = Tweet.query.filter_by(polarity=None).all()
    print(f"Tweets to analyze: {tweets_to_analyze}")
    loop_count = 0
    for tweet in tweets_to_analyze:

        if loop_count == 100:
            loop_count = 0
            db.session.commit()

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
    loop_count = 0
    for tweet in tweets_to_analyze:

        if loop_count == 100:
            loop_count = 0
            db.session.commit()

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
    loop_count = 0
    for submission in submissions_to_analyze:

        if loop_count == 100:
            loop_count = 0
            db.session.commit()

        if submission.text:
            polarity, subjectivity = pattern_analyzer(submission.text)
            submission.polarity = polarity
            submission.subjectivity = subjectivity
        else:
            submission.polarity = None
            submission.subjectivity = None
        assign_score_reddit_submission(submission)
    db.session.commit()


@celery.task
def reddit_submission_analysis_by_ids(*ids: int):
    print("Running reddit submission analysis")
    submissions_to_analyze = RedditSubmission.query.filter(
        RedditSubmission.id.in_(ids)
    ).all()
    print(f"Reddit submissions to analyze: {submissions_to_analyze}")
    loop_count = 0
    for submission in submissions_to_analyze:

        if loop_count == 100:
            loop_count = 0
            db.session.commit()

        if submission.text:
            polarity, subjectivity = pattern_analyzer(submission.text)
            submission.polarity = polarity
            submission.subjectivity = subjectivity
        else:
            submission.polarity = None
            submission.subjectivity = None
        assign_score_reddit_submission(submission)
    db.session.commit()
    return ids


@celery.task
def reddit_comment_analysis():
    print("Running reddit comment analysis")
    comments_to_analyze = RedditComment.query.filter_by(polarity=None).all()
    print(f"Reddit comments to analyze: {comments_to_analyze}")
    loop_count = 0
    for comment in comments_to_analyze:

        if loop_count == 100:
            loop_count = 0
            db.session.commit()

        if comment.text:
            polarity, subjectivity = pattern_analyzer(comment.text)
            comment.polarity = polarity
            comment.subjectivity = subjectivity
        else:
            comment.polarity = None
            comment.subjectivity = None
        assign_score_reddit_comment(comment)

    db.session.commit()


@celery.task
def reddit_comment_analysis_by_ids(*ids: int):
    print("Running reddit comment analysis")
    comments_to_analyze = RedditComment.query.filter(RedditComment.id.in_(ids)).all()
    print(f"Reddit comments to analyze: {comments_to_analyze}")
    loop_count = 0
    for comment in comments_to_analyze:

        if loop_count == 100:
            loop_count = 0
            db.session.commit()

        if comment.text:
            polarity, subjectivity = pattern_analyzer(comment.text)
            comment.polarity = polarity
            comment.subjectivity = subjectivity
        else:
            comment.polarity = None
            comment.subjectivity = None
        assign_score_reddit_comment(comment)
    db.session.commit()
    return ids
