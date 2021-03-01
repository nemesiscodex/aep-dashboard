#!/bin/sh

echo "Collecting static files"
rm -rf /app/staticfiles
mkdir /app/staticfiles
python manage.py collectstatic

echo "Running migrations"
python manage.py migrate

gunicorn --bind :8000 --workers 3 aep.wsgi:application 