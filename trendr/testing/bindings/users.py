"""
This file is for creating functions to call /users endpoints
"""
from trendr.testing.bindings.auth import login, logout


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
