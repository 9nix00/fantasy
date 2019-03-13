"""
=============
测试用例
=============
"""

import sys

import pytest
from flask import url_for

sys.path.insert(0, __file__.rsplit('/', 2)[0])

pytest_plugins = "pytest_fantasy.fixtures",


def test_hello(client):
    response = client.get(url_for('hello'))
    assert 200 == response.status_code
    assert 'hello' in response.json.keys()
    assert 'world' == response.json['hello']

    assert hasattr(pytest, 'custom')
    assert hasattr(pytest, 'active_db')
    pass
