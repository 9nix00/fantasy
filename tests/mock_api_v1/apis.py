"""
=============

=============
"""

from flask import Blueprint

api = Blueprint('mock_api_v1', __name__)


@api.route('/')
def hello():
    return 'Hello World'
