# app/models/user.py

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.Text())
    jwt_auth_active = db.Column(db.Boolean())
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self): return f"User {self.username}"
    def save(self): db.session.add(self); db.session.commit()
    def set_password(self, password): self.password = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password, password)
    def check_jwt_auth_active(self): return self.jwt_auth_active
    def set_jwt_auth_active(self, status): self.jwt_auth_active = status

    def toJSON(self):
        return {
            "_id": self.id,
            "username": self.username,
            "email": self.email,
        }

    @classmethod
    def get_by_email(cls, email): return cls.query.filter_by(email=email).first()
    @classmethod
    def get_by_username(cls, username): return cls.query.filter_by(username=username).first()

class JWTTokenBlocklist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jwt_token = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    def __repr__(self): return f"Expired Token: {self.jwt_token}"
    def save(self): db.session.add(self); db.session.commit()
