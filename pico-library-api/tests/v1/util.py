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


def get_agents(test_client, **kwargs):
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


def create_bookshelf(test_client, auth_token, **kwargs):
    with test_client.application.test_request_context():
        response = test_client.post(
            url_for("api.bookshelves"),
            headers={"Authorization": f"Bearer {auth_token}"},
            json=kwargs,
            content_type="application/json",
        )
        return response


def get_bookshelves(test_client, page=1, per_page=10):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for("api.bookshelves", page=page, per_page=per_page),
        )
        return response


def delete_bookshelf(test_client, auth_token, bookshelf_id):
    with test_client.application.test_request_context():
        response = test_client.delete(
            url_for("api.bookshelf", bookshelf_id=bookshelf_id),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response


def get_bookshelf(test_client, bookshelf_id):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for("api.bookshelf", bookshelf_id=bookshelf_id),
        )
        return response


def update_bookshelf(test_client, auth_token, bookshelf_id, data):
    with test_client.application.test_request_context():
        response = test_client.put(
            url_for("api.bookshelf", bookshelf_id=bookshelf_id),
            headers={"Authorization": f"Bearer {auth_token}"},
            json=data,
            content_type="application/json",
        )
        return response


def add_bookshelf_book(test_client, auth_token, bookshelf_id, book_id):
    with test_client.application.test_request_context():
        response = test_client.post(
            url_for("api.bookshelf_book", bookshelf_id=bookshelf_id, book_id=book_id),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response


def remove_bookshelf_book(test_client, auth_token, bookshelf_id, book_id):
    with test_client.application.test_request_context():
        response = test_client.delete(
            url_for("api.bookshelf_book", bookshelf_id=bookshelf_id, book_id=book_id),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response


def get_bookshelf_books(test_client, bookshelf_id, page=1, per_page=10):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for(
                "api.bookshelf_books",
                bookshelf_id=bookshelf_id,
                page=page,
                per_page=per_page,
            ),
        )
        return response


def create_resource(test_client, auth_token, book_id, data):
    with test_client.application.test_request_context():
        response = test_client.post(
            url_for("api.resources", book_id=book_id),
            headers={"Authorization": f"Bearer {auth_token}"},
            json=data,
            content_type="application/json",
        )
        return response


def get_resources(test_client, book_id):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for("api.resources", book_id=book_id),
        )
        return response


def get_resource(test_client, resource_id):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for("api.resource", resource_id=resource_id),
        )
        return response


def delete_resource(test_client, auth_token, resource_id):
    with test_client.application.test_request_context():
        response = test_client.delete(
            url_for("api.resource", resource_id=resource_id),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response


def update_resource(test_client, auth_token, resource_id, data):
    with test_client.application.test_request_context():
        response = test_client.put(
            url_for("api.resource", resource_id=resource_id),
            headers={"Authorization": f"Bearer {auth_token}"},
            json=data,
            content_type="application/json",
        )
        return response


def create_subject(test_client, auth_token, name):
    with test_client.application.test_request_context():
        response = test_client.post(
            url_for("api.subjects", name=name),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response


def get_subjects(test_client, page=1, per_page=10):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for("api.subjects", page=page, per_page=per_page),
        )
        return response


def get_subject(test_client, subject_id):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for("api.subject", subject_id=subject_id),
        )
        return response


def delete_subject(test_client, auth_token, subject_id):
    with test_client.application.test_request_context():
        response = test_client.delete(
            url_for("api.subject", subject_id=subject_id),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response


def update_subject(test_client, auth_token, subject_id, name):
    with test_client.application.test_request_context():
        response = test_client.put(
            url_for("api.subject", subject_id=subject_id, name=name),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response


def get_subject_books(test_client, subject_id, page=1, per_page=10):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for(
                "api.subject_books", subject_id=subject_id, page=page, per_page=per_page
            ),
        )
        return response


def create_subject_book(test_client, auth_token, subject_id, book_id):
    with test_client.application.test_request_context():
        response = test_client.post(
            url_for("api.subject_book", subject_id=subject_id, book_id=book_id),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response


def delete_subject_book(test_client, auth_token, subject_id, book_id):
    with test_client.application.test_request_context():
        response = test_client.delete(
            url_for("api.subject_book", subject_id=subject_id, book_id=book_id),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response


def create_subject_user(test_client, auth_token, subject_id, user_public_id):
    with test_client.application.test_request_context():
        response = test_client.post(
            url_for(
                "api.subject_user", subject_id=subject_id, user_public_id=user_public_id
            ),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response


def delete_subject_user(test_client, auth_token, subject_id, user_public_id):
    with test_client.application.test_request_context():
        response = test_client.delete(
            url_for(
                "api.subject_user", subject_id=subject_id, user_public_id=user_public_id
            ),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response


def get_subject_user(test_client, auth_token, subject_id, user_public_id):
    with test_client.application.test_request_context():
        response = test_client.get(
            url_for(
                "api.subject_user", subject_id=subject_id, user_public_id=user_public_id
            ),
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        return response
