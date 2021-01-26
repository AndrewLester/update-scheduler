redis-server ~/.local/etc/redis.conf &
rq worker update-scheduler --with-scheduler &
npm run dev &
flask run --host 0.0.0.0

kill $(jobs -p | tail -r)