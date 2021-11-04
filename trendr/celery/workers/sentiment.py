from trendr.app import init_celery
from trendr.tasks.sentiment.sentiment_analysis import (
    tweet_analysis,
    reddit_comment_analysis,
    reddit_submission_analysis,
)

celery = init_celery()
