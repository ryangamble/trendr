from trendr.models.reddit_model import RedditComment
from .test_data import new_reddit_comments_data


def test_add_reddit_comment(db_session):
    """
    Generate new RedditComment and make sure database can add it

    :param db_session: sqlalchemy database session
    """
    new_reddit_comment = RedditComment(**new_reddit_comments_data[0])
    db_session.add(new_reddit_comment)
    db_session.commit()

    query_res = db_session.query(RedditComment).filter_by(id=new_reddit_comment.id).first()
    assert query_res is new_reddit_comment
