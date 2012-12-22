CACHE_S_MAXAGE = 86400
DEBUG = False

try:
    from local_settings import *
except ImportError:
    pass
