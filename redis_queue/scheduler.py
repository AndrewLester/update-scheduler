from config import Config
from rq_scheduler import Scheduler
from .redis import connection

if __name__ == '__main__':
    scheduler = Scheduler(connection=connection,
                          interval=Config.SCHEDULER_INTERVAL)
    scheduler.run()
