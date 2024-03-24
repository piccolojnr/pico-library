from tests.v1.util import (
    get_subject,
    get_subject_books,
    create_subject,
    create_subject_book,
    create_subject_user,
    delete_subject,
    delete_subject_book,
    delete_subject_user,
    get_subjects,
    login_user,
    update_subject,
    ADMIN_EMAIL,
)

from pprint import pprint


def test_create_subject(db_session, client, admin_user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    response = create_subject(client, auth_token, name="test subject")
    assert response.status_code == 201
    assert response.json["item"]["name"] == "test subject"

    subject_id = response.json["item"]["id"]

    response = get_subject(client, subject_id)
    assert response.status_code == 200
    assert response.json["name"] == "test subject"

    response = update_subject(client, auth_token, subject_id, name="updated subject")
    assert response.status_code == 200

    response = get_subject(client, subject_id)
    assert response.status_code == 200
    assert response.json["name"] == "updated subject"

    response = delete_subject(client, auth_token, subject_id)
    assert response.status_code == 200

    response = get_subject(client, subject_id)
    assert response.status_code == 404


def test_get_subjects(db_session, client, admin_user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    for i in range(20):
        response = create_subject(client, auth_token, name=f"test subject {i}")
        assert response.status_code == 201
        assert response.json["item"]["name"] == f"test subject {i}"

    response = get_subjects(client)
    assert response.status_code == 200
    assert len(response.json["items"]) == 10


def test_create_subject_book(db_session, client, admin_user, book_factory):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    book = book_factory.create()

    db_session.add(book)
    db_session.commit()

    auth_token = response.json["auth"]["auth_token"]

    response = create_subject(client, auth_token, name="test subject")
    assert response.status_code == 201
    assert response.json["item"]["name"] == "test subject"

    subject_id = response.json["item"]["id"]

    response = create_subject_book(client, auth_token, subject_id, book_id=book.id)
    assert response.status_code == 200

    response = get_subject_books(client, subject_id)
    assert response.status_code == 200
    assert len(response.json["items"]) == 1

    response = delete_subject_book(client, auth_token, subject_id, book_id=book.id)
    assert response.status_code == 200

    response = get_subject_books(client, subject_id)
    assert response.status_code == 200
    assert len(response.json["items"]) == 0


def test_subject_users(db_session, client, admin_user, user_factory):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    response = create_subject(client, auth_token, name="test subject")
    assert response.status_code == 201
    assert response.json["item"]["name"] == "test subject"

    subject_id = response.json["item"]["id"]

    user_1 = user_factory.create()
    user_2 = user_factory.create()

    db_session.add(user_1)
    db_session.add(user_2)
    db_session.commit()

    response = create_subject_user(
        client, auth_token, subject_id, user_public_id=user_1.public_id
    )
    assert response.status_code == 200

    response = delete_subject_user(
        client, auth_token, subject_id, user_public_id=user_1.public_id
    )

    response = get_subject_books(client, subject_id)
    assert response.status_code == 200
    assert len(response.json["items"]) == 0


def test_update_subject_score(db_session, client, book_factory, admin_user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    response = create_subject(client, auth_token, name="Test subject")
    assert response.status_code == 201
    assert response.json["item"]["score"] == 0

    subject = response.json["item"]
    # remove null values
    for key in list(subject.keys()):
        if subject[key] is None:
            del subject[key]

    subject["score"] += 1
    response = update_subject(
        client, auth_token, subject_id=subject["id"], score=subject["score"]
    )
    assert response.status_code == 200

    response = get_subject(client, subject_id=subject["id"])

    assert response.status_code == 200
    assert response.json["score"] == 1
