import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evil_flowers_catalog.settings.development')

app = Celery(f"evil_flowers_catalog_{os.getenv('DJANGO_SETTINGS_MODULE').split('.')[-1]}")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'popularity': {
        'task': 'apps.core.tasks.popularity',
        'schedule': crontab(minute='*/10'),
    },
}
