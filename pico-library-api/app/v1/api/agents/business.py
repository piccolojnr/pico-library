from http import HTTPStatus
from flask_restx import abort, marshal
from app.v1 import db
from flask import jsonify, url_for
from app.v1.models import Agent, AgentType, Book
from app.v1.utils.pagination import _pagination_nav_header_links, _pagination_nav_links
from app.v1.api.agents.dto import agent_pagination_model, agent_model
from app.v1.api.books.dto import book_pagination_model


def process_create_agent(data):
    data["type"] = AgentType[data["type"].upper()] if data["type"] else None
    data["type"] = AgentType.OTHER if data["type"] == None else data["type"]

    agent = Agent(**data)
    db.session.add(agent)
    db.session.commit()
    agent_data = marshal(agent, agent_model)
    response = {
        "status": "success",
        "message": "Agent created successfully",
        "item": agent_data,
    }
    response_status_code = HTTPStatus.CREATED
    response_headers = {"Location": url_for("api.agent", agent_id=agent.id)}

    return response, response_status_code, response_headers


def process_get_agent(agent_id):
    agent = Agent.query.filter(Agent.id == agent_id).first()
    if not agent:
        abort(HTTPStatus.NOT_FOUND, "Agent not found")
    return marshal(agent, agent_model)


def process_update_agent(agent_id, data):
    agent = Agent.query.filter(Agent.id == agent_id).first()
    if not agent:
        abort(HTTPStatus.NOT_FOUND, "Agent not found")

    for key, value in data.items():
        if value is not None and key != "id":
            if key == "type":
                value = AgentType[value.upper()]
            setattr(agent, key, value)

    db.session.commit()
    return {
        "status": "success",
        "message": f"Agent with ID {agent_id} was successfully updated.",
    }


def process_delete_agent(agent_id):
    agent = Agent.query.filter(Agent.id == agent_id).first()
    if not agent:
        abort(HTTPStatus.NOT_FOUND, "agent not found")
    db.session.delete(agent)
    db.session.commit()
    return {"status": "success", "message": "agent deleted successfully"}


def process_get_agents(page=1, per_page=10, type=None):
    if not type:
        agents = Agent.query.paginate(page=page, per_page=per_page)
    else:
        agent_type = AgentType[type.upper()]
        agents = Agent.query.filter_by(type=agent_type).paginate(
            page=page, per_page=per_page
        )

    pagination = dict(
        page=agents.page,
        items_per_page=agents.per_page,
        total_pages=agents.pages,
        total_items=agents.total,
        items=agents.items,
        has_next=agents.has_next,
        has_prev=agents.has_prev,
        next_num=agents.next_num,
        prev_num=agents.prev_num,
        links=[],
    )
    response_data = marshal(pagination, agent_pagination_model)
    response_data["links"] = _pagination_nav_links(pagination, "agents")
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(pagination, "agents")
    response.headers["Total-Count"] = agents.pages
    return response


def process_get_agent_books(agent_id, page=1, per_page=10):
    agent = Agent.query.filter(Agent.id == agent_id).first()
    if not agent:
        abort(HTTPStatus.NOT_FOUND, "Agent not found")

    books = Book.query.filter(Book.agents.any(Agent.id == agent_id)).paginate(
        page=page, per_page=per_page
    )

    pagination = dict(
        page=books.page,
        items_per_page=books.per_page,
        total_pages=books.pages,
        total_items=books.total,
        items=books.items,
        has_next=books.has_next,
        has_prev=books.has_prev,
        next_num=books.next_num,
        prev_num=books.prev_num,
        links=[],
    )
    response_data = marshal(pagination, book_pagination_model)
    response_data["links"] = _pagination_nav_links(
        pagination, "agent_books", agent_id=agent_id
    )
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(
        pagination, "agent_books", agent_id=agent_id
    )
    response.headers["Total-Count"] = books.pages
    return response


def process_add_agent_book(agent_id, book_id):
    agent = Agent.query.filter(Agent.id == agent_id).first()
    if not agent:
        abort(HTTPStatus.NOT_FOUND, "Agent not found")

    book = Book.query.filter(Book.id == book_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, "Book not found")

    if book in agent.books:
        abort(HTTPStatus.CONFLICT, "Book already assigned to agent")

    agent.books.append(book)
    db.session.commit()
    return {"status": "success", "message": "Book added successfully"}


def process_remove_agent_book(agent_id, book_id):
    agent = Agent.query.filter(Agent.id == agent_id).first()
    if not agent:
        abort(HTTPStatus.NOT_FOUND, "Agent not found")

    book = Book.query.filter(Book.id == book_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, "Book not found")

    if book not in agent.books:
        abort(HTTPStatus.NOT_FOUND, "Book not found")

    agent.books.remove(book)
    db.session.commit()
    return {"status": "success", "message": "Book removed successfully"}
