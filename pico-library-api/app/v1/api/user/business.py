from flask_pyjwt import current_token
from app.v1.models import User, Profile, Book, Comment, CommentType
from flask_restx import abort, marshal
from http import HTTPStatus
from app.v1.services.recommendation_engine import generate_recommendations
from flask import jsonify, url_for
from app.v1.api.user.dto import book_pagination_model, profile_model, comment_model
from app.v1 import db


def process_user_profile_request():
    public_id = current_token.sub
    user: User = User.find_by_public_id(public_id)
    if user:
        if user.profile:
            return user.profile
        else:
            user.profile = Profile(first_name="john", last_name="doe", user_id=user.id)
            user.profile.save_to_db()
            return user.profile
    else:
        abort(HTTPStatus.NOT_FOUND, "User not found")


def process_user_profile_update(profile_dict):
    public_id = current_token.sub
    user: User = User.find_by_public_id(public_id)
    if user:
        profile = Profile.find_by_user_id(user.id)
        if profile:
            for k, v in profile_dict.items():
                if v is not None:
                    if k not in ["created_at", "updated_at", "user"]:
                        if k == "gender":
                            v = v.upper()
                        setattr(profile, k, v)
            db.session.commit()
            message = f"'{public_id}' profile was successfully updated"
            profile_data = marshal(profile, profile_model)
            response_dict = dict(status="success", message=message, item=profile_data)
            return response_dict, HTTPStatus.OK
        else:
            abort(HTTPStatus.NOT_FOUND, "Profile not found")
    else:
        abort(HTTPStatus.NOT_FOUND, "User not found")


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
            pagination, "user_recommendations"
        )
        response = jsonify(response_data)
        response.headers["Link"] = _pagination_nav_header_links(
            pagination, "user_recommendations"
        )
        response.headers["Total-Count"] = total_pages
        return response_data
    else:
        abort(HTTPStatus.NOT_FOUND, "User not found")


def process_user_comment_post(content, book_id, parent_id, comment_type):
    public_id = current_token.sub
    user: User = User.find_by_public_id(public_id)

    if not content:
        abort(HTTPStatus.BAD_REQUEST, "Comment content is required")

    if not comment_type:
        abort(HTTPStatus.BAD_REQUEST, "Comment type is required")

    if type(comment_type) != str:
        abort(HTTPStatus.BAD_REQUEST, "Comment type must be a string")

    comment_type = comment_type.upper()

    if comment_type not in CommentType.__members__:
        abort(HTTPStatus.BAD_REQUEST, "Invalid comment type")

    comment_type = CommentType[comment_type]

    if not user:
        abort(HTTPStatus.NOT_FOUND, "User not found")

    if comment_type == CommentType.REPLY and not parent_id:
        abort(HTTPStatus.BAD_REQUEST, "Parent comment ID is required for replies")

    if book_id:
        book: Book = Book.get_by_id(book_id)
        if not book:
            abort(HTTPStatus.NOT_FOUND, "Book not found")

    if parent_id:
        parent_comment: Comment = Comment.get_by_id(parent_id)
        if not parent_comment:
            abort(HTTPStatus.NOT_FOUND, "Parent comment not found")

    comment = Comment(
        content=content,
        user_id=user.id,
        book_id=book_id if book_id else None,
        parent_id=parent_id if parent_id else None,
        type=comment_type,
    )
    db.session.add(comment)
    db.session.commit()

    comment_data = marshal(comment, comment_model)
    response = {
        "status": "success",
        "message": f"New comment was successfully added: {content}.",
        "item": comment_data,
    }
    response_status_code = HTTPStatus.CREATED
    response_headers = {"Location": url_for("api.user_comment", comment_id=comment.id)}

    return response, response_status_code, response_headers


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
