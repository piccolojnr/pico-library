from flask_restx.reqparse import RequestParser
from flask_restx.inputs import email


auth_register_reqparser = RequestParser(bundle_errors=True)
auth_register_reqparser.add_argument(
    "password",
    type=str,
    required=True,
    location="form",
    help="Password required" "email",
)
auth_register_reqparser.add_argument(
    "email",
    type=email(),
    required=True,
    help="Email required" "first_name",
)
auth_register_reqparser.add_argument(
    "first_name",
    type=str,
    required=True,
    location="form",
    help="First name required" "last_name",
)
auth_register_reqparser.add_argument(
    "last_name",
    type=str,
    required=True,
    location="form",
    help="Last name required",
)
auth_register_reqparser.add_argument(
    "gender",
    type=str,
    choices=["male", "female", "other"],
    required=True,
    location="form",
    help="Gender required",
)
