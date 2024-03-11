import enum
from app.v1 import db

from datetime import datetime, timezone

from sqlalchemy.ext.hybrid import hybrid_property

from app.v1.util.datetime_util import (
    get_local_utcoffset,
    localized_dt_string,
    make_tzaware,
)


class UserGender(enum.Enum):
    """ """

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Profile(db.Model):
    """
    Profile model
    """

    __tablename__ = "profile"
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    gender = db.Column(db.Enum(UserGender))
    bio = db.Column(db.Text)
    location = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user = db.relationship("User", back_populates="profile")

    @hybrid_property
    def gender_str(self):
        return self.gender.value if self.gender else None

    @hybrid_property
    def created_at_str(self):
        created_at_utc = make_tzaware(
            self.created_at, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(created_at_utc, use_tz=get_local_utcoffset())

    @hybrid_property
    def updated_at_str(self):
        updated_at_utc = make_tzaware(
            self.updated_at, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(updated_at_utc, use_tz=get_local_utcoffset())

    def __repr__(self):
        return f"<Profile {self.user_id} {self.first_name} {self.last_name}>"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
