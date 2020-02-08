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

import pytest
pytest_plugins = "pytest_flask",

def pytest_configure():
    pytest.resource_root = None
    pytest.app_name = None
    pytest.app_config = {}


def pytest_addoption(parser):
    parser.addoption("--keep-database", action="store_true",
                     default=False,
                     help="keep database data after test finished.")
    pass


@pytest.fixture
def app():
    from fantasy.bootstrap import create_app
    app = create_app(pytest.app_name, config=pytest.app_config)
    app.config['TESTING'] = True
    return app
