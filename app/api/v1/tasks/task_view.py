# app/api/v1/tasks/task_view.py
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.v1.tasks import tasks_bp
from app.utils.response_template import response_template
from app.extensions.db_helper import DBHelper

db = DBHelper()


@tasks_bp.route("/", methods=["GET"])
@jwt_required()
def list_tasks(request=request):
    user_id = get_jwt_identity()
    records = db.execute_query("SELECT * FROM todoapp.ttasktbl WHERE user_id=%s", (user_id,))
    return response_template(success=True, error_code=0, message="Tasks fetched", data={"tasks": records}, request=request)


@tasks_bp.route("/", methods=["POST"])
@jwt_required()
def create_task(request=request):
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    title = data.get("title")
    if not title:
        return response_template(success=False, error_code=400, message="title is required", status=400, request=request)

    records = db.execute_query(
        """
        INSERT INTO todoapp.ttasktbl (user_id, title, description, due_date)
        VALUES (%s, %s, %s, %s)
        RETURNING task_id
        """,
        (user_id, title, data.get("description"), data.get("due_date")),
    )
    if records:
        return response_template(success=True, error_code=0, message="Task created", data={"task_id": records[0].get("task_id")}, status=201, request=request)
    return response_template(success=False, error_code=500, message="Failed to create task", status=500, request=request)


@tasks_bp.route("/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id, request=request):
    user_id = get_jwt_identity()
    records = db.execute_query("SELECT * FROM todoapp.ttasktbl WHERE task_id=%s AND user_id=%s", (task_id, user_id))
    if not records:
        return response_template(success=False, error_code=404, message="Task not found", status=404, request=request)
    return response_template(success=True, error_code=0, message="Task fetched", data={"task": records[0]}, request=request)


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id, request=request):
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    # Only update provided fields
    fields = []
    params = []
    if "title" in data:
        fields.append("title=%s")
        params.append(data.get("title"))
    if "description" in data:
        fields.append("description=%s")
        params.append(data.get("description"))
    if "is_completed" in data:
        fields.append("is_completed=%s")
        params.append(bool(data.get("is_completed")))
    if "due_date" in data:
        fields.append("due_date=%s")
        params.append(data.get("due_date"))

    if not fields:
        return response_template(success=False, error_code=400, message="No fields to update", status=400, request=request)

    params.extend([task_id, user_id])
    query = f"UPDATE todoapp.ttasktbl SET {', '.join(fields)} WHERE task_id=%s AND user_id=%s RETURNING task_id"
    records = db.execute_query(query, tuple(params))
    if not records:
        return response_template(success=False, error_code=404, message="Task not found or not updated", status=404, request=request)
    return response_template(success=True, error_code=0, message="Task updated", data={"task_id": records[0].get("task_id")}, request=request)


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id, request=request):
    user_id = get_jwt_identity()
    records = db.execute_query("DELETE FROM todoapp.ttasktbl WHERE task_id=%s AND user_id=%s RETURNING task_id", (task_id, user_id))
    if not records:
        return response_template(success=False, error_code=404, message="Task not found", status=404, request=request)
    return response_template(success=True, error_code=0, message="Task deleted", request=request)


@tasks_bp.route("/<int:task_id>/complete", methods=["PATCH"])
@jwt_required()
def mark_complete(task_id, request=request):
    user_id = get_jwt_identity()
    records = db.execute_query("UPDATE todoapp.ttasktbl SET is_completed=TRUE WHERE task_id=%s AND user_id=%s RETURNING task_id", (task_id, user_id))
    if not records:
        return response_template(success=False, error_code=404, message="Task not found", status=404, request=request)
    return response_template(success=True, error_code=0, message="Task marked complete", data={"task_id": records[0].get("task_id")}, request=request)
