from app.v1 import db

from sqlalchemy.ext.hybrid import hybrid_property
from .bookshelves import book_bookshelves_association
from .agents import book_agents_association
from .languages import book_languages_association
from .publishers import book_publishers_association
from .subjects import book_subjects_association
from .resources import book_resource_association
from datetime import timezone
from app.v1.util.datetime_util import (
    make_tzaware,
    utc_now,
    localized_dt_string,
    get_local_utcoffset,
)


class Book(db.Model):
    """
    Book model
    """

    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    format = db.Column(db.String)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    downloads = db.Column(db.Integer)
    license = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=utc_now)

    bookshelves = db.relationship(
        "Bookshelf", secondary=book_bookshelves_association, back_populates="books"
    )
    agents = db.relationship(
        "Agent", secondary=book_agents_association, back_populates="books"
    )
    languages = db.relationship(
        "Language", secondary=book_languages_association, back_populates="books"
    )
    publishers = db.relationship(
        "Publisher", secondary=book_publishers_association, back_populates="books"
    )
    subjects = db.relationship(
        "Subject", secondary=book_subjects_association, back_populates="books"
    )
    resources = db.relationship(
        "Resource", secondary=book_resource_association, back_populates="books"
    )
    ratings = db.relationship("Rating", back_populates="book")
    comments = db.relationship("Comment", back_populates="book")
    bookmarks = db.relationship("Bookmark", back_populates="book")

    @hybrid_property
    def average_rating(self):
        ratings = self.ratings
        if ratings:
            return sum(rating.rating for rating in ratings) / len(ratings)
        return 0

    @hybrid_property
    def reviews(self):
        from .comments import Comment, CommentType

        return self.comments.filter(Comment.type == CommentType.REVIEW)

    @hybrid_property
    def date_created_str(self):
        date_created_utc = make_tzaware(
            self.date_created, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(date_created_utc, use_tz=get_local_utcoffset())

    def __repr__(self):
        return f"<Book {self.title}>"
