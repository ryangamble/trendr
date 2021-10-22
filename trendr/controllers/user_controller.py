from flask_security import hash_password

from trendr.extensions import db, security
from trendr.models.association_tables import user_asset_association

user_datastore = security.datastore


def find_user(email):
    return user_datastore.find_user(email=email)


def create_user(email, password, roles=None, **kwargs):
    if roles is not None:
        kwargs["roles"] = roles

    new_user = user_datastore.create_user(
        email=email, password=hash_password(password), **kwargs
    )
    db.session.commit()
    return new_user


def get_followed_assets(user_id: int) -> []:  # TODO: List of what?
    """
    Gets a list of the asset identifiers that a user follows
    :param user_id: The database user id to check followed assets on
    :return: list of rows
    """
    return db.session.query(user_asset_association).filter_by(user_id=user_id).all()
