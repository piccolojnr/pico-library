from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.v1.config import get_config


cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app(config_name):
    
