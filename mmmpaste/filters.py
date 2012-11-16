from functools import wraps
from time import time as now

from flask import make_response

from mmmpaste import app

def runtime(f):
    """
    Add a header that shows the runtime of the route.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = now()
        response = make_response(f(*args, **kwargs))
        end = now()
        response.headers["X-Runtime"] = "{0}s".format(end - start)
        return response
    return wrapper


def no_cache(f):
    """
    Add "Cache-Control: no-cache" header.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        response.cache_control.no_cache = True
        return response
    return wrapper


def cache(f):
    """
    Add "Cache-Control: s-maxage" header.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        response.cache_control.s_maxage = app.config.get('CACHE_S_MAXAGE')
        return response
    return wrapper
