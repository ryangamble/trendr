from trendr.extensions import celery
from trendr.extensions import db
from trendr.models import *
from trendr.connectors import reddit_connector, db_interface


# pmaw_api = reddit_connector.create_pmaw_api()

# create_praw_pmaw_api = celery.task(reddit_connector.create_pmaw_api)
# create_pmaw_api = celery.task(reddit_connector.create_pmaw_api)
# gather_items = celery.task(reddit_connector.gather_items)
# gather_submissions = celery.task(reddit_connector.gather_submissions)
# gather_comments = celery.task(reddit_connector.gather_comments)
# gather_items_by_id = celery.task(reddit_connector.gather_items_by_id)
# gather_submissions_by_id = celery.task(reddit_connector.gather_submissions_by_id)
# gather_comments_by_id = celery.task(reddit_connector.gather_comments_by_id)

# @celery.task
# @db_interface.store_tweet_in_db(overwrite=True)


# @celery.task
# def reddit_sentiment():

#     results = reddit_connector.gather_submissions(
#         api=pmaw_api, keywords=["AAPL"], limit=5
#     )

#     ret_arr = []

#     for result in results:
#         ret_arr.append(
#             {
#                 "title": result["title"],
#                 "selftext": result["selftext"],
#                 "subreddit": result["subreddit"],
#             }
#         )

#     print(ret_arr)

#     return ret_arr
