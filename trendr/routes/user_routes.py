from flask import Blueprint, request, jsonify
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

@users.route("/test", methods=["GET"])
def test_function():
    return jsonify({"light" : True})



@users.route("/<user_id>", methods=["PUT"])
def update_user(user_id):
    pass


@users.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    pass


@users.route("/follow-asset", methods=["POST"])
@auth_required('session')
def follow_asset_curr():
    content = request.get_json()
    
    asset = None
    if "identifier" in content:
        asset = content["identifier"]
    else:
        asset = content["id"]

    # TODO: Get current user workflow working (requires frontend changes)
    if follow_asset(current_user, asset):
        return json_response(status=200, payload={"success": True})
    else:
        return json_response(status=400, payload={"success": False})


@users.route("/unfollow-asset", methods=["POST"])
@auth_required('session')
def unfollow_asset_curr():
    content = request.get_json()

    asset = None
    if "identifier" in content:
        asset = content["identifier"]
    else:
        asset = content["id"]

    if unfollow_asset(current_user, asset):
        return json_response(status=200, payload={"success": True})
    else:
        return json_response(status=400, payload={"success": False})


@users.route("/assets-followed", methods=["GET"])
@auth_required('session')
def get_followed_assets_curr():
    return json_response(
        payload={"assets": get_followed_assets(user=current_user)}
    )


@users.route("/assets-followed/<username>", methods=["GET"])
@auth_required('session')
def get_assets_followed_by_user(username):
    """
    Gets a list of the asset identifiers that a user follows
    :param username: The username of the user to check followed assets on
    :return: JSON Response containing a list of asset identifiers
    """
    return json_response(payload={"assets": get_followed_assets(user=username)})

@users.route("/settings", methods=["GET"])
@auth_required('session')
def get_settings():
    return json_response(current_user.get_settings())

@users.route("/settings", methods=["PUT"])
@auth_required('session')
def set_settings():
    content = request.get_json()

    current_user.set_settings(content)
    return json_response({"success": "true"})
