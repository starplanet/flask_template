import datetime
import decimal
import json
import tarfile
import re
import io

import shortuuid
from flask import jsonify
from sqlalchemy.orm.query import Query


def utcnow():
    return datetime.datetime.utcnow()


def now():
    return datetime.datetime.now()


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoding class, to handle Decimal and datetime.date instances."""

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)

        if isinstance(o, datetime.date):
            return o.isoformat()

        if isinstance(o, datetime.timedelta):
            return str(o)

        if isinstance(o, Query):
            return list(o)

        super(JSONEncoder, self).default(o)


def json_dumps(data, **kwargs):
    return json.dumps(data, cls=JSONEncoder, **kwargs)


def pretty_print(v):
    print(json_dumps(v, indent=2, ensure_ascii=False))


def ok_jsonify(data=None):
    return jsonify({'ok': True, 'data': data if data != None else {}})


def fail_jsonify(reason, data=None):
    return jsonify({'ok': False, 'data': data if data != None else {}, 'reason': reason})


def validate_email(address):
    return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", address) is not None


def safe_int(v, default=0):
    try:
        return int(v)
    except (TypeError, ValueError) as e:
        return default


def pager(query, model, orderby='', page=1, count=100):
    """根据一个 query 对象和排序规则，返回本页的内容，及记录总数.

    :type query: flask_sqlalchemy.BaseQuery
    :type model: flask_sqlalchemy.Model
    :param orderby: 从参数获取的排序字段及顺序，格式是正序：'+field' 或 'field'，降序：'-field'
    :type orderby: str
    :param page: 页码，用于计算 offset
    :type page: int
    :param count: 返回数量，limit
    :type count: int
    """
    total = query.count()

    if orderby:
        order_field = orderby.lstrip('+-')
        field = getattr(model, order_field, None)
        if field is None or not hasattr(field, 'asc'):
            field = model.id

        if orderby.startswith('-'):
            query = query.order_by(field.desc())
        else:
            query = query.order_by(field.asc())

    page = max(1, page)
    rows = query.offset((page - 1) * count).limit(count).all()
    return rows, total


def camelcase_to_underscore(s):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def random_string(length=10):
    return shortuuid.random(length)


def decompress_file(fname):
    '''解压缩文件'''
    if fname.endswith("tar.gz"):
        tar = tarfile.open(fname, "r:gz")
        tar.extractall()
        tar.close()
    elif fname.endswith("tar"):
        tar = tarfile.open(fname, "r:")
        tar.extractall()
        tar.close()


def compress_file(uncompress_path, compress_path):
    '''压缩文件'''
    tar = tarfile.open(compress_path, "w:gz")
    tar.add(uncompress_path)
    tar.close()


def create_csv_file(df):
    '''创建 file-object 对象'''
    buf = io.StringIO()
    df.to_csv(buf)
    buf.seek(0)
    return buf


def check_file_suffix(fname):
    """
    检查上传的文件 格式是否符合要求
    """
    accept_suffix = ['.csv', '.xls', '.xlsx']
    for item in accept_suffix:
        if fname.endswith(item):
            return True
    return False
