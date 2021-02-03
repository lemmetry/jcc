# jcc

## Prerequisites
1. Install [Pyenv](https://github.com/pyenv/pyenv):
   Follow [installation](https://github.com/pyenv/pyenv#installation) steps.
2. Install [pipenv](https://pipenv.pypa.io/en/latest/):
   `$ pip install pipenv`
3. Clone this repo and go to project's directory.
4. Install project dependencies:
   `$ pipenv install`
___
## Running it locally
1. Activate the virtual environment
   `$ pipenv shell`
2. Synchronizes the database state with the current set of models and migrations.
   `$ python manage.py migrate`
3. Create superuser account.
   `$ python manage.py createsuperuser`
4. Launch the project
   `$ python manage.py runserver`

- Admin console: [http://localhost:8000/admin/](http://localhost:8000/admin/).
- Site itself [here](http://localhost:8000/jcc/stations).