from flask import Blueprint
from flask_restx import Api

category_bp = Blueprint('category', __name__, url_prefix='/api/users')
rest_api = Api(category_bp, version="1.0", title="Users API")

from . import routes
