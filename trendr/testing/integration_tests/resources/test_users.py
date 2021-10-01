import requests

from trendr.testing.helpers import create_random_string


# Positive Tests

def test_create_user():
    body = {
        "username": create_random_string(20),
        "email": create_random_string(20),
        "password": create_random_string(20),
    }
    resp = requests.post("http://localhost:5000/auth/signup", json=body)
    assert resp.status_code == 200
    data = resp.json()
    assert "message" in data
    assert data["message"] == "Success"


# Negative Tests


def test_create_user_missing_username():
    body = {
        "email": create_random_string(20),
        "password": create_random_string(20),
    }
    resp = requests.post("http://localhost:5000/auth/signup", json=body)
    assert resp.status_code == 400
    data = resp.json()
    assert "error" in data
    assert data["error"] == "Field username is required"


def test_create_user_missing_email():
    body = {
        "username": create_random_string(20),
        "password": create_random_string(20),
    }
    resp = requests.post("http://localhost:5000/auth/signup", json=body)
    assert resp.status_code == 400
    data = resp.json()
    assert "error" in data
    assert data["error"] == "Field email is required"


def test_create_user_missing_password():
    body = {
        "username": create_random_string(20),
        "email": create_random_string(20),
    }
    resp = requests.post("http://localhost:5000/auth/signup", json=body)
    assert resp.status_code == 400
    data = resp.json()
    assert "error" in data
    assert data["error"] == "Field password is required"


def test_create_user_duplicate_username():
    # Create a random user
    body = {
        "username": create_random_string(20),
        "email": create_random_string(20),
        "password": create_random_string(20),
    }
    requests.post("http://localhost:5000/auth/signup", json=body)

    # Create a new random user with the same username as the first
    body["email"] = create_random_string(20)
    resp = requests.post("http://localhost:5000/auth/signup", json=body)
    assert resp.status_code == 400
    data = resp.json()
    assert "error" in data
    assert data["error"] == "Username must be unique"


def test_create_user_duplicate_email():
    # Create a random user
    body = {
        "username": create_random_string(20),
        "email": create_random_string(20),
        "password": create_random_string(20),
    }
    requests.post("http://localhost:5000/auth/signup", json=body)

    # Create a new random user with the same email as the first
    body["username"] = create_random_string(20)
    resp = requests.post("http://localhost:5000/auth/signup", json=body)
    assert resp.status_code == 400
    data = resp.json()
    assert "error" in data
    assert data["error"] == "Email must be unique"
