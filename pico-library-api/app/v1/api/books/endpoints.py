from flask_restx import Namespace, Resource
from flask_pyjwt import require_token
from app.v1.api.books.business import process_search_books, process_get_recommedations
from http import HTTPStatus
from app.v1.api.books.dto import (
    book_model,
    book_pagination_model,
    recommendation_pagination_reqparse,
    agent_model,
    pagination_links_model,
    books_search_reqparse,
)

books_ns = Namespace(name="books", validate=True)
books_ns.models[book_model.name] = book_model
books_ns.models[book_pagination_model.name] = book_pagination_model
books_ns.models[agent_model.name] = agent_model
books_ns.models[pagination_links_model.name] = pagination_links_model


@books_ns.route("/recommendations", endpoint="book_recommendations")
class GetRecommendations(Resource):
    @require_token()
    @books_ns.doc(security="Bearer")
    @books_ns.expect(recommendation_pagination_reqparse)
    @books_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @books_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @books_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def get(self):
        """
        Get user's recommendations.
        """
        args = recommendation_pagination_reqparse.parse_args()
        page = args.get("page")
        per_page = args.get("per_page")
        return process_get_recommedations(page, per_page)


@books_ns.route("/search", endpoint="book_search")
class BookSearchResource(Resource):
    @books_ns.expect(books_search_reqparse)
    def get(self):
        """
        Search for books.
        """
        args = books_search_reqparse.parse_args()
        query = args.get("q")
        criteria = args.get("criteria")
        page = args.get("page")
        per_page = args.get("per_page")
        return process_search_books(query=query, page=page, per_page=per_page)
