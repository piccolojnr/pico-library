from tests.v1.util import (
    get_user_profile,
    register_user,
    create_comment,
    retrive_comments,
)
from pprint import pprint
from http import HTTPStatus


def test_create_comment(db_session, app, client, book_factory):
    book = book_factory.create()
    db_session.add(book)
    db_session.commit()

    assert book.id is not None

    response = register_user(client)
    assert response.status_code == 201

    auth_token1 = response.json["auth"]["auth_token"]

    response = create_comment(
        client,
        auth_token1,
        book_id=book.id,
        type="comment",
        content="This is a test comment",
    )

    assert response.status_code == HTTPStatus.CREATED
    assert (
        response.json["message"]
        == "New comment was successfully added: This is a test comment."
    )
    assert response.json["status"] == "success"
    assert response.json["item"]["content"] == "This is a test comment"
    assert response.json["item"]["type"] == "comment"
    assert response.json["item"]["book_id"] == book.id
    assert response.json["item"]["parent_id"] is None
    assert response.json["item"]["number_of_replies"] == 0
    assert response.json["item"]["upvotes"] == 0
    assert response.json["item"]["downvotes"] == 0
    assert response.json["item"]["average_rating"] == 0.0
    assert response.json["item"]["created_at"] is not None

    response_rev = create_comment(
        client,
        auth_token1,
        book_id=book.id,
        type="review",
        content="This is a test comment",
    )
    assert response_rev.status_code == HTTPStatus.CREATED
    assert response_rev.json["item"]["type"] == "review"

    response = create_comment(
        client,
        auth_token1,
        book_id=book.id,
        type="reply",
        content="This is a test comment",
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json["message"] == "Parent comment ID is required for replies"

    response = create_comment(
        client,
        auth_token1,
        parent_id=response_rev.json["item"]["id"],
        type="reply",
        content="This is a test comment",
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json["item"]["type"] == "reply"


def test_retrieve_comments(db_session, app, client, book_factory):
    book = book_factory.create()
    db_session.add(book)
    db_session.commit()

    assert book.id is not None

    response = register_user(client)
    assert response.status_code == 201

    auth_token1 = response.json["auth"]["auth_token"]

    response = get_user_profile(client, auth_token1)
    assert response.status_code == HTTPStatus.OK

    for i in range(20):
        response = create_comment(
            client,
            auth_token1,
            book_id=book.id,
            type="comment",
            content=f"This is a test comment: {i}",
        )
        assert response.status_code == HTTPStatus.CREATED

    response = retrive_comments(
        client, type="comment", book_id=book.id, page=2, per_page=5
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json["has_next"] == True
    assert response.json["has_prev"] == True
    assert response.json["items_per_page"] == 5
    assert response.json["page"] == 2
    assert response.json["total_items"] == 20
    assert response.json["total_pages"] == 4

    comment_1 = response.json["items"][0]

    response = register_user(
        client, email="reply@gmail.com", first_name="reply", last_name="reply"
    )
    assert response.status_code == 201

    auth_token2 = response.json["auth"]["auth_token"]

    for i in range(10):
        response = create_comment(
            client,
            auth_token2,
            parent_id=comment_1["id"],
            type="reply",
            content=f"This is a test reply: {i}",
        )
        assert response.status_code == HTTPStatus.CREATED

    response = retrive_comments(
        client, type="reply", parent_id=comment_1["id"], per_page=5
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json["has_next"] == True
    assert response.json["has_prev"] == False
    assert response.json["items_per_page"] == 5
    assert response.json["page"] == 1
    assert response.json["total_pages"] == 2

    for i in range(20):
        response = create_comment(
            client,
            auth_token1,
            book_id=book.id,
            type="review",
            content=f"This is a test review: {i}",
        )
        assert response.status_code == HTTPStatus.CREATED

    response = retrive_comments(
        client, type="review", book_id=book.id, page=2, per_page=5
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json["has_next"] == True
    assert response.json["has_prev"] == True
    assert response.json["items_per_page"] == 5
    assert response.json["page"] == 2
    assert response.json["total_pages"] == 4
