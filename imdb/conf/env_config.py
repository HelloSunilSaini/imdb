import os
from dotenv import load_dotenv

load_dotenv()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(object):
    __metaclass__ = Singleton

    CORS_ALLOW_HEADERS = ['Origin', 'X-Requested-With', 'Content-Type', 'Accept', 'Authorization']
    CORS_ALLOW_ORIGIN = ['*']
    LOGGER_CONFIG = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s [%(process)d-%(thread)d] %(levelname)s "
                          "%(pathname)s:%(lineno)s "
                          " - %(message)s"
            },
            "verbose": {
                "format": "[%(asctime)s] [%(process)d-%(thread)d] %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "detailed": {
                "class": "logging.StreamHandler",
                "formatter": "detailed"
            },
            "verbose": {
                "class": "logging.StreamHandler",
                "formatter": "verbose"
            }
        },
        "loggers": {
            "": {
                "handlers": [os.getenv('LOGGER_FORMAT', 'verbose')],
                "level": "DEBUG"
            },
            "werkzeug": {
                "level": "CRITICAL"
            }
        }
    }
