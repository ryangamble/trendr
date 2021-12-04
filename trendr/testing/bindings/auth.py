"""
This file is for creating functions to call flask-security-too /auth endpoints
"""
from trendr.testing.data import test_user


def login(client, email=test_user["email"], password=test_user["password"]):
    return client.post(
        "/auth/login",
        json=dict(email=email, password=password),
        follow_redirects=True,
    )


def logout(client):
    return client.post("/auth/logout", json=dict(), follow_redirects=True)
