from flask import Blueprint, request
from flask_security import current_user, auth_required
from trendr.controllers.user_controller import (
    get_followed_assets,
    follow_asset,
    unfollow_asset,
)
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


@users.route("/follow-asset", methods=["POST"])
@auth_required()
def follow_asset_curr():
    content = request.get_json()

    if "identifier" in content:
        asset_identifier = content["identifier"]
    else:
        asset_identifier = content["id"]
    email = content["email"]

    # TODO: Get current user workflow working (requires frontend changes)
    if follow_asset(email, asset_identifier):
        return json_response(status=200, payload={"success": True})
    else:
        return json_response(status=400, payload={"success": False})


@users.route("/unfollow-asset", methods=["POST"])
@auth_required()
def unfollow_asset_curr():
    content = request.get_json()

    # TODO: Get current user workflow working (requires frontend changes)
    asset = None
    if "identifier" in content:
        asset = content["identifier"]
    elif "id" in content:
        asset = content["id"]
    email = content["email"]

    if unfollow_asset(email, asset):
        return json_response(status=200, payload={"success": True})
    else:
        return json_response(status=400, payload={"success": False})


@users.route("/assets-followed", methods=["GET"])
@auth_required()
def get_followed_assets_curr():
    return json_response(
        payload={"assets": get_followed_assets(user_id=current_user.id)}
    )


@users.route("/assets-followed/<email>", methods=["GET"])
def get_assets_followed_by_user(email):
    """
    Gets a list of the asset identifiers that a user follows
    :param email: The email of the user to check followed assets on
    :return: JSON Response containing a list of asset identifiers
    """
    # TODO: Get user id working (requires returning user_id to frontend)
    return json_response(payload={"assets": get_followed_assets(email=email)})
