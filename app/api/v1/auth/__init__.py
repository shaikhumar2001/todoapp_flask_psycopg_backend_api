from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

from . import auth_view  # noqa: F401

