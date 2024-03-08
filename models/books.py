from . import Base
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from .bookshelves import book_bookshelves_association
from .agents import book_agents_association
from .languages import book_languages_association
from .publishers import book_publishers_association
from .subjects import book_subjects_association
from .resources import book_resource_association
from datetime import datetime

class Book(Base):
    """
    Book model
    """
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    format = Column(String)
    title = Column(String)
    description = Column(Text)
    downloads = Column(Integer)
    license = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)

    bookshelves = relationship(
        "Bookshelf", secondary=book_bookshelves_association, back_populates="books"
    )
    agents = relationship(
        "Agent", secondary=book_agents_association, back_populates="books"
    )
    languages = relationship(
        "Language", secondary=book_languages_association, back_populates="books"
    )
    publishers = relationship(
        "Publisher", secondary=book_publishers_association, back_populates="books"
    )
    subjects = relationship("Subject", secondary=book_subjects_association, back_populates="books")
    resources = relationship("Resource", secondary=book_resource_association, back_populates="books")
    ratings = relationship("Rating", secondary="ratings")
    comments = relationship("Comment", secondary="comments")
    bookmarks = relationship("Bookmark", secondary="bookmarks")
    
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
