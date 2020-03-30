from flask_mongoengine import MongoEngine
from celery import Celery

from proj.hamlet import HamletClient
from proj.config import CONF

db = MongoEngine()
hamlet = HamletClient()
celery = Celery(__name__, broker=CONF.CELERY_BROKER_URL)
