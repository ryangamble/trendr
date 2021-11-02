from trendr.analyzers.TextBlobAnalyzers import pattern_analyzer
from trendr.extensions import celery, db
from trendr.models.reddit_model import RedditSubmission, RedditComment
from trendr.models.tweet_model import Tweet


@celery.task
def tweet_analysis():
    print("Running tweet analysis")
    tweets_to_analyze = Tweet.query.filter_by(polarity=None).all()
    print(f"Tweets to analyze: {tweets_to_analyze}")
    for tweet in tweets_to_analyze:
        polarity, subjectivity = pattern_analyzer(tweet.text)
        tweet.polarity = polarity
        tweet.subjectivity = subjectivity
    db.session.commit()


@celery.task
def reddit_submission_analysis():
    print("Running reddit submission analysis")
    submissions_to_analyze = RedditSubmission.query.filter_by(polarity=None).all()
    print(f"Reddit submissions to analyze: {submissions_to_analyze}")
    for submission in submissions_to_analyze:
        polarity, subjectivity = pattern_analyzer(submission.text)
        submission.polarity = polarity
        submission.subjectivity = subjectivity
    db.session.commit()


@celery.task
def reddit_comment_analysis():
    print("Running reddit comment analysis")
    comments_to_analyze = RedditComment.query.filter_by(polarity=None).all()
    print(f"Reddit comments to analyze: {comments_to_analyze}")
    for comment in comments_to_analyze:
        polarity, subjectivity = pattern_analyzer(comment.text)
        comment.polarity = polarity
        comment.subjectivity = subjectivity
    db.session.commit()
