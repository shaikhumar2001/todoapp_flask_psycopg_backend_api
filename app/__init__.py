# app/__init__.py
from flask import Flask, request
from .extensions.extensions import jwt, bcrypt, cors
from .utils.db_middleware import set_current_db_name
from .config.config import Config
from .extensions.db_helper import DBHelper
from app.utils.response_template import response_template

db = DBHelper()
conf = Config()


def create_app(config_object: str | object = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    # initialize extensions
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    # ── DB middleware  ───────────────────────────────────────────────────
    @app.before_request
    def set_db():
        db_name = request.headers.get("X-Database-Name", None)
        if db_name and db_name in conf.ALLOWED_DATABASES:
            set_current_db_name(db_name)
        else:
            set_current_db_name(None)

    @app.teardown_request
    def clear_db(exception=None):
        set_current_db_name(None)
    # ─────────────────────────────────────────────────────────────────────

    # register blueprints
    from .api.v1.auth import auth_bp
    from .api.v1.tasks import tasks_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(tasks_bp, url_prefix="/api/v1/tasks")

    # health check endpoint
    @app.route("/healthz/")
    def healthz():
        result = db.execute_query("SELECT 1 AS db_ok")
        db_ok = result is not None and len(result) > 0
        return response_template(
            success=db_ok,
            message="OK" if db_ok else "Database connection failed",
            data={"db_ok": db_ok},
            status=200 if db_ok else 500,
            request=request,
        )
    
    return app
