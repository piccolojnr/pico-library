"""API blueprint configuration."""

from flask import Blueprint
from flask_restx import Api


from app.v1.api.auth.endpoints import auth_ns
# from app.api.items.endpoints import items_ns
# from app.api.player.endpoints import player_ns

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
# api.add_namespace(items_ns, "/items")
# api.add_namespace(player_ns, "/player")