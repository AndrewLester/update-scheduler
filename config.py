import os
from urllib.parse import urlparse
basedir = os.path.abspath(os.path.dirname(__file__))


# Settings for rq-worker
redis_url = urlparse(os.environ.get('REDIS_URL') or 'redis://localhost:6379')
REDIS_HOST = redis_url.hostname
REDIS_PORT = redis_url.port
REDIS_PASSWORD = redis_url.password
REDIS_SSL = redis_url.scheme == "rediss"
REDIS_SSL_CERT_REQS = None


class Config:
    APP_NAME = 'Update Scheduler'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECONNECT = 1000
    # ClearDB's idle limit is 90 seconds, so set the recycle to be under 90
    if os.environ.get('DATABASE_URL'):
        SQLALCHEMY_POOL_SIZE = 3
        SQLALCHEMY_MAX_OVERFLOW = 3
        SQLALCHEMY_POOL_RECYCLE = 55
        SQLALCHEMY_POOL_TIMEOUT = 5

    SCHOOLOGY_CLIENT_ID = os.environ.get('CONSUMER_KEY')
    SCHOOLOGY_CLIENT_SECRET = os.environ.get('CONSUMER_SECRET')

    CACHE_TYPE = 'redis'
    CACHE_DEFAULT_TIMEOUT = 1000
    CACHE_KEY_PREFIX = 'redis_flask_cache'
    CACHE_REDIS_HOST = REDIS_HOST
    CACHE_REDIS_PORT = REDIS_PORT
    CACHE_REDIS_PASSWORD = REDIS_PASSWORD
    CACHE_OPTIONS = {
        'ssl': REDIS_SSL,
        'ssl_cert_reqs': REDIS_SSL_CERT_REQS,
    }
    CACHE_IGNORE_ERRORS = True
