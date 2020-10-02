FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY . .

RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile
