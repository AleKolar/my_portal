import os
from celery import Celery
from django.conf import settings
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_portal.settings")

django.setup()

installed_apps = settings.INSTALLED_APPS

debug_mode = settings.DEBUG
database_settings = settings.DATABASES

app = Celery('my_portal')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

from news.tasks import send_email_notification_to_subscribers

app.task(send_email_notification_to_subscribers)

app.conf.update(
    worker_log_level='INFO'
)