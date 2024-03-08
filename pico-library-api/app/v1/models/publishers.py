from . import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Table, PrimaryKeyConstraint
from sqlalchemy.orm import relationship


book_publishers_association = Table(
    "book_publishers",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE")),
    Column("publisher_id", String, ForeignKey("publishers.name", ondelete="CASCADE")),
    PrimaryKeyConstraint("book_id", "publisher_id"),
)

class Publisher(Base):
    """
    Publisher model
    """
    __tablename__ = "publishers"
    name = Column(String, primary_key=True)

    books = relationship("Book", secondary=book_publishers_association, back_populates="publishers")

    def __repr__(self):
        return f"<Publisher(name={self.name})>"
    
    def __init__(self, name):
        self.name = name