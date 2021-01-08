web: gunicorn update_scheduler:app --worker-class gevent --workers 3
init: flask db init
worker: python redis_queue/worker.py
scheduler: python redis_queue/scheduler.py