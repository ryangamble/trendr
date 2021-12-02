from trendr.testing.bindings import users as user_bindings


def test_follow_asset_401(client):
    response = user_bindings.follow_asset_curr(client, {"id": "AAPL"})
    assert response.status_code == 401
    assert (
        response.json["response"]["error"]
        == "You are not authenticated. Please supply the correct credentials."
    )


def test_unfollow_asset_401(client):
    response = user_bindings.unfollow_asset_curr(client, {"id": "AAPL"})
    assert response.status_code == 401
    assert (
        response.json["response"]["error"]
        == "You are not authenticated. Please supply the correct credentials."
    )


def test_get_followed_assets_curr_302(client):
    response = user_bindings.get_followed_assets_curr(client)
    assert response.status_code == 302


def test_get_assets_followed_by_user_302(client):
    response = user_bindings.get_assets_followed_by_user(client, "fake-username")
    assert response.status_code == 302


def test_get_settings_302(client):
    response = user_bindings.get_settings(client)
    assert response.status_code == 302


def test_set_settings_401(client):
    response = user_bindings.set_settings(client, {})
    assert response.status_code == 401
    assert (
        response.json["response"]["error"]
        == "You are not authenticated. Please supply the correct credentials."
    )

def test_change_email_401(client):
    response = user_bindings.change_email(client, "new_email@gmail.com")
    assert response.status_code == 401
    assert (
        response.json["response"]["error"]
        == "You are not authenticated. Please supply the correct credentials."
    )
