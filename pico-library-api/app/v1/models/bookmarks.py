from app.v1 import db

from datetime import datetime
import enum


class BookmarkStatus(enum.Enum):
    """
    Bookmark status
    """

    READ = "read"
    UNREAD = "unread"
    WANT_TO_READ = "want to read"
    CURRENTLY_READING = "currently reading"


class Bookmark(db.Model):
    """
    Bookmark model
    """

    __tablename__ = "bookmarks"
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    book_id = db.Column(
        db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"), primary_key=True
    )
    status = db.Column(db.Enum(BookmarkStatus), nullable=False, default=BookmarkStatus.UNREAD)
    last_read = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="bookmarks")
    book = db.relationship("Book", back_populates="bookmarks")

    def __repr__(self):
        return f"<Bookmark {self.book_id} {self.status}>"

    def __init__(self, user_id, book_id, status, last_read):
        self.user_id = user_id
        self.book_id = book_id
        self.status = status
        self.last_read = last_read
