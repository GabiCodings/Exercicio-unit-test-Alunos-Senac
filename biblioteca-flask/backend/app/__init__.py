"""Factory da aplicação Flask."""

from flask import Flask
from flask_cors import CORS

from app.routes.books import bp as books_bp


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    if test_config:
        app.config.update(test_config)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.register_blueprint(books_bp)
    return app
