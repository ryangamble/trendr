import pytest
from trendr.extensions import security, db as database
from trendr.app import create_app
from trendr.testing.data import test_user
from unittest.mock import MagicMock


@pytest.fixture(scope="session")
def app():
    app = create_app(for_testing=True)
    # mock mail sending
    app.extensions["security"]._mail_util.send_mail = MagicMock()
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture
def db():
    try:
        database.create_all()
        security.datastore.create_user(
            email=test_user["email"],
            username=test_user["username"],
            password=test_user["password"],
        )
        yield database
    finally:
        database.drop_all()


# @pytest.fixture(scope="session")
# def db_engine():
#     """yields a SQLAlchemy engine which is suppressed after the test session"""
#     engine_ = None
#     try:
#         # Create an engine for the in memory sqlite database which isn't preserved between runs
#         db_url = "sqlite:///:memory:"
#         engine_ = create_engine(db_url, echo=True)

#         yield engine_
#     finally:
#         if engine_:
#             engine_.dispose()


# @pytest.fixture(scope="session")
# def db_tables(db_engine):
#     base_model = None
#     try:
#         base_model = db.Model
#         base_model.metadata.create_all(db_engine)
#         yield
#     finally:
#         if base_model:
#             base_model.metadata.drop_all(db_engine)


# @pytest.fixture
# def db_session(db_engine, db_tables):
#     """Returns an sqlalchemy session, and after the test tears down everything properly."""
#     session = None
#     transaction = None
#     connection = None
#     try:
#         connection = db_engine.connect()
#         # begin the nested transaction
#         transaction = connection.begin()
#         # use the connection with the already started transaction
#         session = Session(bind=connection)

#         yield session
#     finally:
#         if session:
#             session.close()
#         if transaction:
#             # roll back the broader transaction
#             transaction.rollback()
#         if connection:
#             # put back the connection to the connection pool
#             connection.close()
