build:
	poetry install
	poetry run python manage.py migrate

test:
	poetry run python manage.py test

run:
	poetry run python manage.py runserver
