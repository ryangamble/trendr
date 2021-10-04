from flask import Blueprint, request

from trendr.controllers.user_controller import find_user
from trendr.routes.helpers.json_response import json_response
from trendr.tasks.email import send_flask_mail

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


@users.route("/request-reset", methods=["POST"])
def request_reset_password():
    data = request.json

    # Verify all required fields are present and have values
    required_fields = ["email"]
    for field in required_fields:
        if field not in data or not data[field]:
            return json_response({"error": f"Field '{field}' is required"}, status=400)

    # If a user was found with the provided email, send them a password reset code
    user = find_user(email=data["email"])
    if user:
        # TODO: Send the email to the user
        pass

    return json_response({"message": "Success"}, status=200)


@users.route("/reset-password/<reset_token>", methods=["POST"])
def reset_password(reset_token):
    if not reset_token:
        return json_response({"error": "Invalid Token"}, status=400)

    # TODO: implement


