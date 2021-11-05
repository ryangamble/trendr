from trendr.app import init_celery
from trendr.tasks.search import (
    perform_search,
    aggregate_sentiment_simple_mean_search,
)

celery = init_celery()
