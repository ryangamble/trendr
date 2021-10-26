from trendr.extensions import celery
from trendr.connectors import twitter_connector
from trendr.controllers.social_controller.utils import store_in_db
from trendr.config import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET

api = twitter_connector.auth_to_api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)


@celery.task
@store_in_db(api=api, wraps=twitter_connector.get_tweets_mentioning_asset)
def store_tweets_mentioning_asset(*args, **kwargs):
    return twitter_connector.get_tweets_mentioning_asset(*args, **kwargs)


@celery.task
@store_in_db(api=api, wraps=twitter_connector.get_tweet_by_id)
def store_tweet_by_id(*args, **kwargs):
    return twitter_connector.get_tweet_by_id(*args, **kwargs)
