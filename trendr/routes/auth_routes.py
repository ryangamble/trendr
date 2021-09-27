from flask import Blueprint, redirect, url_for
from flask_login import login_required, logout_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    pass


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    pass


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
