<p align="center">
  <a href="https://github.com/bminusl/ihatetobudget/">
    <img src="https://raw.githubusercontent.com/bminusl/ihatetobudget/master/static/logo.png" alt="IHateToBudget logo" height="75">
  </a>
</p>


<h3 align="center">IHateToBudget</h3>

<p align="center">
  A simple web app to understand and control your expenses.
  <br>
  Designed to be self-hosted.
</p>

## Table of contents
* [About](#About)
* [Features](#Features)
* [Installation & Configuration](#installation--configuration)
  * [Docker method](#docker-method)
* [Updating](#updating)
  * [Docker method](#docker-method-1)
* [License](#license)
* [Acknowledgements](#acknowledgements)




## About

WIP

## Features

WIP

## Installation & Configuration

### Docker method

1. Install [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/), if you haven't already.

2. Clone the repository:

   ```bash
   git clone https://github.com/bminusl/ihatetobudget.git
   cd ihatetobudget
   ```

3. Create a copy of:

   * `docker-compose.yml.example` as `docker-compose.yml`
   * `docker-compose.env.example` as `docker-compose.env`
   * `Caddyfile.example` as `Caddyfile`

   ```bash
   cp docker-compose.yml.example docker-compose.yml
   cp docker-compose.env.example docker-compose.env
   cp Caddyfile.example Caddyfile
   ```

   Note: Making copies ensures that you can `git pull` (or equivalent) to receive updates without risking merge conflicts with upstream changes.

4. Edit `docker-compose.env` and adapt the following environment variables:

   * `DJANGO_SECRET_KEY`: This is the secret key used by Django.

5. Run `docker-compose up -d`. This will build the main image, and create and start the necessary containers.

6. To be able to login, you will need a super user. To create it, execute the following commands:

   ```bash
   docker-compose run --rm ihatetobudget pipenv run python manage.py migrate
   docker-compose run --rm ihatetobudget pipenv run python manage.py createsuperuser
   ```

   This will prompt you to set a username, an optional e-mail address and finally a password.

7. You should now be able to visit your [IHateToBudget instance](http://127.0.0.1:80) at `http://127.0.0.1:80`. You can login with the username and password you just created.

## Updating

### Docker method

**The following instructions are guidelines. You're free to adapt these to your needs.**

1. Navigate to the root of the repository.

2. Run `docker-compose down`. This will stop all containers.

3. **Create a backup of the database**—just in case—, e.g. run `cp db.sqlite3 db.sqlite3.bak`.

4. Upgrade the codebase to the desired revision, e.g. run `git pull`.

5. Migrate the database:

   ```bash
   docker-compose run --rm ihatetobudget pipenv run python manage.py migrate
   ```

   This action will synchronize the database state with the current set of models and migrations.

6. Run `docker-compose up --build -d`. This will rebuild the main image, and create and start the necessary containers.

## License

Distributed under the GPLv3 License. See `COPYING` for more information.

## Acknowledgements

WIP
