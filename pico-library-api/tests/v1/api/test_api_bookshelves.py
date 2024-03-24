from tests.v1.util import (
    login_user,
    create_bookshelf,
    get_bookshelves,
    update_bookshelf,
    delete_bookshelf,
    get_bookshelf,
    add_bookshelf_book,
    get_bookshelf_books,
    remove_bookshelf_book,
)


def test_create_bookshelf(db_session, client, user):
    response = login_user(client)
    assert response.status_code == 200
    auth_token = response.json["auth"]["auth_token"]

    response = create_bookshelf(
        client,
        auth_token,
        name="Test Bookshelf 1",
        description="Test Description",
        cover_image="Test Cover Image",
    )

    assert response.status_code == 201
    assert response.json["item"]["name"] == "Test Bookshelf 1"
    assert response.json["item"]["description"] == "Test Description"
    assert response.json["item"]["cover_image"] == "Test Cover Image"
    assert response.json["item"]["score"] == 0
    assert response.json["item"]["is_public"] == True

    response = create_bookshelf(
        client,
        auth_token,
        name="Test Bookshelf 2",
        description="Test Description",
        cover_image="Test Cover Image",
        is_public=False,
    )
    assert response.status_code == 201
    assert response.json["item"]["name"] == "Test Bookshelf 2"
    assert response.json["item"]["description"] == "Test Description"
    assert response.json["item"]["cover_image"] == "Test Cover Image"
    assert response.json["item"]["score"] == 0
    assert response.json["item"]["is_public"] == False

    bookshelf_data = response.json["item"]
    bookshelf_data["name"] = "Test Bookshelf 3"
    response = update_bookshelf(
        client, auth_token, bookshelf_id=bookshelf_data["id"], data=bookshelf_data
    )
    assert response.status_code == 200

    response = get_bookshelf(client, bookshelf_id=bookshelf_data["id"])
    assert response.status_code == 200
    assert response.json["name"] == "Test Bookshelf 3"

    response = delete_bookshelf(client, auth_token, bookshelf_id=bookshelf_data["id"])
    assert response.status_code == 200

    response = get_bookshelf(client, bookshelf_id=bookshelf_data["id"])
    assert response.status_code == 404


def test_retrieve_bookshelves(db_session, client, user):
    response = login_user(client)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    for i in range(20):
        response = create_bookshelf(client, auth_token, name=f"Test Bookshelf {i}")
        assert response.status_code == 201

    response = get_bookshelves(client, per_page=5)
    assert response.status_code == 200
    assert len(response.json["items"]) == 5
    assert response.json["total_items"] == 20
    assert response.json["total_pages"] == 4


def test_bookshelf_books(db_session, client, book_factory, user):
    response = login_user(client)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    bookshelf = create_bookshelf(client, auth_token, name="Test Bookshelf")
    assert bookshelf.status_code == 201

    for i in range(20):
        book = book_factory.create(id=i * 20, title=f"Test Book {i}")
        db_session.add(book)
        db_session.commit()

        assert book.id is not None
        assert len(book.bookshelves) == 0

        response = add_bookshelf_book(
            client,
            auth_token,
            bookshelf_id=bookshelf.json["item"]["id"],
            book_id=book.id,
        )
        assert response.status_code == 200

    response = get_bookshelf_books(client, bookshelf_id=bookshelf.json["item"]["id"])
    assert response.status_code == 200
    assert len(response.json["items"]) == 10
    assert response.json["total_items"] == 20
    assert response.json["total_pages"] == 2

    for i in range(20):
        response = remove_bookshelf_book(
            client,
            auth_token,
            bookshelf_id=bookshelf.json["item"]["id"],
            book_id=i * 20,
        )
        assert response.status_code == 200

    response = get_bookshelf_books(client, bookshelf_id=bookshelf.json["item"]["id"])
    assert response.status_code == 200
    assert len(response.json["items"]) == 0
