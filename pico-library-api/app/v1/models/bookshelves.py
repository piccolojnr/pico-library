from app.v1 import db


book_bookshelves_association = db.Table(
    "book_bookshelves",
    
    db.Column("book_id", db.Integer, db.ForeignKey("books.id", ondelete="CASCADE")),
    db.Column(
        "bookshelf_id", db.Integer, db.ForeignKey("bookshelves.id", ondelete="CASCADE")
    ),
    db.PrimaryKeyConstraint("book_id", "bookshelf_id"),
)


class Bookshelf(db.Model):
    """
    Bookshelf model
    """

    __tablename__ = "bookshelves"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    books = db.relationship(
        "Book", secondary=book_bookshelves_association, back_populates="bookshelves"
    )

    def __repr__(self):
        return f"<Bookshelf {self.name}>"

    def __init__(self, name):
        self.name = name
