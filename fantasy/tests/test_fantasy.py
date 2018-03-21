"""
=============
测试用例
=============
"""

import os
import sys

import pytest
from click.testing import CliRunner


def pytest_namespace():
    return {'resource_root': None}


@pytest.fixture
def app(request):
    from flask.cli import ScriptInfo

    dsn = str('mysql+pymysql://root'
              ':root@localhost/'
              'test-hive?charset=utf8mb4')
    hive_path = os.path.dirname(__file__.rsplit('/', 3)[0])

    sys.path.insert(1, hive_path)
    os.environ['FANTASY_PRIMARY_NODE'] = 'yes'
    os.environ['FANTASY_ACTIVE_SENTRY'] = 'no'
    os.environ['FANTASY_MIGRATION_PATH'] = os.path.join(hive_path,
                                                        'bootstrap')

    from fantasy import create_app

    def test_create_app(info):
        app = create_app('account.username', {
            'CACHE_TYPE': 'redis',
            'CACHE_REDIS_URL': 'redis://127.0.0.1:6379/2',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SQLALCHEMY_DATABASE_URI': dsn,
            'ACCOUNT_USERNAME_DISABLE_REGISTER': False
        })
        return app

    pytest.resource_root = os.path.join(os.path.dirname(__file__),
                                        'test_resources')

    yield ScriptInfo(create_app=test_create_app)

    # from sqlalchemy.engine.url import make_url
    # from sqlalchemy_utils import drop_database
    # drop_database(make_url(dsn))
    pass


def test_command(app):
    """
    虽然参考了security的代码，但是仍然无法正常运行

    AttributeError: 'ScriptInfo' object
    has no attribute 'response_class'
    后续有空再研究
    """
    from fantasy.cli import requirements

    runner = CliRunner()

    root = os.path.join(os.path.dirname(__file__), 'test_resources',
                        'requirements')

    result = runner.invoke(requirements, ['--requirements-root', root],
                           obj=app)

    print(result.exit_code, result.output)
    pass
