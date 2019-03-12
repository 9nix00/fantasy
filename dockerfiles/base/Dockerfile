FROM jamiehewland/alpine-pypy:latest
MAINTAINER stormxx <stormxx@1024.engineer>

COPY requirements.txt /tmp/requirements.txt
RUN title='Install Depends Packages' && \
    apk add --no-cache --virtual .build-deps \
        git gcc && \
    apk add --no-cache --virtual .run-deps \
        openssl ca-certificates \
        musl-dev libffi-dev openssl-dev python3-dev && \
    pip install -r /tmp/requirements.txt --no-cache-dir  --retries=20 --timeout=30 && \
    pip install flask-fantasy --no-cache-dir  --retries=20 --timeout=30 && \
    apk del .build-deps && \
    rm -f /tmp/requirements.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /flask-app

ENV FLASK_SETTINGS_MODULE web.conf
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=no

ENV FLASK_JSON_AS_ASCII=yes
ENV FLASK_CACHE_TYPE=redis
ENV FLASK_REDIS_URL=redis://redis:6379/0

ENV FLASK_MONGODB_DB=fantasy
ENV FLASK_MONGODB_HOST=mongodb

ENV SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:root@mysql:3306/fantasy?charset=utf8mb4
ENV SQLALCHEMY_TRACK_MODIFICATIONS=yes

ENV CELERY_TASK_SERIALIZER=json
ENV CELERY_RESULT_SERIALIZER=json
