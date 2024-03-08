from . import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

class Status(enum.Enum):
    """
    Bookmark status
    """
    READ = 'read'
    UNREAD = 'unread'
    WANT_TO_READ = 'want to read'
    CURRENTLY_READING = 'currently reading'

class Bookmark(Base):
    """
    Bookmark model
    """
    __tablename__ = 'bookmarks'
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete="CASCADE"), primary_key=True)
    status = Column(Enum(Status), nullable=False, default=Status.UNREAD)
    last_read = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='bookmarks')
    book = relationship('Book', back_populates='bookmarks')
    
    def __repr__(self):
        return f'<Bookmark {self.book_id} {self.status}>'
    
    def __init__(self, user_id, book_id, status, last_read):
        self.user_id = user_id
        self.book_id = book_id
        self.status = status
        self.last_read = last_read