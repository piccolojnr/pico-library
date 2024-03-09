from app.v1 import db


class Rating(db.Model):
    """
    Rating model
    """
    __tablename__ = 'ratings'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete="CASCADE"), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    rating = db.Column(db.Float)

    user = db.relationship('User', back_populates='ratings')
    book = db.relationship('Book', back_populates='ratings')
    
    def __repr__(self):
        return f'<Rating {self.user_id} {self.book_id} {self.rating}>'
    
    def __init__(self, user_id, book_id, rating):
        self.user_id = user_id
        self.book_id = book_id
        self.rating = rating