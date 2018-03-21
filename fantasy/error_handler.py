"""
=============

=============
"""

from flask import jsonify
from webargs.flaskparser import abort


def webargs_error(error):
    abort(422, errors=error.messages, exc=error)


def http422(error):
    if hasattr(error, 'data'):
        return jsonify(error.data), 422
    return error, 422


def http500(error):
    if hasattr(error, 'data'):
        return jsonify(error.data), 500
    return error, 500
