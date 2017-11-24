import os
from celery import Celery
import json, requests, redis
#from constants import *
MESSAGE_KEY="messages"
MAX_MESSAGES_VALUE = 1000

env=os.environ

REDIS_HOST = os.getenv('REDIS_PORT_6379_TCP_ADDR','localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT_6379_TCP_PORT',6379))
redis_url = "redis://%s:%s/0" % (REDIS_HOST, REDIS_PORT)

CELERY_BROKER_URL=redis_url
CELERY_RESULT_BACKEND=redis_url

conn = redis.Redis(REDIS_HOST)

celery= Celery('tasks',
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND)


@celery.task(name='mytasks.save_message_redis')
def save_message_redis(contact_cel, message):
    #Save message to redis
    message = {"contact":contact_cel, "message": message}
    message_dump = json.dumps(message)
    conn.rpush(MESSAGE_KEY, message_dump)
