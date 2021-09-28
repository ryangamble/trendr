from flask import Flask
from trendr.extensions import login_manager, celery, migrate, db
from trendr.models.user_model import UserModel
from trendr.models.search_model import SearchModel
from trendr.models.tweet_model import TweetModel
from trendr.models.reddit_post_model import RedditPostModel
from trendr.models.association_tables import tweet_association_table, reddit_post_association_table
from trendr.routes.asset_routes import assets as assets_blueprint
from trendr.routes.auth_routes import auth as auth_blueprint
from trendr.routes.user_routes import users as users_blueprint


def create_app():
    app = Flask(__name__)
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
    login_manager.login_view = 'routes.auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return UserModel.query.get(int(user_id))


def register_blueprints(app):
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
