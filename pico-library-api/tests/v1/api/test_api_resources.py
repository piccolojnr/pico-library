from tests.v1.util import (
    get_resource,
    create_resource,
    delete_resource,
    update_resource,
    get_resources,
    login_user,
    ADMIN_EMAIL,
)
from pprint import pprint


def test_create_resource(db_session, client, book_factory, admin_user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200
    auth_token = response.json["auth"]["auth_token"]

    book = book_factory.create()
    db_session.add(book)
    db_session.commit()

    data = {
        "url": "url.com",
        "type": "image/jpg",
        "modified": "2020-01-01",
        "size": 100,
    }

    response = create_resource(client, auth_token, book_id=book.id, data=data)
    assert response.status_code == 201
    assert response.json["item"]["url"] == data["url"]
    assert response.json["item"]["type"] == data["type"]
    assert response.json["item"]["size"] == data["size"]
    assert response.json["item"]["book"] is not None

    response_id = response.json["item"]["id"]
    data["size"] = 200

    response = update_resource(client, auth_token, resource_id=response_id, data=data)
    assert response.status_code == 200
    assert response.json["item"]["size"] == data["size"]

    response = get_resource(client, resource_id=response_id)
    assert response.status_code == 200

    response = delete_resource(client, auth_token, resource_id=response_id)
    assert response.status_code == 200

    response = get_resource(client, resource_id=response_id)
    assert response.status_code == 404


def test_get_resources(db_session, client, book_factory, admin_user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200
    auth_token = response.json["auth"]["auth_token"]
    book = book_factory.create()
    db_session.add(book)
    db_session.commit()
    for i in range(10):
        data = {
            "url": f"url{i}.com",
            "type": "image/jpg",
            "modified": "2020-01-01",
            "size": 100,
        }
        response = create_resource(client, auth_token, book_id=book.id, data=data)
        assert response.status_code == 201

    response = get_resources(client, book_id=book.id)
    assert response.status_code == 200
    assert len(response.json["items"]) == 10
