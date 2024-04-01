from flask import Blueprint

web_bp = Blueprint("site", __name__, url_prefix="/")

from .endpoints import (
    login,
    register,
    admin_panel,
    book_details,
    book_listings,
    bookmarks_management,
    bookshelves_management,
    index,
    recommendations,
    user_profile,
    agent_details,
    internal_server_error,
    page_not_found,
    bookshelf_listings,
)


__all__ = [
    "login",
    "register",
    "page_not_found",
    "internal_server_error",
    "admin_panel",
    "book_details",
    "book_listings",
    "bookmarks_management",
    "bookshelves_management",
    "index",
    "recommendations",
    "user_profile",
    "agent_details",
    "bookshelf_listings",
]
