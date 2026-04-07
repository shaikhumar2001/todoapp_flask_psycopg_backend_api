# app/config/config.py
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    JSON_SORT_KEYS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", os.getenv("SECRET_KEY", "change-me"))
    ALLOWED_DATABASES = ["todoapp_db", "todoapp_db_uat", "todoapp_db_test"]  # For validating tenant DB names from headers

    # server settings
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("FLASK_ENV", "production") == "development" # Default to False i.e. "production" unless explicitly set to "development"

    # db creds
    DB_USER = os.getenv("DB_USER", "todoapp_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "todoapp@786")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "todoapp_db")
