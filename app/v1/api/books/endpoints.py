from flask_restx import Namespace, Resource
from flask_pyjwt import require_token
from flask import request
from app.v1.api.books.business import (
    process_search_books,
    process_get_recommedations,
    process_create_book,
    process_delete_book,
    process_get_book,
    process_get_books,
    process_update_book,
    process_get_popular_books,
    process_get_book_by_title,
)
from http import HTTPStatus
from app.v1.api.books.dto import (
    book_model_short,
    book_model,
    book_pagination_model,
    pagination_links_model,
    pagination_reqparse,
    create_book_model,
    update_book_model,
)

books_ns = Namespace(name="books", validate=True)
books_ns.models[book_model.name] = book_model
books_ns.models[book_model_short.name] = book_model_short
books_ns.models[book_pagination_model.name] = book_pagination_model
books_ns.models[pagination_links_model.name] = pagination_links_model
books_ns.models[create_book_model.name] = create_book_model
books_ns.models[update_book_model.name] = update_book_model


@books_ns.route("/", endpoint="books")
class BooksResource(Resource):
    @require_token(scope={"is_admin": True})
    @books_ns.doc(security="Bearer")
    @books_ns.expect(create_book_model)
    @books_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @books_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @books_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self):
        """
        Create book.
        """
        data = request.get_json()
        return process_create_book(data)

    @books_ns.expect(pagination_reqparse)
    def get(self):
        """
        Get books.
        """
        args = pagination_reqparse.parse_args()
        page = args.get("page")
        per_page = args.get("per_page")
        lan = args.get("lan")
        return process_get_books(page, per_page, lan)


@books_ns.route("/<book_id>", endpoint="book")
class BookResource(Resource):

    @books_ns.marshal_with(book_model)
    def get(self, book_id):
        """
        Get book by id.
        """
        return process_get_book(book_id)

    @require_token(scope={"is_admin": True})
    @books_ns.doc(security="Bearer")
    @books_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @books_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @books_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, book_id):
        """
        Delete book.
        """
        return process_delete_book(book_id)

    @require_token(scope={"is_admin": True})
    @books_ns.doc(security="Bearer")
    @books_ns.expect(update_book_model)
    @books_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @books_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @books_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def put(self, book_id):
        """
        Update book.
        """
        data = request.get_json()

        return process_update_book(book_id, data)


@books_ns.route("/recommendations", endpoint="book_recommendations")
class GetRecommendations(Resource):
    @require_token()
    @books_ns.doc(security="Bearer")
    @books_ns.expect(pagination_reqparse)
    @books_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @books_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @books_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def get(self):
        """
        Get user's recommendations.
        """
        args = pagination_reqparse.parse_args()
        page = args.get("page")
        per_page = args.get("per_page")
        lan = args.get("lan")
        return process_get_recommedations(page, per_page, lan)


@books_ns.route("/popular", endpoint="popular_books")
class GetRecommendations(Resource):
    @books_ns.expect(pagination_reqparse)
    def get(self):
        """
        Get popular books
        """
        args = pagination_reqparse.parse_args()
        page = args.get("page")
        per_page = args.get("per_page")
        lan = args.get("lan")
        return process_get_popular_books(page, per_page, lan)


@books_ns.route("/search", endpoint="book_search")
class BookSearchResource(Resource):
    @books_ns.expect(pagination_reqparse)
    def get(self):
        """
        Search for books.
        """
        args = pagination_reqparse.parse_args()
        query = args.get("q")
        criteria = args.get("criteria")
        page = args.get("page")
        per_page = args.get("per_page")
        lan = args.get("lan")
        return process_search_books(
            query=query, criteria=criteria, page=page, per_page=per_page, lan=lan
        )
