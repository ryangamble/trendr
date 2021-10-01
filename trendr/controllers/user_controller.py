from trendr.extensions import db
from trendr.models.user_model import UserModel


def create_user(username, email, password, access_level):
    user = UserModel(username, email, password, access_level)
    db.session.add(user)
    db.session.commit()
    return user
