#!/usr/bin/env bash

function die {
    echo "Dying on signal $1"
    exit 0
}


trap 'die "SIGINT"' SIGINT
trap 'die "SIGQUIT"' SIGQUIT

WORKER_CLASS=uvicorn.workers.UvicornWorker

#gunicorn -k $WORKER_CLASS \
#  --log-level info \
#  --bind localhost:${SLACK_APP_PORT} \
#  --pid rbacker.pid \
#  rbacker:api

uvicorn rbacker:api --host 0.0.0.0 --port ${SLACK_APP_PORT} --log-level info
