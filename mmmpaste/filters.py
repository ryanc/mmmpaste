from functools import wraps
from time import time as now

from flask import make_response

from mmmpaste import app

def runtime(fn):
    """
    Add a header that shows the runtime of the route.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = now()
        response = make_response(fn(*args, **kwargs))
        end = now()
        response.headers["X-Runtime"] = "{0}s".format(end - start)
        return response
    return wrapper


def no_cache(fn):
    """
    Add "Cache-Control: no-cache" header.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        response = make_response(fn(*args, **kwargs))
        response.cache_control.no_cache = True
        return response
    return wrapper


def cache(fn):
    """
    Add "Cache-Control: s-maxage" header.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        response = make_response(fn(*args, **kwargs))
        response.cache_control.s_maxage = app.config.get('CACHE_S_MAXAGE')
        return response
    return wrapper
