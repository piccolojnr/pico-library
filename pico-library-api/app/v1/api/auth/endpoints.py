from flask_restx import Namespace, Resource
from app.v1.api.auth.business import (
    process_login_request,
    process_registeration_reguest,
)

from app.v1.api.auth.dto import auth_register_reqparser

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


@auth_ns.route("/login")
class Login(Resource):
    def post(self):
        return process_login_request()
