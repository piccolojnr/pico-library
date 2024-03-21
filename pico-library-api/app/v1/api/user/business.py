from flask_pyjwt import current_token
from app.v1.models import User, Profile
from flask_restx import abort, marshal
from http import HTTPStatus
from app.v1.services.recommendation_engine import generate_recommendations
from flask import jsonify, url_for
from app.v1.api.user.dto import book_pagination_model


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
