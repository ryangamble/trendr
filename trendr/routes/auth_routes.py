import unicodedata
from flask import Blueprint, request
from flask_security import auth_required, login_user, logout_user, current_user
from trendr.extensions import db, security
from trendr.config import SECURITY_PASSWORD_NORMALIZE_FORM
from trendr.models.user_model import User
from trendr.controllers.user_controller import create_user, find_user
from trendr.routes.helpers.json_response import json_response

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        response_body = {
            "username": current_user.username,
            "email": current_user.email,
            "roles": current_user.roles,
        }
        return json_response(response_body, status=200)

    data = request.json

    # Verify all required fields are present and have values
    required_fields = ["email", "password"]
    for field in required_fields:
        if field not in data or not data[field]:
            return json_response({"error": f"Field '{field}' is required"}, status=400)

    # validate and noramlize email
    try:
        email = security._mail_util.validate(data["email"])
    except ValueError as e:
        return json_response({"error": f"Email: {e!s}"}, status=400)

    # check if user exists
    user = find_user(email=email)
    if user is None:
        return json_response({"error": f"Email does not exist"}, status=400)

    # normalize password
    pbad, password = security._password_util.validate(data["password"], True)
    # check for invalid or non-matching password
    if (pbad is not None) or (not user.verify_and_update_password(password)):
        return json_response({"error": f"Email/password did not match"}, status=400)

    login_user(user)

    response_body = {
        "username": current_user.username,
        "email": user.email,
        "roles": user.roles,
    }
    return json_response(response_body, status=200)


@auth.route("/signup", methods=["POST"])
def signup():
    data = request.json

    # Verify all required fields are present and have values
    required_fields = ["username", "email", "password"]
    for field in required_fields:
        if field not in data or not data[field]:
            return json_response({"error": f"Field '{field}' is required"}, status=400)

    # normalize username
    username = unicodedata.normalize(SECURITY_PASSWORD_NORMALIZE_FORM, data["username"])

    # validate and noramlize email
    try:
        email = security._mail_util.validate(data["email"])
    except ValueError as e:
        return json_response({"error": f"Email: {e!s}"}, status=400)

    # validate and normalize password
    pbad, password = security._password_util.validate(data["password"], True)
    if pbad is not None:
        return json_response({"error": pbad}, status=400)

    # If either of the reserved fields are taken, throw an error
    if db.session.query(User).filter(User.username == data["username"]).all():
        return json_response({"error": f"Username must be unique"}, status=400)
    if db.session.query(User).filter(User.email == data["email"]).all():
        return json_response({"error": f"Email must be unique"}, status=400)

    # Create the user in the database
    user = create_user(username=username, email=email, password=password)
    login_user(user)

    return json_response({"message": "Success"}, status=200)


@auth.route("/logout", methods=["POST"])
@auth_required("session")
def logout():
    logout_user()

    return json_response({"message": "Success"}, status=200)
