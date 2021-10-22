from flask import Blueprint

from trendr.controllers.user_controller import get_followed_assets
from trendr.routes.helpers.json_response import json_response

users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/", methods=["GET"])
def get_users():
    pass


@users.route("/<user_id>", methods=["GET"])
def get_users_by_id(user_id):
    pass


@users.route("/<user_id>", methods=["PUT"])
def update_user(user_id):
    pass


@users.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    pass


@users.route("/assets-followed/<user_id>", methods=["GET"])
def get_assets_followed_by_user(user_id):
    """
    Gets a list of the asset identifiers that a user follows
    :param user_id: The database user id to check followed assets on
    :return: JSON Response containing a list of asset identifiers
    """
    asset_associations = get_followed_assets(user_id)
    followed_assets = []
    for row in asset_associations:
        followed_assets.append(row.identifer)  # TODO: After we can add followed assets, check this works
    return json_response(status=200, payload={"assets": followed_assets})
