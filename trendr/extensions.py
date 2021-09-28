# all extensions used and initialized stored here
from flask_migrate import Migrate
from flask_login import LoginManager
from celery import Celery

migrate = Migrate()
login_manager = LoginManager()
celery = Celery()
