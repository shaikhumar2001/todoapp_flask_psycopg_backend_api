import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    JSON_SORT_KEYS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", os.getenv("SECRET_KEY", "change-me"))
    ALLOWED_DATABASES = ["edusoft_db", "edusoft_db_local"]  # For validating tenant DB names from headers

    # db creds
    DB_USER = os.getenv("DB_USER", "todoapp_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "todoapp@786")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "todoapp_db")

    # CORS settings
    DEBUG = os.getenv("FLASK_ENV", "production") == "development" # Default to False i.e. "production" unless explicitly set to "development"
