from flask import Blueprint, redirect, url_for, request
from flask_login import login_required, logout_user

from trendr.app import db
from trendr.models.user_model import create_user, AccessLevelEnum, UserModel
from trendr.routes.helpers.json_response import json_response

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["GET", "POST"])
def login():
    pass


@auth.route("/signup", methods=["POST"])
def signup():
    data = request.json

    # Verify all required fields are present and have values
    required_fields = ["username", "first_name", "last_name", "email", "password"]
    for field in required_fields:
        if field not in data or not data[field]:
            return json_response({"error": f"Field {field} is required"}, status=400)

    # If either of the reserved fields are taken, throw an error
    if db.session.query(UserModel).filter(UserModel.username == data["username"]).all():
        return json_response({"error": f"Username must be unique"}, status=400)
    if db.session.query(UserModel).filter(UserModel.email == data["email"]).all():
        return json_response({"error": f"Email must be unique"}, status=400)

    # Create the user in the database
    create_user(data["username"], data["first_name"], data["last_name"], data["email"], data["password"],
                AccessLevelEnum.basic)

    return json_response({"message": "Success"}, status=200)


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
