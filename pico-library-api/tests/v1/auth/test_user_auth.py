import pytest
from tests.v1.util import get_protected_route, refresh_token
import time


def test_create_user(db_session, user_factory):
    user = user_factory.create()
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.email is not None
    with pytest.raises(AttributeError):
        user.password

    assert user.check_password("password") is False


def test_user_encode_auth_token(db_session, app, client, user):
    auth_: dict[str, bytes] | Exception = user.encode_auth_token()
    assert isinstance(auth_["auth_token"], str)
    assert isinstance(auth_["refresh_token"], str)

    with app.app_context():
        response = get_protected_route(client, auth_["auth_token"])
        assert response.status_code == 200
        assert response.json["message"] == "You've reached the protected route!"


def test_user_auth_token_expired(db_session, app, client, user):
    auth_: dict[str, bytes] | Exception = user.encode_auth_token()
    time.sleep(5)
    with app.app_context():
        response = get_protected_route(client, auth_["auth_token"])
        assert response.status_code == 401
        assert response.json["message"] == "auth token is not valid"


def test_user_no_auth_token(db_session, app, client, user):
    with app.app_context():
        response = get_protected_route(client, "")
        assert response.status_code == 401
        assert response.json["message"] == "auth token is not valid"


def test_user_refresh_token(db_session, app, client, user):
    auth_: dict[str, bytes] | Exception = user.encode_auth_token()
    response = refresh_token(client, auth_["refresh_token"])
    assert isinstance(response.json["auth_token"], str)
    assert response.json["message"] == "token refreshed"

    with app.app_context():
        response = get_protected_route(client, response.json["auth_token"])
        assert response.status_code == 200
        assert response.json["message"] == "You've reached the protected route!"
