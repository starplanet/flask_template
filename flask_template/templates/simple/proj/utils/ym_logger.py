import logging
from logging.config import dictConfig

from flask import current_app, g
from werkzeug.local import LocalProxy


class YmLogger:

    @staticmethod
    def init_logger(app):

        dictConfig({
            'version': 1,
            'formatters': {
                'default': {
                    'format': '[%(asctime)s][%(levelname)s][%(module)s][%(funcName)s][%(lineno)s]: %(message)s',
                }},
            'handlers': {
                'default': {
                    'formatter': 'default',
                    'class': 'logging.StreamHandler',
                }},
            'root': {
                'level': 'INFO',
                'handlers': ['default']
            }
        })

        level = app.config.get('LOG_LEVEL', logging.INFO)
        app.logger.setLevel(level)


    @staticmethod
    def get_logger():
        def __get_logger():
            logger = getattr(g, '_logger', None)
            if logger is None:
                logger = g._logger = current_app.logger
            return logger

        return LocalProxy(__get_logger)

