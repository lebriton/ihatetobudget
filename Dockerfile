FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

# Note: Rust is required by `cryptography` (python package)
RUN apt-get update && apt-get -y install cron rustc

RUN pip install pipenv

WORKDIR /usr/src/app

COPY ./scripts/entrypoint.sh .

COPY ./app .

RUN pipenv install --deploy --ignore-pipfile

EXPOSE 8000

CMD ./entrypoint.sh
