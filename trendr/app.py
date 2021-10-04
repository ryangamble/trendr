from flask import Flask
from flask_security import SQLAlchemyUserDatastore
# from flask_security.models import fsqla_v2 as fsqla
from trendr.extensions import db, security, mail, celery, migrate
from trendr.models import *

def create_app():
    app = Flask(__name__)
    app.config.from_object("trendr.config")

    configure_extensions(app)
    register_blueprints(app)
    init_celery(app)

    with app.app_context():
        # TODO: When we care about saving data, stop dropping the tables
        db.drop_all()
        db.create_all()

    return app


def configure_extensions(app):
    # fsqla.FsModels.set_db_info(
    #     db, user_table_name="users", role_table_name="roles"
    # )

    # from trendr.models import (
    #     User,
    #     Role,
    #     Search,
    #     RedditPost,
    #     Tweet,
    #     search_tweet_association,
    #     search_reddit_post_association,
    # )

    db.init_app(app)
    migrate.init_app(app, db)

    mail.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)


def register_blueprints(app):
    
    from trendr.routes.asset_routes import assets as assets_blueprint
    from trendr.routes.auth_routes import auth as auth_blueprint
    from trendr.routes.user_routes import users as users_blueprint

    app.register_blueprint(assets_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(users_blueprint)

    # logging routes
    print("\nApp routes:")
    print([str(p) for p in app.url_map.iter_rules()])
    print("\n")


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
    app.run(debug=True)
