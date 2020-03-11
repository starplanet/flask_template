import json
import re
import urllib.parse

from sqlalchemy import Column, Integer, SmallInteger, String, Text, DateTime, Boolean
from sqlalchemy import TypeDecorator, ForeignKey, inspect
from sqlalchemy.orm import relationship, backref

from proj.config import CONF
from proj.extensions import db
from proj.utils import utcnow, now, json_dumps, random_string, camelcase_to_underscore
from proj.utils.encrypt import aes
from proj.utils import ok_jsonify, fail_jsonify


class EncryptedType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        return aes.encrypt(value)

    def process_result_value(self, value, dialect):
        return aes.decrypt(value)


class JSONType(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        return json_dumps(value)

    def process_result_value(self, value, dialect):
        if not value:
            return value
        return json.loads(value)


class ModelMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_dict(self, values, allowed_fields=None):
        if not allowed_fields:
            columns = values.keys()
        else:
            columns = set(allowed_fields) & set(values.keys())
        for col in columns:
            setattr(self, col, values[col])

    def null(self, txt):
        if txt == '':
            return None
        return txt


class TimestampMixin(object):
    created_at = Column(DateTime, default=now, nullable=False)
    updated_at = Column(DateTime, default=now, onupdate=now, nullable=False)


class MyModel(db.Model, ModelMixin, TimestampMixin):
    __tablename__ = 'my_model'

    id = Column(Integer, primary_key=True)

    def to_dict(self):
        return {
            'id': self.id
        }

    def __repr__(self):
        return '<MyModel(id={})>'.format(self.id)
