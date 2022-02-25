# Expose environment variables (primarily for the rq worker)
. ./.env
redis-server ~/.local/etc/redis.conf &
rq worker update-scheduler --with-scheduler &
npm run dev &
flask run --host 0.0.0.0 --with-threads --port 3000

if [ -n "$ZSH_VERSION" ]; then
    kill ${${(v)jobstates##*:*:}%=*}
else
    jobs -p | xargs kill
fi
