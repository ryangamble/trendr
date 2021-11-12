from trendr.testing.data import test_user
from trendr.testing.helpers import login, logout
from trendr.testing.conftest import client, db

def test_login_logout(client, db):
    
    rv = login(client)
    assert rv.status_code == 200
    res_data = rv.get_json()
    print(res_data)

    rv = logout(client)
    assert rv.status_code == 200
    res_data = rv.get_json()
    print(res_data)