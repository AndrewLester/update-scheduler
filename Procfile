web: gunicorn update_scheduler:app --worker-class gevent --workers 5
init: flask db upgrade
worker: rq worker update-scheduler --with-scheduler -c config
