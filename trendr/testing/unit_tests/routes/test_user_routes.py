import json
import pytest

from trendr.testing.bindings.users import follow_asset_curr


# Positive tests

# TODO: Figure out how to set current_user
# @pytest.mark.parametrize(
#     "req_body,follow_result", [
#         ({"identifier": "AAPL"}, True),
#         ({"identifier": "AAPL"}, False),
#         ({"id": "AAPL"}, True),
#         ({"id": "AAPL"}, False),
#     ]
# )
# def test_follow_asset(client, mocker, req_body, follow_result):
#     mocked_follow_asset = mocker.patch("trendr.controllers.user_controller.follow_asset", return_value=follow_result)
#     response = follow_asset_curr(client, req_body)
#     mocked_follow_asset.assert_not_called_once()
#     if follow_result:
#         assert response.status == 200
#         assert response.payload == {"success": True}
#     else:
#         assert response.status == 400
#         assert response.payload == {"success": False}


# Negative tests

def test_follow_asset_401(client, mocker):
    mocked_follow_asset = mocker.patch("trendr.controllers.user_controller.follow_asset")
    response = follow_asset_curr(client, {"id": "AAPL"})
    mocked_follow_asset.assert_not_called()
    assert response.status_code == 401
    assert response.json["response"]["error"] == 'You are not authenticated. Please supply the correct credentials.'
