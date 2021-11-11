from typing import Union
from flask_security import hash_password
from sqlalchemy.orm.exc import NoResultFound

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


def follow_asset(user: Union[User, str, int], asset: Union[Asset, str, int]) -> bool:
    """
    Follows asset for user

    :param user: user or user.id
    :param asset: asset or asset.identifier or asset.id
    :return: success
    """

    if type(user) == int:
        user = User.query.filter_by(id=user).one()
    elif type(user) == str:
        user = User.query.filter_by(email=user).one()

    if type(asset) == str:
        try:
            asset = Asset.query.filter_by(identifier=asset).one()
        except NoResultFound:
            # TODO: remove this and init all assets when db created
            asset = Asset(identifier=asset)
    elif type(asset) == int:
        asset = Asset.query.filter_by(id=asset).one()

    if (user and isinstance(user, User)) and (asset and isinstance(asset, Asset)):
        user.assets.append(asset)
        db.session.commit()
        return True

    return False


def unfollow_asset(user: Union[User, str, int], asset: Union[Asset, str, int]) -> bool:
    """
    Unfollows asset for user

    :param user: user or user.id
    :param asset: asset or asset.identifier or asset.id
    :return: success
    """

    if type(user) == int:
        user = User.query.filter_by(id=user).one()
    elif type(user) == str:
        user = User.query.filter_by(email=user).one()

    if type(asset) == str:
        asset = Asset.query.filter_by(identifier=asset).one()
    elif type(asset) == int:
        asset = Asset.query.filter_by(id=asset).one()

    if (user and isinstance(user, User)) and (asset and isinstance(asset, Asset)):
        user.assets.remove(asset)
        db.session.commit()
        return True

    return False


def get_followed_assets(user: Union[User, str, int]) -> list[str]:
    """
    Gets a list of the asset identifiers that a user follows
    :param user: user or user.id
    :return: list of asset identifiers
    :raises: Exception if user_id is not found
    """
    if type(user) == int:
        user = User.query.filter_by(id=user).one()
    elif type(user) == str:
        user = User.query.filter_by(email=user).one()

    if user and isinstance(user, User):
        return [asset.identifier for asset in user.assets]
    else:
        return None


def get_settings(user: User) -> dict:
    """
    Get settings dict from user

    :param user: user to get settings for
    :return: dictionary of settings
    """

    settings = {}
    for attr in user._settings_attrs:
        if hasattr(user, attr):
            settings[attr] = getattr(user, attr)

    return settings


def set_settings(user: User, settings: dict):
    """
    Set settings for user

    :param user: user to set settings for
    :param settings: settings dict. keys should be
        User attributes which are defined as settings attributes
    """
    for key, val in settings.items():
        if key in user._settings_attrs and hasattr(user, key):
            setattr(user, key, val)

    db.session.commit()
