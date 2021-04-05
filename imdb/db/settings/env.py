from imdb.db.settings.base import *

from imdb.utils.config import get_config_object

config = get_config_object()

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# TODO : change HOST,USER,PASS,PORT,DBNAME from env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'imdb',
        'USER': config.DB_USER,
        'PASSWORD': config.DB_PASS,
        'HOST': config.DB_HOST,
        'PORT': '',
        'STORAGE_ENGINE': 'MyISAM / INNODB / ETC',
    }
}
