from . import Base

from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, Text, DateTime,ForeignKey

from datetime import datetime

class Profile(Base):
    """
    Profile model
    """
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    full_name = Column(String)
    bio = Column(Text)
    occupation = Column(String)
    location = Column(String)
    profile_image = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='profile')
    
    def __repr__(self):
        return f"<Profile {self.id}>"
    
    def __init__(self, user_id, full_name, bio, occupation, location, profile_image):
        self.user_id = user_id
        self.full_name = full_name
        self.bio = bio
        self.occupation = occupation
        self.location = location
        self.profile_image = profile_image
    