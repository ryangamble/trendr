from flask import Blueprint

users = Blueprint("users", __name__)


@users.route("/", methods=["GET"])
def get_users():
    pass


@users.route("/<user_id>", methods=["GET"])
def get_users_by_id(user_id):
    pass


@users.route("/<user_id", methods=["PUT"])
def update_user(user_id):
    pass


@users.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    pass
