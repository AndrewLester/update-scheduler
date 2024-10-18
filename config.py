import os
from urllib.parse import urlparse
basedir = os.path.abspath(os.path.dirname(__file__))


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

    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379'
    CACHE_REDIS_URL = REDIS_URL
    CACHE_TYPE = 'redis'
    CACHE_DEFAULT_TIMEOUT = 1000
    CACHE_KEY_PREFIX = 'redis_flask_cache'
    CACHE_REDIS_HOST = REDIS_URL.rsplit(':', 1)[0]
    CACHE_REDIS_PORT = REDIS_URL.rsplit(':', 1)[1]
    CACHE_IGNORE_ERRORS = True


# Settings for rq-worker
redis_url = urlparse(Config.REDIS_URL)
REDIS_HOST = redis_url.hostname
REDIS_PORT = redis_url.port
REDIS_PASSWORD = redis_url.password
REDIS_SSL = redis_url.scheme == "rediss"
REDIS_SSL_CA_CERTS = None
REDIS_DB = 0
REDIS_SSL_CERT_REQS = None
