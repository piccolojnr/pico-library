from flask_restx import Namespace, Resource
from app.v1.api.user.dto import user_model, profile_model
from flask_pyjwt import require_token
from app.v1.api.user.business import process_user_profile_request
from http import HTTPStatus


user_ns = Namespace(name="user", validate=True)
user_ns.models[user_model.name] = user_model
user_ns.models[profile_model.name] = profile_model


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
