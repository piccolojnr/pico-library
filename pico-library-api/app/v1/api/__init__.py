"""API blueprint configuration."""

from flask import Blueprint
from flask_restx import Api


from app.v1.api.auth.endpoints import auth_ns
from app.v1.api.user.endpoints import user_ns
from app.v1.api.comments.endpoints import comments_ns
from app.v1.api.books.endpoints import books_ns
from app.v1.api.agents.endpoints import agents_ns
from app.v1.api.bookshelves.endpoints import bookshelves_ns
from app.v1.api.resources.endpoints import resources_ns
from app.v1.api.subjects.endpoints import subjects_ns
from app.v1.api.languages.endpoints import language_ns
from app.v1.api.publishers.endpoints import publisher_ns
from app.v1.api.bookmarks.endpoints import bookmark_ns

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    api_bp,
    version="1.0",
    title="Flask API with JWT-Based Authentication",
    description="Welcome to the Swagger UI documentation for the Widget API",
    doc="/ui",
    authorizations=authorizations,
)


api.add_namespace(auth_ns, path="/auth")
api.add_namespace(user_ns, path="/user")
api.add_namespace(comments_ns, path="/comments")
api.add_namespace(books_ns, path="/books")
api.add_namespace(agents_ns, path="/agents")
api.add_namespace(bookshelves_ns, path="/bookshelves")
api.add_namespace(resources_ns, path="/resources")
api.add_namespace(subjects_ns, path="/subjects")
api.add_namespace(language_ns, path="/languages")
api.add_namespace(publisher_ns, path="/publishers")
api.add_namespace(bookmark_ns, path="/bookmarks")
