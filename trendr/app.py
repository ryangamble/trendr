import logging
import os
from flask import Flask
from flask_cors import CORS
from flask_security import SQLAlchemyUserDatastore
from flask_wtf.csrf import CSRFProtect

from trendr.extensions import db, security, mail, celery, migrate
from trendr.mail_util import CeleryMailUtil
from trendr.models.association_tables import (
    search_tweet_association,
    search_reddit_submission_association,
    search_reddit_comment_association,
)
from trendr.models.reddit_model import (
    RedditSubmissionType,
    RedditSubmission,
    RedditComment,
)
from trendr.models.tweet_model import Tweet
from trendr.models.search_model import Search
from trendr.models.user_model import User, Role


def create_app(for_celery=False):
    app = Flask(__name__)
    app.config.from_object("trendr.config")

    configure_extensions(app)
    configure_logging(app)

    if not for_celery:
        CORS(app)
        register_blueprints(app)
        init_celery(app)

    with app.app_context():
        db.create_all()

    return app


def configure_extensions(app):

    db.init_app(app)
    migrate.init_app(app, db)

    mail.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, mail_util_cls=CeleryMailUtil)
    CSRFProtect(app)


def configure_logging(app):
 
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)
 
    root = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(root, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file = os.path.join(logdir, 'app.log')
    handler = logging.FileHandler(log_file)
    
    formatter = logging.Formatter('%(asctime)s - %(filename)s: %(funcName)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    log_level = logging.DEBUG
    handler.setLevel(log_level)
    
    app.logger.addHandler(handler)
    app.logger.setLevel(log_level)


def register_blueprints(app):

    from trendr.routes.asset_routes import assets as assets_blueprint
    from trendr.routes.user_routes import users as users_blueprint

    app.register_blueprint(assets_blueprint)
    app.register_blueprint(users_blueprint)

    # logging routes
    print("\nApp routes:\n")
    print(app.url_map)
    # print("\n".join(sorted([f"{p.method}" for p in app.url_map.iter_rules()])))


def init_celery(app=None):
    app = app or create_app(for_celery=True)
    celery.conf.broker_url = app.config["CELERY_BROKER_URL"]
    celery.conf.result_backend = app.config["CELERY_RESULT_BACKEND"]
    celery.conf.timezone = "US/Eastern"
    celery.conf.task_routes = app.config["CELERY_TASK_ROUTES"]
    celery.conf.task_default_queue = app.config["CELERY_TASK_DEFAULT_QUEUE"]
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True, port=5000)
