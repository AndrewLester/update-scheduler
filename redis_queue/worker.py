from config import Config
from rq import Worker, Queue, Connection
from .redis import connection

listen = ['high', 'default', 'low']


if __name__ == '__main__':
    with Connection(connection):
        worker = Worker(map(Queue, listen), name=Config.APP_NAME + '-worker')
        worker.work()
