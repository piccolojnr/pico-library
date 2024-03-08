from app.v1 import db



book_resource_association = db.Table(
    "book_resources",
    
    db.Column(
        "book_id",
        db.Integer,
        db.ForeignKey("books.id", ondelete="CASCADE"),
    ),
    db.Column(
        "resource_id",
        db.Integer,
        db.ForeignKey("resources.id", ondelete="CASCADE"),
    ),
    db.PrimaryKeyConstraint("book_id", "resource_id"),
)


class ResourceType(db.Model):
    """
    
    """
    __tablename__ = "resource_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    resources = db.relationship("Resource", back_populates="type")



class Resource(db.Model):
    """
    
    """
    __tablename__ = "resources"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True)
    size = db.Column(db.Integer)
    modified = db.Column(db.DateTime)
    type_id = db.Column(db.Integer, db.ForeignKey("resource_type.id", ondelete="CASCADE"))

    type = db.relationship("ResourceType", back_populates="resources")
    books = db.relationship("Book", secondary=book_resource_association, back_populates="resources")
    __table_args__ = (db.UniqueConstraint("url", "type_id"),)

    def __repr__(self):
        return f"<Resource {self.url}>"
    
    def __init__(self, url, size, modified, type_id):
        self.url = url
        self.size = size
        self.modified = modified
        self.type_id = type_id
