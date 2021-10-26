import pytest
from trendr.models.search_model import Search
from .test_data import new_searches_data
from .fixtures import db_engine, db_tables, db_session


def test_add_search(db_session):
    """
    Generate new search and make sure database can add it

    :param db_session: sqlalchemy database session
    """


    new_search = Search(**new_searches_data[0])
    db_session.add(new_search)
    db_session.commit()

    query_res = db_session.query(Search).filter_by(id=new_search.id).first()
    assert query_res is new_search
