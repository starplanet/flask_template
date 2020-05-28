from flask import Flask

from proj.config import CONF
from proj import handlers


def create_app():
    app = Flask(__name__)
    app.config.from_object(CONF)

    configure_log(app)
    register_extensions(app)

    from proj import models  # noqa
    return app


def register_extensions(app):
    from proj.extensions import db, hamlet, celery

    db.init_app(app)
    hamlet.init_app(app)
    celery.config_from_object(CONF)
    handlers.init_app(app)


def configure_log(app):
    import logging

    if not app.config['DEBUG']:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)

    logger = logging.getLogger('thiqa')
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(app.config.get('LOG_FORMAT')))
    logger.addHandler(handler)
    logger.setLevel(app.config.get('LOG_LEVEL'))
