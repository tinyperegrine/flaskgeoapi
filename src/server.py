from flask import Flask


def _create_app():
    """Initialize the flask application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://docker:docker@localhost:25432/gis'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    with app.app_context():

        from data.models import db
        db.init_app(app)

        from api import api_blueprint
        app.register_blueprint(api_blueprint)

        return app


def main():
    """driver for flask application"""
    app = _create_app()
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    main()
