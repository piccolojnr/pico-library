from flask_restx import Namespace, Resource
from flask_pyjwt import require_token
from http import HTTPStatus

resources_ns = Namespace(name="resources", validate=True)


@resources_ns.route("/<book_id>", endpoint="resources")
class ResourcesResource(Resource):
    def get(self, book_id):
        """
        Get  books resources.
        """
        return {"resources": ["resource1", "resource2"]}

    @require_token()
    @resources_ns.doc(security="Bearer")
    @resources_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @resources_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @resources_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self, book_id):
        """
        Create  books resource.
        """
        return {"resource": "resource1"}


@resources_ns.route("/<book_id>/books/<resource_id>", endpoint="resourc_book")
class ResourceResource(Resource):
    def get(self, book_id, resource_id):
        """
        Get  book resource.
        """
        return {"resource": resource_id}

    @require_token()
    @resources_ns.doc(security="Bearer")
    @resources_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @resources_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @resources_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, resource_id):
        """
        Delete  book resource.
        """
        return {"resource": resource_id}

    @require_token()
    @resources_ns.doc(security="Bearer")
    @resources_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @resources_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @resources_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def put(self, book_id, resource_id):
        """
        Update  book resource.
        """
        return {"resource": resource_id}
