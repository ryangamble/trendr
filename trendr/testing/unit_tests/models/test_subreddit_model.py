import pytest
from trendr.models.reddit_model import Subreddit
from .test_data import new_subreddits_data
from .fixtures import db_engine, db_tables, db_session


def test_add_subreddit(db_session):
    """
    Generate new Subreddit and make sure database can add it

    :param db_session: sqlalchemy database session
    """


    new_subreddit = Subreddit(**new_subreddits_data[0])
    db_session.add(new_subreddit)
    db_session.commit()

    query_res = db_session.query(Subreddit).filter_by(id=new_subreddit.id).first()
    assert query_res is new_subreddit
