from trendr.extensions import celery
from trendr.connectors import reddit_connector
from trendr.controllers.social_controller.utils import store_in_db

pmaw_api = reddit_connector.create_pmaw_api()


@celery.task
@store_in_db(api=pmaw_api, wraps=reddit_connector.gather_submissions)
def store_submissions(*args, **kwargs):
    return reddit_connector.gather_submissions(*args, **kwargs)


@celery.task
@store_in_db(api=pmaw_api, wraps=reddit_connector.gather_comments)
def store_comments(*args, **kwargs):
    return reddit_connector.gather_comments(*args, **kwargs)


@celery.task
@store_in_db(api=pmaw_api, wraps=reddit_connector.gather_submissions_by_id)
def store_submissions_by_id(*args, **kwargs):
    return reddit_connector.gather_submissions_by_id(*args, **kwargs)


@celery.task
@store_in_db(api=pmaw_api, wraps=reddit_connector.gather_comments_by_id)
def store_comments_by_id(*args, **kwargs):
    return reddit_connector.gather_comments_by_id(*args, **kwargs)
