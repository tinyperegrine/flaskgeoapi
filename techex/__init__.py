from flask import Flask


def create_app():
    """Initialize the flask application"""
    app = Flask(__name__, instance_relative_config=False)
    with app.app_context():
        from techex.api import api_blueprint
        app.register_blueprint(api_blueprint)
        return app
