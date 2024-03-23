from flask_restx import Namespace, Resource
from flask_pyjwt import require_token
from app.v1.api.books.business import (
    process_search_books,
    process_get_recommedations,
    process_create_book,
    process_delete_book,
    process_get_book,
    process_get_books,
    process_update_book,
)
from http import HTTPStatus
from app.v1.api.books.dto import (
    book_model_short,
    book_pagination_model,
    recommendation_pagination_reqparse,
    agent_model,
    pagination_links_model,
    books_search_reqparse,
)

books_ns = Namespace(name="books", validate=True)
books_ns.models[book_model_short.name] = book_model_short
books_ns.models[book_pagination_model.name] = book_pagination_model
books_ns.models[agent_model.name] = agent_model
books_ns.models[pagination_links_model.name] = pagination_links_model


@books_ns.route("/", endpoint="books")
class BooksResource(Resource):
    @require_token()
    @books_ns.doc(security="Bearer")
    @books_ns.expect(books_search_reqparse)
    @books_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @books_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @books_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self):
        """
        Create book.
        """

        return process_create_book()

    @books_ns.expect(books_search_reqparse)
    def get(self):
        """
        Get books.
        """
        args = books_search_reqparse.parse_args()
        page = args.get("page")
        per_page = args.get("per_page")
        return process_search_books(page, per_page)

    @require_token()
    @books_ns.doc(security="Bearer")
    @books_ns.expect(books_search_reqparse)
    @books_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @books_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @books_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def put(self):
        pass

    @require_token()
    @books_ns.doc(security="Bearer")
    @books_ns.expect(books_search_reqparse)
    @books_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @books_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @books_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self):
        """
        Delete book.
        """
        return {"book": "book_id"}


@books_ns.route("/<book_id>", endpoint="book")
class BookResource(Resource):
    @require_token()
    @books_ns.doc(security="Bearer")
    @books_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @books_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @books_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def get(self, book_id):
        """
        Get book by id.
        """
        return {"book": book_id}

    # def post(self, book_id):
    #     """
    #     Create book.
    #     """
    #     return {"book": book_id}
    # def delete(self, book_id):
    #     """
    #     Delete book.
    #     """
    #     return {"book": book_id}
    # def put(self, book_id):
    #     """
    #     Update book.
    #     """
    #     return {"book": book_id}


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
        return process_search_books(
            query=query, criteria=criteria, page=page, per_page=per_page
        )


# @books_ns.route("/bookshelves", endpoint="bookshelves")
# class BookshelvesResource(Resource):
#     def get(self):
#         """
#         Get bookshelves.
#         """
#         return {"bookshelves": ["bookshelf1", "bookshelf2"]}

#     def post(self):
#         """
#         Create bookshelf.
#         """
#         return {"bookshelf": "bookshelf1"}


# @books_ns.route("/bookshelves/<bookshelf_id>", endpoint="bookshelf")
# class BookshelfResource(Resource):
#     def get(self, bookshelf_id):
#         """
#         Get bookshelf.
#         """
#         return {"bookshelf": bookshelf_id}

#     def delete(self, bookshelf_id):
#         """
#         Delete bookshelf.
#         """
#         return {"bookshelf": bookshelf_id}

#     def put(self, bookshelf_id):
#         """
#         Update bookshelf.
#         """
#         return {"bookshelf": bookshelf_id}


# @books_ns.route("/bookshelves/<bookshelf_id>/books", endpoint="bookshelf_books")
# class BookshelfBooksResource(Resource):
#     def get(self, bookshelf_id):
#         """
#         Get bookshelf's books.
#         """
#         return {"books": ["book1", "book2"]}


# @books_ns.route("/resources/<book_id>", endpoint="resources")
# class BookshelfBookResource(Resource):
#     def get(self, book_id):
#         """
#         Get  books resources.
#         """
#         return {"resources": ["resource1", "resource2"]}

#     def post(self, book_id):
#         """
#         Create  books resource.
#         """
#         return {"resource": "resource1"}


# @books_ns.route("/resources/<resource_id>", endpoint="resource")
# class BookshelfBookResource(Resource):
#     def get(self, resource_id):
#         """
#         Get  book resource.
#         """
#         return {"resource": resource_id}

#     def delete(self, resource_id):
#         """
#         Delete  book resource.
#         """
#         return {"resource": resource_id}

#     def put(self, resource_id):
#         """
#         Update  book resource.
#         """
#         return {"resource": resource_id}
