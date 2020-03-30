import logging
import os
import datetime


class Config(object):
    # noinspection PyPackageRequirements
    DEBUG = False

    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    LOG_LEVEL = logging.INFO

    #  发件箱设置
    SMTP = {
        'host': 'smtp.exmail.qq.com',
        'port': 0,
        'username': 'itservice@xxx.com.cn',
        'password': '',
        'use_ssl': False,
        'use_tls': False,
        'fromname': 'APP Name <itservice@xxx.com.cn>'
    }
    DEV_EMAIL = 'xxxx@xx.com.cn'

    # celery设置
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/1')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')

    # Flask-MongoEngine settings
    MONGO_DATABASE = 'db name'
    MONGO_SERVER = 'server url'
    MONGO_PORT = 28017
    MONGO_USER = 'user'
    MONGO_PASSWORD = 'password'
    MONGODB_SETTINGS = {
        'db': 'db name',
        'host': f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_SERVER}:{MONGO_PORT}/{MONGO_DATABASE}?authSource=admin'
    }


class DevelopmentConfig(Config):
    DEBUG = True

    # Hamlet设置 staging
    HAMLET_URL = ''
    HAMLET_APP_KEY = ''
    HAMLET_APP_SECRET = ''
    HAMLET_API_KEY = ''


class ProductionConfig(Config):
    LOG_LEVEL = logging.WARNING

    # Hamlet设置 prod
    HAMLET_URL = ''
    HAMLET_APP_KEY = ''
    HAMLET_APP_SECRET = ''
    HAMLET_API_KEY = ''


def get_config_class():
    env = os.environ.get('proj_env'.upper(), 'dev').lower()
    if env == 'prod':
        return ProductionConfig
    return DevelopmentConfig


# CONF 是一个全局对象，用于获取配置项。
# 在 Flask Application Context 里，也可以通过 current_app.config 获取配置项
CONF = get_config_class()
