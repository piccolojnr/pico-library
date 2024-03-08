from app.v1 import db

book_subjects_association = db.Table(
    "book_subjects",
    db.Column("book_id", db.Integer, db.ForeignKey("books.id", ondelete="CASCADE")),
    db.Column("subject_id", db.Integer, db.ForeignKey("subjects.id", ondelete="CASCADE")),
    db.PrimaryKeyConstraint("book_id", "subject_id"),
)


class Subject(db.Model):
    """
    Subject model
    """
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    books = db.relationship("Book", secondary=book_subjects_association, back_populates="subjects")


    def __repr__(self):
        return f"<Subject(name={self.name})>"
    
    def __init__(self, name):
        self.name = name