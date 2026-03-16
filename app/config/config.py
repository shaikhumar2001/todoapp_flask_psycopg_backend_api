import os
from datetime import datetime, timezone
from typing import Any
from flask import jsonify, make_response


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    JSON_SORT_KEYS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", os.getenv("SECRET_KEY", "change-me"))

    DB_USER = os.getenv("DB_USER", "todoapp_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "todoapp@786")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "todoapp_db")

    SQLALCHEMY_DATABASE_URI = (
        os.getenv(
            "DATABASE_URL",
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        )
    )


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


def response_template(
    success: bool = True,
    error_code: int = 0,
    message: str = "Success",
    data: Any = None,
    status: int = 200,
    request: Any = None,
):
    """Standard API JSON response"""
    return make_response(
        jsonify(
            {
                "success": success,
                "error_code": error_code,
                "message": message or "",
                "data": data or {},
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "path": request.path if request else None,
            }
        ),
        status,
    )
