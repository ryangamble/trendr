"""
This file is for creating functions to call /users endpoints
"""
from trendr.testing.bindings.auth import login, logout
from trendr.testing.data import test_user


def follow_asset_curr(client, json, as_user=False):
    if as_user:
        login(client)
        response = client.post("/users/follow-asset", json=json)
        logout(client)
        return response
    else:
        return client.post("/users/follow-asset", json=json)


def unfollow_asset_curr(client, json, as_user=False):
    if as_user:
        login(client)
        response = client.post("/users/unfollow-asset", json=json)
        logout(client)
        return response
    else:
        return client.post("/users/unfollow-asset", json=json)


def get_followed_assets_curr(client, as_user=False):
    if as_user:
        login(client)
        response = client.get("/users/assets-followed")
        logout(client)
        return response
    else:
        return client.get("/users/assets-followed")


def get_assets_followed_by_user(client, username, as_user=False):
    if as_user:
        login(client)
        response = client.get(f"/users/assets-followed/{username}")
        logout(client)
        return response
    else:
        return client.get(f"/users/assets-followed/{username}")


def get_settings(client, as_user=False):
    if as_user:
        login(client)
        response = client.get("/users/settings")
        logout(client)
        return response
    else:
        return client.get("/users/settings")


def set_settings(client, json, as_user=False):
    if as_user:
        login(client)
        response = client.put("/users/settings", json=json)
        logout(client)
        return response
    else:
        return client.put("/users/settings", json=json)


def change_email(client, new_email, as_user=False):
    form_data = {
        "email": test_user["email"],
        "new_email": new_email,
        "new_email_confirm": new_email,
        "submit": "Change email",
    }
    if as_user:
        login(client)
        response = client.post("/users/change-email", json=form_data)
        logout(client)
        return response
    else:
        return client.post("/users/change-email", json=form_data)


def confirm_change_email(client, token, as_user=False):
    req_url = f"/users/confirm-change-email/{token}"
    if as_user:
        login(client)
        response = client.get(req_url)
        logout(client)
        return response
    else:
        return client.get(req_url)
