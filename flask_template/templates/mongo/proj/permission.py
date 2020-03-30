# -*- coding: utf-8 -*-

import functools

from flask import abort, request, redirect

from proj.proxy import current_user


def login_required_check_token(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user:
            abort(401)
            # return redirect('/auth/login/')
        return view_func(*args, **kwargs)

    return wrapper


def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user:
            abort(401)
            # return redirect('/auth/login/')
        return view_func(*args, **kwargs)

    return wrapper


def authorize(roles=['admin']):
    def wrapper(view_func):
        @functools.wraps(view_func)
        def inner_func(*args, **kwargs):
            if not current_user:
                abort(401)
            #role = current_user['Role']
            role = current_user.role
            if role not in roles:
                abort(403)
            return view_func(*args, **kwargs)  # 这里

        return inner_func

    return wrapper
