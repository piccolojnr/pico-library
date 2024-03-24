from tests.v1.util import (
    create_bookmark,
    delete_bookmark,
    update_bookmark,
    get_bookmark,
    get_bookmarks,
    login_user,
)
from pprint import pprint


def test_create_bookmark(db_session, client, book_factory, user):
    response = login_user(client)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    book = book_factory.create()
    db_session.add(book)
    db_session.commit()

    response = create_bookmark(
        client,
        auth_token,
        book_id=book.id,
        status="unread",
    )

    assert response.status_code == 201
    bookmark_id = response.json["item"]["id"]

    response = get_bookmark(client, bookmark_id=bookmark_id)
    assert response.status_code == 200
    assert response.json["status"] == "unread"

    response = update_bookmark(
        client, auth_token, bookmark_id=bookmark_id, status="read"
    )
    assert response.status_code == 200
    assert response.json["item"]["status"] == "read"

    response = delete_bookmark(
        client,
        auth_token,
        bookmark_id=bookmark_id,
    )
    assert response.status_code == 200

    response = get_bookmark(client, bookmark_id=bookmark_id)
    assert response.status_code == 404


def test_get_bookmarks(db_session, client, book_factory, user):
    response = login_user(client)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    for i in range(10):
        book = book_factory.create(id=i + 1)
        db_session.add(book)
        db_session.commit()

        response = create_bookmark(
            client, auth_token, book_id=book.id, status=f"unread"
        )
        assert response.status_code == 201

    response = get_bookmarks(client, per_page=5)
    assert response.status_code == 200
    assert len(response.json["items"]) == 5
