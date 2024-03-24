from datetime import timezone
from app.v1 import db
from app.v1.utils.datetime_util import (
    get_local_utcoffset,
    localized_dt_string,
    make_tzaware,
    utc_now,
)
from sqlalchemy.ext.hybrid import hybrid_property


book_bookshelves_association = db.Table(
    "book_bookshelves",
    db.Column("book_id", db.Integer, db.ForeignKey("books.id", ondelete="CASCADE")),
    db.Column(
        "bookshelf_id", db.Integer, db.ForeignKey("bookshelves.id", ondelete="CASCADE")
    ),
    db.PrimaryKeyConstraint("book_id", "bookshelf_id"),
)


# user_bookshelves_association = db.Table(
#     "user_bookshelves",
#     db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE")),
#     db.Column(
#         "bookshelf_id", db.Integer, db.ForeignKey("bookshelves.id", ondelete="CASCADE")
#     ),
#     db.PrimaryKeyConstraint("user_id", "bookshelf_id"),
# )
class UserBookshelf(db.Model):
    """
    UserBookshelf model
    """

    __tablename__ = "user_bookshelves"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    bookshelf_id = db.Column(
        db.Integer, db.ForeignKey("bookshelves.id", ondelete="CASCADE")
    )
    score = db.Column(db.Integer, default=0)

    user = db.relationship("User", back_populates="user_bookshelves")
    bookshelf = db.relationship("Bookshelf", back_populates="user_bookshelves")

    def __repr__(self):
        return f"<UserBookshelf {self.user_id} {self.bookshelf_id}>"


class Bookshelf(db.Model):
    """
    Bookshelf model
    """

    __tablename__ = "bookshelves"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    score = db.Column(db.Integer, default=0)
    cover_image = db.Column(db.String)
    description = db.Column(db.String)
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    user = db.relationship("User", back_populates="bookshelves")

    books = db.relationship(
        "Book", secondary=book_bookshelves_association, back_populates="bookshelves"
    )
    user_bookshelves = db.relationship("UserBookshelf", back_populates="bookshelf")

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
        return f"<Bookshelf {self.name}>"
