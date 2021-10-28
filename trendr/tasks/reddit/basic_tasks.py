from trendr.extensions import celery
from trendr.extensions import db
from trendr.models import *

from trendr.connectors import reddit_connector

pmaw_api = reddit_connector.create_pmaw_api()


@celery.task
def reddit_sentiment():

    results = reddit_connector.gather_submissions(
        api=pmaw_api, keywords=["AAPL"], limit=5
    )

    ret_arr = []

    for result in results:
        ret_arr.append(
            {
                "title": result["title"],
                "selftext": result["selftext"],
                "subreddit": result["subreddit"],
            }
        )

    print(ret_arr)

    return ret_arr
