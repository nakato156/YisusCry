from flask import request, session, redirect, abort
from app.models.logger import Log
from functools import wraps
from os import getenv

def valid_data_user(campos: tuple = ("username", "password")):
    def function_wrap(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = dict(val for val in request.values.items() if val)
            if not campos and all(val for val in data.values() if str(val).strip()): return abort(400)
            elif campos and not all(data.get(campo) for campo in campos): return abort(400)
            return func(*args, **kwargs)
        return wrapper
    return function_wrap

def delete_csrf(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = dict(request.form)
        data.update(dict(request.args))
        if "csrf_token" in data: data.pop("csrf_token")
        return func(data=data, *args, **kwargs)
    return wrapper

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not "user" in session: return redirect("/login")
        return func(*args, **kwargs)
    return wrapper

def not_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user" in session: return redirect("/perfil")
        return func(*args, **kwargs)
    return wrapper

def save_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            logger = Log(getenv("BD_TABLE_ERRORS"))
            logger.log({
                "error": str(e),
                "data": str(args) + str(kwargs)
            })
    return wrapper