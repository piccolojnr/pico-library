"""API blueprint configuration."""

from flask import Blueprint
from flask_restx import Api


from app.v1.api.auth.endpoints import auth_ns
from app.v1.api.user.endpoints import user_ns
from app.v1.api.comments.endpoints import comments_ns
from app.v1.api.books.endpoints import books_ns
from app.v1.api.agents.endpoints import agents_ns

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
