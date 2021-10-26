import pytest
from trendr.models.reddit_model import RedditSubmission
from .test_data import new_reddit_submissions_data
from .fixtures import db_engine, db_tables, db_session


def test_add_search(db_session):
    """
    Generate new search and make sure database can add it

    :param db_session: sqlalchemy database session
    """


    new_reddit_post = RedditSubmission(**new_reddit_submissions_data[0])
    db_session.add(new_reddit_post)
    db_session.commit()

    query_res = db_session.query(RedditSubmission).filter_by(id=new_reddit_post.id).first()
    assert query_res is new_reddit_post
