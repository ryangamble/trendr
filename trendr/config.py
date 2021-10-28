import os


def fetch_config(name: str, default: any = None, cast: any = str):
    """
    Fetch variable from environment if it exists and cast it

    :param name: name of environmental variable
    :type name: str
    :param default: default value to return if env var does not exist, defaults to None
    :type default: any, optional
    :param cast: type to cast env var value to if it exists, defaults to str
    :type cast: any, optional
    :return: env var value from current environment
    :rtype: cast
    """

    if name in os.environ:
        val = os.getenv(name)
        try:
            return cast(val)
        except Exception:
            return val
    return default


defaults = {
    "FLASK_ENV": "development",
    "SECRET_KEY": "secret-key",
    "SECURITY_PASSWORD_SALT": "146585145368132386173505678016728509634",
    "PASSWORD_SCHEMES": "pbkdf2_sha512",
    "SECURITY_PASSWORD_NORMALIZE_FORM": "NFKD",
    "SECURITY_PASSWORD_COMPLEXITY_CHECKER": "zxcvbn",
    "SQLALCHEMY_DATABASE_URI": "sqlite:///db.sqlite",
    "CELERY_BROKER_URL": "pyamqp://rabbitmq:5672",
    "CELERY_RESULT_BACKEND": "rpc://rabbitmq:5672",
}

ENV = fetch_config("FLASK_ENV", default=defaults["FLASK_ENV"])
DEBUG = ENV == "development"

SECRET_KEY = fetch_config("SECRET_KEY", default=defaults["SECRET_KEY"])
if SECRET_KEY == defaults["SECRET_KEY"]:
    insecure_exc = Exception("WARNING: Default secret key used")
    if ENV == "development":
        print(str(insecure_exc))
    else:
        raise insecure_exc

SECURITY_PASSWORD_SALT = fetch_config(
    "SECURITY_PASSWORD_SALT", default=defaults["SECURITY_PASSWORD_SALT"]
)
if SECURITY_PASSWORD_SALT == defaults["SECURITY_PASSWORD_SALT"]:
    insecure_exc = Exception("WARNING: Default password salt used")
    if ENV == "development":
        print(str(insecure_exc))
    else:
        raise insecure_exc

PASSWORD_SCHEMES = fetch_config(
    "PASSWORD_SCHEMES", default=defaults["PASSWORD_SCHEMES"]
)
SECURITY_PASSWORD_NORMALIZE_FORM = fetch_config(
    "SECURITY_PASSWORD_NORMALIZE_FORM",
    default=defaults["SECURITY_PASSWORD_NORMALIZE_FORM"],
)
SECURITY_PASSWORD_COMPLEXITY_CHECKER = fetch_config(
    "SECURITY_PASSWORD_COMPLEXITY_CHECKER",
    default=defaults["SECURITY_PASSWORD_COMPLEXITY_CHECKER"],
)
SECURITY_BLUEPRINT_NAME = "auth"
SECURITY_URL_PREFIX = "/auth"
SECURITY_CSRF_COOKIE_NAME = "XSRF-TOKEN"
WTF_CSRF_TIME_LIMIT = None
WTF_CSRF_CHECK_DEFAULT = False
SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True
SECURITY_LOGOUT_METHODS = ["POST"]
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True
SECURITY_CHANGEABLE = True
SECURITY_CONFIRMABLE = False
SECURITY_REGISTERABLE = True
SECURITY_USERNAME_ENABLE = True
SECURITY_EMAIL_SENDER = "admin@trendr.dev"
SQLALCHEMY_DATABASE_URI = fetch_config(
    "SQLALCHEMY_DATABASE_URI", default=defaults["SQLALCHEMY_DATABASE_URI"]
)
if SQLALCHEMY_DATABASE_URI == defaults["SQLALCHEMY_DATABASE_URI"]:
    print("WARNING: Local database being used")

SQLALCHEMY_TRACK_MODIFICATIONS = False

CELERY_BROKER_URL = fetch_config(
    "CELERY_BROKER_URL", default=defaults["CELERY_BROKER_URL"]
)
if CELERY_BROKER_URL == defaults["CELERY_BROKER_URL"]:
    print("WARNING: Local insecure celery broker being used")

CELERY_RESULT_BACKEND = fetch_config(
    "CELERY_RESULT_BACKEND", default=defaults["CELERY_RESULT_BACKEND"]
)
if CELERY_RESULT_BACKEND == defaults["CELERY_RESULT_BACKEND"]:
    print("WARNING: Local insecure celery backend being used")

"""
Reddit API secrets
"""
TWITTER_CONSUMER_KEY = fetch_config("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = fetch_config("TWITTER_CONSUMER_SECRET")

"""
Reddit API secrets
"""
REDDIT_CLIENT_ID = fetch_config("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = fetch_config("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = fetch_config("REDDIT_USER_AGENT")

"""
Mail config
"""
MAIL_SERVER = fetch_config("MAIL_SERVER")
MAIL_PORT = fetch_config("MAIL_PORT")
MAIL_USE_SSL = fetch_config("MAIL_USE_SSL")
MAIL_USERNAME = fetch_config("MAIL_USERNAME")
MAIL_PASSWORD = fetch_config("MAIL_PASSWORD")

'''
ETHplrere secret
'''
ETHPLORERE_KEY = fetch_config("ETHPLORER_KEY")
