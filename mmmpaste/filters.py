from flask import make_response
from functools import update_wrapper
from mmmpaste import app

def no_cache(f):
    def new_func(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        response.cache_control.no_cache = True
        return response
    return update_wrapper(new_func, f)


def cache(f):
    def new_func(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        response.cache_control.s_maxage = app.config.get('CACHE_S_MAXAGE')
        return response
    return update_wrapper(new_func, f)
