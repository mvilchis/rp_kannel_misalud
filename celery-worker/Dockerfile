FROM ubuntu:14.04


RUN apt-get update -y
RUN apt-get install -y python-pip python-dev

ENV C_FORCE_ROOT true


# copy source code
COPY . /celery-worker
COPY ../constants.py /flask-app

WORKDIR /celery-worker

# install requirements

RUN pip install -r requirements.txt


# run the worker
#ENTRYPOINT ['celery']
#CMD ['-A','tasks', 'worker','--loglevel=info']
ENTRYPOINT celery -A tasks worker --loglevel=info
