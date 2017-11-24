import os
from celery import Celery

env=os.environ
REDIS_HOST = os.getenv('REDIS_PORT_6379_TCP_ADDR','localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT_6379_TCP_PORT','6379'))
redis = "redis://%s:%s/0" % (REDIS_HOST, REDIS_PORT)

CELERY_BROKER_URL=redis
CELERY_RESULT_BACKEND=redis


celery= Celery('tasks',
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND)
