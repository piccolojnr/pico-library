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


def update_user_profile(test_client, auth_token, data):
    with test_client.application.test_request_context():
        response = test_client.put(
            url_for("api.user_profile"),
            headers={"Authorization": f"Bearer {auth_token}"},
            json=data,
            content_type="application/json",
        )
        return response


def get_user_recommendations(test_client, auth_token, page=1, per_page=10):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for("api.book_recommendations", page=page, per_page=per_page),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response


def create_comment(test_client, auth_token, **kwargs):
    with test_client.application.test_request_context():
        response = test_client.post(
            url_for("api.comments"),
            headers={"Authorization": f"Bearer {auth_token}"},
            json=kwargs,
            content_type="application/json",
        )
        return response


def retrive_comments(test_client, **kwargs):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for("api.comments", **kwargs),
        )
        return response


def search_books(test_client, query, criteria="title", page=1, per_page=10):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for(
                "api.book_search",
                q=query,
                criteria=criteria,
                page=page,
                per_page=per_page,
            ),
        )
        return response


def get_book(test_client, book_id):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for("api.book", book_id=book_id),
        )
        return response


def create_agent(test_client, auth_token, **kwargs):
    with test_client.application.test_request_context():
        response = test_client.post(
            url_for("api.agents"),
            headers={"Authorization": f"Bearer {auth_token}"},
            json=kwargs,
            content_type="application/json",
        )
        return response


def retrieve_agents(test_client, **kwargs):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for("api.agents", **kwargs),
        )
        return response


def get_agent(test_client, agent_id):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for("api.agent", agent_id=agent_id),
        )
        return response


def delete_agent(test_client, auth_token, agent_id):
    with test_client.application.test_request_context():
        response = test_client.delete(
            url_for("api.agent", agent_id=agent_id),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response


def update_agent(test_client, auth_token, agent_id, data):
    with test_client.application.test_request_context():
        response = test_client.put(
            url_for("api.agent", agent_id=agent_id),
            headers={"Authorization": f"Bearer {auth_token}"},
            json=data,
            content_type="application/json",
        )
        return response


def get_agent_books(test_client, agent_id, page=1, per_page=10):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for("api.agent_books", agent_id=agent_id, page=page, per_page=per_page)
        )
        return response


def add_agent_book(test_client, auth_token, agent_id, book_id):
    with test_client.application.test_request_context():
        response = test_client.post(
            url_for("api.agent_book", agent_id=agent_id, book_id=book_id),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response


def remove_agent_book(test_client, auth_token, agent_id, book_id):
    with test_client.application.test_request_context():
        response = test_client.delete(
            url_for("api.agent_book", agent_id=agent_id, book_id=book_id),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response


# def get_book_agents(test_client, book_id):
#     with test_client.application.test_request_context():
#         response = test_client.get(
#             url_for("api.book_agents", book_id=book_id),
#         )
#         return response