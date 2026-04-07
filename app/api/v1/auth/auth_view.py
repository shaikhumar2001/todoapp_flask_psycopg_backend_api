# app/api/v1/auth/auth_view.py
from flask import request
from flask_jwt_extended import create_access_token

from app.api.v1.auth import auth_bp
from app.utils.response_template import response_template
from app.extensions.db_helper import DBHelper
from app.extensions.extensions import bcrypt

db = DBHelper()


@auth_bp.route("/get/users/", methods=["GET"])
def get_all_users(request=request):
    """_summary_

    Args:
        request (_type_, optional): _description_. Defaults to request.

    Returns:
        _type_: _description_
    """
    try:
        records = db.execute_query("SELECT * FROM todoapp.tusertbl")
        if not records:
            return response_template(
                success=False,
                error_code=404,
                message="No users found.",
                request=request,
                status=404,
            )
        return response_template(
            success=True,
            error_code=0,
            message="Welcome to the TodoApp API!",
            data={"users": records},
            request=request,
        )
    except Exception as e:
        return response_template(
            success=False,
            error_code=500,
            message=f"Internal server error: {str(e)}",
            request=request,
            status=500,
        )


@auth_bp.route("/register", methods=["POST"])
def register(request=request):
    """_summary_

    Args:
        request (_type_, optional): _description_. Defaults to request.

    Returns:
        _type_: _description_
    """
    try:
        data = request.get_json() or {}
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        if not name or not email or not password:
            return response_template(
                success=False,
                error_code=400,
                message="Name, email and password are required.",
                request=request,
                status=400,
            )

        # hash password
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        records = db.execute_query(
            """
            INSERT INTO 
                todoapp.tusertbl (name, email, password_hash) 
            VALUES 
                (%s, %s, %s)
            RETURNING user_id
        """,
            (
                name,
                email,
                password_hash,
            ),
        )
        if records:
            return response_template(
                success=True,
                error_code=0,
                message="User created successfully.",
                data={"user_id": records[0].get("user_id")},
                request=request,
                status=201,
            )
        else:
            return response_template(
                success=False,
                error_code=500,
                message="Failed to create user.",
                request=request,
                status=500,
            )
    except Exception as e:
        return response_template(
            success=False,
            error_code=500,
            message=f"Internal server error: {str(e)}",
            request=request,
            status=500,
        )


@auth_bp.route("/login", methods=["POST"])
def login(request=request):
    """_summary_

    Args:
        request (_type_, optional): _description_. Defaults to request.

    Returns:
        _type_: _description_
    """    
    try:
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return response_template(
                success=False,
                error_code=400,
                message="email and password required",
                status=400,
                request=request,
            )

        rows = db.execute_query(
            "SELECT * FROM todoapp.tusertbl WHERE email=%s", (email,)
        )
        if not rows:
            return response_template(
                success=False,
                error_code=401,
                message="Invalid credentials",
                status=401,
                request=request,
            )
        user = rows[0]
        if not bcrypt.check_password_hash(user.get("password_hash"), password):
            return response_template(
                success=False,
                error_code=401,
                message="Invalid credentials",
                status=401,
                request=request,
            )

        access = create_access_token(identity=int(user.get("user_id")))
        return response_template(
            success=True,
            error_code=0,
            message="Logged in",
            data={"access_token": access},
            request=request,
        )
    except Exception as e:
        return response_template(
            success=False,
            error_code=500,
            message=f"Internal server error: {str(e)}",
            status=500,
            request=request,
        )
