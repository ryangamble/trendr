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
