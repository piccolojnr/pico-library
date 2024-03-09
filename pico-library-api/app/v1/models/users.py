from app.v1 import db

from sqlalchemy.ext.hybrid import hybrid_property

from datetime import timezone
from app.v1.util.datetime_util import (
    get_local_utcoffset,
    localized_dt_string,
    make_tzaware,
    utc_now,
)
import enum


class UserGender(enum.Enum):
    """ """

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class User(db.Model):
    """
    User model
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    gender = db.Column(db.Enum(UserGender))
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)
    last_logged_in = db.Column(db.DateTime, default=utc_now)

    profile = db.relationship("Profile", back_populates="user")
    bookmarks = db.relationship("Bookmark", back_populates="user")
    comments = db.relationship("Comment", back_populates="user")
    comment_votes = db.relationship("CommentVote", back_populates="user")
    ratings = db.relationship("Rating", back_populates="user")

    @hybrid_property
    def created_at_str(self):
        created_at_utc = make_tzaware(
            self.created_at, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(created_at_utc, use_tz=get_local_utcoffset())

    @hybrid_property
    def last_logged_in(self):
        last_logged_in_utc = make_tzaware(
            self.last_logged_in, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(last_logged_in_utc, use_tz=get_local_utcoffset())

    def __repr__(self):
        return f"<User {self.email}>"

    def __init__(self, email, gender, password_hash):
        self.email = email
        self.gender = gender
        self.password_hash = password_hash
