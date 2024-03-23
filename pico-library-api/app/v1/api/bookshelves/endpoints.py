from flask_restx import Namespace, Resource
from flask_pyjwt import require_token

from http import HTTPStatus

bookshelves = Namespace(name="bookshelves", validate=True)


@bookshelves.route("/", endpoint="bookshelves")
class BookshelvesResource(Resource):
    def get(self):
        """
        Get bookshelves.
        """
        return {"bookshelves": ["bookshelf1", "bookshelf2"]}

    @require_token()
    @bookshelves.doc(security="Bearer")
    @bookshelves.response(int(HTTPStatus.OK), "Token is currently valid.")
    @bookshelves.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @bookshelves.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self):
        """
        Create bookshelf.
        """
        return {"bookshelf": "bookshelf1"}


@bookshelves.route("/<bookshelf_id>", endpoint="bookshelf")
class BookshelfResource(Resource):
    def get(self, bookshelf_id):
        """
        Get bookshelf.
        """
        return {"bookshelf": bookshelf_id}

    @require_token()
    @bookshelves.doc(security="Bearer")
    @bookshelves.response(int(HTTPStatus.OK), "Token is currently valid.")
    @bookshelves.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @bookshelves.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, bookshelf_id):
        """
        Delete bookshelf.
        """
        return {"bookshelf": bookshelf_id}

    @require_token()
    @bookshelves.doc(security="Bearer")
    @bookshelves.response(int(HTTPStatus.OK), "Token is currently valid.")
    @bookshelves.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @bookshelves.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def put(self, bookshelf_id):
        """
        Update bookshelf.
        """
        return {"bookshelf": bookshelf_id}


@bookshelves.route("/<bookshelf_id>/books", endpoint="bookshelf_books")
class BookshelfBooksResource(Resource):
    def get(self, bookshelf_id):
        """
        Get bookshelf's books.
        """
        return {"books": ["book1", "book2"]}


@bookshelves.route("<bookshelf_id>/books/<book_id>", endpoint="bookshelf_book")
class BookshelfBookResource(Resource):
    @require_token()
    @bookshelves.doc(security="Bearer")
    @bookshelves.response(int(HTTPStatus.OK), "Token is currently valid.")
    @bookshelves.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @bookshelves.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, bookshelf_id, book_id):
        """
        Delete bookshelf's book.
        """
        return {"book": book_id}

    @require_token()
    @bookshelves.doc(security="Bearer")
    @bookshelves.response(int(HTTPStatus.OK), "Token is currently valid.")
    @bookshelves.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @bookshelves.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self, bookshelf_id, book_id):
        """
        Add book to bookshelf.
        """
        return {"book": book_id}
