from tests.v1.util import (
    create_publisher_book,
    create_publisher,
    delete_publisher,
    delete_publisher_book,
    update_publisher,
    get_publisher_books,
    get_publisher,
    get_publishers,
    login_user,
    ADMIN_EMAIL,
)


def test_create_publisher(db_session, client, admin_user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    response = create_publisher(client, auth_token, name="publisher")
    assert response.status_code == 201
    assert response.json["item"]["name"] == "publisher"
    publisher_id = response.json["item"]["id"]

    response = get_publisher(client, publisher_id=publisher_id)
    assert response.status_code == 200
    assert response.json["name"] == "publisher"

    response = update_publisher(
        client, auth_token, publisher_id=publisher_id, name="publisher_new"
    )
    assert response.status_code == 200
    assert response.json["item"]["name"] == "publisher_new"

    response = delete_publisher(
        client,
        auth_token,
        publisher_id=publisher_id,
    )
    assert response.status_code == 200

    response = get_publisher(client, publisher_id=publisher_id)
    assert response.status_code == 404


def test_get_publishers(db_session, client, admin_user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    for i in range(10):
        response = create_publisher(client, auth_token, name=f"name_{i}")
        assert response.status_code == 201

    response = get_publishers(client, per_page=5)
    assert response.status_code == 200
    assert len(response.json["items"]) == 5


def test_publisher_books(db_session, client, admin_user, book_factory):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    response = create_publisher(client, auth_token, name="publisher")
    assert response.status_code == 201
    assert response.json["item"]["name"] == "publisher"
    publisher_id = response.json["item"]["id"]

    for i in range(10):
        book = book_factory.create(id=i)
        db_session.add(book)
        db_session.commit()

        response = create_publisher_book(
            client, auth_token, publisher_id=publisher_id, book_id=book.id
        )
        assert response.status_code == 200

    response = get_publisher_books(client, publisher_id=publisher_id, per_page=5)
    assert response.status_code == 200
    assert len(response.json["items"]) == 5

    for i in range(10):
        response = delete_publisher_book(
            client, auth_token, publisher_id=publisher_id, book_id=i
        )
        assert response.status_code == 200

    response = get_publisher_books(client, publisher_id=publisher_id, per_page=5)
    assert response.status_code == 200
    assert len(response.json["items"]) == 0
