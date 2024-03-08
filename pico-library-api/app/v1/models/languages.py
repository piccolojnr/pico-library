from . import Base
from sqlalchemy import Column, Integer, String,ForeignKey,Table, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

book_languages_association = Table(
    'book_languages',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id', ondelete="CASCADE")),
    Column('language_id', Integer, ForeignKey('languages.id', ondelete="CASCADE")),
    PrimaryKeyConstraint('book_id', 'language_id')
)


class Language(Base):
    """
    Language model
    """
    __tablename__ = 'languages'
    code = Column(String, primary_key=True)
    
    books = relationship("Book", secondary=book_languages_association, back_populates="languages")
    
    def __repr__(self):
        return f"<Language {self.code}>"
    
    def __init__(self, code):
        self.code = code