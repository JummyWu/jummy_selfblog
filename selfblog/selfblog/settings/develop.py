# coding:utf-8
from .base import *  # NOQA
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/4',
        "OPTIONS": {
            "CLIENT_CLASS": 'django_redis.client.DefaultClient',
            "PARSER_CLASS": 'redis.connection.HiredisParser',
        }
    }
}
