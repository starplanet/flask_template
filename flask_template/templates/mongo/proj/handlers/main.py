# -*- coding: utf-8 -*-
from flask import Blueprint, request

bp_main = Blueprint('main', __name__, url_prefix=None)


@bp_main.route('/index')
def index():
    return 'ok'
