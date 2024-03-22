from flask_pyjwt import current_token
from sqlalchemy import or_, and_
from app.v1.models import Book, Subject, Bookshelf, Agent, User
from flask_restx import abort, marshal
from http import HTTPStatus
from app.v1.services.recommendation_engine import generate_recommendations
from flask import jsonify, url_for
from app.v1.api.books.dto import (
    book_pagination_model,
)
from app.v1 import db


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
        books = Book.query.filter(Book.agents.name.ilike(f"%{query}%")).paginate(
            page=page, per_page=per_page
        )
    elif criteria == "subject":
        books = Book.query.filter(Book.subjects.name.ilike(f"%{query}%")).paginate(
            page=page, per_page=per_page
        )
    elif criteria == "shelf":
        books = Book.query.filter(Book.bookshelves.name.ilike(f"%{query}%")).paginate(
            page=page, per_page=per_page
        )

    pagination = dict(
        page=books.page,
        items_per_page=books.per_page,
        total_pages=books.pages,
        total_items=len(books.items),
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


def _pagination_nav_links(pagination, endpoint):
    nav_links = {}
    per_page = pagination["items_per_page"]
    this_page = pagination["page"]
    last_page = pagination["total_pages"]
    nav_links["self"] = url_for(f"api.{endpoint}", page=this_page, per_page=per_page)
    nav_links["first"] = url_for(f"api.{endpoint}", page=1, per_page=per_page)
    if pagination["has_prev"]:
        nav_links["prev"] = url_for(
            f"api.{endpoint}", page=this_page - 1, per_page=per_page
        )
    if pagination["has_next"]:
        nav_links["next"] = url_for(
            f"api.{endpoint}", page=this_page + 1, per_page=per_page
        )
    nav_links["last"] = url_for(f"api.{endpoint}", page=last_page, per_page=per_page)
    return nav_links


def _pagination_nav_header_links(pagination, endpoint):
    url_dict = _pagination_nav_links(pagination, endpoint)
    link_header = ""
    for rel, url in url_dict.items():
        link_header += f"<{url}>; rel={rel}"
    return link_header.strip().strip(",")
