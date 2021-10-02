from flask import Blueprint, redirect, url_for, request
from flask_login import login_required, logout_user
from sqlalchemy.orm.exc import NoResultFound

from trendr.extensions import db
from trendr.models.user_model import AccessLevelEnum, UserModel
from trendr.controllers.user_controller import create_user
from trendr.routes.helpers.json_response import json_response

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["POST"])
def login():
    data = request.json

    # Verify all required fields are present and have values
    required_fields = ["email", "password"]
    for field in required_fields:
        if field not in data or not data[field]:
            return json_response({"error": f"Field {field} is required"}, status=400)

    try:
        user = db.session.query(UserModel).filter(UserModel.email == data["email"]).one()
    except NoResultFound:
        return json_response({"error": f"Email does not exist"}, status=400)

    if user.password != data["password"]:
        return json_response({"error": f"Email/password did not match"}, status=400)

    response_body = {
        "username": user.username,
        "email": user.email,
        "access_level": user.access_level.name
    }
    return json_response(response_body, status=200)


@auth.route("/signup", methods=["POST"])
def signup():
    data = request.json

    # Verify all required fields are present and have values
    required_fields = ["username", "email", "password"]
    for field in required_fields:
        if field not in data or not data[field]:
            return json_response({"error": f"Field {field} is required"}, status=400)

    # If either of the reserved fields are taken, throw an error
    if db.session.query(UserModel).filter(UserModel.username == data["username"]).all():
        return json_response({"error": f"Username must be unique"}, status=400)
    if db.session.query(UserModel).filter(UserModel.email == data["email"]).all():
        return json_response({"error": f"Email must be unique"}, status=400)

    # Create the user in the database
    create_user(data["username"], data["email"], data["password"], AccessLevelEnum.basic)

    return json_response({"message": "Success"}, status=200)


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
