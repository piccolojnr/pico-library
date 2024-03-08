from . import Base

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class Rating(Base):
    """
    Rating model
    """
    __tablename__ = 'ratings'
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete="CASCADE"), primary_key=True)
    rating = Column(Float)

    user = relationship('User', back_populates='ratings')
    book = relationship('Book', back_populates='ratings')
    
    def __repr__(self):
        return f'<Rating {self.user_id} {self.book_id} {self.rating}>'
    
    def __init__(self, user_id, book_id, rating):
        self.user_id = user_id
        self.book_id = book_id
        self.rating = rating