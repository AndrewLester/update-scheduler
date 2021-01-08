redis-server ~/.local/etc/redis.conf &
python3 redis_queue/worker.py &
python3 redis_queue/scheduler.py &
npm run build
gunicorn update_scheduler:app --worker-class gevent -b 0.0.0.0:5000 --workers 3


kill %4
kill %3
kill %2
kill %1