from imdb.db.settings.base import *

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# TODO : change HOST,USER,PASS,PORT,DBNAME from env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'imdb',
        'USER': 'root',
        'PASSWORD': 'as2d2p',
        'HOST': 'localhost',
        'PORT': '',
        'STORAGE_ENGINE': 'MyISAM / INNODB / ETC',
    }
}
