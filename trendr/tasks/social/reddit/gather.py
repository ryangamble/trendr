from trendr.extensions import celery
from trendr.connectors import reddit_connector
from trendr.controllers.social_controller.utils import store_in_db

pmaw_api = None


@celery.task
@store_in_db(wraps=reddit_connector.gather_submissions)
def store_submissions(*args, **kwargs):
    global pmaw_api
    if pmaw_api is None:
        pmaw_api = reddit_connector.create_pmaw_api()
    kwargs["api"] = pmaw_api
    return reddit_connector.gather_submissions(*args, **kwargs)


@celery.task
@store_in_db(wraps=reddit_connector.gather_comments)
def store_comments(*args, **kwargs):
    global pmaw_api
    if pmaw_api is None:
        pmaw_api = reddit_connector.create_pmaw_api()
    kwargs["api"] = pmaw_api
    return reddit_connector.gather_comments(*args, **kwargs)


@celery.task
@store_in_db(wraps=reddit_connector.gather_submissions_by_id)
def store_submissions_by_id(*args, **kwargs):
    global pmaw_api
    if pmaw_api is None:
        pmaw_api = reddit_connector.create_pmaw_api()
    kwargs["api"] = pmaw_api
    return reddit_connector.gather_submissions_by_id(*args, **kwargs)


@celery.task
@store_in_db(wraps=reddit_connector.gather_comments_by_id)
def store_comments_by_id(*args, **kwargs):
    global pmaw_api
    if pmaw_api is None:
        pmaw_api = reddit_connector.create_pmaw_api()
    kwargs["api"] = pmaw_api
    return reddit_connector.gather_comments_by_id(*args, **kwargs)
