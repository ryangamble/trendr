from flask import Blueprint, redirect, url_for, request
from flask_login import login_required, logout_user
from sqlalchemy.orm import sessionmaker

from trendr.models.user_model import create_user
from trendr.routes.helpers.json_response import json_response

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    pass


@auth.route("/signup", methods=["POST"])
def signup():
    data = request.data

    # Verify all required fields are present and have values
    required_fields = ["username", "first_name", "last_name", "email", "password"]
    for field in required_fields:
        if field not in data or not data.__getattribute__(field):
            return json_response({"error": f"Field {field} is required"}, status=400)

    create_user(data["username"], data["first_name"], data["last_name"], data["email"], data["password"])









@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
