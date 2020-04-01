# -*- coding: utf-8 -*-
import urllib.parse

from flask import Blueprint, request, make_response
import pandas as pd
import tablib

from proj.proxy import current_user
from proj.utils import ok_jsonify, fail_jsonify, check_file_suffix
from proj.tasks.download import download_result

bp_main = Blueprint('main', __name__, url_prefix=None)


@bp_main.route('/index')
def index():
    return 'ok'


@bp_main.route('/files', methods=['POST'])
def read_file():
    '''从请求读取文件'''
    if 'file' not in request.files.keys():
        return fail_jsonify(reason='file is null')

    file = request.files['file']
    file_name = file.filename
    if not check_file_suffix(file_name):
        return fail_jsonify(reason="仅支持xlx/csv/xlsx格式文件")

    if file_name.split('.')[1] == 'csv':
        df = pd.read_csv(file)
    elif file_name.split('.')[1] in ['xlsx', 'xls']:
        df = pd.read_excel(file)

    return ok_jsonify()


@bp_main.route('/export', methods=['GET'])
def export_file():
    '''返回Excel文件'''
    filename = 'test_file'

    test_data1 = [['name1', 'age1', 'sex1'], ['name2', 'age2', 'sex2'], ['name3', 'age3', 'sex3']]
    data1 = tablib.Dataset(*test_data1, headers=['name', 'name', 'sex'], title='test1')

    test_data2 = [['address1', 'email1'], ['address2', 'email2']]
    data2 = tablib.Dataset(*test_data2, headers=['address', 'email'], title='test2')
    ds = tablib.Databook((data1, data2))  # Databook 用来合并多个sheet  , 只有一个sheet可以直接使用 tablib.Dataset
    # 生成文件 并返回
    response = make_response(ds.xls, 200, {'mimetype': 'application/vnd.ms-excel'})
    response.headers['Content-Disposition'] = "attachment; filename={}.xls" \
        .format(urllib.parse.quote(filename))
    return response


@bp_main.route('/celery', methods=['POST'])
def download_file():
    '''异步下载文件'''
    param = request.json
    download_url = param.get('result_url')
    email = current_user.email
    download_result.delay(download_url, email)
    return ok_jsonify()
