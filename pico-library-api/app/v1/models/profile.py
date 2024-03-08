from app.v1 import db

from datetime import datetime

class Profile(db.Model):
    """
    Profile model
    """
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    full_name = db.Column(db.String)
    bio = db.Column(db.Text)
    occupation = db.Column(db.String)
    location = db.Column(db.String)
    profile_image = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='profile')
    
    def __repr__(self):
        return f"<Profile {self.id}>"
    
    def __init__(self, user_id, full_name, bio, occupation, location, profile_image):
        self.user_id = user_id
        self.full_name = full_name
        self.bio = bio
        self.occupation = occupation
        self.location = location
        self.profile_image = profile_image
    