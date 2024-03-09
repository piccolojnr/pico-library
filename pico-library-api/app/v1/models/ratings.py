from app.v1 import db

from datetime import timezone
from app.v1.util.datetime_util import (
    localized_dt_string,
    get_local_utcoffset,
    utc_now,
    make_tzaware,
)

from sqlalchemy.ext.hybrid import hybrid_property


class Rating(db.Model):
    """
    Rating model
    """

    __tablename__ = "ratings"
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    book_id = db.Column(
        db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"), primary_key=True
    )
    created_at = db.Column(db.DateTime, default=utc_now)
    rating = db.Column(db.Float)

    user = db.relationship("User", back_populates="ratings")
    book = db.relationship("Book", back_populates="ratings")

    @hybrid_property
    def created_at_str(self):
        created_at_utc = make_tzaware(self.created_at, timezone.utc, localize=False)
        return localized_dt_string(created_at_utc, get_local_utcoffset())

    def __repr__(self):
        return f"<Rating {self.user_id} {self.book_id} {self.rating}>"

    def __init__(self, user_id, book_id, rating):
        self.user_id = user_id
        self.book_id = book_id
        self.rating = rating
