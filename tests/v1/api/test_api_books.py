from tests.v1.util import (
    get_book,
    get_books,
    create_book,
    delete_book,
    login_user,
    create_language,
    create_agent,
    create_bookshelf,
    create_publisher,
    create_subject,
    update_book,
    ADMIN_EMAIL,
)


def test_create_book(db_session, client, admin_user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    response = create_language(client, auth_token, name="english", code="en")
    assert response.status_code == 201
    language_id = response.json["item"]["id"]

    response = create_publisher(client, auth_token, name="publisher")
    assert response.status_code == 201
    publisher_id = response.json["item"]["id"]

    response = create_agent(
        client, auth_token, name="agent name", alias="agent alias", type="author"
    )
    assert response.status_code == 201
    agent_id = response.json["item"]["id"]

    response = create_bookshelf(
        client, auth_token, name="shelf", description="description"
    )
    assert response.status_code == 201
    bookshelf_id = response.json["item"]["id"]

    response = create_subject(client, auth_token, name="subject")
    assert response.status_code == 201
    subject_id = response.json["item"]["id"]

    book = dict(
        id=323,
        title="title of this book",
        description="description of this book",
        resources=[{"url": "english", "size": 43, "type": "html/jpg"}],
        languages=[language_id],
        publishers=[publisher_id],
        agents=[agent_id],
        bookshelves=[bookshelf_id],
        subjects=[subject_id],
    )
    response = create_book(client, auth_token, data=book)
    assert response.status_code == 201
    assert response.json["item"]["id"] == 323
    assert response.json["item"]["title"] == "title of this book"
    assert response.json["item"]["description"] == "description of this book"
    assert response.json["item"]["resources"][0]["url"] == "english"
    assert response.json["item"]["resources"][0]["size"] == 43
    assert response.json["item"]["resources"][0]["type"] == "html/jpg"
    assert response.json["item"]["languages"][0]["id"] == language_id
    assert response.json["item"]["publishers"][0]["id"] == publisher_id
    assert response.json["item"]["agents"][0]["id"] == agent_id
    assert response.json["item"]["bookshelves"][0]["id"] == bookshelf_id
    assert response.json["item"]["subjects"][0]["id"] == subject_id
    assert response.json["item"]["updated_at"]

    book_id = response.json["item"]["id"]
    response = get_book(client, book_id)
    assert response.status_code == 200
    assert response.json["id"] == 323
    assert response.json["title"] == "title of this book"

    response = delete_book(client, auth_token, book_id)
    assert response.status_code == 200

    response = get_book(client, book_id)
    assert response.status_code == 404


def test_get_books(db_session, client, admin_user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200
    auth_token = response.json["auth"]["auth_token"]

    for i in range(1, 10):
        response = create_book(client, auth_token, data=dict(title=f"book {i}"))
        assert response.status_code == 201

    response = get_books(client, per_page=5)
    assert response.status_code == 200


def test_update_book(db_session, client, admin_user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200
    auth_token = response.json["auth"]["auth_token"]

    response = create_book(client, auth_token, data=dict(title="book 1"))
    assert response.status_code == 201
    book_id = response.json["item"]["id"]

    response = update_book(client, auth_token, book_id, data=dict(title="book 2"))
    assert response.status_code == 200

    response = get_book(client, book_id)
    assert response.status_code == 200
    assert response.json["title"] == "book 2"
