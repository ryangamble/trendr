from flask import Flask
from flask_cors import CORS
from flask_security import SQLAlchemyUserDatastore
from flask_wtf.csrf import CSRFProtect

from trendr.extensions import db, security, mail, celery, migrate
from trendr.mail_util import CeleryMailUtil
from trendr.models import (
    User,
    Role,
    Search,
    RedditPost,
    Tweet,
    search_tweet_association,
    search_reddit_post_association,
)


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object("trendr.config")

    configure_extensions(app)
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


def register_blueprints(app):

    from trendr.routes.asset_routes import assets as assets_blueprint
    from trendr.routes.user_routes import users as users_blueprint

    app.register_blueprint(assets_blueprint)
    app.register_blueprint(users_blueprint)

    # logging routes
    print("\nApp routes:")
    print(app.url_map)
    # print("\n".join(sorted([f"{p.method}" for p in app.url_map.iter_rules()])))


def init_celery(app=None):
    app = app or create_app()
    celery.conf.broker_url = app.config["CELERY_BROKER_URL"]
    celery.conf.result_backend = app.config["CELERY_RESULT_BACKEND"]
    celery.conf.timezone = "US/Eastern"
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
