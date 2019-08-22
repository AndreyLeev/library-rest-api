#!/bin/sh
python src/manage.py makemigrations
python src/manage.py migrate
python src/manage.py loaddata user_fixtures
python src/manage.py loaddata book_fixtures
exec "$@" 
