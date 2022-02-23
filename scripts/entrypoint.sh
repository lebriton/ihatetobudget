#!/usr/bin/env sh

# Collect static files
pipenv run python manage.py collectstatic --noinput

# Migrate DB (if exists)
if [ -f /usr/src/app/data/db.sqlite3 ]; then
  pipenv run python manage.py migrate
fi

# Add jobs to crontab
pipenv run python manage.py crontab add

# Start crontab service
crond -b -l 2

# Start ihatetobudget server
pipenv run uvicorn ihatetobudget.asgi:application --host 0.0.0.0 --port 8000
