from tests.v1.util import (
    get_user_profile,
    register_user,
    EMAIL,
    FIRST_NAME,
    LAST_NAME,
    GENDER,
)
from pprint import pprint


def test_user_profile(db_session, app, client):
    with app.app_context():
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
