"""
================
test bootstrap
================
"""

from flask import url_for


def test_hello(client):
    response = client.get(url_for('.hello'))
    assert 200 == response.status_code
    assert b'Hello World' == response.data
    pass
