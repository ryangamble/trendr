import pytest
from sqlalchemy.orm import Session
from trendr.extensions import db
from sqlalchemy import create_engine


@pytest.fixture(scope='session')
def db_engine(request):
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    # db_url = request.config.getoption("--dburl")
    db_url = "sqlite:///db.sqlite"
    engine_ = create_engine(db_url, echo=True)

    yield engine_

    engine_.dispose()


@pytest.fixture(scope="session")
def db_tables(db_engine):
    base_model = db.Model
    base_model.metadata.create_all(db_engine)
    yield
    base_model.metadata.drop_all(db_engine)


@pytest.fixture
def db_session(db_engine, db_tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = db_engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()
