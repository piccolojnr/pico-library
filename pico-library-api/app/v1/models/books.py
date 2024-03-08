from app.v1 import db

from sqlalchemy.ext.hybrid import hybrid_property
from .bookshelves import book_bookshelves_association
from .agents import book_agents_association
from .languages import book_languages_association
from .publishers import book_publishers_association
from .subjects import book_subjects_association
from .resources import book_resource_association
from datetime import datetime


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
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

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
    ratings = db.relationship("Rating", secondary="ratings")
    comments = db.relationship("Comment", secondary="comments")
    bookmarks = db.relationship("Bookmark", secondary="bookmarks")

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

    def __repr__(self):
        return f"<Book {self.title}>"

    def __init__(self, id, format, title, description, downloads, license):
        self.id = id
        self.format = format
        self.title = title
        self.description = description
        self.downloads = downloads
        self.license = license
