# -*- coding: utf-8 -*-

import datetime
import logging
import time
import urllib.parse

import jwt
import requests
from flask import request
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)


def ensure_timestamp(v):
    if isinstance(v, datetime.datetime):
        return int(time.mktime(v.utctimetuple()))
    if isinstance(v, datetime.date):
        return int(time.mktime(v.timetuple()))
    return int(v)


class HamletClient(object):
    def __init__(self, base_url=None, app_key=None, api_key=None, app_secret=None, app=None):
        self.base_url = base_url
        self.app_key = app_key
        self.api_key = api_key
        self.app_secret = app_secret
        self.decode_token_by_server = False

        self._session = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.base_url = app.config['HAMLET_URL']
        self.app_key = app.config['HAMLET_APP_KEY']
        self.api_key = app.config['HAMLET_API_KEY']
        self.app_secret = app.config['HAMLET_APP_SECRET']
        self.decode_token_by_server = app.config.get('HAMLET_DECODE_TOKEN_BY_SERVER', False)

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['hamlet'] = self

    @property
    def session(self):
        if self._session is None:
            self._session = requests.Session()
            self._session.auth = HTTPBasicAuth(self.app_key, self.api_key)
        return self._session

    def _request(self, method, url, params=None, data=None, *args, **kwargs):
        url = urllib.parse.urljoin(self.base_url, url)
        r = self.session.request(method, url, params=params, json=data, timeout=5)
        # logger.info('%s %s, taken %s ms', method, r.request.url, r.elapsed.total_seconds() * 1000)

        r.raise_for_status()
        # raise_for_status(r)
        result = r.json()
        # if kwargs.get('raise_on_api_error', False):
        #     check_error(result, reason_key='reason', code=r.status_code)
        return result

    def _get(self, url, params=None, *args, **kwargs):
        return self._request('GET', url, params=params, *args, **kwargs)

    def _post(self, url, data=None, *args, **kwargs):
        return self._request('POST', url, data=data, *args, **kwargs)

    def _put(self, url, data=None, *args, **kwargs):
        return self._request('PUT', url, data=data, *args, **kwargs)

    def _delete(self, url, *args, **kwargs):
        return self._request('DELETE', url, *args, **kwargs)

    # --------------------------------- API ---------------------------------

    def decode_token(self, token):
        return self._get('/api/decode_token', params={'token': token}, raise_on_api_error=False)

    def list_users(self):
        """获取用户列表"""
        return self._get('/api/users')

    def create_user(self, username, password, email=None, role=None, operator_id=None):
        """新建用户账号

        :param username: 用户名，不能重复
        :type username: str
        :param password: 密码，需要满足一定的格式
        :type password: str
        :param email: 邮箱，是否需要邮箱，由配置决定
        :type email: str
        :param role: 角色
        :type role: str
        :param operator_id: 操作者 user_id
        :type operator_id: int
        :return:
        """
        return self._post('/api/users', data={
            'username': username,
            'password': password,
            'email': email,
            'role': role,
            'operator_id': operator_id
        })

    def apply_bind_user(self, email, role=None, operator_id=None):
        """
        发起用户绑定
        :param email: 邮箱
        :type email: str
        :param role: 角色
        :type role: str
        :param operator_id: 操作者 user_id
        :type operator_id: int
        :return: <User>
        """
        # No need Basic Auth
        return self._post('/auth/bind/apply', data={
            'app_key': self.app_key,
            'email': email,
            'role': role,
            'operator_id': operator_id
        })

    def get_user(self, user_id):
        """获取指定用户信息

        :param user_id: 用户 ID
        :type user_id: int
        :return:
        """
        return self._get('/api/users/{}'.format(user_id))

    def edit_user(self, user_id, role):
        """编辑用户信息
        :param user_id: 用户 ID
        :type user_id: int
        :param role: 角色
        :type role: str
        """
        return self._put('/api/users/{}'.format(user_id), data={'role': role})

    def delete_user(self, user_id, operator_id):
        """删除用户

        :param user_id: 用户 ID
        :type user_id: int
        :param operator_id: 操作者 user_id
        :type operator_id: int
        :return:
        """
        return self._delete('/api/users/{}'.format(user_id), params={'operator_id': operator_id})

    def reset_password(self, user_id, password, confirm_password):
        """重置密码

        :param user_id: 用户 ID
        :type user_id: int
        :param password: 新密码
        :type password: str
        :param confirm_password: 确认密码
        :type confirm_password: str
        :return:
        """
        url = '/api/users/{}/password'.format(user_id)
        return self._post(url, data={'password': password, 'confirm_password': confirm_password})

    def unlock(self, user_id):
        """解锁账号

        :param user_id: 用户 ID
        :type user_id: int
        :return:
        """
        return self._post('/api/users/{}/unlock'.format(user_id))

    def logs(self, user_id=None, since=None, until=None, events=None, orderby=None, page=1, count=100):
        """搜索日志

        :param user_id: 用户 ID
        :type user_id: 用户列表，可以是 list 或 ',' 分割的字符串
        :param since: 开始时间戳，精确到秒
        :type since: int | datetime.datetime
        :param until: 截止时间戳，精确到秒
        :type until: int | datetime.datetime
        :param events: 事件名称，可以是 list 或 ',' 分割的字符串
        :type events: str | list
        :param orderby: 排序字段，通过前缀 '+'（asc） 或 '-'（desc） 来指定顺序，默认 asc. 支持的字段：
                        id （默认）、event、user_id、created_at
        :param page: 页码
        :type page: int
        :param count: 每页数量
        :type count: int
        :return:
        """
        params = {}
        if user_id:
            params['user_id'] = user_id
        if since:
            params['since'] = ensure_timestamp(since)
        if until:
            params['until'] = ensure_timestamp(until)
        if events:
            if isinstance(events, (list, tuple, set)):
                events = ','.join(events)
            params['events'] = events
        if orderby:
            params['orderby'] = orderby
        if page:
            params['page'] = page
        if count:
            params['count'] = count

        return self._get('/api/logs', params)

    # -------------------------------- TOKEN --------------------------------

    def decode_access_token(self, token):
        """解码 access_token，返回 user_id"""
        if not token:
            return None

        user_id = None
        if self.decode_token_by_server:
            resp = self.decode_token(token)
            if resp['ok']:
                user_id = resp['data']['user']['id']
        else:
            try:
                payload = jwt.decode(token, key=self.app_secret, audience=self.app_key)
                user_id = payload['user_id']
            except jwt.InvalidTokenError as e:
                logger.info('failed to decode token "%s", error: "%s"', token, str(e))
        return user_id

    def get_access_token(self):
        """从 Authorization 请求头获取 access_token"""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            auth_header = request.cookies.get('Authorization')
        token = ''
        if not auth_header:
            token = request.args.get('access_token')
            return token

        parts = auth_header.split(' ')
        if len(parts) != 2:
            return token
        if parts[0].lower() != 'bearer':
            return token
        token = parts[1]
        return token

    def get_user_by_token(self, token):
        if not token:
            return None
        resp = self.decode_token(token)
        if not resp['ok']:
            # TODO: logging or raise exception?
            return None
        return resp['data']['user']

    def current_user_id(self):
        """获取当前请求的用户 ID，先从 Authorization 获取 access_token，然后解码出 user_id"""
        token = self.get_access_token()
        return self.decode_access_token(token)

    def current_user(self):
        token = self.get_access_token()
        return self.get_user_by_token(token)

    def login(self, username, password):
        params = {"username": username, "password": password, "app_key": self.app_key}
        return self._post('/auth/login', params)
