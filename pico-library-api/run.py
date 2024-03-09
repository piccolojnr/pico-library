from app.v1 import create_app, db
from app.v1.models import User, Book
import os

app = create_app(os.environ.get("FLASK_ENV", "development"))


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Book": Book}
