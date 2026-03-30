from flask import Flask
from .config.config import DevelopmentConfig
from .extensions.extensions import jwt, bcrypt, cors


def create_app(config_object: str | object = DevelopmentConfig) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    # initialize extensions
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    # register blueprints
    from .api.v1.auth import auth_bp
    from .api.v1.tasks import tasks_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(tasks_bp, url_prefix="/api/v1/tasks")

    @app.route("/healthz")
    def healthz():
        return {"status": "ok"}

    return app
