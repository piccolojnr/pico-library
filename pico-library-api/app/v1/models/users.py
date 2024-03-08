from app.v1 import db

from datetime import datetime
import enum

class UserGender(enum.Enum):
    """
    
    """
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    
class User(db.Model):
    """
    User model
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    gender = db.Column(db.Enum(UserGender))
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_logged_in = db.Column(db.DateTime, default=datetime.utcnow)
    
    profile = db.relationship('Profile', back_populates='user')
    bookmarks = db.relationship('Bookmark', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')
    comment_votes = db.relationship('CommentVote', back_populates='user')
    ratings = db.relationship('Rating', back_populates='user')
    
    def __repr__(self):
        return f"<User {self.email}>"
    
    def __init__(self, email, gender, password_hash):
        self.email = email
        self.gender = gender
        self.password_hash = password_hash
    
    
    
    
