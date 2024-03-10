from flask import url_for


EMAIL = "new_user@example.com"
PASSWORD = "XXXXXXXX"
FIRST_NAME = "firstname"
LAST_NAME = "lastname"


def register_user(
    test_client,
    email=EMAIL,
    password=PASSWORD,
    first_name=FIRST_NAME,
    last_name=LAST_NAME,
):
    return test_client.post(
        url_for("api.auth_register"),
        data=f"email={email}&password={password}&first_name={first_name}&last_name={last_name}",
        content_type="application/x-www-form-urlencoded",
    )
