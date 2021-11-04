from flask import Blueprint

from trendr.routes.helpers.json_response import json_response

health = Blueprint("health", __name__, url_prefix="/health")


@health.route('/test', methods=['GET'])
def fear_greed():
    """
    Returns 200 OK if the application is running
    :return: JSON 200 OK response
    """
    return json_response(payload={"message": "OK"}, status=200)
