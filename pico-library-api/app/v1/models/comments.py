from . import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

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


class CommentVote(Base):
    """
    A vote on a comment.
    """

    __tablename__ = "comment_votes"
    id = Column(Integer, primary_key=True)
    vote_type = Column(Enum(CommentVoteType), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    comment = relationship("Comment", backref="comment_votes")
    user = relationship("User", backref="comment_votes")

    def __repr__(self):
        return f"<CommentVote {self.id}>"

    def __init__(self, vote_type, comment_id, user_id):
        self.vote_type = vote_type
        self.comment_id = comment_id
        self.user_id = user_id


ondelete = "CASCADE"


class Comment(Base):
    """
    A comment on a book.
    """
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    type = Column(Enum(CommentType), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    parent_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"))

    book = relationship("Book", backref="comments")
    user = relationship("User", backref="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")
    replies = relationship("Comment", backref="parent")

    def __repr__(self):
        return f"<Comment {self.id}>"

    def __init__(self, content, type, book_id, user_id, parent_id=None):
        self.content = content
        self.type = type
        self.book_id = book_id
        self.user_id = user_id
        self.parent_id = parent_id
