import pytest
from sqlalchemy.orm import Session
from trendr.extensions import db
from sqlalchemy import create_engine


@pytest.fixture(scope='session')
def db_engine():
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    engine_ = None
    try:
        # Create an engine for the in memory sqlite database which isn't preserved between runs
        db_url = "sqlite:///:memory:"
        engine_ = create_engine(db_url, echo=True)

        yield engine_
    finally:
        if engine_:
            engine_.dispose()


@pytest.fixture(scope="session")
def db_tables(db_engine):
    base_model = None
    try:
        base_model = db.Model
        base_model.metadata.create_all(db_engine)
        yield
    finally:
        if base_model:
            base_model.metadata.drop_all(db_engine)


@pytest.fixture
def db_session(db_engine, db_tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    session = None
    transaction = None
    connection = None
    try:
        connection = db_engine.connect()
        # begin the nested transaction
        transaction = connection.begin()
        # use the connection with the already started transaction
        session = Session(bind=connection)

        yield session
    finally:
        if session:
            session.close()
        if transaction:
            # roll back the broader transaction
            transaction.rollback()
        if connection:
            # put back the connection to the connection pool
            connection.close()
