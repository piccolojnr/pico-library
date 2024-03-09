from app.v1 import db

from datetime import datetime

class Profile(db.Model):
    """
    Profile model
    """
    __tablename__ = 'profile'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    full_name = db.Column(db.String)
    bio = db.Column(db.Text)
    location = db.Column(db.String)
    avatar = db.Column(db.String)
    cover = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='profile')
    
    def __repr__(self):
        return f"<Profile {self.id}>"
    
    # def __init__(self, user_id, full_name, bio, occupation, location, profile_image):
    #     self.user_id = user_id
    #     self.full_name = full_name
    #     self.bio = bio
    #     self.occupation = occupation
    #     self.location = location
    #     self.profile_image = profile_image
    