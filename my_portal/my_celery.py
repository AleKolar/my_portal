import os
from celery import Celery
from django.conf import settings
import django
from celery.schedules import crontab



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




app.conf.update(
    worker_log_level='INFO'
)

# app.conf.beat_schedule = {
#     'send-weekly-article-list': {
#         'task': 'path.to.send_weekly_article_list',
#         'schedule': crontab(day_of_week='monday', hour=8, minute=0),
#     },
# }
app.conf.beat_schedule = {
    'send-weekly-article-list': {
        'task': 'news.tasks.send_email_notification_to_subscribers',
        'schedule': crontab(day_of_week='monday', hour=8, minute=0),
    },
}