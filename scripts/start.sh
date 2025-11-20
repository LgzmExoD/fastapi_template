#! /usr/bin/env bash
set -e

if [ -f /app/app/main.py ]; then
    DEFAULT_MODULE_NAME=app.main
elif [ -f /app/main.py ]; then
    DEFAULT_MODULE_NAME=main
fi
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
EXPORT_NAME=${EXPORT_NAME:-$MODULE_NAME:$VARIABLE_NAME}

APP_MODULE=${APP_MODULE:-$EXPORT_NAME}

# Start Gunicorn with Uvicorn workers
exec gunicorn -k uvicorn.workers.UvicornWorker -c /app/gunicorn_conf.py "$APP_MODULE"
