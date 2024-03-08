from . import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Table,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship


book_resource_association = Table(
    "book_resources",
    Base.metadata,
    Column(
        "book_id",
        Integer,
        ForeignKey("books.id", ondelete="CACADE"),
    ),
    Column(
        "resource_id",
        Integer,
        ForeignKey("resources.id", ondelete="CASCADE"),
    ),
    PrimaryKeyConstraint("book_id", "resource_id"),
)


class ResourceType(Base):
    """
    
    """
    __tablename__ = "resource_type"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    resources = relationship("Resource", back_populates="type")



class Resource(Base):
    """
    
    """
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    size = Column(Integer)
    modified = Column(DateTime)
    type_id = Column(Integer, ForeignKey("resource_type.id", ondelete="CASCADE"))

    type = relationship("ResourceType", back_populates="resources")
    books = relationship("Book", secondary=book_resource_association, back_populates="resources")
    __table_args__ = (UniqueConstraint("url", "type_id"),)

    def __repr__(self):
        return f"<Resource {self.url}>"
    
    def __init__(self, url, size, modified, type_id):
        self.url = url
        self.size = size
        self.modified = modified
        self.type_id = type_id
