FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1

# Creating working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Update packages and install pipenv
RUN apk upgrade --no-cache && pip install pipenv

# Copy entrypoint script
COPY ./scripts/entrypoint.sh .

# Copy Pipfile and install dependencies
COPY ./app/Pipfile .
COPY ./app/Pipfile.lock .
RUN pipenv install --deploy --ignore-pipfile

# Copy app code
COPY ./app .

EXPOSE 8000

CMD ./entrypoint.sh
