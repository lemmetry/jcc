# jcc

## Prerequisites
1. Follow [installation](https://github.com/pyenv/pyenv#installation) steps to install [Pyenv](https://github.com/pyenv/pyenv),
2. `$ pip install pipenv` to install [pipenv](https://pipenv.pypa.io/en/latest/),
3. Clone this repo and go to project's directory,
4. `$ pipenv install` to install project dependencies.

## Running it locally
1. `$ pipenv shell` to activate the virtual environment,
2. `$ python manage.py migrate` to synchronize the database state with the current set of models and migrations,
3. `$ python manage.py createsuperuser` to create superuser account,
4. `$ python manage.py runserver` to launch the project.

- Admin console: http://localhost:8000/admin/
- Site itself: http://localhost:8000/jcc/stations