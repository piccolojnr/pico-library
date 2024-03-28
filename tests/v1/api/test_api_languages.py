from tests.v1.util import (
    create_language_book,
    create_language,
    delete_language,
    delete_language_book,
    update_language,
    get_language_books,
    get_language,
    get_languages,
    login_user,
    ADMIN_EMAIL,
)


def test_create_language(db_session, client, admin_user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    response = create_language(client, auth_token, code="en", name="english")
    assert response.status_code == 201
    assert response.json["item"]["code"] == "en"
    assert response.json["item"]["name"] == "english"
    language_id = response.json["item"]["id"]

    response = get_language(client, language_id=language_id)
    assert response.status_code == 200
    assert response.json["code"] == "en"
    assert response.json["name"] == "english"

    response = update_language(
        client, auth_token, language_id=language_id, name="english_new"
    )
    assert response.status_code == 200
    assert response.json["item"]["code"] == "en"
    assert response.json["item"]["name"] == "english_new"

    response = delete_language(
        client,
        auth_token,
        language_id=language_id,
    )
    assert response.status_code == 200

    response = get_language(client, language_id=language_id)
    assert response.status_code == 404


def test_get_languages(db_session, client, admin_user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    for i in range(10):
        response = create_language(
            client, auth_token, code=f"code_{i}", name=f"name_{i}"
        )
        assert response.status_code == 201

    response = get_languages(client, per_page=5)
    assert response.status_code == 200


def test_language_books(db_session, client, admin_user, book_factory):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    response = create_language(client, auth_token, code="en", name="english")
    assert response.status_code == 201
    assert response.json["item"]["code"] == "en"
    assert response.json["item"]["name"] == "english"
    language_id = response.json["item"]["id"]

    for i in range(10):
        book = book_factory.create(id=i)
        db_session.add(book)
        db_session.commit()

        response = create_language_book(
            client, auth_token, language_id=language_id, book_id=book.id
        )
        assert response.status_code == 200

    response = get_language_books(client, language_id=language_id, per_page=5)
    assert response.status_code == 200
    assert len(response.json["items"]) == 5

    for i in range(10):
        response = delete_language_book(
            client, auth_token, language_id=language_id, book_id=i
        )
        assert response.status_code == 200

    response = get_language_books(client, language_id=language_id, per_page=5)
    assert response.status_code == 200
    assert len(response.json["items"]) == 0
