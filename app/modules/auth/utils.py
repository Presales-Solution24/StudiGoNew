from functools import wraps
from flask import request
import jwt
from app.config import BaseConfig
from app.models.user import Users, JWTTokenBlocklist, db

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("authorization", None)
        if not token:
            return {"success": False, "msg": "Valid JWT token is missing"}, 400
        try:
            data = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=["HS256"])
            current_user = Users.get_by_email(data["email"])
            if not current_user or not current_user.check_jwt_auth_active():
                return {"success": False, "msg": "Token expired or invalid"}, 400
            if db.session.query(JWTTokenBlocklist.id).filter_by(jwt_token=token).scalar():
                return {"success": False, "msg": "Token revoked."}, 400
        except:
            return {"success": False, "msg": "Token is invalid"}, 400
        return f(current_user, *args, **kwargs)
    return decorator
