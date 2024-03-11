from flask_pyjwt import current_token
from app.v1.models import User, Profile
from flask_restx import abort
from http import HTTPStatus


def process_user_profile_request():
    public_id = current_token.sub
    user: User = User.find_by_public_id(public_id)
    if user:
        if user.profile:
            return user.profile
        else:
            user.profile = Profile(first_name="john", last_name="doe", user_id=user.id)
            user.profile.save_to_db()
            return user.profile
    else:
        abort(HTTPStatus.NOT_FOUND, "User not found")
