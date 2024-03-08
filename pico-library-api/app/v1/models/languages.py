from app.v1 import db


book_languages_association = db.Table(
    "book_languages",
    db.Column("book_id", db.Integer, db.ForeignKey("books.id", ondelete="CASCADE")),
    db.Column(
        "language_id", db.String, db.ForeignKey("languages.code", ondelete="CASCADE")
    ),
    db.PrimaryKeyConstraint("book_id", "language_id"),
)


class Language(db.Model):
    """
    Language model
    """
    __tablename__ = "languages"
    code = db.Column(db.String, primary_key=True)

    books = db.relationship(
        "Book", secondary=book_languages_association, back_populates="languages"
    )

    def __repr__(self):
        return f"<Language {self.code}>"

    def __init__(self, code):
        self.code = code
