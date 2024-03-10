import enum
from app.v1 import db

from datetime import datetime


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

    def __repr__(self):
        return f"<Profile {self.id}>"
