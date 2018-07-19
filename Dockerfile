FROM jamiehewland/alpine-pypy:latest
MAINTAINER stormxx <stormxx@1024.engineer>


COPY requirements.txt /tmp/requirements.txt
RUN title='Install Depends Packages' && \
    pip install -r /tmp/requirements.txt && \
    rm -f /tmp/requirements.txt

COPY . /fantasy

VOLUME /web

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /web:/fantasy

ENV FLASK_SETTINGS_MODULE web.conf
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=no

ENV FLASK_JSON_AS_ASCII=yes
ENV FLASK_CACHE_TYPE=redis
ENV FLASK_REDIS_URL=redis://127.0.0.1:6379/0

ENV FLASK_MONGODB_DB=fantasy
ENV FLASK_MONGODB_HOST=127.0.0.1

ENV SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:root@127.0.0.1:3306/fantasy?charset=utf8mb4
ENV SQLALCHEMY_TRACK_MODIFICATIONS=yes

ENV CELERY_TASK_SERIALIZER=json
ENV CELERY_RESULT_SERIALIZER=json
