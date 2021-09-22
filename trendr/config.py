import os
import logging


# def fetch_config(
#     name: str,
#     default: any = None,
#     cast: any = str
# ):
#     """
#     Fetch variable from environment if it exists and cast it

#     :param name: name of environmental variable
#     :type name: str
#     :param default: default value to return if env var does not exist, defaults to None
#     :type default: any, optional
#     :param cast: type to cast env var value to if it exists, defaults to str
#     :type cast: any, optional
#     :return: env var value from current environment
#     :rtype: cast
#     """

#     if name in os.environ:
#         val = os.getenv(name)
#         if cast != str:
#             try:
#                 return cast(val)
#             except Exception:
#                 return val
#         else:
#             return val

#     return default


# defaults = {
#     "FLASK_ENV": "development",
#     "SECRET_KEY": "secret-key",
#     "PASSWORD_SCHEMES": "pbkdf2_sha512",
#     "DATABASE_URI": "sqlite:///db.sqlite",
#     "CELERY_BROKER_URL": "amqp://localhost:5672",
#     "CELERY_RESULT_BACKEND": "amqp://localhost:5672",
# }

# ENV = fetch_config("FLASK_ENV", default="development")
# if ENV == "development": DEBUG = ENV

# SECRET_KEY = fetch_config("SECRET_KEY", default="secret-key")
# if SECRET_KEY == 

if "FLASK_ENV" in os.environ:
    ENV = os.getenv("FLASK_ENV")
else:
    DEBUG = ENV = "development"

if "SECRET_KEY" in os.environ:
    SECRET_KEY = os.getenv("SECRET_KEY")
else:
    insecure_exc = Exception("WARNING: Default secret key used")
    if ENV == "development":
        print(str(insecure_exc))
        SECRET_KEY = 'secret-key'
    else:
        raise insecure_exc

PASSWORD_SCHEMES = "pbkdf2_sha512"

if "DATABASE_URI" in os.environ:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
else:
    print("WARNING: Local database being used")
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"

SQLALCHEMY_TRACK_MODIFICATIONS = False

if "CELERY_BROKER_URL" in os.environ:
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
else:
    print("WARNING: Local insecure celery broker being used")
    CELERY_BROKER_URL = "amqp://localhost:5672"

if "CELERY_RESULT_BACKEND" in os.environ:
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
else:
    print("WARNING: Local insecure celery result backend being used")
    CELERY_RESULT_BACKEND = "amqp://localhost:5672"


"""
Reddit API secrets
"""
if "REDDIT_CLIENT_ID" in os.environ:
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
else:
    REDDIT_CLIENT_ID = None
if "REDDIT_CLIENT_SECRET" in os.environ:
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
else:
    REDDIT_CLIENT_SECRET = None
if "REDDIT_USER_AGENT" in os.environ:
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
else:
    REDDIT_USER_AGENT = None
