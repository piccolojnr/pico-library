from app.v1.models import Subject, User, Book, Language
from app.v1 import db
from flask import jsonify, url_for
from flask_restx import marshal, abort
from http import HTTPStatus
from sqlalchemy import desc
from app.v1.utils.pagination import _pagination_nav_header_links, _pagination_nav_links
from .dto import subject_model, subject_pagination_model
from app.v1.api.books.dto import book_pagination_model


def process_create_subject(name):
    subject = Subject(name=name)
    db.session.add(subject)
    db.session.commit()
    subject_data = marshal(subject, subject_model)
    response = {
        "status": "success",
        "message": "Subject created successfully",
        "item": subject_data,
    }
    response_status_code = HTTPStatus.CREATED
    response_headers = {"Location": url_for("api.subjects", subject_id=subject.id)}

    return response, response_status_code, response_headers


def process_get_subject(subject_id):
    subject = Subject.query.filter_by(id=subject_id).first()
    if subject:
        return subject
    else:
        abort(HTTPStatus.NOT_FOUND, "Subject not found")


def process_get_subjects(page=1, per_page=10):
    subject = Subject.query.order_by(desc(Subject.score)).paginate(
        page=page,
        per_page=per_page,
    )

    pagination = dict(
        page=subject.page,
        items_per_page=subject.per_page,
        total_pages=subject.pages,
        total_items=subject.total,
        items=subject.items,
        has_next=subject.has_next,
        has_prev=subject.has_prev,
        next_num=subject.next_num,
        prev_num=subject.prev_num,
        links=[],
    )
    response_data = marshal(pagination, subject_pagination_model)
    response_data["links"] = _pagination_nav_links(pagination, "subjects")
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(pagination, "subjects")
    response.headers["Total-Count"] = subject.pages
    return response


def process_delete_subject(subject_id):
    subject = Subject.query.filter_by(id=subject_id).first()
    if subject:
        db.session.delete(subject)
        db.session.commit()
        return {"status": "success", "message": "Subject deleted successfully"}
    else:
        abort(HTTPStatus.NOT_FOUND, "Subject not found")


def process_update_subject(subject_id, name, score):
    subject = Subject.query.filter_by(id=subject_id).first()
    if subject:
        if name:
            subject.name = name

        if score:
            subject.score = score

        db.session.commit()
        return {"status": "success", "message": "Subject updated successfully"}
    else:
        abort(HTTPStatus.NOT_FOUND, "Subject not found")


def process_create_subject_book(subject_id, book_id):
    subject = Subject.query.filter_by(id=subject_id).first()
    if not subject:
        abort(HTTPStatus.NOT_FOUND, "Subject not found")

    book = Book.query.filter_by(id=book_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, "Book not found")

    subject.books.append(book)

    db.session.commit()
    return {"status": "success", "message": "Book added to subject successfully"}


def process_delete_subject_book(subject_id, user_public_id):
    subject = Subject.query.filter_by(id=subject_id).first()
    if not subject:
        abort(HTTPStatus.NOT_FOUND, "Subject not found")

    book = Book.query.filter_by(id=user_public_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, "Book not found")

    subject.books.remove(book)
    db.session.commit()

    return {
        "status": "success",
        "message": "Book removed from subject successfully",
    }


def process_get_subject_books(subject_id, page=1, per_page=10, lan="all"):
    subject = Subject.query.filter(Subject.id == subject_id).first()
    if not subject:
        abort(HTTPStatus.NOT_FOUND, "Subject not found")
    if lan == "all":
        books = Book.query.filter(Book.subjects.any(Subject.id == subject.id)).paginate(
            page=page,
            per_page=per_page,
        )
    else:
        books = Book.query.filter(
            Book.languages.any(Language.id == lan),
            Book.subjects.any(Subject.id == subject.id),
        ).paginate(
            page=page,
            per_page=per_page,
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
        pagination, "subject_books", subject_id=subject_id
    )
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(
        pagination, "subject_books", subject_id=subject_id
    )
    response.headers["Total-Count"] = books.pages
    return response


def process_create_subject_user(subject_id, user_public_id):
    subject = Subject.query.filter(Subject.id == subject_id).first()
    if not subject:
        abort(HTTPStatus.NOT_FOUND, "Subject not found")

    user = User.query.filter(User.public_id == user_public_id).first()
    if not user:
        abort(HTTPStatus.NOT_FOUND, "User not found")

    subject.users.append(user)

    db.session.commit()

    return {"status": "success", "message": "User added to subject successfully"}


def process_delete_subject_user(subject_id, user_public_id):
    subject = Subject.query.filter(Subject.id == subject_id).first()
    if not subject:
        abort(HTTPStatus.NOT_FOUND, "Subject not found")

    user = User.query.filter(User.public_id == user_public_id).first()
    if not user:
        abort(HTTPStatus.NOT_FOUND, "User not found")

    subject.users.remove(user)

    db.session.commit()
    return {
        "status": "success",
        "message": "User removed from subject successfully",
    }
