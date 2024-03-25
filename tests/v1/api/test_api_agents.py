from tests.v1.util import (
    create_agent,
    login_user,
    get_agents,
    delete_agent,
    update_agent,
    get_agent_books,
    add_agent_book,
    remove_agent_book,
    ADMIN_EMAIL,
)
from pprint import pprint
import pytest


@pytest.mark.parametrize(
    "type, name",
    [
        ("ANNOTATOR", "Agent 1"),
        ("AUTHOR", "Agent 2"),
        ("COMMENTATOR", "Agent 3"),
        ("COMPILER", "Agent 4"),
        ("COMPOSER", "Agent 5"),
        ("CONTRIBUTOR", "Agent 6"),
        ("EDITOR", "Agent 7"),
        ("ILLUSTRATOR", "Agent 8"),
        ("OTHER", "Agent 9"),
        ("PHOTOGRAPHER", "Agent 10"),
        ("TRANSLATOR", "Agent 11"),
    ],
)
def test_create_agent(db_session, client, admin_user, name, type):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    response = create_agent(client, auth_token, name=name, alias="alias", type=type)
    assert response.status_code == 201
    assert response.json["item"]["name"] == name
    assert response.json["item"]["alias"] == "alias"


def test_retrive_agents(db_session, app, client, admin_user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]
    agent_types = [
        "ANNOTATOR",
        "AUTHOR",
        "COMMENTATOR",
        "COMPILER",
        "COMPOSER",
        "CONTRIBUTOR",
        "EDITOR",
        "ILLUSTRATOR",
        "OTHER",
        "PHOTOGRAPHER",
        "TRANSLATOR",
    ]
    for i in range(12 * 5):
        agent_type = agent_types[i % len(agent_types)]
        response = create_agent(
            client,
            auth_token,
            name=f"Agent {i}",
            alias="alias",
            birth_date=2000,
            death_date=2004,
            webpage="author.com",
            type=agent_type,
        )
        assert response.status_code == 201

    response = get_agents(client, page=1, per_page=5)
    assert response.status_code == 200
    assert response.json["page"] == 1
    assert response.json["items_per_page"] == 5


@pytest.mark.parametrize(
    "type",
    [
        "ANNOTATOR",
        "AUTHOR",
        "COMMENTATOR",
        "COMPILER",
        "COMPOSER",
        "CONTRIBUTOR",
        "EDITOR",
        "ILLUSTRATOR",
        "OTHER",
        "PHOTOGRAPHER",
        "TRANSLATOR",
    ],
)
def test_retrieve_agents_by_type(db_session, client, admin_user, type):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]
    agent_types = [
        "ANNOTATOR",
        "AUTHOR",
        "COMMENTATOR",
        "COMPILER",
        "COMPOSER",
        "CONTRIBUTOR",
        "EDITOR",
        "ILLUSTRATOR",
        "OTHER",
        "PHOTOGRAPHER",
        "TRANSLATOR",
    ]
    for i in range(12 * 5):
        agent_type = agent_types[i % len(agent_types)]
        response = create_agent(
            client,
            auth_token,
            name=f"Agent {i}",
            alias="alias",
            birth_date=2000,
            death_date=2004,
            webpage="author.com",
            type=agent_type,
        )
        assert response.status_code == 201

    response = get_agents(client, type=type)

    assert response.status_code == 200


def test_get_delete_update_agent(db_session, client, admin_user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    response = create_agent(
        client,
        auth_token,
        name=f"Agent 1",
        alias="alias",
        birth_date=2000,
        death_date=2004,
        webpage="author.com",
        type="AUTHOR",
    )
    assert response.status_code == 201
    agent_data = response.json["item"]

    agent_data["name"] = "Agent 2"
    agent_data["type"] = "AUTHOR"
    response = update_agent(
        client, auth_token, agent_id=agent_data["id"], data=agent_data
    )
    assert response.status_code == 200

    response = delete_agent(client, auth_token, agent_id=1)
    assert response.status_code == 200


def test_add_agent_book(db_session, book_factory, client, admin_user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    response = create_agent(
        client,
        auth_token,
        name=f"Agent 1",
        alias="alias",
        birth_date=2000,
        death_date=2004,
        webpage="author.com",
        type="AUTHOR",
    )
    assert response.status_code == 201
    agent_data = response.json["item"]

    book = book_factory.create()
    db_session.add(book)
    db_session.commit()
    assert len(book.agents) == 0

    response = add_agent_book(
        client, auth_token, agent_id=agent_data["id"], book_id=book.id
    )
    assert response.status_code == 200
    assert len(book.agents) == 1

    response = remove_agent_book(
        client, auth_token, agent_id=agent_data["id"], book_id=book.id
    )
    assert response.status_code == 200
    assert len(book.agents) == 0


def test_agent_books(db_session, book_factory, client, admin_user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    response = create_agent(
        client,
        auth_token,
        name=f"Agent 1",
        alias="alias",
        birth_date=2000,
        death_date=2004,
        webpage="author.com",
        type="AUTHOR",
    )
    assert response.status_code == 201
    agent_data = response.json["item"]

    for i in range(5):
        book = book_factory.create(id=i + 1, title=f"Book {i}")
        db_session.add(book)
        db_session.commit()
        assert len(book.agents) == 0
        response = add_agent_book(
            client, auth_token, agent_id=agent_data["id"], book_id=book.id
        )

    response = get_agent_books(client, agent_id=agent_data["id"])
    assert response.status_code == 200
