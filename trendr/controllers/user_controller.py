from typing import Union
from flask_security import hash_password

from trendr.extensions import db, security
from trendr.models.asset_model import Asset
from trendr.models.association_tables import user_asset_association
from trendr.models.user_model import User, Role

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


def follow_asset(email: str, asset: Union[Asset, str, int]) -> bool:
    """
    Follows asset for user

    :param email: user email
    :param asset: asset or asset.identifier or asset.id
    :return: success
    """
    # TODO: Undo email changes in favor of id when frontend can handle it
    # if type(user) == int:
    user = User.query.filter_by(email=email).first()

    if type(asset) == str:
        asset = Asset.query.filter_by(identifier=asset).first()
    elif type(asset) == int:
        asset = Asset.query.filter_by(id=asset).first()

    if (user and isinstance(user, User)) and (
        asset and isinstance(asset, Asset)
    ):
        user.assets.append(asset)
        db.session.commit()
        return True

    return False


def unfollow_asset(email: str, asset: Union[Asset, str, int]) -> bool:
    """
    Unfollows asset for user

    :param email: user email
    :param asset: asset or asset.identifier or asset.id
    :return: success
    """
    # TODO: Undo email changes in favor of id when frontend can handle it
    # if type(user) == int:
    user = User.query.filter_by(email=email).first()

    if type(asset) == str:
        asset = Asset.query.filter_by(identifier=asset).first()
    elif type(asset) == int:
        asset = Asset.query.filter_by(id=asset).first()

    if (user and isinstance(user, User)) and (
        asset and isinstance(asset, Asset)
    ):
        user.assets.remove(asset)
        db.session.commit()
        return True

    return False


def get_followed_assets(user: User = None, user_id: int = None, email: str = None) -> list[str]:
    """
    Gets a list of the asset identifiers that a user follows
    :param user: user
    :param user_id: user.id
    :param email: user email
    :return: list of asset identifiers
    :raises: Exception if user_id is not found
    """
    # TODO: Undo email changes in favor of id when frontend can handle it
    if user_id:
        user = User.query.filter_by(id=user).first()
    elif email:
        user = User.query.filter_by(email=email).first()

    if user and isinstance(user, User):
        return [asset.identifier for asset in user.assets]
    else:
        return None
