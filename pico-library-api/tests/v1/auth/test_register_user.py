from tests.v1.util import (
    register_user,
    login_user,
    logout_user,
    get_protected_route,
    change_password,
)
from pprint import pprint


def test_register_user(db_session, app, client):
    with app.app_context():
        response = register_user(client)
        assert response.status_code == 201
        assert response.json["message"] == "User registered successfully"
        assert "auth" in response.json
        assert (
            "auth_token" in response.json["auth"]
            and type(response.json["auth"]["auth_token"]) == str
        )
        assert (
            "refresh_token" in response.json["auth"]
            and type(response.json["auth"]["refresh_token"]) == str
        )
        assert "status" in response.json and response.json["status"] == "success"
        assert "token_type" in response.json and response.json["token_type"] == "Bearer"


def test_login_user(db_session, app, client):
    with app.app_context():
        response = register_user(client, email="test@example.com", password="password")

        assert response.status_code == 201
        assert response.json["message"] == "User registered successfully"
        assert "auth" in response.json
        assert (
            "auth_token" in response.json["auth"]
            and type(response.json["auth"]["auth_token"]) == str
        )
        assert (
            "refresh_token" in response.json["auth"]
            and type(response.json["auth"]["refresh_token"]) == str
        )
        assert "status" in response.json and response.json["status"] == "success"
        assert "token_type" in response.json and response.json["token_type"] == "Bearer"

        response = login_user(client, email="test@example.com", password="password")
        assert response.status_code == 200
        assert response.json["message"] == "Logged in successfully"
        assert "auth" in response.json
        assert (
            "auth_token" in response.json["auth"]
            and type(response.json["auth"]["auth_token"]) == str
        )
        assert (
            "refresh_token" in response.json["auth"]
            and type(response.json["auth"]["refresh_token"]) == str
        )
        assert "status" in response.json and response.json["status"] == "success"
        assert "token_type" in response.json and response.json["token_type"] == "Bearer"


def test_logout_user(db_session, app, client):
    with app.app_context():
        response = register_user(client, email="test2@example.com", password="password")

        assert response.status_code == 201
        assert response.json["message"] == "User registered successfully"
        assert "auth" in response.json
        assert (
            "auth_token" in response.json["auth"]
            and type(response.json["auth"]["auth_token"]) == str
        )
        assert (
            "refresh_token" in response.json["auth"]
            and type(response.json["auth"]["refresh_token"]) == str
        )
        assert "status" in response.json and response.json["status"] == "success"
        assert "token_type" in response.json and response.json["token_type"] == "Bearer"

        p_response = get_protected_route(client, response.json["auth"]["auth_token"])
        assert p_response.status_code == 200
        assert p_response.json["message"] == "You've reached the protected route!"

        log_response = logout_user(client, response.json["auth"]["auth_token"])
        assert log_response.status_code == 200
        assert log_response.json["message"] == "Logged out successfully"
        assert "auth" not in log_response.json

        p_response = get_protected_route(client, response.json["auth"]["auth_token"])
        assert p_response.status_code == 401
        assert p_response.json["message"] == "Unauthorized"


def test_change_password(db_session, app, client):
    with app.app_context():
        response = register_user(client, email="test3@example.com", password="password")

        assert response.status_code == 201
        assert response.json["message"] == "User registered successfully"
        assert "auth" in response.json
        assert (
            "auth_token" in response.json["auth"]
            and type(response.json["auth"]["auth_token"]) == str
        )
        assert (
            "refresh_token" in response.json["auth"]
            and type(response.json["auth"]["refresh_token"]) == str
        )
        assert "status" in response.json and response.json["status"] == "success"
        assert "token_type" in response.json and response.json["token_type"] == "Bearer"

        p_response = get_protected_route(client, response.json["auth"]["auth_token"])
        assert p_response.status_code == 200

        ch_response = change_password(
            client, response.json["auth"]["auth_token"], "password", "new_password"
        )
        assert ch_response.status_code == 200
        assert ch_response.json["message"] == "Password changed successfully"

        response = login_user(
            client, email="test3@example.com", password="new_password"
        )
        assert "auth" in response.json
        assert (
            "auth_token" in response.json["auth"]
            and type(response.json["auth"]["auth_token"]) == str
        )
        assert (
            "refresh_token" in response.json["auth"]
            and type(response.json["auth"]["refresh_token"]) == str
        )
        assert "status" in response.json and response.json["status"] == "success"
        assert "token_type" in response.json and response.json["token_type"] == "Bearer"

        p_response = get_protected_route(client, response.json["auth"]["auth_token"])
        assert p_response.status_code == 200
