# to run in development
# =====================
# cd to parent
# source venv/bin/activate
# cd to this folder
# python server.py --log_dir=./logs

# to build
# ========
# cd to src folder (folder with this file)
# bazel build :server
# cp -a bazel-bin/. ../dist
# cd to parent
# pip freeze > requirements.txt
# cp requirements.txt dist

# to checkin code
# ===============
# cd to parent
# git status
# git add .
# git commit -m "commit message"
# git push origin master

# to install
# ==========
# move dist folder contents to different machine
# pip install -r requirements.txt

# to run
# =======
# cd to where dist folder was copied
# ./server --log_dir=./logs

import os

from absl import app
from absl import flags
from absl import logging

from flask import Flask
from data import db
from api import api_blueprint

# command line flags
FLAGS = flags.FLAGS
flags.DEFINE_string("flask_host", '0.0.0.0', "Flask Application IP Address.")
flags.DEFINE_integer("flask_port", 5000, "Flask Application Port.")
flags.DEFINE_string("api_prefix", '/api/v1', "API Route Prefix.")
flags.DEFINE_string("postgres_host", '127.0.0.1',
                    "Postgres Database IP Address.")
flags.DEFINE_integer("postgres_port", 25432, "Postgres Database Port.")
flags.DEFINE_string("postgres_db", 'gis', "Postgres Database Name.")
flags.DEFINE_string("postgres_user", 'docker', "Postgres Database Username.")
flags.DEFINE_string("postgres_pw", 'docker', "Postgres Database Password.")

# add docker support
# add testing


# obsolete
def _configure_standard_logging(flask_app):
    """python standard logging"""
    import logging
    from logging.handlers import RotatingFileHandler
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/techex.log',
                                       maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
    file_handler.setLevel(logging.INFO)
    flask_app.logger.addHandler(file_handler)
    flask_app.logger.setLevel(logging.INFO)
    flask_app.logger.info('Techex startup')


def _create_flask_app():
    """Initialize the flask application"""
    flask_app = Flask(__name__, instance_relative_config=False)

    # db uri = 'SQLALCHEMY_DATABASE_URI'] = 'postgresql://docker:docker@localhost:25432/gis'
    flask_app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgresql://{user}:{pw}@{host}:{port}/{db}'.format(
            user=FLAGS.postgres_user,
            pw=FLAGS.postgres_pw,
            host=FLAGS.postgres_host,
            port=FLAGS.postgres_port,
            db=FLAGS.postgres_db)
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if flask_app.env == 'development':
        flask_app.config['SQLALCHEMY_ECHO'] = True
    else:
        flask_app.config['SQLALCHEMY_ECHO'] = False

    with flask_app.app_context():
        #_configure_standard_logging(flask_app)
        flask_app.logger.addHandler(logging.get_absl_handler())
        db.init_app(flask_app)
        flask_app.register_blueprint(api_blueprint, url_prefix=FLAGS.api_prefix)
        return flask_app


def main(argv):
    """driver for flask application"""
    if len(argv) > 1:
        raise app.UsageError('Too many command-line arguments.')
    # absl logging set to file logging if specified
    if FLAGS.log_dir:
        if not os.path.exists(FLAGS.log_dir):
            os.makedirs(FLAGS.log_dir)
        logging.get_absl_handler().use_absl_log_file()
    logging.info('Techex started')
    flask_app = _create_flask_app()
    flask_app.run(host=FLAGS.flask_host, port=FLAGS.flask_port)


if __name__ == '__main__':
    app.run(main)
