# utils/db_middleware.py
import threading
from app.config.config import Config

conf = Config()

# Thread-local storage for database name
_thread_locals = threading.local()


def get_current_database_name():
    """Get the current database name from thread-local storage"""
    return getattr(_thread_locals, "database_name", None)


def set_current_database_name(database_name):
    """Set the current database name in thread-local storage"""
    _thread_locals.database_name = database_name


class DatabaseMiddleware:
    """
    Middleware to set database name based on X-Database-Name header from client.
    This allows the frontend to specify which database to use (dev or production)
    based on the devMode flag.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get database name from header
        db_name = request.headers.get("X-Database-Name", None)

        # If header is present, set it in thread-local storage
        if db_name:
            # Validate database name (security: only allow specific database names)
            allowed_databases = conf.ALLOWED_DATABASES
            if db_name in allowed_databases:
                set_current_database_name(db_name)
            else:
                # If invalid database name, use default
                set_current_database_name(None)
        else:
            # No header, use default (will be handled by DBHelper)
            set_current_database_name(None)

        response = self.get_response(request)

        # Clean up thread-local storage after request
        set_current_database_name(None)

        return response
