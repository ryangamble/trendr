import pytest
import requests

from trendr.testing.helpers import create_random_string


# Positive Tests

def test_create_user_login():
    username = create_random_string(20)
    email = create_random_string(20)
    password = create_random_string(20)

    # Create a user
    body = {
        "username": username,
        "email": email,
        "password": password,
    }
    resp = requests.post("http://localhost:5000/auth/signup", json=body)
    assert resp.status_code == 200
    data = resp.json()
    assert "message" in data
    assert data["message"] == "Success"

    # Attempt to login as the created user
    body = {
        "email": email,
        "password": password,
    }
    resp = requests.post("http://localhost:5000/auth/login", json=body)
    assert resp.status_code == 200
    data = resp.json()
    assert "username" in data
    assert data["username"] == username
    assert "email" in data
    assert data["email"] == email
    assert "access_level" in data
    assert data["access_level"] == "basic"


# Negative Tests

@pytest.mark.parametrize(
    "missing_field",
    [
        "username",
        "email",
        "password"
    ],
)
def test_create_user_missing_field(missing_field):
    """
    Test to make sure that the appropriate response is returned when a field is missing on /auth/signup
    """
    body = {
        "username": create_random_string(20),
        "email": create_random_string(20),
        "password": create_random_string(20),
    }
    del body[missing_field]
    resp = requests.post("http://localhost:5000/auth/signup", json=body)
    assert resp.status_code == 400
    data = resp.json()
    assert "error" in data
    assert data["error"] == f"Field {missing_field} is required"


@pytest.mark.parametrize(
    "missing_field",
    [
        "email",
        "password"
    ],
)
def test_login_missing_field(missing_field):
    """
    Test to make sure that the appropriate response is returned when a field is missing on /auth/login
    """
    body = {
        "email": create_random_string(20),
        "password": create_random_string(20),
    }
    del body[missing_field]
    resp = requests.post("http://localhost:5000/auth/login", json=body)
    assert resp.status_code == 400
    data = resp.json()
    assert "error" in data
    assert data["error"] == f"Field {missing_field} is required"


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
