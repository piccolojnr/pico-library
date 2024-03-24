from flask_pyjwt import current_token
from app.v1.utils.pagination import _pagination_nav_header_links, _pagination_nav_links
from app.v1.models import Book, User, Agent, Subject, Bookshelf
from flask_restx import abort, marshal
from http import HTTPStatus
from app.v1.services.recommendation_engine import generate_recommendations
from flask import jsonify, url_for
from app.v1.api.books.dto import book_pagination_model, book_model
from app.v1 import db
from sqlalchemy import or_
from app.v1.utils.functions import (
    add_agents,
    add_bookshelves,
    add_languages,
    add_resources,
    add_subjects,
    add_publishers,
)


def process_create_book(data):
    agents = add_agents(data["agents"]) if "agents" in data else []
    bookshelves = add_bookshelves(data["bookshelves"]) if "bookshelves" in data else []
    languages = add_languages(data["languages"]) if "languages" in data else []
    resources = add_resources(data["resources"]) if "resources" in data else []
    subjects = add_subjects(data["subjects"]) if "subjects" in data else []
    publishers = add_publishers(data["publishers"]) if "publishers" in data else []
    data["agents"] = agents
    data["bookshelves"] = bookshelves
    data["languages"] = languages
    data["resources"] = resources
    data["subjects"] = subjects
    data["publishers"] = publishers
    book = Book(**data)
    book_data = marshal(book, book_model)
    response = {
        "status": "success",
        "message": "Book created successfully",
        "item": book_data,
    }
    response_status_code = HTTPStatus.CREATED
    response_headers = {"Location": url_for("api.book", book_id=book.id)}

    return response, response_status_code, response_headers


def process_delete_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return {"status": "success", "message": "Book deleted successfully"}
    else:
        abort(HTTPStatus.NOT_FOUND, "Book not found")


def process_update_book(book_id, data):
    book = Book.query.filter(Book.id == book_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, "Book not found")

    for key, value in data.items():
        if value is not None and key not in ["id", "created_at", "updated_at"]:
            setattr(book, key, value)

    db.session.commit()
    return {
        "status": "success",
        "message": f"Book with ID {book_id} was successfully updated.",
    }


def process_get_books(page, per_page):
    books = Book.query.paginate(page=page, per_page=per_page)

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
    response_data["links"] = _pagination_nav_links(pagination, "books")
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(pagination, "books")
    response.headers["Total-Count"] = books.pages
    return response


def process_get_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book:
        return book
    else:
        abort(HTTPStatus.NOT_FOUND, "Book not found")


def process_get_recommedations(page, per_page):
    public_id = current_token.sub
    user: User = User.find_by_public_id(public_id)
    if user:
        recommendations, has_next, has_prev, total_pages = generate_recommendations(
            user, page, per_page
        )
        pagination = dict(
            page=page,
            items_per_page=per_page,
            total_pages=total_pages,
            total_items=len(recommendations),
            items=recommendations,
            has_next=has_next,
            has_prev=has_prev,
            next_num=page + 1 if has_next else None,
            prev_num=page - 1 if has_prev else None,
            links=[],
        )
        response_data = marshal(pagination, book_pagination_model)
        response_data["links"] = _pagination_nav_links(
            pagination, "book_recommendations"
        )
        response = jsonify(response_data)
        response.headers["Link"] = _pagination_nav_header_links(
            pagination, "book_recommendations"
        )
        response.headers["Total-Count"] = total_pages
        return response_data
    else:
        abort(HTTPStatus.NOT_FOUND, "User not found")


def process_search_books(query="", criteria="title", page=1, per_page=10):
    query = query.lower()

    if criteria == "title":
        books = Book.query.filter(Book.title.ilike(f"%{query}%")).paginate(
            page=page, per_page=per_page
        )
    elif criteria == "author":
        books = Book.query.filter(
            or_(
                Book.agents.any(Agent.name.ilike(f"%{query}%")),
                Book.agents.any(Agent.alias.ilike(f"%{query}%")),
            )
        ).paginate(page=page, per_page=per_page)
    elif criteria == "subject":
        books = Book.query.filter(
            Book.subjects.any(Subject.name.ilike(f"%{query}%"))
        ).paginate(page=page, per_page=per_page)
    elif criteria == "shelf":
        books = Book.query.filter(
            Book.bookshelves.any(Bookshelf.name.ilike(f"%{query}%"))
        ).paginate(page=page, per_page=per_page)

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
    response_data["links"] = _pagination_nav_links(pagination, "book_search")
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(pagination, "book_search")
    response.headers["Total-Count"] = books.pages
    return response
