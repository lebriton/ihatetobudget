#!/bin/sh

# Collect static files
pipenv run python manage.py collectstatic --noinput

# Migrate DB
pipenv run python manage.py migrate

# Add jobs to crontab
pipenv run python manage.py crontab add

# Start crontab service
service cron start

# Start ihatetobudget server
pipenv run uvicorn ihatetobudget.asgi:application --host 0.0.0.0 --port 8000
