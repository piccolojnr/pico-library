from sqlalchemy import  Column, Integer, String, DateTime,Enum
from sqlalchemy.orm import relationship
from . import Base

from datetime import datetime
import enum

class Gender(enum.Enum):
    """
    
    """
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    
class User(Base):
    """
    User model
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    gender = Column(Enum(Gender))
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_logged_in = Column(DateTime, default=datetime.utcnow)
    
    profile = relationship('Profile', back_populates='user')
    bookmarks = relationship('Bookmark', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    comment_votes = relationship('CommentVote', back_populates='user')
    ratings = relationship('Rating', back_populates='user')
    
    def __repr__(self):
        return f"<User {self.email}>"
    
    def __init__(self, email, gender, password_hash):
        self.email = email
        self.gender = gender
        self.password_hash = password_hash
    
    
    
    
