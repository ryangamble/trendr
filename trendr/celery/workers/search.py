from trendr.app import init_celery
from trendr.tasks.search import perform_search, create_datapoints

celery = init_celery()
