from app.v1 import db, bcrypt, auth_manager
from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property
from uuid import uuid4
from datetime import timedelta, timezone, datetime
from app.v1.util.datetime_util import (
    get_local_utcoffset,
    localized_dt_string,
    make_tzaware,
    utc_now,
)
import enum

from app.v1.models.token_blacklist import BlacklistedToken


class User(db.Model):
    """
    User model
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)
    last_logged_in = db.Column(db.DateTime, default=utc_now)

    profile = db.relationship("Profile", back_populates="user")
    bookmarks = db.relationship("Bookmark", back_populates="user")
    comments = db.relationship("Comment", back_populates="user")
    comment_votes = db.relationship("CommentVote", back_populates="user")
    ratings = db.relationship("Rating", back_populates="user")

    public_id = db.Column(db.String, default=lambda: str(uuid4()))

    @hybrid_property
    def created_at_str(self):
        created_at_utc = make_tzaware(
            self.created_at, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(created_at_utc, use_tz=get_local_utcoffset())

    @hybrid_property
    def last_logged_in_str(self):
        last_logged_in_utc = make_tzaware(
            self.last_logged_in, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(last_logged_in_utc, use_tz=get_local_utcoffset())

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password):
        log_rounds = current_app.config.get("BCRYPT_LOG_ROUNDS")
        hash_bytes = bcrypt.generate_password_hash(password, log_rounds)
        self.password_hash = hash_bytes.decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:

            auth_token = auth_manager.auth_token(self.public_id, self.email)
            refresh_token = auth_manager.refresh_token(self.public_id)
            return dict(
                auth_token=auth_token.signed,
                refresh_token=refresh_token.signed,
            )

        except Exception as e:
            return e

    # @staticmethod
    # def decode_auth_token(auth_token):
    #     """
    #     Decodes the auth token
    #     :param auth_token:
    #     :return: integer|string
    #     """
    #     if isinstance(auth_token, bytes):
    #         auth_token = auth_token.decode(encoding="utf-8", errors="strict")
    #     if auth_token.startswith("Bearer "):
    #         auth_token = auth_token[7:]
    #     try:
    #         payload = jwt.decode(
    #             auth_token, current_app.config.get("SECRET_KEY"), algorithms=["HS256"]
    #         )
    #         if BlacklistedToken.check_blacklist(auth_token):
    #             return dict(
    #                 success=False, error="Token blacklisted. Please log in again."
    #             )
    #         return dict(
    #             success=True,
    #             public_id=payload["sub"],
    #             token=auth_token,
    #             expires_at=payload["exp"],
    #         )
    #     except jwt.ExpiredSignatureError:
    #         return dict(
    #             success=False,
    #             error="Signature expired. Please log in again.",
    #         )
    #     except jwt.InvalidTokenError:
    #         return dict(success=False, error="Invalid token. Please log in again.")
    #     except Exception as e:
    #         return dict(success=False, error=str(e))

    # @classmethod
    # def blacklist_token(cls, auth_token):
    #     """
    #     Adds a token to the blacklist
    #     :param token: string
    #     :return: Response
    #     """
    #     try:
    #         decoded_token = cls.decode_auth_token(auth_token)
    #         if decoded_token["success"]:
    #             token = decoded_token["token"]
    #             expires_at = decoded_token["expires_at"]
    #             blacklist_token = BlacklistedToken(token=token, expires_at=expires_at)
    #             db.session.add(blacklist_token)
    #             db.session.commit()
    #             return dict(success=True)
    #         else:
    #             return dict(success=False, error=decoded_token["error"])
    #     except Exception as e:
    #         return dict(success=False, error=str(e))

    # @staticmethod
    # def get_user_by_token(token):
    #     """
    #     Get user by token
    #     :param token:
    #     :return: User
    #     """
    #     decoded_token = User.decode_auth_token(token)
    #     if decoded_token["success"]:
    #         public_id = decoded_token["public_id"]
    #         return User.query.filter_by(public_id=public_id).first()
    #     return None

    def __repr__(self):
        return f"<User {self.email}>"
