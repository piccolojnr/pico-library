from flask_restx import Namespace, Resource
from flask_pyjwt import require_token
from http import HTTPStatus

subjects_ns = Namespace(name="subjects", validate=True)


@subjects_ns.route("/subjects", endpoint="subjects")
class SubjectsResource(Resource):
    def get(self):
        """
        Get subjects.
        """
        return {"subjects": ["subject1", "subject2"]}

    @require_token()
    @subjects_ns.doc(security="Bearer")
    @subjects_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @subjects_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @subjects_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self):
        """
        Create subject.
        """
        return {"subject": "subject1"}


@subjects_ns.route("/subjects/<subject_id>", endpoint="subject")
class SubjectResource(Resource):
    def get(self, subject_id):
        """
        Get subject.
        """
        return {"subject": subject_id}

    @require_token()
    @subjects_ns.doc(security="Bearer")
    @subjects_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @subjects_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @subjects_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, subject_id):
        """
        Delete subject.
        """
        return {"subject": subject_id}

    @require_token()
    @subjects_ns.doc(security="Bearer")
    @subjects_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @subjects_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @subjects_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def put(self, subject_id):
        """
        Update subject.
        """
        return {"subject": subject_id}


@subjects_ns.route("/subjects/<subject_id>/books", endpoint="subject_books")
class SubjectBooksResource(Resource):
    def get(self, subject_id):
        """
        Get subject's books.
        """
        return {"books": ["book1", "book2"]}


@subjects_ns.route("/subjects/<subject_id>/books/<book_id>", endpoint="subject_book")
class SubjectBookResource(Resource):
    @require_token()
    @subjects_ns.doc(security="Bearer")
    @subjects_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @subjects_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @subjects_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, subject_id, book_id):
        """
        Delete subject's book.
        """
        return {"book": book_id}

    @require_token()
    @subjects_ns.doc(security="Bearer")
    @subjects_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @subjects_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @subjects_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self, subject_id, book_id):
        """
        Create subject's book.
        """
        return {"book": "book1"}
