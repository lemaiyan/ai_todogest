#!/usr/bin/env bash
set -e
python manage.py makemigrations --noinput
python manage.py migrate --noinput

#python manage.py collectstatic —-noinput

echo yes | python manage.py collectstatic

#python manage.py runserver 0.0.0.0:80
gunicorn --bind=0.0.0.0:80 configurations.wsgi --workers=2 --log-level=info --log-file=---access-logfile=- --error-logfile=- --timeout 30000 --reload