from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.v1.config import get_config
from flask_pyjwt import AuthManager, current_token
from http import HTTPStatus
from flask_restx import abort
from apscheduler.schedulers.background import BackgroundScheduler

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
auth_manager = AuthManager()

from apscheduler.schedulers.background import BackgroundScheduler


def start_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule the function to run daily at a specific time (e.g., midnight)
    from app.v1.services.popular_books_engine import preprocess_popularity_data

    scheduler.add_job(preprocess_popularity_data, "interval", days=7)
    scheduler.start()


def create_app(config_name):
    app = Flask("pico-library-api")
    app.config.from_object(get_config(config_name))

    from app.v1.api import api_bp
    from app.v1.web import web_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)

    @app.before_request
    def check_blacklist():
        if current_token:
            from app.v1.models import BlacklistedToken

            token = BlacklistedToken.check_blacklist(current_token.signed)
            if token:
                abort(HTTPStatus.UNAUTHORIZED, "Unauthorized")

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    bcrypt.init_app(app)
    auth_manager.init_app(app)

    # Error Pages
    @app.errorhandler(404)
    def page_not_found(error):
        print("this is a 404 page")
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("errors/500.html"), 500

    start_scheduler()
    return app
