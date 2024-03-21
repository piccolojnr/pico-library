from flask import url_for


EMAIL = "new_user@example.com"
PASSWORD = "XXXXXXXX"
FIRST_NAME = "firstname"
LAST_NAME = "lastname"
GENDER = "male"


def get_protected_route(test_client, auth_token):
    with test_client.application.test_request_context():
        return test_client.get(
            url_for("api.protected_route"),
            headers={"Authorization": f"Bearer {auth_token}"},
        )


def register_user(
    test_client,
    email=EMAIL,
    password=PASSWORD,
    first_name=FIRST_NAME,
    last_name=LAST_NAME,
    gender=GENDER,
):
    with test_client.application.test_request_context():
        response = test_client.post(
            url_for("api.auth_register"),
            data=f"email={email}&password={password}&first_name={first_name}\
                &last_name={last_name}&gender={gender}",
            content_type="application/x-www-form-urlencoded",
        )

    return response


def login_user(test_client, email=EMAIL, password=PASSWORD):
    with test_client.application.test_request_context():
        response = test_client.post(
            url_for("api.auth_login"),
            data=f"email={email}&password={password}",
            content_type="application/x-www-form-urlencoded",
        )

    return response


def refresh_token(test_client, refresh_token):
    with test_client.application.test_request_context():
        response = test_client.post(
            url_for("api.auth_refresh"),
            headers={"Authorization": f"Bearer {refresh_token}"},
        )

    return response


def logout_user(test_client, auth_token):
    with test_client.application.test_request_context():
        response = test_client.post(
            url_for("api.auth_logout"),
            headers={"Authorization": f"Bearer {auth_token}"},
        )

    return response


def change_password(test_client, auth_token, old_password, new_password):
    with test_client.application.test_request_context():
        response = test_client.post(
            url_for("api.auth_change_password"),
            data=f"old_password={old_password}&new_password={new_password}",
            headers={"Authorization": f"Bearer {auth_token}"},
            content_type="application/x-www-form-urlencoded",
        )

    return response


def get_user_profile(test_client, auth_token):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for("api.user_profile"),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response


def get_user_recommendations(test_client, auth_token, page=1, per_page=10):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for("api.user_recommendations", page=page, per_page=per_page),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response
