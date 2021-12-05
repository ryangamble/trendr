from flask import Blueprint, request, current_app
from flask_security import current_user, auth_required
from trendr.controllers.security_email_controller import (
    change_email,
    confirm_change_email,
)
from trendr.controllers.user_controller import (
    get_followed_assets,
    follow_asset,
    unfollow_asset,
    get_settings,
    set_settings,
    get_result_history,
    add_result_history,
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


@users.route("/logged-in", methods=["GET"])
@auth_required("session")
def logged_in():
    if current_user is not None:
        return json_response(status=200, payload={"success": True})
    else:
        return json_response(status=400, payload={"success": False})


@users.route("/follow-asset", methods=["POST"])
@auth_required("session")
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
@auth_required("session")
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
@auth_required("session")
def get_followed_assets_curr():
    current_app.logger.info("Getting assets follwed for " + str(current_user.id))
    return json_response(payload={"assets": get_followed_assets(user=current_user)})


@users.route("/assets-followed/<username>", methods=["GET"])
@auth_required("session")
def get_assets_followed_by_user(username):
    """
    Gets a list of the asset identifiers that a user follows
    :param username: The username of the user to check followed assets on
    :return: JSON Response containing a list of asset identifiers
    """
    return json_response(payload={"assets": get_followed_assets(user=username)})


@users.route("/settings", methods=["GET"])
@auth_required("session")
def get_settings_route():
    return json_response(get_settings(current_user))


@users.route("/settings", methods=["PUT"])
@auth_required("session")
def set_settings_route():
    content = request.get_json()

    set_settings(current_user, content)
    return json_response({"success": "true"})


@users.route("/result-history", methods=["GET"])
@auth_required("session")
def get_result_history_route():
    return json_response(get_result_history(current_user))


@users.route("/result-history", methods=["POST"])
@auth_required("session")
def add_result_history_route():
    content = request.get_json()
    if "symbol" not in content:
        return json_response({"error": "Data field 'symbol' is required"}, status=400)
    if "type" not in content:
        return json_response({"error": "Data field 'type' is required"}, status=400)

    if add_result_history(current_user, content):
        return json_response({"success": "true"})
    else:
        return json_response({"success": False}, status=400)


users.add_url_rule(
    "/confirm-change-email/<token>", endpoint=None, view_func=confirm_change_email
)


users.add_url_rule(
    "/change-email", endpoint=None, view_func=change_email, methods=["GET", "POST"]
)
