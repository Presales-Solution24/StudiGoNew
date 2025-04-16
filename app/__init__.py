from flask import Flask
from flask_cors import CORS
from app.config import BaseConfig
from app.models import db
from flask_migrate import Migrate

# Blueprint imports
from app.apis.auth_api import auth_bp
from app.apis.category_api import category_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)
    
    db.init_app(app)
    CORS(app)
    
    Migrate(app, db)

    # Register API Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)

    # Create database
    with app.app_context():
        db.create_all()

    return app