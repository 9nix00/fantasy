"""
=============
How to Use？
=============

1. create conftest.py file in you tests packages

1. add plugins

..code-block::

    pytest_plugins = "pytest_fantasy.fixtures",


1. define current test package namespace/configure
   see https://github.com/pytest-dev/pytest/pull/4421

..code-block::

    def pytest_configure():
        return {
            'entry_app': 'app-name'
        }


"""

import os

import pytest

pytest_plugins = "pytest_flask",


def pytest_configure(config):
    pytest.resource_root = None
    pytest.app_name = None
    pytest.app_config = {}
    pytest.keep_database = False
    config.addinivalue_line(
        "markers", "env(name): mark test to run only on named environment"
    )


@pytest.fixture
def keep_database():
    pytest.keep_database = True


@pytest.fixture
def app():
    from fantasy.bootstrap import create_app
    app = create_app(pytest.app_name, config=pytest.app_config)
    app.config['TESTING'] = True
    yield app

    if pytest.keep_database is False \
            and os.environ['FANTASY_ACTIVE_DB'] == 'yes':
        from sqlalchemy.engine.url import make_url
        from sqlalchemy_utils import drop_database
        drop_database(make_url(pytest.app_config['SQLALCHEMY_DATABASE_URI']))

    pass
