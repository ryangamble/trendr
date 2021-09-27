import enum

import flask

from flask_login import UserMixin
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, PasswordType, force_auto_coercion
from werkzeug.security import generate_password_hash, check_password_hash

from trendr.extensions import db


force_auto_coercion()


class AccessLevelEnum(enum.Enum):
    basic = 1
    pro = 2
    admin = 3


class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # https://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html#module-sqlalchemy_utils.types.password
    # implements basic setting and checking against plaintext
    password = db.Column(
        PasswordType(
            onload=lambda **kwargs: dict(
                schemes=flask.current_app.config["PASSWORD_SCHEMES"], **kwargs
            ),
        ),
        nullable=False
    )

    username = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(EmailType, nullable=False, unique=True)
    access_level = db.Column(Enum(AccessLevelEnum), nullable=False)

    # There is a one-many relationship between users and searches
    searches = relationship("SearchModel", backref="users")

    def __repr__(self):
        return '<User {}>'.format(self.username)
