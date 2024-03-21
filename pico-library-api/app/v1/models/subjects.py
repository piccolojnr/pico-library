from app.v1 import db

book_subjects_association = db.Table(
    "book_subjects",
    db.Column("book_id", db.Integer, db.ForeignKey("books.id", ondelete="CASCADE")),
    db.Column(
        "subject_id", db.Integer, db.ForeignKey("subjects.id", ondelete="CASCADE")
    ),
    db.PrimaryKeyConstraint("book_id", "subject_id"),
)

# user_subjects_association = db.Table(
#     "user_subjects",
#     db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE")),
#     db.Column(
#         "subject_id", db.Integer, db.ForeignKey("subjects.id", ondelete="CASCADE")
#     ),
#     db.PrimaryKeyConstraint("user_id", "subject_id"),
# )


class UserSubject(db.Model):
    """
    UserSubject model
    """

    __tablename__ = "user_subjects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id", ondelete="CASCADE"))
    score = db.Column(db.Integer, default=0)

    user = db.relationship("User", back_populates="user_subjects")
    subject = db.relationship("Subject", back_populates="user_subjects")

    def __repr__(self):
        return f"<UserSubject(user_id={self.user_id}, subject_id={self.subject_id})>"


class Subject(db.Model):
    """
    Subject model
    """

    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)

    books = db.relationship(
        "Book", secondary=book_subjects_association, back_populates="subjects"
    )
    user_subjects = db.relationship("UserSubject", back_populates="subject")

    def __repr__(self):
        return f"<Subject(name={self.name})>"

    def __init__(self, name):
        self.name = name
