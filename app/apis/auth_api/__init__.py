from flask import Blueprint

auth_bp = Blueprint("auth_api", __name__, url_prefix="/api/users")

from . import routes  # pastikan ini tetap di bawah agar route terdaftar
