from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.v1.config import get_config
from flask_pyjwt import AuthManager


cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
auth_manager = AuthManager()


def create_app(config_name):
    app = Flask("pico-library-api")
    app.config.from_object(get_config(config_name))

    from app.v1.api import api_bp

    app.register_blueprint(api_bp)

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    bcrypt.init_app(app)
    auth_manager.init_app(app)

    return app
