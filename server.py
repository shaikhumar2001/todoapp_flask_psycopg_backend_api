from app.config.config import app, response_template, request
from app.extensions.db_helper import DBHelper

db = DBHelper()

@app.route("/health", methods=["GET"])
def health_check():
    return response_template(
        success=True,
        error_code=0,
        message="API is running healthy...",
        request=request,
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
