from flask_restx import Namespace, Resource
from flask import request
from app.v1.api.user.dto import user_model, profile_model
from flask_pyjwt import require_token
from app.v1.api.user.business import (
    process_user_profile_request,
    process_get_recommedations,
    process_user_profile_update,
    process_user_comment_post,
)
from http import HTTPStatus
from app.v1.api.user.dto import (
    book_model,
    book_pagination_model,
    recommendation_pagination_reqparse,
    comment_reqparse,
    short_profile_model,
    agent_model,
    comment_model,
    pagination_links_model,
)

user_ns = Namespace(name="user", validate=True)
user_ns.models[user_model.name] = user_model
user_ns.models[profile_model.name] = profile_model
user_ns.models[book_model.name] = book_model
user_ns.models[book_pagination_model.name] = book_pagination_model
user_ns.models[short_profile_model.name] = short_profile_model
user_ns.models[agent_model.name] = agent_model
user_ns.models[comment_model.name] = comment_model
user_ns.models[pagination_links_model.name] = pagination_links_model


@user_ns.route("/profile", endpoint="user_profile")
class ProfileRoute(Resource):

    @require_token()
    @user_ns.doc(security="Bearer")
    @user_ns.response(int(HTTPStatus.OK), "Token is currently valid.", profile_model)
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @user_ns.marshal_with(profile_model)
    def get(self):
        return process_user_profile_request()

    @require_token()
    @user_ns.doc(security="Bearer")
    @user_ns.expect(profile_model)
    @user_ns.response(int(HTTPStatus.OK), "Token is currently valid.", profile_model)
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def put(self):
        profile_dict = request.get_json()
        return process_user_profile_update(profile_dict)


@user_ns.route("/recommendations", endpoint="user_recommendations")
class GetRecommendations(Resource):
    @require_token()
    @user_ns.doc(security="Bearer")
    @user_ns.expect(recommendation_pagination_reqparse)
    @user_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def get(self):
        """
        Get user's recommendations.
        """
        args = recommendation_pagination_reqparse.parse_args()
        page = args.get("page")
        per_page = args.get("per_page")
        return process_get_recommedations(page, per_page)


@user_ns.route("/comments", endpoint="user_comments")
class CommentResource(Resource):
    @require_token()
    @user_ns.doc(security="Bearer")
    @user_ns.expect(comment_model)
    @user_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self):
        # Submit a new comment
        data = request.get_json()
        content = data.get("content")
        book_id = data.get("book_id")
        parent_id = data.get("parent_id")
        type = data.get("type")
        return process_user_comment_post(content, book_id, parent_id, type)

    # @require_token()
    # def get(self, comment_id):
    #     # Retrieve details about a specific comment
    #     comment = Comment.query.get(comment_id)
    #     if comment:
    #         return comment.to_dict(), HTTPStatus.OK
    #     else:
    #         return {'message': 'Comment not found'}, HTTPStatus.NOT_FOUND

    # @require_token()
    # def put(self, comment_id):
    #     # Update a comment
    #     comment = Comment.query.get(comment_id)
    #     if comment and comment.user_id == request.user_id:
    #         data = request.get_json()
    #         content = data.get('content')

    #         comment.content = content
    #         db.session.commit()

    #         return {'message': 'Comment updated successfully'}, HTTPStatus.OK
    #     else:
    #         return {'message': 'Comment not found or unauthorized'}, HTTPStatus.NOT_FOUND

    # @require_token()
    # def delete(self, comment_id):
    #     # Delete a comment
    #     comment = Comment.query.get(comment_id)
    #     if comment and comment.user_id == request.user_id:
    #         db.session.delete(comment)
    #         db.session.commit()

    #         return {'message': 'Comment deleted successfully'}, HTTPStatus.OK
    #     else:
    #         return {'message': 'Comment not found or unauthorized'}, HTTPStatus.NOT_FOUND


@user_ns.route("/comments/<int:comment_id>", endpoint="user_comment")
class CommentResource(Resource):

    def get(self, comment_id):
        pass
