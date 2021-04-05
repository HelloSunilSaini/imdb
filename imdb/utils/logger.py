import time
import logging
import logging.config
from functools import wraps

from imdb.utils.config import get_config_object

config = get_config_object()

def get_root_logger():
    logging.config.dictConfig(config.LOGGER_CONFIG)
    logger = logging.getLogger()
    return logger


def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ts = time.time()
        module_name = func.__module__.split('.')[-1]
        func_name = func.__name__
        logging.info("{} {} started...".format(module_name, func.__name__))
        response = func(*args, **kwargs)
        te = time.time()
        logging.info("{} {} finished. Time taken = {:.2f} sec".format(module_name, func_name, te-ts))
        return response
    return wrapper
