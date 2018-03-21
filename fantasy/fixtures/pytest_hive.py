"""
=============
基础依赖
=============
"""

import os
import sys

import pytest


def pytest_namespace():
    return {
        'resource_root': None,
        'app_entry': None,
        'active_db': True,
        'active_celery': True,
        'app_config': {
            'DEBUG': True,
            'FANTASY_ACTIVE_DB': 'yes',
            'SECURITY_LOGIN_WITHIN': '10 days',
            'SECURITY_PASSWORD_HASH': 'sha256_crypt',
            'SECURITY_PASSWORD_SALT': 'Hello,Password Salt',
            'SECURITY_LOGIN_SALT': 'Hello,Login',
            'SECURITY_REMEMBER_SALT': 'Hello,Token',
            'CACHE_TYPE': 'redis',
            'CACHE_REDIS_URL': 'redis://127.0.0.1:6379/2',
            'CELERY_BROKER_URL': 'redis://redis:6379/1',
            'CELERY_RESULT_BACKEND': 'redis://redis:6379/2',
            'SECRET_KEY': 'HELLO,TEST',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SQLALCHEMY_DATABASE_URI': str('mysql+pymysql://root'
                                           ':root@localhost/'
                                           'test-hive?charset=utf8mb4'),
            'ACCOUNT_USERNAME_DISABLE_REGISTER': False
        },
        'entry_config': {}
    }


def pytest_addoption(parser):
    parser.addoption("--keep-database", action="store_true",
                     default=False,
                     help="操作完成不清理数据库")
    pass


@pytest.fixture
def app(request):
    if not pytest.entry_app:
        raise KeyError("Please set entry_app namespace.")

    hive_path = os.path.dirname(__file__.rsplit('/', 2)[0])
    sys.path.insert(1, hive_path)
    os.environ['FANTASY_PRIMARY_NODE'] = 'yes'
    os.environ['FANTASY_MIGRATION_PATH'] = os.path.join(hive_path,
                                                        'bootstrap')

    app_config = {key: getattr(pytest.app_config,
                               key) for key in dir(pytest.app_config)
                  if not key.startswith('_')}

    if hasattr(pytest, 'entry_config'):
        temp_config = {key: getattr(pytest.entry_config,
                                    key) for key in dir(pytest.entry_config)
                       if not key.startswith('_')}

        entry_config = {}
        for key, value in temp_config.items():
            if hasattr(value,
                       '__name__') and \
                    value.__name__.split('.', 1)[0] == 'pytest':
                entry_config[key] = {k: getattr(value,
                                                k) for k in dir(value)
                                     if not k.startswith('_')}
            else:
                entry_config[key] = value
            pass

        app_config.update(entry_config)

    from fantasy import create_app

    db = None
    if pytest.active_db:
        from flask_sqlalchemy import SQLAlchemy
        db = SQLAlchemy()
        pass

    celery = None
    if pytest.active_celery:
        from celery import Celery
        celery = Celery(pytest.entry_app)
        pass

    app = create_app(pytest.entry_app, app_config, db, celery)

    yield app
    # print(request.config.getoption('--keep-database'))

    from sqlalchemy.engine.url import make_url
    from sqlalchemy_utils import drop_database
    drop_database(make_url(app_config['SQLALCHEMY_DATABASE_URI']))

    mongodb_config = app.config.get('MONGODB_SETTINGS')

    if mongodb_config:
        try:
            from mongoengine.connection import get_db
            current_mongodb = get_db()
            current_mongodb.client.drop_database(mongodb_config['DB'])
        except Exception as e:
            print("drop mongodb ignored", e)
            pass

    if hasattr(pytest, 'entry_tear_down'):
        func = getattr(pytest, 'entry_tear_down')
        func(app)
        pass

    pass


@pytest.fixture
def fantasy_celery_app(client):
    app = client.application
    celery_app = app.celery
    celery_app.conf.update(CELERY_ALWAYS_EAGER=True)
    return celery_app
