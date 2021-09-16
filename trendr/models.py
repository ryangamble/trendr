import flask
from .extensions import db
from sqlalchemy_utils import EmailType, PasswordType, force_auto_coercion
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

force_auto_coercion()

class User(UserMixin, db.Model):
    # __tablename__ = 'flasklogin-users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    email = db.Column(EmailType)

    # https://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html#module-sqlalchemy_utils.types.password
    # implements basic setting and checking against plaintext
    password = db.Column(
        PasswordType(
            onload=lambda **kwargs: dict(
                schemes=flask.current_app.config['PASSWORD_SCHEMES'],
                **kwargs
            ),
        ),
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)