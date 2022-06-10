import os
import time

import cronitor.celery
from celery import Celery

celery = Celery(__name__, backend=os.getenv("CELERY_RESULT_BACKEND"), broker=os.getenv("CELERY_BROKER_URL"))

# See Celery's config page (https://docs.celeryq.dev/en/stable/userguide/configuration.html) for more details
celery.conf.imports = ('tasks',)
celery.conf.timezone = 'UTC'
celery.conf.result_expires = 120
celery.conf.beat_schedule = {
    'scheduled_delayed_greetings': {
        'task': 'tasks.scheduled_delayed_greetings',
        # Every 20 Seconds
        'schedule': 20
    }
}

# Auto discover all tasks for monitoring in cronitor
cronitor.celery.initialize(celery, api_key="<Paste your Cronitor API Key here>")


@celery.task()
def scheduled_delayed_greetings():
    print("Inside scheduled delayed greetings")
    time.sleep(20)
    print("Completed scheduled delayed greetings")


@celery.task()
def get_celery_stats():
    print("Inside post_celery_stats")
    inspect_output = celery.control.inspect()
    print("Stats ", inspect_output.stats(), flush=True)
    return inspect_output.stats()


cronitor.Monitor.put([{
    'type': 'check',
    'key': 'Celery Stats',
    'request': {
        'url': 'https://<Your Apps Public HOST/IP and port>/celery/stats',
        'regions': ['us-east-1', 'eu-central-1', 'ap-south-1']
    },
    'assertions': [
        'response.code = 200',
        'response.time < 1s',
        'response.body contains tasks.get_celery_stats'
    ]
}
])
