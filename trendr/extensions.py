from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security
from flask_security.models import fsqla_v2 as fsqla
from flask_mail import Mail
from celery import Celery

db = SQLAlchemy()
fsqla.FsModels.set_db_info(db)
migrate = Migrate()
# security = Security(register_blueprint=False)
security = Security()
mail = Mail()
celery = Celery()