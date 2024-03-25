from flask_restx import Namespace, Resource
from flask import request
from flask_pyjwt import require_token
from app.v1.api.comments.business import (
    process_user_comment_post,
    process_retrieve_user_comments,
    process_delete_comment,
    process_update_comment,
    process_retrieve_specific_comment,
)
from http import HTTPStatus
from app.v1.api.comments.dto import (
    comment_model,
    retrieve_comments_reqparse,
    comment_pagination_model,
    pagination_links_model,
)

comments_ns = Namespace(name="comments", validate=True)
comments_ns.models[comment_model.name] = comment_model
comments_ns.models[comment_pagination_model.name] = comment_pagination_model
comments_ns.models[pagination_links_model.name] = pagination_links_model


@comments_ns.route("/", endpoint="comments")
class CommentsResource(Resource):
    @require_token()
    @comments_ns.doc(security="Bearer")
    @comments_ns.expect(comment_model)
    @comments_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @comments_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @comments_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self):
        # Submit a new comment
        data = request.get_json()
        content = data.get("content")
        book_id = data.get("book_id")
        parent_id = data.get("parent_id")
        type = data.get("type")
        return process_user_comment_post(content, book_id, parent_id, type)

    @comments_ns.expect(retrieve_comments_reqparse)
    def get(self):
        # Retrieve comments for a book
        args = retrieve_comments_reqparse.parse_args()
        public_id = args.get("public_id")
        book_id = args.get("book_id")
        parent_id = args.get("parent_id")
        comment_type = args.get("type")
        page = args.get("page")
        per_page = args.get("per_page")
        return process_retrieve_user_comments(
            public_id=public_id,
            book_id=book_id,
            parent_id=parent_id,
            comment_type=comment_type,
            page=page,
            per_page=per_page,
        )


@comments_ns.route("/<int:comment_id>", endpoint="comment")
class CommentResource(Resource):

    @comments_ns.marshal_with(comment_model)
    def get(self, comment_id):
        return process_retrieve_specific_comment(comment_id)

    def put(self, comment_id):
        return process_update_comment(comment_id)

    def delete(self, comment_id):
        return process_delete_comment(comment_id)
