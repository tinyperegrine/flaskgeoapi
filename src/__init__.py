from flask import Flask


def create_app():
    """Initialize the flask application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://docker:docker@localhost:25432/gis'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True



    with app.app_context():

        from src.models import db
        db.init_app(app)

        from src.api import api_blueprint
        app.register_blueprint(api_blueprint)

        return app
