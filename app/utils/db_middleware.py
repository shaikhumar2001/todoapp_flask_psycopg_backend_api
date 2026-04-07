# utils/db_middleware.py
from flask import g

def get_current_db_name():
    """Get the current database name from thread-local storage"""
    return getattr(g, "db_name", None)


def set_current_db_name(db_name):
    """Set the current database name in thread-local storage"""
    g.db_name = db_name