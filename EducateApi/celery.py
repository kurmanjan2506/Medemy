import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EducateApi.settings')

app = Celery('EducateApi')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# celery spam tasks
app.conf.beat_schedule = {
    'send-spam-every-5-minutes': {
        'task': 'EducateApi.tasks.send_spam_email',
        'schedule': crontab(minute='*/1')
    }
}
