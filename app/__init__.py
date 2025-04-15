from flask import Flask
from flask_cors import CORS
from app.config import BaseConfig
from app.models.user import db
from app.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)
    db.init_app(app)
    CORS(app)
    app.register_blueprint(auth_bp)
    return app
