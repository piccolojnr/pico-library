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
    id = db.Column(db.Integer, primary_key=True)
    vote_type = db.Column(db.Enum(CommentVoteType), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))

    comment = db.relationship("Comment", backref="comment_votes")
    user = db.relationship("User", backref="comment_votes")

    def __repr__(self):
        return f"<CommentVote {self.id}>"

    def __init__(self, vote_type, comment_id, user_id):
        self.vote_type = vote_type
        self.comment_id = comment_id
        self.user_id = user_id


ondelete = "CASCADE"


class Comment(db.Model):
    """
    A comment on a book.
    """

    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    type = db.Column(db.Enum(CommentType), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    parent_id = db.Column(db.Integer, db.ForeignKey("comments.id", ondelete="CASCADE"))

    book = db.relationship("Book", backref="comments")
    user = db.relationship("User", backref="comments")
    parent = db.relationship("Comment", remote_side=[id], backref="replies")
    replies = db.relationship("Comment", backref="parent")

    def __repr__(self):
        return f"<Comment {self.id}>"

    def __init__(self, content, type, book_id, user_id, parent_id=None):
        self.content = content
        self.type = type
        self.book_id = book_id
        self.user_id = user_id
        self.parent_id = parent_id
