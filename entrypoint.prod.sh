#!/bin/sh

python manage.py makemigrations

python manage.py migrate --noinput

python manage.py compress

exec uvicorn settings.asgi:application --host 0.0.0.0 --port 8000 --workers 4
