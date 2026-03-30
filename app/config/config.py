import os
from datetime import datetime, timezone
from typing import Any
from flask import jsonify, make_response


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    JSON_SORT_KEYS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", os.getenv("SECRET_KEY", "change-me"))

    DB_USER = os.getenv("DB_USER", "todoapp_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "todoapp@786")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "todoapp_db")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


