#!/bin/sh
ADD_PORT=${PORT:-8001}
cd /app/
/opt/venv/bin/python manage.py collectstatic --noinput
#/opt/venv/bin/python manage.py migrate --noinput
/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm crm.wsgi:application --bind "0.0.0.0:${ADD_PORT}"

