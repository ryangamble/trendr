from trendr.extensions import celery
from trendr.extensions import db
from trendr.models import *
from trendr.connectors import twitter_connector, db_interface
from trendr.config import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET

api = twitter_connector.auth_to_api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)

@celery.task
@db_interface.store_in_db(api=api, wraps=twitter_connector.get_tweets_mentioning_asset)
def store_tweets_mentioning_asset(*args, **kwargs):
    return twitter_connector.get_tweets_mentioning_asset(*args, **kwargs)

@celery.task
@db_interface.store_in_db(api=api, wraps=twitter_connector.get_tweet_by_id)
def store_tweet_by_id(*args, **kwargs):
    return twitter_connector.get_tweet_by_id(*args, **kwargs)



# creating a wrapper isn't ideal, but it is much better than alternatives
#  of manually setting __name__ and __module__ of function
#
# The alternative is probably the most difficult-to-understand python code I have every written:
#
#   store_tweets_mentioning_asset = db_interface.store_in_db(api=api)(
#        twitter_connector.get_tweets_mentioning_asset
#   )
#   store_tweets_mentioning_asset.__name__ = "store_tweets_mentioning_asset"
#   store_tweets_mentioning_asset.__module__ = __name__
#   store_tweets_mentioning_asset = celery.task(store_tweets_mentioning_asset)