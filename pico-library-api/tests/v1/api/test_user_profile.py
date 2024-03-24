from tests.v1.util import (
    get_user_profile,
    register_user,
    update_user_profile,
    login_user,
    EMAIL,
    ADMIN_EMAIL,
    FIRST_NAME,
    LAST_NAME,
    GENDER,
)
from pprint import pprint


def test_user_profile(db_session, app, client):
    response = register_user(client)
    assert response.status_code == 201

    auth_token = response.json["auth"]["auth_token"]

    response = get_user_profile(client, auth_token)
    assert response.status_code == 200
    assert response.json["user"]["email"] == EMAIL
    assert response.json["user"]["public_id"] is not None
    assert response.json["bio"] is None
    assert response.json["location"] is None
    assert response.json["first_name"] == FIRST_NAME
    assert response.json["last_name"] == LAST_NAME
    assert response.json["gender"] == GENDER
    assert response.json["created_at"] is not None
    assert response.json["updated_at"] is not None


def test_update_profile(db_session, app, client):
    response = register_user(client)
    assert response.status_code == 201

    auth_token = response.json["auth"]["auth_token"]

    response = get_user_profile(client, auth_token)
    assert response.status_code == 200
    assert response.json["user"]["email"] == EMAIL
    assert response.json["user"]["public_id"] is not None
    assert response.json["bio"] is None
    assert response.json["location"] is None
    assert response.json["first_name"] == FIRST_NAME
    assert response.json["last_name"] == LAST_NAME
    assert response.json["gender"] == GENDER
    assert response.json["created_at"] is not None
    assert response.json["updated_at"] is not None

    profile_data = {
        "bio": "This is my bio",
        "location": "This is my location",
        "first_name": "John",
        "last_name": "Doe",
        "gender": "male",
    }
    response = update_user_profile(client, auth_token, profile_data)
    assert response.status_code == 200
    assert response.json["item"]["user"]["email"] == EMAIL
    assert response.json["item"]["user"]["public_id"] is not None
    assert response.json["item"]["bio"] == "This is my bio"
    assert response.json["item"]["location"] == "This is my location"
    assert response.json["item"]["first_name"] == "John"
    assert response.json["item"]["last_name"] == "Doe"
    assert response.json["item"]["gender"] == "male"
    assert response.json["item"]["created_at"] is not None
    assert response.json["item"]["updated_at"] is not None
