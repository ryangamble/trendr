"""
This file is for creating functions to call /users endpoints
"""


def follow_asset_curr(client, json):
    return client.post("/users/follow-asset", json=json)


def unfollow_asset_curr(client, json):
    return client.post("/users/unfollow-asset", json=json)


def get_followed_assets_curr(client):
    return client.get("/users/assets-followed")


def get_assets_followed_by_user(client, username):
    return client.get(f"/users/assets-followed/{username}")


def get_settings(client):
    return client.get("/users/settings")


def set_settings(client, json):
    return client.put("/users/settings", json=json)

