from app.v1 import db


import enum
from datetime import datetime


class CommentVoteType(enum.Enum):
    UPVOTE = "upvote"
    DOWNVOTE = "downvote"
    NONE = "none"


class CommentType(enum.Enum):
    COMMENT = "comment"
    REPLY = "reply"
    REVIEW = "review"


class CommentVote(db.Model):
    """
    A vote on a comment.
    """

    __tablename__ = "comment_votes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vote = db.Column(db.Enum(CommentVoteType), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))

    comment = db.relationship("Comment", back_populates="comment_votes")
    user = db.relationship("User", back_populates="comment_votes")

    def __repr__(self):
        return f"<CommentVote {self.id}>"

    # def __init__(self, vote_type, comment_id, user_id):
    #     self.vote_type = vote_type
    #     self.comment_id = comment_id
    #     self.user_id = user_id




class Comment(db.Model):
    """
    A comment on a book.
    """

    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    type = db.Column(db.Enum(CommentType), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    parent_id = db.Column(db.Integer, db.ForeignKey("comments.id", ondelete="CASCADE"))

    book = db.relationship("Book", back_populates="comments")
    user = db.relationship("User", back_populates="comments")
    parent = db.relationship("Comment", remote_side=[id], back_populates="replies")
    replies = db.relationship("Comment", back_populates="parent")
    comment_votes = db.relationship('CommentVote', back_populates='comment')

    def __repr__(self):
        return f"<Comment {self.id}>"

    # def __init__(self, content, type, book_id, user_id, parent_id=None):
    #     self.content = content
    #     self.type = type
    #     self.book_id = book_id
    #     self.user_id = user_id
    #     self.parent_id = parent_id
