from tests.v1.util import get_user_profile, register_user, create_comment
from pprint import pprint
from http import HTTPStatus


def test_create_comment(db_session, app, client, book_factory):
    book = book_factory.create()
    db_session.add(book)
    db_session.commit()

    assert book.id is not None

    with app.app_context():
        response = register_user(client)
        assert response.status_code == 201

        auth_token1 = response.json["auth"]["auth_token"]

        response = get_user_profile(client, auth_token1)
        assert response.status_code == HTTPStatus.OK

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
