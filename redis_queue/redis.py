import redis
from config import Config
import os


redis_url = os.getenv(Config.REDIS_URL, 'redis://localhost:6379')

connection = redis.from_url(redis_url)