from flask import Flask, request, jsonify, make_response
from datetime import datetime
from typing import Any

# export the app and request objects for use in other modules
app = Flask(__name__)

# export the request object for use in other modules
request = request


# export a standard response template
def response_template(
    success: bool = True,
    error_code: int = 0,
    message: str = "Success",
    data: Any = None,
    request: Any = None,
    status: int = 200,
):
    """
    Standard API JSON response
    """
    return jsonify(
        {
            "success": success,
            "error_code": error_code,
            "message": message or "",
            "data": data or {},
            "timestamp": datetime.now().isoformat(),
            "path": request.path if request else None,
        }
    ), status
