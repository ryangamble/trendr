import pytest
from trendr.models.reddit_post_model import RedditPost
from .test_data import new_reddit_posts_data
from .fixtures import *


def test_add_search(db_session):
    """
    Generate new search and make sure database can add it

    :param db_session: sqlalchemy database session
    """


    new_reddit_post = RedditPost(**new_reddit_posts_data[0])
    db_session.add(new_reddit_post)
    db_session.commit()

    query_res = db_session.query(RedditPost).filter_by(id=new_reddit_post.id).first()
    assert query_res is new_reddit_post
