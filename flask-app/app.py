import os, json, requests, redis
##############     Flask libraries     ##############
from flask import request, url_for
from flask_api import FlaskAPI
from flask import jsonify
#############     My libraries File     #############
from worker_proxy import celery
#from constants import *
MESSAGE_KEY="messages"
MAX_MESSAGES_VALUE = 1000

REDIS_HOST = os.getenv('REDIS_PORT_6379_TCP_ADDR','localhost')
conn = redis.Redis(REDIS_HOST)
app = FlaskAPI(__name__)

@app.route("/", methods=['GET'])
def save_message():
    """
    Send message to task
    """
    task = celery.send_task('mytasks.save_message_redis', args=[str(request.args.get('to')),request.args.get('text')],kwargs={})
    return {'status':'4'}


@app.route("/get_messages", methods=['GET'])
def get_all_nessage():
    """
    Send message from redis to client
    """
    current_length = conn.llen(MESSAGE_KEY)
    number_of_dics = min(current_length, MAX_MESSAGES_VALUE)
    list_message = []
    item = ""
    for i in range(number_of_dics):
        item = json.loads(conn.lpop(MESSAGE_KEY))
        list_message.append(item)
    return jsonify({"results":list_message})


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True,host="0.0.0.0", port= int(os.getenv('WEBHOOK_PORT', 5000)))