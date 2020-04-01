from mongoengine import DateTimeField

from proj.extensions import db
from proj.utils import utcnow


class HamletUser:
    def __init__(self, data):
        self._data = data
        self.id = self._data['id']
        self.username = self._data['username']
        self.email = self._data.get('email')
        self.role = self._data.get('role')

    def __repr__(self):
        # 服务器的python是3.5.0, 以下语法不支持
        # return f'<HamletUser {self.username}#{self.id} {self.role}>'
        return '<HamletUser {username}#{id} {role}>'.format(username=self.username, id=self.id, role=self.role)

    def to_dict(self):
        return self._data


class TimestampMixin(object):
    created_at = DateTimeField(required=True, default=utcnow())
    updated_at = DateTimeField(required=True)


class ModelMixin(db.Document):
    meta = {'abstract': True}

    def save(self):
        self.updated_at = utcnow()
        super().save()


class MyModel(ModelMixin, TimestampMixin):

    def to_dict(self):
        return {
            'id': self.id
        }
