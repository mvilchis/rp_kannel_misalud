import os, json, requests, redis, unicodedata
##############     Flask libraries     ##############
from flask import request, url_for
from flask_api import FlaskAPI
from flask import jsonify
#############     My libraries File     #############
from worker_proxy import celery
from constants import *
MESSAGE_KEY="messages"
MAX_MESSAGES_VALUE = 1000

REDIS_HOST = os.getenv('REDIS_PORT_6379_TCP_ADDR','redis')
conn = redis.Redis(REDIS_HOST)
app = FlaskAPI(__name__)

@app.route("/", methods=['GET'])
def save_message():
    """
    Send message to task
    """
    text = request.args.get('text')
    user = request.args.get('from')
    org = ""
    if user :
        if user == MISALUD_USER:
            org = MISALUD_MODEM
        elif user == PROSPERA_USER:
            org = PROSPERA_MODEM
        elif user == INCLUSION_USER:
            org == INCLUSION_MODEM
    message = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
    task = celery.send_task('mytasks.save_message_redis', args=[str(request.args.get('to')),message,org],kwargs={})
    return {'status':'4'}


@app.route("/get_messages", methods=['GET'])
def get_all_messages():
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

@app.route("/show_messages", methods=['GET'])
def show_queue_messages():
    """
    Send message from redis to client
    """
    current_length = conn.llen(MESSAGE_KEY)
    list_message = []
    item = ""
    for i in range(current_length):
        item = json.loads(conn.lindex(MESSAGE_KEY,i))
        list_message.append(item)
    return jsonify({"results":list_message})


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True,host="0.0.0.0", port= int(os.getenv('WEBHOOK_PORT', 5000)))
