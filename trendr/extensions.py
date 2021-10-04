# all extensions used and initialized stored here
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security
from flask_mail import Mail
from celery import Celery
from flask_security.models import fsqla_v2 as fsqla

db = SQLAlchemy()
migrate = Migrate()
security = Security()
mail = Mail()
celery = Celery()


fsqla.FsModels.set_db_info(
    db, user_table_name="users", role_table_name="roles"
)