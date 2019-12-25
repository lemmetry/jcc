# jcc

## Prerequisites

* pyenv
* pipenv

## Running it locally

* `pipenv shell` to activate the virtual environment.
* `pipenv install` to install the dependencies.
* `python manage.py migrate` to initialize the database.
* `python manage.py createsuperuser` to create the admin user.
* `python manage.py runserver` to launch the app.
* Admin console: http://localhost:8000/admin/ 

## Running the tests

* `./manage.py test`
