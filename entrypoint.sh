#!/usr/bin/env bash
#!/bin/sh
apk-get update && apk-get install -y netcat
echo "Waiting for postgres..."
# Wait for postgres
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"
# Define out commands
# Be careful! If you use AWS S3 bucked comment out the line below
python manage.py collectstatic --no-input
python manage.py migrate
gunicorn -b 0.0.0.0:8000 tasks_organizer.wsgi --reload
# Execute all the above commands
exec "$@"