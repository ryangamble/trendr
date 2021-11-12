import random
import string
from trendr.testing.data import test_user

def create_random_string(num_char: int) -> str:
    """
    Returns a random string of length num_char

    :param num_char: The number of characters to use
    :return: The random string
    """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(num_char))

def login(client, email=test_user["email"], password=test_user["password"]):
    return client.post(
        "/auth/login",
        json=dict(email=email, password=password),
        follow_redirects=True,
    )

def logout(client):
    return client.post("/auth/logout", json=dict(), follow_redirects=True)
