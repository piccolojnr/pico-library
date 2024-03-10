from flask_restx import Namespace, Resource
from app.v1.api.auth.business import (
    process_login_request,
    process_registeration_reguest,
    process_refresh_token_request,
    process_logout_request,
)
from flask_pyjwt import require_token, current_token
from app.v1.api.auth.dto import auth_register_reqparser, auth_login_reqparser

auth_ns = Namespace(name="auth", validate=True)


@auth_ns.route("/register", endpoint="auth_register")
class RegisterUser(Resource):
    @auth_ns.expect(auth_register_reqparser)
    @auth_ns.response(201, "User created successfully")
    @auth_ns.response(400, "Bad request")
    @auth_ns.response(409, "User already exists")
    @auth_ns.response(500, "Internal server error")
    @auth_ns.doc(description="Register a new user")
    @auth_ns.doc(security="apikey")
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
    @auth_ns.response(200, "User logged in successfully")
    @auth_ns.response(400, "Bad request")
    @auth_ns.response(401, "Unauthorized")
    @auth_ns.response(500, "Internal server error")
    @auth_ns.doc(description="Login a user")
    @auth_ns.doc(security="apikey")
    def post(self):
        request_data = auth_login_reqparser.parse_args()
        email = request_data["email"]
        password = request_data["password"]
        return process_login_request(email, password)


@auth_ns.route("/refresh", endpoint="auth_refresh")
class RefreshToken(Resource):
    @require_token("refresh")
    def post(self):
        if current_token:
            return process_refresh_token_request(current_token)
        else:
            return {"message": "Invalid token"}, 401


@auth_ns.route("/logout", endpoint="auth_logout")
class LogoutUser(Resource):
    @require_token()
    def post(self):
        if current_token:
            return process_logout_request(current_token)
        else:
            return {"message": "Invalid token"}, 401


@auth_ns.route("/protected_route", endpoint="protected_route")
class ProtectedRoute(Resource):
    @require_token()
    def get(self):
        return {"message": "You've reached the protected route!"}, 200
