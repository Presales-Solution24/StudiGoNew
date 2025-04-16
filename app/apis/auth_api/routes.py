from flask import request, jsonify
from app.models.auth_models.models import Users, JWTTokenBlocklist
from app.models import db
from app.config import BaseConfig
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps

def token_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("authorization", None)
        if not token:
            return jsonify({"success": False, "msg": "JWT token is missing"}), 400
        try:
            data = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=["HS256"])
            current_user = Users.get_by_email(data["email"])
            if not current_user:
                return jsonify({"success": False, "msg": "Invalid token user"}), 400
            if db.session.query(JWTTokenBlocklist.id).filter_by(jwt_token=token).scalar():
                return jsonify({"success": False, "msg": "Token revoked"}), 400
            if not current_user.check_jwt_auth_active():
                return jsonify({"success": False, "msg": "Token expired"}), 400
        except:
            return jsonify({"success": False, "msg": "Invalid token"}), 400
        return f(current_user, *args, **kwargs)
    return decorated

from . import auth_bp

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if Users.get_by_email(data["email"]):
        return jsonify({"success": False, "msg": "Email already taken"}), 400
    user = Users(username=data["username"], email=data["email"])
    user.set_password(data["password"])
    user.save()
    return jsonify({"success": True, "userID": user.id}), 200

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = Users.get_by_email(data["email"])
    if not user or not user.check_password(data["password"]):
        return jsonify({"success": False, "msg": "Invalid credentials"}), 400
    token = jwt.encode(
        {"email": user.email, "exp": datetime.utcnow() + timedelta(minutes=30)},
        BaseConfig.SECRET_KEY
    )
    user.set_jwt_auth_active(True)
    user.save()
    return jsonify({"success": True, "token": token, "user": user.toJSON()}), 200

@auth_bp.route("/logout", methods=["POST"])
@token_required
def logout(current_user):
    token = request.headers.get("authorization")
    jwt_block = JWTTokenBlocklist(jwt_token=token, created_at=datetime.now(timezone.utc))
    jwt_block.save()
    current_user.set_jwt_auth_active(False)
    current_user.save()
    return jsonify({"success": True}), 200

@auth_bp.route("/edit", methods=["POST"])
@token_required
def edit_user(current_user):
    data = request.get_json()
    current_user.username = data.get("username", current_user.username)
    current_user.email = data.get("email", current_user.email)
    current_user.save()
    return jsonify({"success": True}), 200
