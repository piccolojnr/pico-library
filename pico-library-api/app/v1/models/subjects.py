from . import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

book_subjects_association = Table(
    "book_subjects",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE")),
    Column("subject_id", Integer, ForeignKey("subjects.id", ondelete="CASCADE")),
    PrimaryKeyConstraint("book_id", "subject_id"),
)


class Subject(Base):
    """
    Subject model
    """
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    books = relationship("Book", secondary=book_subjects_association, back_populates="subjects")


    def __repr__(self):
        return f"<Subject(name={self.name})>"
    
    def __init__(self, name):
        self.name = name