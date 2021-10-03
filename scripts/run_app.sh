# Expose environment variables (primarily for the rq worker)
. .env
npm run build
redis-server ~/.local/etc/redis.conf &
rq worker update-scheduler --with-scheduler &
gunicorn update_scheduler:app --worker-class gevent -b 0.0.0.0:5000 --workers 3

if [ -n "$ZSH_VERSION" ]; then
    kill ${${(v)jobstates##*:*:}%=*}
else
    jobs -p | xargs kill
fi
