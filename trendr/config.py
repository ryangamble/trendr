import os

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

PASSWORD_SCHEMES = 'pbkdf2_sha512'

if "DATABASE_URI" in os.environ:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
else:
    print("WARNING: Local database being used")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'

SQLALCHEMY_TRACK_MODIFICATIONS = False

if "CELERY_BROKER_URL" in os.environ:
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
else:
    print("WARNING: Local insecure celery broker being used")
    CELERY_BROKER_URL = 'amqp://localhost:5672'

if "CELERY_RESULT_BACKEND" in os.environ:
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
else:
    print("WARNING: Local insecure celery result backend being used")
    CELERY_RESULT_BACKEND = 'amqp://localhost:5672'

"""
Twitter API secrets
"""
if "TWITTER_CONSUMER_KEY" in os.environ:
    TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
else:
    TWITTER_CONSUMER_KEY = None
if "TWITTER_CONSUMER_SECRET" in os.environ:
    TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
else:
    TWITTER_CONSUMER_SECRET = None
if "TWITTER_ACCESS_TOKEN" in os.environ:
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
else:
    TWITTER_ACCESS_TOKEN = None
if "TWITTER_ACCESS_TOKEN_SECRET" in os.environ:
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
else:
    TWITTER_ACCESS_TOKEN_SECRET = None


# TODO: Add some kind of secret loader function that handles all of this in a much more modular way.
#  likely want to put all of the secret names in some kind of data structure that we can loop over
