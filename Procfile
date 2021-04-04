web: gunicorn tasks_organizer.wsgi --log-file -
worker: celery worker --tasks.organizer=tasks.app