import pytest
from trendr.models.tweet_model import Tweet
from .test_data import new_tweets_data
from .fixtures import db_engine, db_tables, db_session


def test_add_search(db_session):
    """
    Generate new search and make sure database can add it

    :param db_session: sqlalchemy database session
    """


    new_tweet = Tweet(**new_tweets_data[0])
    db_session.add(new_tweet)
    db_session.commit()

    query_res = db_session.query(Tweet).filter_by(id=new_tweet.id).first()
    assert query_res is new_tweet
