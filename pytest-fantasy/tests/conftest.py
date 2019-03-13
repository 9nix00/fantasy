"""
=============

=============
"""

import pytest
from flask import Flask, jsonify


def pytest_namespace():
    return {'resource_root': 'resource', 'custom': 'yes'}


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a key'

    @app.route('/')
    def hello():
        return jsonify({
            'hello': 'world'
        })

    return app
