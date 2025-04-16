# app/__init__.py

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from app.config import BaseConfig
from app.models import db
from app.apis.auth_api import auth_bp
from app.apis.category_api import category_bp

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)

    return app
