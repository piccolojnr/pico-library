import pytest
from tests.v1.util import (
    ADMIN_EMAIL,
    get_protected_route,
    get_admin_protected_route,
    login_user,
    refresh_token,
)
import time

from pprint import pprint
from flask_pyjwt import JWT


def test_create_user(db_session, user_factory):
    user = user_factory.create()
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.email is not None
    with pytest.raises(AttributeError):
        user.password

    assert user.check_password("password") is False


def test_user_encode_auth_token(db_session, app, client, admin_user):
    auth_: dict[str, bytes] | Exception = admin_user.encode_auth_token()
    assert isinstance(auth_["auth_token"], str)
    assert isinstance(auth_["refresh_token"], str)

    response = get_protected_route(client, auth_["auth_token"])
    assert response.status_code == 200
    assert response.json["message"] == "You've reached the protected route!"


def test_user_auth_token_expired(db_session, app, client, admin_user):
    auth_: dict[str, bytes] | Exception = admin_user.encode_auth_token()
    time.sleep(5)

    response = get_protected_route(client, auth_["auth_token"])
    assert response.status_code == 401
    assert response.json["message"] == "auth token is not valid"


def test_user_no_auth_token(db_session, app, client, admin_user):
    response = get_protected_route(client, "")
    assert response.status_code == 401
    assert response.json["message"] == "auth token is not valid"


def test_user_refresh_token(db_session, app, client, admin_user):
    auth_: dict[str, bytes] | Exception = admin_user.encode_auth_token()
    response = refresh_token(client, auth_["refresh_token"])
    assert isinstance(response.json["auth_token"], str)
    assert response.json["message"] == "token refreshed"

    response = get_protected_route(client, response.json["auth_token"])
    assert response.status_code == 200
    assert response.json["message"] == "You've reached the protected route!"


def test_admin_user(db_session, client, admin_user, user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    admin_auth_token = response.json["auth"]["auth_token"]

    response = login_user(client)
    assert response.status_code == 200
    auth_token = response.json["auth"]["auth_token"]

    response = get_protected_route(client, admin_auth_token)
    assert response.status_code == 200
    assert response.json["message"] == "You've reached the protected route!"

    response = get_admin_protected_route(client, admin_auth_token)
    assert response.status_code == 200
    assert response.json["message"] == "You've reached the admin protected route!"

    response = get_admin_protected_route(client, auth_token)
    assert response.status_code == 403
    assert response.json["message"] == "Missing required scope(s)"
