from flask_restx import Namespace, Resource
from app.v1.api.auth.business import (
    process_login_request,
    process_registeration_reguest,
    process_refresh_token_request,
    process_logout_request,
    process_change_password,
    process_confirm_email,
    _send_confirmation_email,
)
from flask_pyjwt import require_token, current_token
from http import HTTPStatus
from app.v1.api.auth.dto import (
    auth_register_reqparser,
    auth_login_reqparser,
    auth_change_password_reqparser,
)

auth_ns = Namespace(name="auth", validate=True)


@auth_ns.route("/register", endpoint="auth_register")
class RegisterUser(Resource):
    @auth_ns.expect(auth_register_reqparser)
    @auth_ns.response(HTTPStatus.CREATED, "User created successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.CONFLICT, "User already exists")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @auth_ns.response(HTTPStatus.NOT_FOUND, "Not found")
    @auth_ns.doc(description="Register a new user")
    @auth_ns.doc(security="Bearer")
    def post(self):
        request_data = auth_register_reqparser.parse_args()
        email = request_data["email"]
        password = request_data["password"]
        first_name = request_data["first_name"]
        last_name = request_data["last_name"]
        gender = request_data["gender"]
        return process_registeration_reguest(
            email, password, first_name, last_name, gender
        )


@auth_ns.route("/login", endpoint="auth_login")
class LoginUser(Resource):
    @auth_ns.expect(auth_login_reqparser)
    @auth_ns.response(HTTPStatus.OK, "User logged in successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.CONFLICT, "User already exists")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @auth_ns.response(HTTPStatus.NOT_FOUND, "Not found")
    @auth_ns.doc(description="Login a user")
    @auth_ns.doc(security="Bearer")
    def post(self):
        request_data = auth_login_reqparser.parse_args()
        email = request_data["email"]
        password = request_data["password"]
        return process_login_request(email, password)


@auth_ns.route("/refresh", endpoint="auth_refresh")
class RefreshToken(Resource):
    @require_token("refresh")
    @auth_ns.response(HTTPStatus.OK, "Token refreshed successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.CONFLICT, "User already exists")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @auth_ns.response(HTTPStatus.NOT_FOUND, "Not found")
    @auth_ns.doc(description="Refresh a token")
    @auth_ns.doc(security="Bearer")
    def post(self):
        return process_refresh_token_request()


@auth_ns.route("/logout", endpoint="auth_logout")
class LogoutUser(Resource):
    @require_token()
    @auth_ns.response(HTTPStatus.OK, "User logged out successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.CONFLICT, "User already exists")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @auth_ns.response(HTTPStatus.NOT_FOUND, "Not found")
    @auth_ns.doc(description="Logout a user")
    @auth_ns.doc(security="Bearer")
    def post(self):
        return process_logout_request()


@auth_ns.route("/change_password", endpoint="auth_change_password")
class ChangePassword(Resource):
    @require_token()
    @auth_ns.expect(auth_change_password_reqparser)
    @auth_ns.response(HTTPStatus.OK, "Password changed successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.CONFLICT, "User already exists")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @auth_ns.response(HTTPStatus.NOT_FOUND, "Not found")
    @auth_ns.doc(description="Change a user's password")
    @auth_ns.doc(security="Bearer")
    def post(self):
        request_data = auth_change_password_reqparser.parse_args()
        old_password = request_data["old_password"]
        new_password = request_data["new_password"]
        return process_change_password(old_password, new_password)


@auth_ns.route("/protected_route", endpoint="protected_route")
class ProtectedRoute(Resource):
    @require_token()
    def get(self):
        return {"message": "You've reached the protected route!"}, 200


@auth_ns.route("/admin_protected_route", endpoint="admin_protected_route")
class ProtectedRoute(Resource):
    @require_token(scope={"is_admin": True})
    def get(self):
        return {"message": "You've reached the admin protected route!"}, 200


@auth_ns.route("/confirm_email/<token>", endpoint="confirm_email")
class ConfirmEmail(Resource):
    @auth_ns.expect(auth_login_reqparser)
    def post(self, token):
        request_data = auth_login_reqparser.parse_args()
        email = request_data["email"]
        password = request_data["password"]
        return process_confirm_email(token, email, password)


@auth_ns.route("/send_confirmation_email", endpoint="send_confirmation_email")
class SendConfirmationEmail(Resource):
    @require_token()
    def post(self):
        from app.v1.models import User
        from flask_restx import abort
        from flask import jsonify

        public_id = current_token.sub

        user = User.find_by_public_id(public_id)
        if user is None:
            abort(404, "User not found")
        else:
            _send_confirmation_email(user.email, user.public_id)
            return jsonify({"message": "Email sent successfully"})
