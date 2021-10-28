from flask_security import hash_password
from trendr.extensions import db, security

user_datastore = security.datastore


def find_user(email):
    return user_datastore.find_user(email=email)


def create_user(email, password, roles=None, **kwargs):
    if roles != None:
        kwargs["roles"] = roles

    new_user = user_datastore.create_user(
        email=email, password=hash_password(password), **kwargs
    )
    db.session.commit()
    return new_user
