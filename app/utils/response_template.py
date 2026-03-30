from typing import Any
from datetime import datetime, timezone
from flask import jsonify, make_response

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