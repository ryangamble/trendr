import pytest
from unittest.mock import MagicMock

from trendr.controllers import user_controller
from trendr.models.asset_model import Asset
from trendr.models.user_model import User


def test_find_user(mocker):
    security_mock = mocker.patch("trendr.controllers.user_controller.security")
    email = "test@test.com"
    user_controller.find_user(email)
    security_mock.datastore.find_user.assert_called_once_with(email=email)


@pytest.mark.parametrize(
    "roles",
    [
        None,
        ["mock_role"],
    ],
)
def test_create_user(mocker, roles):
    email = "test@test.com"
    password = "password"
    security_mock = mocker.patch("trendr.controllers.user_controller.security")
    db_mock = mocker.patch("trendr.controllers.user_controller.db")
    hash_mock = mocker.patch(
        "trendr.controllers.user_controller.hash_password", return_value=password
    )
    user_controller.create_user(email, password, roles)
    hash_mock.assert_called_once_with(password)
    if roles:
        security_mock.datastore.create_user.assert_called_once_with(
            email=email, password=password, roles=roles
        )
    else:
        security_mock.datastore.create_user.assert_called_once_with(
            email=email, password=password
        )
    db_mock.session.commit.assert_called_once()


@pytest.mark.parametrize(
    "user_arg,asset_arg",
    [
        (1, 1),
        ("test@test.com", 1),
        (1, "AAPL"),
        ("test@test.com", "AAPL"),
    ],
)
def test_follow_asset(mocker, user_arg, asset_arg):
    user = User()
    asset = Asset(identifier="AAPL")
    mocker.patch("trendr.controllers.user_controller.isinstance", return_value=True)
    db_mock = mocker.patch("trendr.controllers.user_controller.db")
    user_mock = mocker.patch("trendr.controllers.user_controller.User")
    asset_mock = mocker.patch("trendr.controllers.user_controller.Asset")
    sub_user_filter_mock = MagicMock()
    user_mock.query.filter_by.return_value = sub_user_filter_mock
    sub_user_filter_mock.one.return_value = user
    sub_asset_filter_mock = MagicMock()
    asset_mock.query.filter_by.return_value = sub_asset_filter_mock
    sub_asset_filter_mock.one.return_value = asset

    assert user_controller.follow_asset(user_arg, asset_arg)

    if type(user_arg) == int:
        user_mock.query.filter_by.assert_called_once_with(id=user_arg)
    elif type(user_arg) == str:
        user_mock.query.filter_by.assert_called_once_with(email=user_arg)

    if type(asset_arg) == str:
        asset_mock.query.filter_by.assert_called_once_with(identifier=asset_arg)
    elif type(asset_arg) == int:
        asset_mock.query.filter_by.assert_called_once_with(id=asset_arg)

    db_mock.session.commit.assert_called_once()


@pytest.mark.parametrize(
    "user_arg,asset_arg",
    [
        (1, 1),
        ("test@test.com", 1),
        (1, "AAPL"),
        ("test@test.com", "AAPL"),
    ],
)
def test_unfollow_asset(mocker, user_arg, asset_arg):
    user = User()
    asset = Asset(identifier="AAPL")
    user.assets.append(asset)
    mocker.patch("trendr.controllers.user_controller.isinstance", return_value=True)
    db_mock = mocker.patch("trendr.controllers.user_controller.db")
    user_mock = mocker.patch("trendr.controllers.user_controller.User")
    asset_mock = mocker.patch("trendr.controllers.user_controller.Asset")
    sub_user_filter_mock = MagicMock()
    user_mock.query.filter_by.return_value = sub_user_filter_mock
    sub_user_filter_mock.one.return_value = user
    sub_asset_filter_mock = MagicMock()
    asset_mock.query.filter_by.return_value = sub_asset_filter_mock
    sub_asset_filter_mock.one.return_value = asset

    assert user_controller.unfollow_asset(user_arg, asset_arg)

    if type(user_arg) == int:
        user_mock.query.filter_by.assert_called_once_with(id=user_arg)
    elif type(user_arg) == str:
        user_mock.query.filter_by.assert_called_once_with(email=user_arg)

    if type(asset_arg) == str:
        asset_mock.query.filter_by.assert_called_once_with(identifier=asset_arg)
    elif type(asset_arg) == int:
        asset_mock.query.filter_by.assert_called_once_with(id=asset_arg)

    db_mock.session.commit.assert_called_once()


@pytest.mark.parametrize(
    "user_arg,user_returned",
    [
        (1, True),
        ("test@test.com", True),
        (1, False),
        ("test@test.com", False),
    ],
)
def test_get_followed_assets(mocker, user_arg, user_returned):
    user = User()
    asset = Asset(identifier="AAPL")
    user.assets.append(asset)
    mocker.patch(
        "trendr.controllers.user_controller.isinstance", return_value=user_returned
    )
    user_mock = mocker.patch("trendr.controllers.user_controller.User")
    if user_returned:
        sub_mock = MagicMock()
        user_mock.query.filter_by.return_value = sub_mock
        sub_mock.one.return_value = user
    else:
        sub_mock = MagicMock()
        user_mock.query.filter_by.return_value = sub_mock
        sub_mock.one.return_value = None

    if user_returned:
        assert user_controller.get_followed_assets(user_arg) == ["AAPL"]
    else:
        assert user_controller.get_followed_assets(user_arg) is None

    if type(user_arg) == int:
        user_mock.query.filter_by.assert_called_once_with(id=user_arg)
    elif type(user_arg) == str:
        user_mock.query.filter_by.assert_called_once_with(email=user_arg)
