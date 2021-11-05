import json


def json_response(payload, status: int = 200):
    """
    Takes a json-formattable payload and converts it to a json response object

    :param payload: A json-formattable payload
    :param status: An integer http status code
    :return: (json, int, dict)
    """
    return json.dumps(payload), status, {"content-type": "application/json"}
