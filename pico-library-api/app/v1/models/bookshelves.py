from app.v1 import db


book_bookshelves_association = db.Table(
    "book_bookshelves",
    db.Column("book_id", db.Integer, db.ForeignKey("books.id", ondelete="CASCADE")),
    db.Column(
        "bookshelf_id", db.Integer, db.ForeignKey("bookshelves.id", ondelete="CASCADE")
    ),
    db.PrimaryKeyConstraint("book_id", "bookshelf_id"),
)


# user_bookshelves_association = db.Table(
#     "user_bookshelves",
#     db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE")),
#     db.Column(
#         "bookshelf_id", db.Integer, db.ForeignKey("bookshelves.id", ondelete="CASCADE")
#     ),
#     db.PrimaryKeyConstraint("user_id", "bookshelf_id"),
# )
class UserBookshelf(db.Model):
    """
    UserBookshelf model
    """

    __tablename__ = "user_bookshelves"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    bookshelf_id = db.Column(
        db.Integer, db.ForeignKey("bookshelves.id", ondelete="CASCADE")
    )
    score = db.Column(db.Integer, default=0)

    user = db.relationship("User", back_populates="user_bookshelves")
    bookshelf = db.relationship("Bookshelf", back_populates="user_bookshelves")

    def __repr__(self):
        return f"<UserBookshelf {self.user_id} {self.bookshelf_id}>"


class Bookshelf(db.Model):
    """
    Bookshelf model
    """

    __tablename__ = "bookshelves"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)

    books = db.relationship(
        "Book", secondary=book_bookshelves_association, back_populates="bookshelves"
    )
    user_bookshelves = db.relationship("UserBookshelf", back_populates="bookshelf")

    def __repr__(self):
        return f"<Bookshelf {self.name}>"

    def __init__(self, name):
        self.name = name
