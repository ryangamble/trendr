import pytest
from trendr.models.user_model import User, Role
from .test_data import new_role_data, new_user_data
from .fixtures import db_engine, db_tables, db_session


def test_add_role(db_session):
    """
    Generate new role and make sure database can add it

    :param db_session: sqlalchemy database session
    """


    new_role = Role(**new_role_data)
    db_session.add(new_role)
    db_session.commit()

    query_res = db_session.query(Role).filter_by(name=new_role_data["name"]).first()
    assert query_res is new_role


def test_add_user(db_session):
    """
    Generate new user and make sure database can add it

    :param db_session: sqlalchemy database session
    """

    new_user = User(**new_user_data)
    db_session.add(new_user)
    db_session.commit()

    query_res = (
        db_session.query(User).filter_by(username=new_user_data["username"]).first()
    )
    assert query_res is new_user