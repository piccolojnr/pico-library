from . import Base

from sqlalchemy import  Column, Integer, String,ForeignKey, Table, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

book_bookshelves_association = Table(
    'book_bookshelves',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id', ondelete="CASCADE")),
    Column('bookshelf_id', Integer, ForeignKey('bookshelves.id', ondelete="CASCADE")),
    PrimaryKeyConstraint('book_id', 'bookshelf_id')
)


class Bookshelf(Base):
    """
    Bookshelf model
    """
    __tablename__ = 'bookshelves'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
    books = relationship('Book', secondary=book_bookshelves_association, back_populates='bookshelves')

    def __repr__(self):
        return f'<Bookshelf {self.name}>'
    
    def __init__(self, name):
        self.name = name