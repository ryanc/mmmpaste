CACHE_S_MAXAGE = 86400
DEBUG = False
DATABASE_URL = 'sqlite:///db/pastebin.db'

try:
    from local_settings import *
except ImportError:
    pass
