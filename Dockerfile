FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY . .

# Note: Rust is required by `cryptography` (python package)
RUN apt-get update && apt-get -y install cron rustc

RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

RUN pipenv run python manage.py collectstatic --noinput

RUN pipenv run python manage.py crontab add
