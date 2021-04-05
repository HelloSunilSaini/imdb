import logging

from django.conf import settings
from django.db.utils import load_backend
import sqlalchemy.pool as pool

pool_initialized = False

logger = logging.getLogger('pool')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

POOL_SETTINGS = {'pool_size': 10, 'max_overflow': 1, 'recycle': 21600}


class HashableDict(dict):
    def __hash__(self):
        # return hash(tuple(sorted(self.items())))
        return hash(tuple((self.items())))


class HashableList(list):
    def __hash__(self):
        return hash(tuple(sorted(self)))


class ManagerProxy(object):
    def __init__(self, manager):
        self.manager = manager

    def __getattr__(self, key):
        return getattr(self.manager, key)

    def connect(self, *args, **kwargs):
        if 'conv' in kwargs:
            conv = kwargs['conv']
            if isinstance(conv, dict):
                items = []
                for k, v in list(conv.items()):
                    if isinstance(v, list):
                        v = HashableList(v)
                    items.append((k, v))
                kwargs['conv'] = HashableDict(items)
        return self.manager.connect(*args, **kwargs)


def init_pool():
    if not globals().get('pool_initialized', False):
        global pool_initialized
        pool_initialized = True
        try:
            backend_name = settings.DATABASES['default']['ENGINE']
            backend = load_backend(backend_name)

            backend.Database = ManagerProxy(pool.manage(backend.Database, **POOL_SETTINGS))

            backend.DatabaseError = backend.Database.DatabaseError
            backend.IntegrityError = backend.Database.IntegrityError
            logger.info("Initialzied Connection Pool")
        except Exception as e:
            logger.exception(e)
            import traceback
            traceback.print_exc()
            pass


init_pool()
