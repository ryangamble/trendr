from trendr.models.reddit_model import RedditAuthor
from .test_data import new_reddit_authors_data


def test_add_reddit_author(db_session):
    """
    Generate new RedditAuthor and make sure database can add it

    :param db_session: sqlalchemy database session
    """
    new_reddit_author = RedditAuthor(**new_reddit_authors_data[0])
    db_session.add(new_reddit_author)
    db_session.commit()

    query_res = db_session.query(RedditAuthor).filter_by(id=new_reddit_author.id).first()
    assert query_res is new_reddit_author
