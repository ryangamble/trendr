from trendr.app import init_celery
from trendr.tasks.sentiment.sentiment_analysis import (
    analyze_by_ids,
    tweet_analysis_by_ids,
    reddit_comment_analysis_by_ids,
    reddit_submission_analysis_by_ids,
)

celery = init_celery()
