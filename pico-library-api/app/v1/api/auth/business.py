from http import HTTPStatus
import re
from flask import jsonify, current_app
from app.v1 import db
from flask_restx import abort, marshal
from app.v1.models import User, Profile, UserGender


def process_registeration_reguest(email, password, first_name, last_name, gender):
    if User.find_by_email(email):
        abort(HTTPStatus.BAD_REQUEST, "User already exists")

    new_user: User = User(email=email, password_hash=password)
    db.session.add(new_user)
    db.session.flush()

    new_profile: Profile = Profile(
        user_id=new_user.id,
        first_name=first_name,
        last_name=last_name,
        gender=UserGender._value2member_map_[gender],
    )
    db.session.add(new_profile)
    db.session.commit()

    auth = new_user.encode_auth_token()
    response = jsonify(
        status="success",
        message="User registered successfully",
        auth=auth,
        token_type="Bearer",
        expires_in=_get_token_expire_time(),
    )
    response.status_code = HTTPStatus.CREATED
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    return response


def process_login_request(email, password):
    if not email:
        abort(HTTPStatus.BAD_REQUEST, "Email is required")
    if not password:
        abort(HTTPStatus.BAD_REQUEST, "Password is required")

    user: User = User.find_by_email(email)
    if user and user.check_password(password):
        access_token = user.encode_auth_token()
        response = jsonify(
            status="success",
            message="Logged in successfully",
            access_token=access_token.decode(),
            token_type="Bearer",
            expires_in=_get_token_expire_time(),
        )
        response.status_code = HTTPStatus.OK
        response.headers["Cache-Control"] = "no-store"
        response.headers["Pragma"] = "no-cache"
        return response
    else:
        abort(HTTPStatus.UNAUTHORIZED, "Invalid credentials")
        return None


def process_logout_request(user):
    if user:
        user.logout()
        db.session.commit()
        return jsonify({"message": "Logged out successfully"})
    else:
        abort(HTTPStatus.UNAUTHORIZED, "User not found")
        return None


def process_refresh_token_request(user):
    if user:
        token = user.generate_auth_token(user.id)
        return jsonify

    return None


def _get_token_expire_time():
    token_age_h = current_app.config["TOKEN_EXPIRE_HOURS"]
    token_age_m = current_app.config["TOKEN_EXPIRE_MINUTES"]
    expires_in_seconds = token_age_h * 3600 + token_age_m * 60
    return expires_in_seconds
