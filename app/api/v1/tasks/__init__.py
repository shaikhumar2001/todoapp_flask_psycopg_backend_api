from flask import Blueprint

tasks_bp = Blueprint("tasks", __name__)

from . import task_view  # noqa: F401
