from app.v1 import create_app, db
from app.v1.models import __all__
import os

app = create_app(os.environ.get("FLASK_ENV", "development"))

@app.shell_context_processor
def make_shell_context():
    dict_ = {}
    for model in __all__:
        dict_[model.__tablename__] = model
    dict_["db"] = db
    return dict_
