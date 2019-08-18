import os, logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from data import db
from api import api_blueprint


def _create_app():
    """Initialize the flask application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgresql://docker:docker@localhost:25432/gis'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ECHO'] = False

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/techex.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Techex startup')

    with app.app_context():
        db.init_app(app)
        app.register_blueprint(api_blueprint, url_prefix='/api/v1')
        return app


def main():
    """driver for flask application"""
    app = _create_app()
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    main()
