from flask import Blueprint
from flask_restx import Api

auth_bp = Blueprint('auth', __name__, url_prefix='/api/users')
rest_api = Api(auth_bp, version="1.0", title="Users API")

from . import routes
