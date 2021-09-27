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
        if cast != str:
            try:
                return cast(val)
            except Exception:
                return val
        else:
            return val

    return default


defaults = {
    "FLASK_ENV": "development",
    "SECRET_KEY": "secret-key",
    "PASSWORD_SCHEMES": "pbkdf2_sha512",
    "SQLALCHEMY_DATABASE_URI": "sqlite:///db.sqlite",
    "CELERY_BROKER_URL": "pyamqp://rabbitmq:5672",
    "CELERY_RESULT_BACKEND": "rpc://rabbitmq:5672",
}

ENV = fetch_config("FLASK_ENV", default=defaults["FLASK_ENV"])
if ENV == "development":
    DEBUG = ENV

SECRET_KEY = fetch_config("SECRET_KEY", default=defaults["SECRET_KEY"])
if SECRET_KEY == defaults["SECRET_KEY"]:
    insecure_exc = Exception("WARNING: Default secret key used")
    if ENV == "development":
        print(str(insecure_exc))
    else:
        raise insecure_exc

PASSWORD_SCHEMES = fetch_config(
    "PASSWORD_SCHEMES", default=defaults["PASSWORD_SCHEMES"]
)
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
REDDIT_CLIENT_ID = fetch_config("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = fetch_config("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = fetch_config("REDDIT_USER_AGENT")
