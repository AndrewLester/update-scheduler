# Expose environment variables (primarily for the rq worker)
. .env
redis-server ~/.local/etc/redis.conf &
rq worker update-scheduler --with-scheduler &
npm run dev &
flask run --host 0.0.0.0 --with-threads

jobs -p | tac | xargs kill
