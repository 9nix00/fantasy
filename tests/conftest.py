import pytest

pytest_plugins = "fantasy_pytest.fixtures",


def pytest_configure():
    import os
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    pytest.app_name = 'mock_api_v1'

    os.environ['FANTASY_ACTIVE_DB'] = 'no'

    pytest.app_config = {
        'FANTASY_ACTIVE_CACHE': 'no',
    }
    pass
