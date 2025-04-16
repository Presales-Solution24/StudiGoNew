import os, random, string
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class BaseConfig():

    SECRET_KEY = os.getenv('SECRET_KEY') or ''.join(random.choices(string.ascii_letters, k=32))
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or ''.join(random.choices(string.ascii_letters, k=32))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_ENGINE   = os.getenv('DB_ENGINE')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASS     = os.getenv('DB_PASS')
    DB_HOST     = os.getenv('DB_HOST')
    DB_PORT     = os.getenv('DB_PORT')
    DB_NAME     = os.getenv('DB_NAME')

    if all([DB_ENGINE, DB_USERNAME, DB_PASS, DB_HOST, DB_PORT, DB_NAME]):
        SQLALCHEMY_DATABASE_URI = f"{DB_ENGINE}://{DB_USERNAME}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        # Fallback to SQLite
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
