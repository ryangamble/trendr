import json
from flask import request, Blueprint

from trendr.controllers import user_controller
from trendr.routes.helpers.json_response import json_response

users = Blueprint('users', __name__)


@users.route('/', methods=['POST'])
def create_user():
    request_data = json.loads(request.data)
    user = user_controller.create_user(request_data["name"], request_data["password"])
    return json_response(user)


@users.route('/', methods=['GET'])
def get_users():
    pass


@users.route('/<user_id>', methods=['GET'])
def get_users_by_id(user_id):
    pass


@users.route('/<user_id', methods=['GET'])
def update_user(user_id):
    pass


@users.route('/<user_id>', methods=['GET'])
def delete_user(user_id):
    pass
