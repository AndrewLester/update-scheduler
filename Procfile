web: gunicorn update_scheduler:app --worker-class gevent --workers 3
init: flask db init
worker: rq worker update-scheduler --with-scheduler